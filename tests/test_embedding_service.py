"""
INTEGRA O/S: EMBEDDING SERVICE TEST SUITE (offline)

Rodin's rule: a vector is either real, from the model, or it does not exist. These tests prove
the failure paths (wrong count, wrong dimension, NaN, zero, timeout, router refusal, bad config)
raise EmbeddingUnavailable and never return a stand-in vector.

Method: Zenitsu 3.0 order. K (what the documented contract is), U (how the layers connect),
W (what fails over time), Unification (the SDK serialisation check at the end).
Official sources (fetched 2026-10-15):
  [E1] https://ai.google.dev/gemini-api/docs/embeddings
No network, no key, no model. Fakes live in tests/embedding_fakes.py.
"""

import math
import threading

import pytest

from memory.embedding_service import (
    DEFAULT_DIM,
    DEFAULT_MODEL,
    MAX_CHUNKS,
    PROMPT_FORMAT,
    EmbeddingService,
    EmbeddingSpace,
    EmbeddingUnavailable,
    GeminiEmbedBackend,
    max_body_chars,
    resolve_space_from_env,
)
from tests.embedding_fakes import (
    DIM,
    FakeApiError,
    FakeGate,
    FakeGenaiClient,
    ScriptedBackend,
    bow_vector,
)


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def make_service(backend=None, **kw):
    backend = backend or ScriptedBackend()
    return EmbeddingService(backend, kw.pop("space", EmbeddingSpace()), **kw), backend


# ───────────────────────── K: the documented contract ─────────────────────────


def test_space_id_slug_and_collection_name():
    s = EmbeddingSpace()
    assert (s.model, s.dim, s.fmt) == (DEFAULT_MODEL, DEFAULT_DIM, PROMPT_FORMAT)
    assert s.id == "gemini-embedding-2|768|asym-v1"
    assert s.slug() == "gemini-embedding-2-768-asym-v1"
    assert s.collection_name() == "integra_hoard__gemini-embedding-2-768-asym-v1"
    assert EmbeddingSpace.parse(s.id) == s


@pytest.mark.parametrize("model,dim", [("text-embedding-004", 768), ("gemini-embedding-001", 768),
                                       ("gemini-embedding-2", 64), ("gemini-embedding-2", 4096)])
def test_space_rejects_models_and_dimensions_outside_the_documented_contract(model, dim):
    # [E1]: gemini-embedding-2, "Flexible, supports: 128 - 3072"; 001 uses a different task API and is not compatible.
    with pytest.raises(ValueError):
        EmbeddingSpace(model=model, dim=dim)


def test_collection_name_is_accepted_by_real_chroma(tmp_path):
    import chromadb

    client = chromadb.PersistentClient(path=str(tmp_path / "chroma"))
    col = client.get_or_create_collection(name=EmbeddingSpace().collection_name(), metadata={"hnsw:space": "cosine"})
    assert col.count() == 0


def test_query_and_document_use_the_documented_asymmetric_formats():
    svc, backend = make_service()
    svc.embed_query("what is the epiphany equation")
    svc.embed_query("who runs rodin", task="question answering")
    svc.embed_document("body text")
    svc.embed_document("body text two", title="Blueprint")
    sent = [c["texts"][0] for c in backend.calls]
    assert sent[0] == "task: search result | query: what is the epiphany equation"
    assert sent[1] == "task: question answering | query: who runs rodin"
    assert sent[2] == "title: none | text: body text"
    assert sent[3] == "title: Blueprint | text: body text two"


def test_unknown_query_task_is_rejected():
    svc, _ = make_service()
    with pytest.raises(ValueError):
        svc.embed_query("x", task="sentence similarity")  # documented as not for retrieval


def test_result_is_a_unit_vector_in_the_requested_space():
    svc, _ = make_service()
    res = svc.embed_query("sun breathing thirteenth form")
    assert len(res.vector) == DIM
    assert abs(norm(res.vector) - 1.0) < 1e-6
    assert res.space == EmbeddingSpace()
    assert res.cached is False and res.chunks == 1 and res.truncated is False


# ───────────────────────── U: how failures are caught ─────────────────────────


def test_one_embedding_for_two_texts_is_a_bad_response_not_a_silent_merge():
    # [E1] "Embedding aggregation": a list of plain inputs gives ONE embedding on gemini-embedding-2.
    svc, _ = make_service(ScriptedBackend(override=lambda texts, dim: [bow_vector(texts[0], dim)]))
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_documents([("alpha", None), ("beta", None)])
    assert exc.value.code == "BAD_RESPONSE"


def test_wrong_dimension_is_bad_dimension():
    svc, _ = make_service(ScriptedBackend(override=lambda texts, dim: [[0.5] * 1536 for _ in texts]))
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("x")
    assert exc.value.code == "BAD_DIMENSION"


@pytest.mark.parametrize("bad", [float("nan"), float("inf")])
def test_non_finite_values_are_rejected(bad):
    def override(texts, dim):
        v = bow_vector("x", dim)
        v[3] = bad
        return [v for _ in texts]

    svc, _ = make_service(ScriptedBackend(override=override))
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("x")
    assert exc.value.code == "NOT_FINITE"


def test_all_zero_vector_is_rejected():
    svc, _ = make_service(ScriptedBackend(override=lambda texts, dim: [[0.0] * dim for _ in texts]))
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("x")
    assert exc.value.code == "BAD_RESPONSE"


def test_a_vector_that_is_not_unit_length_is_renormalised_and_counted():
    svc, _ = make_service(ScriptedBackend(override=lambda texts, dim: [[2.0 * x for x in bow_vector(t, dim)] for t in texts]))
    res = svc.embed_query("x")
    assert abs(norm(res.vector) - 1.0) < 1e-6
    assert svc.stats()["renormalized"] == 1


def test_a_failure_raises_never_returns_a_vector_and_is_counted():
    svc, backend = make_service(ScriptedBackend(errors=[EmbeddingUnavailable("API_ERROR", "404 model not found")]))
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("x")
    assert exc.value.code == "API_ERROR"
    s = svc.stats()
    assert s["failures"] == 1 and s["consecutive_failures"] == 1
    assert s["last_error"]["code"] == "API_ERROR" and "404" in s["last_error"]["detail"]
    assert svc.state() == "DEGRADED"


def test_unexpected_backend_exception_becomes_backend_error():
    svc, _ = make_service(ScriptedBackend(errors=[RuntimeError("boom")]))
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("x")
    assert exc.value.code == "BACKEND_ERROR" and "boom" in exc.value.detail


def test_state_goes_unproven_then_ready_then_degraded_then_ready():
    svc, backend = make_service(ScriptedBackend(errors=[None, EmbeddingUnavailable("API_ERROR", "x"), None]))
    assert svc.state() == "UNPROVEN"
    svc.embed_query("one")
    assert svc.state() == "READY" and svc.stats()["last_ok_at"] is not None
    with pytest.raises(EmbeddingUnavailable):
        svc.embed_query("two")
    assert svc.state() == "DEGRADED"
    svc.embed_query("three")
    assert svc.state() == "READY" and svc.stats()["consecutive_failures"] == 0


def test_cache_avoids_a_second_backend_call_and_is_bounded():
    svc, backend = make_service(cache_size=2)
    a = svc.embed_query("alpha")
    b = svc.embed_query("alpha")
    assert len(backend.calls) == 1 and b.cached is True and a.vector == b.vector
    svc.embed_query("beta")
    svc.embed_query("gamma")  # evicts "alpha"
    svc.embed_query("alpha")
    assert len(backend.calls) == 4
    assert svc.stats()["cache_hits"] == 1


# ───────────────────── W: size limits and long-lived behaviour ─────────────────────


def test_long_document_is_split_into_chunks_and_mean_pooled_to_one_unit_vector():
    size = max_body_chars() * 2 + 500
    text = ("alpha beta gamma. " * (size // 18 + 1))[:size]
    svc, backend = make_service()
    res = svc.embed_document(text, title="Long")
    assert res.chunks == 3 and res.truncated is False
    assert len(backend.calls) == 1 and len(backend.calls[0]["texts"]) == 3  # one batched call, one Content per chunk
    assert all(t.startswith("title: Long | text: ") for t in backend.calls[0]["texts"])
    assert abs(norm(res.vector) - 1.0) < 1e-6 and len(res.vector) == DIM


def test_document_beyond_the_chunk_cap_is_flagged_truncated():
    text = "x " * (max_body_chars() * (MAX_CHUNKS + 3) // 2)
    svc, backend = make_service()
    res = svc.embed_document(text)
    assert res.chunks == MAX_CHUNKS and res.truncated is True
    assert svc.stats()["truncated"] == 1


def test_long_query_is_truncated_and_flagged():
    svc, backend = make_service()
    res = svc.embed_query("word " * 20000)
    assert res.truncated is True
    assert len(backend.calls[0]["texts"][0]) <= max_body_chars() + 64


def test_empty_text_is_rejected_before_any_call():
    svc, backend = make_service()
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("   ")
    assert exc.value.code == "EMPTY_INPUT" and backend.calls == []


def test_batch_of_documents_returns_results_in_input_order():
    svc, backend = make_service()
    out = svc.embed_documents([("red apple", "A"), ("blue car", "B"), ("red apple", "C")])
    assert [r.chunks for r in out] == [1, 1, 1]
    assert out[0].vector != out[1].vector
    assert len(backend.calls) == 1 and len(backend.calls[0]["texts"]) == 3


# ───────────────────────── gate, concurrency, configuration ─────────────────────────


def test_router_refusal_raises_router_refused_and_never_reaches_the_backend():
    gate = FakeGate(allowed=False, reason="power state P3 dormant")
    svc, backend = make_service(gate=gate)
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("x")
    assert exc.value.code == "ROUTER_REFUSED" and "P3" in exc.value.detail
    assert backend.calls == [] and gate.recorded == []


def test_router_records_each_attempt_success_or_failure():
    gate = FakeGate()
    svc, _ = make_service(ScriptedBackend(errors=[None, EmbeddingUnavailable("API_ERROR", "x")]), gate=gate)
    svc.embed_query("one")
    with pytest.raises(EmbeddingUnavailable):
        svc.embed_query("two")
    assert [k for k, _ in gate.recorded] == ["rodin_retrieval", "rodin_retrieval"]
    assert all(t == 0 for _, t in gate.recorded)  # the API reports no token usage, so none is invented


def test_concurrency_cap_fails_fast_with_busy():
    release = threading.Event()
    svc, backend = make_service(ScriptedBackend(block=release), max_concurrency=1, acquire_timeout_s=0.05)
    started = threading.Event()

    def slow():
        started.set()
        svc.embed_query("slow one")

    t = threading.Thread(target=slow)
    t.start()
    started.wait(1.0)
    for _ in range(100):  # wait until the first call is inside the backend
        if backend.calls:
            break
        threading.Event().wait(0.01)
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("second")
    assert exc.value.code == "BUSY"
    release.set()
    t.join(2.0)


def test_bad_configuration_makes_every_call_fail_loudly():
    svc = EmbeddingService(ScriptedBackend(), EmbeddingSpace(), config_error="RODIN_EMBED_MODEL='text-embedding-004' is not supported")
    assert svc.state() == "MISCONFIGURED"
    with pytest.raises(EmbeddingUnavailable) as exc:
        svc.embed_query("x")
    assert exc.value.code == "BAD_CONFIG" and "text-embedding-004" in exc.value.detail


def test_error_details_never_carry_credentials():
    """GET /rodin/telemetry serves last_error.detail, and API errors can echo a request. Credentials are redacted at the source."""
    made_up = "AIza" + "A" * 35  # a made-up string shaped like a Google API key; it is not one
    exc = EmbeddingUnavailable("API_ERROR", f"failed for https://example.invalid/?key={made_up} header x-goog-api-key: {made_up} AQ.{'b' * 30}")
    assert made_up not in exc.detail and made_up not in str(exc)
    assert "AQ." + "b" * 30 not in exc.detail and "[REDACTED]" in exc.detail
    svc, _ = make_service(ScriptedBackend(errors=[RuntimeError(f"boom key={made_up}")]))
    with pytest.raises(EmbeddingUnavailable):
        svc.embed_query("x")
    assert made_up not in repr(svc.stats()["last_error"])


def test_the_kernels_service_has_a_short_timeout_and_the_operator_service_a_longer_one():
    from memory.embedding_service import get_default_embedding_service, get_operator_embedding_service

    interactive = get_default_embedding_service().backend
    batch = get_operator_embedding_service().backend
    assert (interactive.timeout_s, interactive.max_retries) == (10.0, 1)
    assert batch.timeout_s > interactive.timeout_s and batch.max_retries > interactive.max_retries


def test_operator_service_has_no_router_gate_and_is_separate_from_the_kernels_default():
    """Operator tools (re-embed, ingestion) run by a person with an explicit paid-run flag; the router's duty cycle
    belongs to the kernel's runtime, and a dormant router in a one-shot process would refuse every call."""
    from memory.embedding_service import get_default_embedding_service, get_operator_embedding_service

    operator = get_operator_embedding_service()
    default = get_default_embedding_service()
    assert operator is not default
    assert operator.stats()["gated"] is False and default.stats()["gated"] is True
    assert get_operator_embedding_service() is operator


def test_stats_reports_whether_a_router_gate_is_attached():
    svc, _ = make_service(gate=FakeGate())
    assert svc.stats()["gated"] is True
    assert make_service()[0].stats()["gated"] is False


def test_resolve_space_from_env(monkeypatch):
    monkeypatch.delenv("RODIN_EMBED_MODEL", raising=False)
    monkeypatch.delenv("RODIN_EMBED_DIM", raising=False)
    space, err = resolve_space_from_env()
    assert space == EmbeddingSpace() and err is None

    monkeypatch.setenv("RODIN_EMBED_MODEL", "gemini-embedding-2")
    monkeypatch.setenv("RODIN_EMBED_DIM", "1536")
    space, err = resolve_space_from_env()
    assert space.dim == 1536 and err is None

    monkeypatch.setenv("RODIN_EMBED_MODEL", "text-embedding-004")  # shut down 2026-01-14 on the Developer API
    monkeypatch.setenv("RODIN_EMBED_DIM", "768")
    space, err = resolve_space_from_env()
    assert space == EmbeddingSpace() and "text-embedding-004" in err

    monkeypatch.setenv("RODIN_EMBED_MODEL", "gemini-embedding-2")
    monkeypatch.setenv("RODIN_EMBED_DIM", "not-a-number")
    space, err = resolve_space_from_env()
    assert err is not None


# ───────────────────────── the Gemini backend, against a fake client ─────────────────────────


def make_backend(client, **kw):
    kw.setdefault("sleep", lambda s: None)
    kw.setdefault("rng", lambda: 0.5)
    return GeminiEmbedBackend(client_factory=lambda: client, **kw)


def test_backend_wraps_each_text_in_its_own_content_and_sets_dimension_and_timeout():
    from google.genai import types

    client = FakeGenaiClient()
    vecs = make_backend(client, timeout_s=20.0).embed_texts(["alpha", "beta"], model="gemini-embedding-2", dim=768)
    call = client.calls[0]
    assert call["model"] == "gemini-embedding-2"
    assert isinstance(call["contents"], list) and len(call["contents"]) == 2
    assert all(isinstance(c, types.Content) and len(c.parts) == 1 for c in call["contents"])
    assert call["config"].output_dimensionality == 768
    assert call["config"].http_options.timeout == 20000
    assert len(vecs) == 2 and len(vecs[0]) == 768


def test_backend_retries_a_429_then_succeeds():
    client = FakeGenaiClient(script=[FakeApiError(429)])
    backend = make_backend(client, max_retries=2)
    vecs = backend.embed_texts(["alpha"], model="gemini-embedding-2", dim=768)
    assert len(client.calls) == 2 and backend.retries == 1 and len(vecs) == 1


def test_backend_does_not_retry_a_client_error_and_names_the_model_in_the_detail():
    client = FakeGenaiClient(script=[FakeApiError(404, "models/text-embedding-004 is not found")], vertexai=True)
    backend = make_backend(client, max_retries=2)
    with pytest.raises(EmbeddingUnavailable) as exc:
        backend.embed_texts(["alpha"], model="text-embedding-004", dim=768)
    assert exc.value.code == "API_ERROR"
    assert len(client.calls) == 1
    assert "text-embedding-004" in exc.value.detail and "vertexai=True" in exc.value.detail


def test_backend_gives_up_after_max_retries():
    client = FakeGenaiClient(script=[FakeApiError(503)] * 5)
    backend = make_backend(client, max_retries=2)
    with pytest.raises(EmbeddingUnavailable) as exc:
        backend.embed_texts(["alpha"], model="gemini-embedding-2", dim=768)
    assert exc.value.code == "API_ERROR" and len(client.calls) == 3


def test_backend_without_a_client_is_no_client():
    backend = GeminiEmbedBackend(client_factory=lambda: None)
    with pytest.raises(EmbeddingUnavailable) as exc:
        backend.embed_texts(["alpha"], model="gemini-embedding-2", dim=768)
    assert exc.value.code == "NO_CLIENT"


def test_backend_with_a_missing_embedding_list_is_a_bad_response():
    class Empty:
        embeddings = None

    client = FakeGenaiClient()
    client.models.embed_content = lambda **kw: Empty()
    with pytest.raises(EmbeddingUnavailable) as exc:
        make_backend(client).embed_texts(["alpha"], model="gemini-embedding-2", dim=768)
    assert exc.value.code == "BAD_RESPONSE"


# ───────────── Unification: the installed SDK really serialises the way we rely on ─────────────


def _mock_client(requests_seen):
    import httpx
    from google import genai
    from google.genai import types

    def handler(request: httpx.Request) -> httpx.Response:
        import json as _json

        body = _json.loads(request.content.decode("utf-8"))
        requests_seen.append({"url": str(request.url), "body": body})
        n = len(body.get("requests", []))
        return httpx.Response(200, json={"embeddings": [{"values": bow_vector(f"doc {i}")} for i in range(n)]})

    return genai.Client(
        api_key="test-key-not-real",
        http_options=types.HttpOptions(httpx_client=httpx.Client(transport=httpx.MockTransport(handler))),
    )


def test_installed_sdk_sends_one_request_per_content_with_the_output_dimensionality():
    seen = []
    backend = GeminiEmbedBackend(client_factory=lambda: _mock_client(seen))
    vecs = backend.embed_texts(["alpha", "beta"], model="gemini-embedding-2", dim=768)
    assert len(vecs) == 2
    assert seen[0]["url"].endswith("/models/gemini-embedding-2:batchEmbedContents")
    reqs = seen[0]["body"]["requests"]
    assert len(reqs) == 2
    assert all(r["outputDimensionality"] == 768 and r["model"] == "models/gemini-embedding-2" for r in reqs)
    assert [r["content"]["parts"] for r in reqs] == [[{"text": "alpha"}], [{"text": "beta"}]]


def test_installed_sdk_aggregates_a_plain_list_of_strings_into_one_request():
    """Guards the trap [E1] documents: if a future SDK changes this, the Content wrapping can be revisited."""
    seen = []
    client = _mock_client(seen)
    res = client.models.embed_content(model="gemini-embedding-2", contents=["alpha", "beta"])
    reqs = seen[0]["body"]["requests"]
    assert len(reqs) == 1 and len(reqs[0]["content"]["parts"]) == 2
    assert len(res.embeddings) == 1
