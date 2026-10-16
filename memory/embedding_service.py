"""
INTEGRA O/S: EMBEDDING SERVICE (Rodin's real-vector layer)
Module: memory/embedding_service.py
Layer: 3 (Memory)

Turns text into vectors for Rodin and the Hoard under five rules:

  1. Real vectors only. There is no hash or constant fallback anywhere. A failure raises
     EmbeddingUnavailable with a code, is counted, and shows in telemetry (ADR-005 action 2).
  2. Every vector belongs to an EmbeddingSpace (model | dimension | prompt format). Spaces are
     never mixed: the Hoard keeps one Chroma collection per space.
  3. Queries and documents use the asymmetric text formats Google documents for
     gemini-embedding-2 [E1].
  4. Separate texts are wrapped in one Content object each. A plain list of strings is
     aggregated into ONE embedding by gemini-embedding-2 [E1], and the installed SDK
     serialises it that way (tests/test_embedding_service.py proves both).
  5. Every network call has a timeout, bounded retries and a concurrency cap, so a slow API
     cannot occupy the server's worker threads (Voltron: pace, contain, do not sprawl).

Official sources (fetched 2026-10-15):
  [E1] https://ai.google.dev/gemini-api/docs/embeddings (updated 2026-10-09): gemini-embedding-2 is
       the latest stable model; output dimensions "Flexible, supports: 128 - 3072, Recommended:
       768, 1536, 3072"; truncated dimensions are auto-normalised; task_type is not supported, put
       the task in the text; input limit 8,192 tokens; the space is incompatible with
       gemini-embedding-001, so everything is re-embedded.
  [E2] https://ai.google.dev/gemini-api/docs/deprecations (updated 2026-10-12): text-embedding-004
       shut down 2026-01-14 (replacement gemini-embedding-2).
  [E3] https://ai.google.dev/gemini-api/docs/pricing (updated 2026-10-15): gemini-embedding-2 text
       input $0.20 per 1M tokens (standard), $0.10 (batch). The free tier is marked "used to
       improve our products"; the paid tier is not.

No import of core.* happens at module import time, so this module is safe to import anywhere.
"""

from __future__ import annotations

import hashlib
import logging
import math
import os
import random
import re
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

logger = logging.getLogger("integra.embedding")

# ─────────────────────────────────────────────
#  CONSTANTS (each one traces to [E1]-[E3] or is marked as a choice)
# ─────────────────────────────────────────────

DEFAULT_MODEL = "gemini-embedding-2"       # [E1] latest stable
DEFAULT_DIM = 768                          # [E1] recommended; matches the Hoard schema (embedding_768d)
MIN_DIM, MAX_DIM = 128, 3072               # [E1] supported range
PROMPT_FORMAT = "asym-v1"                  # the query/document formats below; bump it if they change
QUERY_TASKS = ("search result", "question answering", "fact checking", "code retrieval")  # [E1] asymmetric table

MAX_INPUT_TOKENS = 8192                    # [E1] longer input is truncated silently by the service
SAFE_INPUT_TOKENS = 7600                   # choice: headroom for the prefix and tokenizer error
CHARS_PER_TOKEN = 3                        # choice: used for PRICE ESTIMATES (English prose is nearer 4, JSON and code nearer 2.5-3); the tokenizer is not called
CAP_CHARS_PER_TOKEN = 2                    # choice: used for the INPUT LIMIT, pessimistic so dense JSON or code is split rather than silently truncated
PREFIX_RESERVE_CHARS = 256                 # room for "title: ... | text: "
CHUNK_OVERLAP = 200                        # characters shared by neighbouring chunks of one long document
MAX_CHUNKS = 16                            # choice: caps the cost of one document; beyond it the document is flagged truncated
BATCH_SIZE = 16                            # choice: Content objects per request

UNIT_NORM_TOLERANCE = 1e-3

PRICE_PER_M_TOKENS_USD = 0.20              # [E3] standard, paid tier. Re-check the page before relying on it.
BATCH_PRICE_PER_M_TOKENS_USD = 0.10        # [E3] Batch API

RETRYABLE_CODES = frozenset({429, 500, 502, 503, 504})
RETRYABLE_NAMES = frozenset({
    "ReadTimeout", "ConnectTimeout", "WriteTimeout", "PoolTimeout", "TimeoutException",
    "ConnectError", "ReadError", "RemoteProtocolError", "TimeoutError", "ConnectionError",
})


def max_body_chars() -> int:
    """Largest piece of text sent in one input, leaving room for the format prefix. Pessimistic (2 characters per token)."""
    return SAFE_INPUT_TOKENS * CAP_CHARS_PER_TOKEN - PREFIX_RESERVE_CHARS


def approx_tokens(text: str) -> int:
    """Conservative token estimate (3 characters per token). Planning only; never billed on."""
    return max(1, -(-len(text) // CHARS_PER_TOKEN))


def estimate_cost_usd(tokens: int, batch: bool = False) -> float:
    return round(tokens / 1_000_000.0 * (BATCH_PRICE_PER_M_TOKENS_USD if batch else PRICE_PER_M_TOKENS_USD), 4)


# ─────────────────────────────────────────────
#  ERRORS, SPACE, RESULT
# ─────────────────────────────────────────────

_SECRET_PATTERNS = (
    re.compile(r"AIza[0-9A-Za-z_\-]{20,}"),                                   # Google API key shape
    re.compile(r"AQ\.[0-9A-Za-z_\-]{20,}"),                                   # Google express-mode key shape
    re.compile(r"sk-[A-Za-z0-9_\-]{20,}"),                                    # other provider key shape
    re.compile(r"(?i)\b(api[_-]?key|token|authorization|x-goog-api-key)(\s*[=:]\s*)[^\s,;'\"&]+"),
)


def redact(text: str) -> str:
    """Replaces anything shaped like a credential. Error details are served by an unauthenticated telemetry route."""
    out = str(text)
    for pattern in _SECRET_PATTERNS[:3]:
        out = pattern.sub("[REDACTED]", out)
    return _SECRET_PATTERNS[3].sub(lambda m: f"{m.group(1)}{m.group(2)}[REDACTED]", out)


class EmbeddingUnavailable(RuntimeError):
    """
    Raised instead of returning a stand-in vector.
    Codes: NO_CLIENT, API_ERROR, BACKEND_ERROR, BAD_RESPONSE, BAD_DIMENSION, NOT_FINITE,
           ROUTER_REFUSED, BUSY, BAD_CONFIG, EMPTY_INPUT.
    The detail is redacted at the source: it reaches logs and GET /rodin/telemetry.
    """

    def __init__(self, code: str, detail: str = ""):
        detail = redact(detail) if detail else detail
        super().__init__(f"{code}: {detail}" if detail else code)
        self.code = code
        self.detail = detail


@dataclass(frozen=True)
class EmbeddingSpace:
    """The model, dimension and text format a vector was made with. Vectors of different spaces never meet."""

    model: str = DEFAULT_MODEL
    dim: int = DEFAULT_DIM
    fmt: str = PROMPT_FORMAT

    def __post_init__(self):
        if not str(self.model).startswith("gemini-embedding-2"):
            raise ValueError(
                f"unsupported embedding model {self.model!r}: Rodin supports gemini-embedding-2 only "
                "(text-embedding-004 is shut down, gemini-embedding-001 is a different space and API)"
            )
        if not (MIN_DIM <= int(self.dim) <= MAX_DIM):
            raise ValueError(f"dimension {self.dim} is outside the documented range {MIN_DIM}-{MAX_DIM}")

    @property
    def id(self) -> str:
        return f"{self.model}|{self.dim}|{self.fmt}"

    def slug(self) -> str:
        return re.sub(r"[^a-z0-9]+", "-", f"{self.model}-{self.dim}-{self.fmt}".lower()).strip("-")

    def collection_name(self, base: str = "integra_hoard") -> str:
        return f"{base}__{self.slug()}"

    @classmethod
    def parse(cls, space_id: str) -> "EmbeddingSpace":
        model, dim, fmt = str(space_id).split("|")
        return cls(model=model, dim=int(dim), fmt=fmt)


@dataclass
class EmbeddingResult:
    vector: List[float]
    space: EmbeddingSpace
    chunks: int = 1
    truncated: bool = False
    cached: bool = False
    latency_ms: float = 0.0


def resolve_space_from_env() -> Tuple[EmbeddingSpace, Optional[str]]:
    """
    Reads RODIN_EMBED_MODEL and RODIN_EMBED_DIM. Never raises: a bad value returns the default space
    plus an error string, and the service then refuses every call with BAD_CONFIG (loud, not silent).
    """
    model = (os.environ.get("RODIN_EMBED_MODEL") or DEFAULT_MODEL).strip() or DEFAULT_MODEL
    raw_dim = (os.environ.get("RODIN_EMBED_DIM") or str(DEFAULT_DIM)).strip() or str(DEFAULT_DIM)
    try:
        return EmbeddingSpace(model=model, dim=int(raw_dim)), None
    except ValueError as exc:
        return EmbeddingSpace(), f"RODIN_EMBED_MODEL={model!r} RODIN_EMBED_DIM={raw_dim!r}: {exc}"


# ─────────────────────────────────────────────
#  TEXT FORMATS AND CHUNKING
# ─────────────────────────────────────────────

def _clean_title(title: Optional[str]) -> str:
    if not title:
        return "none"
    return re.sub(r"\s+", " ", str(title).replace("|", "/")).strip()[:120] or "none"


def format_query(text: str, task: str = "search result") -> str:
    return f"task: {task} | query: {text}"                      # [E1] asymmetric, query side


def format_document(body: str, title: Optional[str] = None) -> str:
    return f"title: {_clean_title(title)} | text: {body}"       # [E1] asymmetric, document side


def split_body(text: str, size: int, overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Windows of at most `size` characters, cut at a paragraph, sentence or space where one exists. Stops after MAX_CHUNKS + 1."""
    n = len(text)
    if n <= size:
        return [text]
    chunks: List[str] = []
    start = 0
    while start < n and len(chunks) <= MAX_CHUNKS:
        end = min(n, start + size)
        if end < n:
            lo = start + int(size * 0.8)
            cut = max(text.rfind("\n\n", lo, end), text.rfind(". ", lo, end), text.rfind("\n", lo, end), text.rfind(" ", lo, end))
            if cut > start:
                end = cut + 1
        chunks.append(text[start:end])
        if end >= n:
            break
        start = max(end - overlap, start + 1)
    return chunks


# ─────────────────────────────────────────────
#  BACKEND: Gemini API through google-genai
# ─────────────────────────────────────────────

def _default_client_factory():
    from core.api_clients import _make_gemini_client  # lazy: keeps this module free of core imports
    return _make_gemini_client()


class GeminiEmbedBackend:
    """
    client.models.embed_content with one Content per text and output_dimensionality set [E1].
    The synchronous SDK call is used on purpose: it needs no event loop, so it is safe from worker threads.
    """

    name = "gemini"

    def __init__(
        self,
        client_factory: Optional[Callable[[], Any]] = None,
        *,
        timeout_s: float = 10.0,
        max_retries: int = 1,
        base_delay_s: float = 0.5,
        sleep: Callable[[float], None] = time.sleep,
        rng: Callable[[], float] = random.random,
    ):
        self._factory = client_factory or _default_client_factory
        self._client: Any = None
        self._client_lock = threading.Lock()
        self.timeout_s = timeout_s
        self.max_retries = max_retries
        self.base_delay_s = base_delay_s
        self._sleep = sleep
        self._rng = rng
        self.retries = 0

    def _get_client(self) -> Any:
        with self._client_lock:
            if self._client is None:
                self._client = self._factory()  # a missing key returns None; try again next call
            client = self._client
        if client is None:
            raise EmbeddingUnavailable("NO_CLIENT", "no Gemini client: GEMINI_API_KEY is missing or the client could not be created")
        return client

    @staticmethod
    def _retryable(exc: BaseException) -> bool:
        return getattr(exc, "code", None) in RETRYABLE_CODES or type(exc).__name__ in RETRYABLE_NAMES

    def embed_texts(self, texts: Sequence[str], *, model: str, dim: int) -> List[List[float]]:
        if not texts:
            return []
        client = self._get_client()
        from google.genai import types  # lazy

        contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
        config = types.EmbedContentConfig(
            output_dimensionality=dim,
            http_options=types.HttpOptions(timeout=int(self.timeout_s * 1000)),
        )
        attempt = 0
        while True:
            try:
                res = client.models.embed_content(model=model, contents=contents, config=config)
                break
            except Exception as exc:  # noqa: BLE001  (every SDK/transport error is classified below)
                if self._retryable(exc) and attempt < self.max_retries:
                    attempt += 1
                    self.retries += 1
                    self._sleep(self.base_delay_s * (2 ** (attempt - 1)) * (0.5 + self._rng()))
                    continue
                raise EmbeddingUnavailable(
                    "API_ERROR",
                    f"{type(exc).__name__}: {str(exc)[:300]} (model={model}, vertexai={getattr(client, 'vertexai', None)}, attempts={attempt + 1})",
                ) from exc
        embeddings = getattr(res, "embeddings", None)
        if not embeddings:
            raise EmbeddingUnavailable("BAD_RESPONSE", "the response carried no embeddings")
        return [list(getattr(e, "values", None) or []) for e in embeddings]


# ─────────────────────────────────────────────
#  SERVICE
# ─────────────────────────────────────────────

class EmbeddingService:
    """
    Validates, pools, caches and counts. A backend only has to implement
    embed_texts(texts, *, model, dim) -> one vector per text, or raise.
    """

    def __init__(
        self,
        backend: Any,
        space: Optional[EmbeddingSpace] = None,
        *,
        cache_size: int = 512,
        gate: Any = None,
        gate_key: str = "rodin_retrieval",
        max_concurrency: int = 4,
        acquire_timeout_s: float = 3.0,
        clock: Callable[[], float] = time.time,
        config_error: Optional[str] = None,
    ):
        self.backend = backend
        self.space = space or EmbeddingSpace()
        self.config_error = config_error
        self._gate = gate
        self._gate_key = gate_key
        self._clock = clock
        self._cache: "OrderedDict[str, Tuple[List[float], int, bool]]" = OrderedDict()
        self._cache_size = max(0, int(cache_size))
        self._lock = threading.Lock()
        self._sem = threading.BoundedSemaphore(max(1, int(max_concurrency)))
        self._acquire_timeout_s = acquire_timeout_s
        self._counts = {
            "calls": 0, "texts_sent": 0, "cache_hits": 0, "failures": 0, "consecutive_failures": 0,
            "busy_refusals": 0, "renormalized": 0, "truncated": 0,
        }
        self._last_ok_at: Optional[float] = None
        self._last_error: Optional[Dict[str, Any]] = None
        self._seq = 0              # orders successes against failures without relying on clock resolution
        self._last_ok_seq = 0
        self._last_error_seq = 0

    # ── public API ──

    def embed_query(self, text: str, task: str = "search result") -> EmbeddingResult:
        if task not in QUERY_TASKS:
            raise ValueError(f"task {task!r} is not a retrieval task; use one of {QUERY_TASKS}")
        body = (text or "").strip()
        if not body:
            raise EmbeddingUnavailable("EMPTY_INPUT", "query text is empty")  # a caller error, not a service failure
        truncated = len(body) > max_body_chars()
        if truncated:
            body = body[: max_body_chars()]
        return self._embed_items([([format_query(body, task)], truncated)])[0]

    def embed_document(self, text: str, title: Optional[str] = None) -> EmbeddingResult:
        return self.embed_documents([(text, title)])[0]

    def embed_documents(self, items: Sequence[Tuple[str, Optional[str]]]) -> List[EmbeddingResult]:
        prepared: List[Tuple[List[str], bool]] = []
        for text, title in items:
            body = (text or "").strip()
            if not body:
                raise EmbeddingUnavailable("EMPTY_INPUT", "document text is empty")
            pieces = split_body(body, max_body_chars())
            truncated = len(pieces) > MAX_CHUNKS
            prepared.append(([format_document(p, title) for p in pieces[:MAX_CHUNKS]], truncated))
        return self._embed_items(prepared)

    def state(self) -> str:
        """MISCONFIGURED, UNPROVEN (never called), READY (the last call returned valid vectors) or DEGRADED (the last call failed)."""
        with self._lock:
            if self.config_error:
                return "MISCONFIGURED"
            if self._last_error_seq > self._last_ok_seq:
                return "DEGRADED"
            return "READY" if self._last_ok_seq > 0 else "UNPROVEN"

    def stats(self) -> Dict[str, Any]:
        state = self.state()
        with self._lock:
            return {
                "state": state,
                "backend": getattr(self.backend, "name", type(self.backend).__name__),
                "space": self.space.id,
                "gated": self._gate is not None,
                **self._counts,
                "retries": getattr(self.backend, "retries", 0),
                "cache_entries": len(self._cache),
                "last_ok_at": self._last_ok_at,
                "last_error": dict(self._last_error) if self._last_error else None,
                "config_error": self.config_error,
            }

    # ── internals ──

    def _fail(self, exc: EmbeddingUnavailable) -> EmbeddingUnavailable:
        with self._lock:
            self._seq += 1
            self._last_error_seq = self._seq
            self._counts["failures"] += 1
            self._counts["consecutive_failures"] += 1
            self._last_error = {"code": exc.code, "detail": exc.detail, "at": self._clock()}
        logger.error("embedding unavailable: %s", exc)
        return exc

    def _validated(self, vec: Sequence[float]) -> List[float]:
        dim = self.space.dim
        if len(vec) != dim:
            raise EmbeddingUnavailable("BAD_DIMENSION", f"expected {dim} values, got {len(vec)}")
        values = [float(x) for x in vec]
        if not all(math.isfinite(x) for x in values):
            raise EmbeddingUnavailable("NOT_FINITE", "the vector contains NaN or infinity")
        n = math.sqrt(sum(x * x for x in values))
        if n == 0.0:
            raise EmbeddingUnavailable("BAD_RESPONSE", "the vector is all zeros")
        if abs(n - 1.0) > UNIT_NORM_TOLERANCE:
            with self._lock:
                self._counts["renormalized"] += 1
            values = [x / n for x in values]
        return values

    @staticmethod
    def _key(chunks: Sequence[str]) -> str:
        return hashlib.sha256("\x1f".join(chunks).encode("utf-8")).hexdigest()

    @staticmethod
    def _pool(vectors: Sequence[Sequence[float]]) -> List[float]:
        """Mean of the chunk vectors, scaled to unit length (the averaging [E1] suggests for composite inputs)."""
        if len(vectors) == 1:
            return list(vectors[0])
        dim = len(vectors[0])
        mean = [sum(v[i] for v in vectors) / len(vectors) for i in range(dim)]
        n = math.sqrt(sum(x * x for x in mean))
        return [x / n for x in mean] if n > 0.0 else mean

    def _cache_get(self, key: str) -> Optional[Tuple[List[float], int, bool]]:
        with self._lock:
            hit = self._cache.get(key)
            if hit is not None:
                self._cache.move_to_end(key)
                self._counts["cache_hits"] += 1
            return hit

    def _cache_put(self, key: str, value: Tuple[List[float], int, bool]) -> None:
        if self._cache_size == 0:
            return
        with self._lock:
            self._cache[key] = value
            self._cache.move_to_end(key)
            while len(self._cache) > self._cache_size:
                self._cache.popitem(last=False)

    def _call_backend(self, texts: List[str]) -> List[List[float]]:
        if self.config_error:
            raise self._fail(EmbeddingUnavailable("BAD_CONFIG", self.config_error))
        if self._gate is not None:
            allowed, reason = self._gate.can_call(self._gate_key)
            if not allowed:
                raise self._fail(EmbeddingUnavailable("ROUTER_REFUSED", reason or "the model router refused the call"))
        if not self._sem.acquire(timeout=self._acquire_timeout_s):
            with self._lock:
                self._counts["busy_refusals"] += 1
            raise EmbeddingUnavailable("BUSY", "too many embedding calls in flight; try again")
        try:
            with self._lock:
                self._counts["calls"] += 1
                self._counts["texts_sent"] += len(texts)
            try:
                raw = self.backend.embed_texts(texts, model=self.space.model, dim=self.space.dim)
            except EmbeddingUnavailable as exc:
                raise self._fail(exc)
            except Exception as exc:  # noqa: BLE001
                raise self._fail(EmbeddingUnavailable("BACKEND_ERROR", f"{type(exc).__name__}: {str(exc)[:300]}")) from exc
            finally:
                if self._gate is not None:
                    self._gate.record_call(self._gate_key, 0)  # the API reports no token usage, so none is invented
            if len(raw) != len(texts):
                raise self._fail(EmbeddingUnavailable("BAD_RESPONSE", f"sent {len(texts)} texts, received {len(raw)} embeddings"))
            try:
                return [self._validated(v) for v in raw]
            except EmbeddingUnavailable as exc:
                raise self._fail(exc)
        finally:
            self._sem.release()

    def _embed_items(self, prepared: Sequence[Tuple[List[str], bool]]) -> List[EmbeddingResult]:
        t0 = time.time()
        results: List[Optional[EmbeddingResult]] = [None] * len(prepared)
        misses: List[int] = []
        for i, (chunks, truncated) in enumerate(prepared):
            hit = self._cache_get(self._key(chunks))
            if hit is not None:
                vec, n_chunks, was_truncated = hit
                results[i] = EmbeddingResult(list(vec), self.space, n_chunks, was_truncated, cached=True)
            else:
                misses.append(i)
        if misses:
            unique: List[str] = list(dict.fromkeys(c for i in misses for c in prepared[i][0]))
            by_text: Dict[str, List[float]] = {}
            for off in range(0, len(unique), BATCH_SIZE):
                batch = unique[off: off + BATCH_SIZE]
                for text, vec in zip(batch, self._call_backend(batch)):
                    by_text[text] = vec
            elapsed = (time.time() - t0) * 1000.0
            with self._lock:
                self._seq += 1
                self._last_ok_seq = self._seq
                self._last_ok_at = self._clock()
                self._counts["consecutive_failures"] = 0
            for i in misses:
                chunks, truncated = prepared[i]
                vec = self._pool([by_text[c] for c in chunks])
                if truncated:
                    with self._lock:
                        self._counts["truncated"] += 1
                self._cache_put(self._key(chunks), (vec, len(chunks), truncated))
                results[i] = EmbeddingResult(vec, self.space, len(chunks), truncated, cached=False, latency_ms=round(elapsed, 1))
        return [r for r in results if r is not None]


# ─────────────────────────────────────────────
#  DEFAULT SERVICE (one per process, shared by Rodin, the Hoard and the tools)
# ─────────────────────────────────────────────

_default: Optional[EmbeddingService] = None
_operator: Optional[EmbeddingService] = None
_default_lock = threading.Lock()


def _router_gate() -> Any:
    try:
        from core.model_router import MODEL_ROUTER

        return MODEL_ROUTER
    except Exception:  # noqa: BLE001  (offline tests and tools run without the router)
        return None


def get_default_embedding_service() -> EmbeddingService:
    """The kernel's service: gated by the model router (power state and budget), so a dormant router refuses the call."""
    global _default
    with _default_lock:
        if _default is None:
            space, err = resolve_space_from_env()
            _default = EmbeddingService(GeminiEmbedBackend(), space, gate=_router_gate(), config_error=err)
        return _default


def get_operator_embedding_service() -> EmbeddingService:
    """
    For one-shot operator tools (tools/rodin_reembed.py, scripts/ingest_knowledge.py): the same backend and space but
    no router gate. Those tools run in their own process where the router is dormant, and a person has chosen to
    spend (--apply, --yes-paid); the router's duty cycle governs the kernel's runtime, not an operator's run.
    """
    global _operator
    with _default_lock:
        if _operator is None:
            space, err = resolve_space_from_env()
            # a person is waiting on a batch run, not a user on a request: more patience, more retries
            _operator = EmbeddingService(GeminiEmbedBackend(timeout_s=30.0, max_retries=3, base_delay_s=1.0), space, gate=None, config_error=err)
        return _operator


def reset_default_embedding_service(service: Optional[EmbeddingService] = None) -> None:
    """Tests and tools replace or clear the process-wide services."""
    global _default, _operator
    with _default_lock:
        _default = service
        _operator = None
