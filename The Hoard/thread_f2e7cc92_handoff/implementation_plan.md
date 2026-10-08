# Plan v2: Make all 7 model clients real (live-verified)

**Probed:** 2026-10-07 10:05–12:40 CDT (15:05–17:40Z), Baker, LA
**Mode:** `/plan` — nothing has been modified. Every claim comes from a probe I ran, except where marked *(code-read)*.
**Scope:** all 7 clients verified by real calls, Gemini 403 / Vertex resolved, real calls feed the Dashboard counters.

## Your decisions (locked into this plan)

| Role | Model | Source |
|---|---|---|
| `nexus_right` | `claude-opus-5-5` | your call |
| `shiva_orchestrator` | `claude-sonnet-5-5` | your call, probe-checked below |
| `y789_left`, `jean_grey_phoenix` | `gemini-3.1-pro-preview` | the non-preview ID 404s |
| `rodin_retrieval` | `gemini-3.8-flash` (+ `text-embedding-004`, 768-d) | recommendation below |
| `cheshire_cat_kernel`, `cheshire_protocol` | `gemini-3.8-flash` | existing |
| Heimdall | stays local math; optional `heimdall_analyst` = `gemini-3.1-pro-preview` | needs your OK (Q3) |

## Verified findings

### A. Why every Claude call returns 401 (new, root cause)
- Two different Claude keys exist (fingerprints only): `fee06a8f` (len 108) and `d6aa5d50` (len 106).
- `fee06a8f` sits in `.env`, `CLAUDE_API_KEY.env` and `claudehemisphere.env`. It now returns **401 "API key is invalid"**. It worked at ~10:06, so it was revoked or rotated since.
- `d6aa5d50` is only in `env_file_map.env` (edited 12:07, your update). It returns **200**. This is the working key.
- `config/env_loader.py` loads many files and **later files override earlier ones**. The dead key in `CLAUDE_API_KEY.env` / `claudehemisphere.env` wins over your new one.
- `GEMINI_API_KEY.env` has two `GEMINI_API_KEY=` lines with different values. The last one wins and works. The other (`43d94f50`) is untested.
- **Docker consequence:** compose uses `env_file: .env`, which holds the dead Claude key.

### B. Anthropic SDK in the venv is broken (new)
- `import anthropic` fails with `ModuleNotFoundError: anthropic.types.messages`.
- The 12 files in `.venv/Lib/site-packages/anthropic/types/messages/` are missing. A RECORD scan of 20,589 files across 148 packages found only these 12 missing. The cause is unknown (a targeted deletion, not general OneDrive damage).
- The running kernel still has the SDK in memory. A **restart would swallow the error**, because client init catches exceptions and sets `client=None`, so Claude would silently report NO_CLIENT.
- Fix: `pip install --force-reinstall --no-deps anthropic==1.5.0` in the venv, plus make init failures loud.

### C. Gemini (re-verified 12:25 CDT with the new key)
| Mode | `gemini-3.8-flash` | `gemini-3.1-pro-preview` | `gemini-3.1-pro` |
|---|---|---|---|
| `genai.Client(api_key=K)` (today's code) | 403 | 403 | 403 |
| `genai.Client(vertexai=True, api_key=K)` | OK | OK | **404** |
- The key is a Vertex express key (`AQ.` prefix). `.env` sets `USE_VERTEXAI=true`, but the SDK reads `GOOGLE_GENAI_USE_VERTEXAI` and the clients ignore both.
- Thinking works through `thinking_budget` and `thinking_level`. Embeddings work: `text-embedding-004` is 768-d.
- **Trap:** Flash thinks by default. With a small `max_output_tokens` the text comes back **empty**, also when streaming. Clients need an empty-response guard.
- Timings are single samples and noisy:
  - 3.8 Flash: budget 2048 took ~1.3 s, 8192 took ~1.9 s, level HIGH took 3.4 s.
  - 3.1 Pro: budget 8192 took 9.3 s with 815 thought tokens. Level HIGH took **34.9 s** with 3823 thought tokens.

### D. Claude request shape (new probe, valid key, raw API, 12:39 CDT)
- **`output_config` is accepted by the raw API.** Valid `effort` values: **`low`, `medium`, `high`, `xhigh`, `max`**. A bogus value returns 400 with that exact list.
- Output on `claude-sonnet-5-5` + `thinking:{type:"adaptive"}`:

| effort | blocks | out tokens | latency |
|---|---|---|---|
| (unset) | text | 148 | 10.2 s |
| low | text | 176 | 7.0 s |
| medium | text | 159 | 7.6 s |
| high | text | 157 | 6.0 s |
| max | **thinking, text** | 518 | 12.6 s |

- On a trivial prompt, Sonnet only emitted a thinking block at `max`. A thinking block can therefore appear first at any time, so the `content[0].text` crash is a real hazard.
- **Opus 5.5 vs Sonnet 5.5**, same prompt ×3, adaptive, default effort:

| | latencies | mean | out tokens |
|---|---|---|---|
| Sonnet 5.5 | 5.2 / 19.5 / 8.7 s | **11.1 s** | 135 |
| Opus 5.5 | 7.0 / 6.0 / 6.0 s | **6.3 s** | 178 |

- **Honest reading:** n=3 on a trivial prompt, so this is weak evidence. It does **not** support "Sonnet is faster". Sonnet's spread is large (5–19 s), probably server load, and Opus was steady and always emitted a thinking block. The case for Sonnet on Shiva is **price** (~half) and token volume, not latency. I will re-measure both on a realistic Shiva-lens prompt during the live selftest.
- Whether SDK 1.5.0 takes `output_config` natively or needs `extra_body` is **still unverified**, because the SDK is broken. I will test it right after the reinstall, before writing the client code.

### E. Other
- `models.yml` overrides `.env` and class defaults through `ModelRouter.get_routed_client`. It currently holds Y789/Jean Grey = `gemini-3.1-pro` (404), Rodin = `gemini-3.6-flash` (my earlier 3.8 edit never took effect), and Nexus/Shiva = `claude-sonnet-5.5` (dotted, 404). The correct Claude IDs use dashes.
- `config/env_loader.py` has stale defaults (`claude-sonnet-4-6`).
- `/models/telemetry` shows 0 calls on all models. `/swds/awaken` does not call `MODEL_ROUTER.activate()`. SWDS persisted timestamps are inconsistent (leftover from the frozen-clock bug).

> [!WARNING]
> **Corrections to my earlier claims.** I reported Task #2 (Nexus/Shiva → 5.5) and Task #3 (Rodin → 3.8) as done. Both were file edits never verified by a live call, and both were wrong or ineffective as shipped. "7 agents locked in" came from startup logs only.

## Answers to your questions

1. **Selftest auth: yes, require a header.** It spends real money. Use `X-Integra-Admin` checked against an env `INTEGRA_ADMIN_TOKEN` (constant-time compare), plus a rate limit of 1 run per 30 s. A custom header also stops a web page you visit from POSTing to `127.0.0.1:8000` (CSRF / DNS rebinding), which a plain open endpoint allows. Keep the status GETs open. `/swds/*` POSTs are also unauthenticated; that is out of scope but noted.
2. **Nexus = Opus, Shiva = Sonnet: agree.** Nexus is low-frequency, high-judgment synthesis, so the Opus premium is justified. Shiva runs per lens and often, so Sonnet's half price matters. The probe did not show a latency advantage for Sonnet (see D). I will re-check with real prompts, and the split stays unless that contradicts it.
3. **Rodin: 3.8 Flash, not Opus.** Rodin's hot path is a Gemini embedding plus KNN retrieval, and Anthropic has no embeddings. Opus would add 2×+ cost on a path that needs low latency. Use a modest thinking budget (~2048). "Extended" buys little here.
4. **Heimdall 3.1: keep the sentinel local and deterministic.** It is an EMA of Shannon entropy polled every 5 s, so it is not a model call. Calling a Pro model per poll would be slow (9 s at budget 8192, 35 s at HIGH) and costly. **Proposal:** add an optional 8th router component `heimdall_analyst` on `gemini-3.1-pro-preview` with `thinking_budget=8192`. It runs event-driven only when `H_smooth > 2.5`, asynchronously, under a router token budget, for UGL / P-SSR re-grounding. This is new scope and needs your OK.

## Proposed changes

### Step 0 — Key consolidation (confirm with you before touching secret files)
- Put the working Claude key into `.env`. Blank or remove the stale entries in `CLAUDE_API_KEY.env` and `claudehemisphere.env`. Remove the duplicate Gemini line in `GEMINI_API_KEY.env`.
- `config/env_loader.py`: apply a sane precedence (OS environment, then `.env`, then the others) and log **fingerprint-only** warnings when files conflict.
- Key values are never printed. Rotation stays deferred to the end.

### Step 1 — Repair the SDK
- `pip install --force-reinstall --no-deps anthropic==1.5.0` in `.venv`. Then run the probe for native `output_config` vs `extra_body`.

### core/api_clients.py — [MODIFY]
- `_make_gemini_client()`: Vertex express when `GOOGLE_GENAI_USE_VERTEXAI` or `USE_VERTEXAI` is truthy.
- `_first_text(resp)` for Claude: join the `text` blocks only (Nexus and Shiva).
- `_claude_thinking_kwargs(model, enable, budget, effort)`:
  - 5.x: `adaptive` + `output_config.effort` (validated against `low|medium|high|xhigh|max`).
  - 4.x: `enabled` + `budget_tokens`.
- Gemini empty-text guard returns `error="EMPTY_RESPONSE"` with thought-token counts.
- Client init failures are logged at ERROR and surfaced in telemetry (`last_error`), not swallowed.
- Defaults and the `ModelTokenTelemetryHub` / `INTEGRA_MODEL_REGISTRY` display strings are aligned to the table above.

### models.yml / .env / config/env_loader.py — [MODIFY]
- Aligned to the model table. Remove the stale `claude-sonnet-4-6` defaults.
- Add `INTEGRA_ADMIN_TOKEN` to `.env` (generated locally, never printed).

### main.py — [MODIFY]
- `POST /models/selftest` (header-gated, rate-limited): one minimal call per router key through `MODEL_ROUTER.get_routed_client(...)`, so `record_call` and the Dashboard counters get real data. Rodin also tests `embed()`. It returns per-model `{ok, model, latency_ms, tokens, thinking_tokens, error}`.
- `/swds/awaken` calls `MODEL_ROUTER.activate()`.

### tests/test_api_clients.py — [NEW]
- Offline: thinking-first fake response, 4.x vs 5.x kwargs, effort validation, Vertex factory switch, empty-text guard, selftest auth (401/429/200).
- `@pytest.mark.live` (skipped by default): one call per provider.

## Verification plan
1. `pytest tests\test_api_clients.py -q` (offline), then `-m live`.
2. Restart the kernel. Confirm clean startup with no swallowed init errors.
3. `POST /models/selftest` with the header. Expect 7/7 `ok:true`. Failures are reported verbatim.
4. `GET /models/telemetry` shows calls ≥ 1 and non-zero tokens. `/dashboard` shows the corrected model names.
5. Re-measure Opus vs Sonnet on a realistic Shiva-lens prompt, and report whether the split holds.
6. Afterwards: `docker compose up -d --build` (needs Step 0, because compose reads `.env`), then check health and mounts.

## Out of scope / tracked
- **Key rotation and security cleanup** — last, as you asked. The `.env` keys were also printed into this session earlier.
- Stale SWDS timestamps, and whether the SWDS "dream sequences" are simulated (0 model calls observed so far).
- Tonight's 07:00 SWDS wake is the real test of the clock fix.

## Risks
- Preview model IDs can be retired; the selftest is the early warning.
- Express-mode billing and quota follow the Vertex project behind the key.
- If SDK 1.5.0 can't pass `output_config`, I use `extra_body`. If that also fails, fall back to `adaptive` without effort (verified working).
- Consolidating key files is irreversible-ish; I will back the files up locally first and show you the fingerprint diff, not the values.

## Open decisions for you
- **Q1:** OK to consolidate the key files as in Step 0 (with local backups)?
- **Q2:** OK to add the optional `heimdall_analyst` (event-driven on breach only)?
- **Q3:** Default Claude effort: `high` for Nexus (Opus) and `medium` for Shiva (Sonnet)? That is my suggestion.
