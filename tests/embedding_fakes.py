"""
TEST DOUBLES for the embedding layer.

Production code must never import this module. Nothing here calls a network or a model.

bow_vector() is a hashing-trick bag of words: texts that share words share coordinates, so
cosine similarity means something inside a test. It is a stand-in for a real embedding model,
not a model, and it is the only place in the repository where a text is turned into a vector
without a model.
"""

import hashlib
import math
import re
import threading
from typing import Any, Callable, Dict, List, Optional, Sequence

DIM = 768

_PREFIX = re.compile(r"^(task: [^|]+\| query: |title: [^|]+\| text: )")


def strip_prefix(text: str) -> str:
    """Drop the documented task / title prefix so tests compare the content, not the format."""
    return _PREFIX.sub("", text, count=1)


def bow_vector(text: str, dim: int = DIM) -> List[float]:
    vec = [0.0] * dim
    for tok in re.findall(r"[a-z0-9]+", strip_prefix(text).lower()):
        h = int(hashlib.sha256(tok.encode("utf-8")).hexdigest(), 16)
        vec[h % dim] += 1.0
    norm = math.sqrt(sum(v * v for v in vec))
    if norm == 0.0:
        vec[0], norm = 1.0, 1.0
    return [v / norm for v in vec]


class ScriptedBackend:
    """An EmbedBackend whose behaviour a test controls."""

    name = "scripted"

    def __init__(
        self,
        errors: Optional[Sequence[Optional[BaseException]]] = None,
        override: Optional[Callable[[List[str], int], List[List[float]]]] = None,
        block: Optional[threading.Event] = None,
    ):
        self.calls: List[Dict[str, Any]] = []
        self._errors = list(errors or [])
        self._override = override
        self._block = block
        self.retries = 0

    def embed_texts(self, texts: Sequence[str], *, model: str, dim: int) -> List[List[float]]:
        self.calls.append({"texts": list(texts), "model": model, "dim": dim})
        if self._block is not None:
            self._block.wait(timeout=5.0)
        if self._errors:
            err = self._errors.pop(0)
            if err is not None:
                raise err
        if self._override is not None:
            return self._override(list(texts), dim)
        return [bow_vector(t, dim) for t in texts]


class FakeApiError(Exception):
    """Looks like google.genai.errors.APIError: it carries an HTTP-style .code."""

    def __init__(self, code: int, message: str = ""):
        super().__init__(message or f"fake API error {code}")
        self.code = code


class _Emb:
    def __init__(self, values: List[float]):
        self.values = values


class _Resp:
    def __init__(self, embeddings: List[_Emb]):
        self.embeddings = embeddings


def _text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    parts = getattr(content, "parts", None) or []
    return " ".join(getattr(p, "text", "") or "" for p in parts)


class _Models:
    def __init__(self, outer: "FakeGenaiClient"):
        self._outer = outer

    def embed_content(self, *, model: str, contents: Any, config: Any = None):
        self._outer.calls.append({"model": model, "contents": contents, "config": config})
        if self._outer.script:
            item = self._outer.script.pop(0)
            if isinstance(item, BaseException):
                raise item
        items = contents if isinstance(contents, list) else [contents]
        dim = getattr(config, "output_dimensionality", None) or DIM
        return _Resp([_Emb(bow_vector(_text_of(c), dim)) for c in items])


class FakeGenaiClient:
    """Enough of google.genai.Client for GeminiEmbedBackend: .models.embed_content and .vertexai."""

    def __init__(self, script: Optional[Sequence[Any]] = None, vertexai: bool = False):
        self.calls: List[Dict[str, Any]] = []
        self.script = list(script or [])
        self.vertexai = vertexai
        self.models = _Models(self)


class FakeGate:
    """Stands in for MODEL_ROUTER: can_call(key) -> (allowed, reason), record_call(key, tokens)."""

    def __init__(self, allowed: bool = True, reason: str = "test refusal"):
        self.allowed = allowed
        self.reason = reason
        self.recorded: List[Any] = []
        self.checked: List[str] = []

    def can_call(self, key: str):
        self.checked.append(key)
        return (self.allowed, "" if self.allowed else self.reason)

    def record_call(self, key: str, tokens: int = 0) -> None:
        self.recorded.append((key, tokens))
