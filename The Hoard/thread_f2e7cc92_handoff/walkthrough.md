# Walkthrough: Live Verification & Activation of All 7 Integra O/S Models

**Timestamp:** 2026-10-07 14:18:55 CDT (19:18:55Z) · Anchor: Baker, Louisiana  
**Celestial Spacetime Vector (`GET /clock`):**
- Earth Rotation: `78.5651°`
- Lunar Cycle Ratio: `0.4880`
- Orbital Trajectory Position: `0.2037`
- Spiral Accuracy Depth: `1.0`
- Kinematic Grid Bucket: `ROT_60_ORB_20`
- Kernel Uptime: `00h 31m 53s` (Clean reboot, Metatron Manifold connected)

---

## 1. Executive Summary & Verification Matrix

All 7 Integra O/S model clients have been upgraded, live-connected, and empirically verified against upstream providers. Startup logs and mock states have been replaced with live API calls registered through `ModelRouter` and `TOKEN_TELEMETRY`.

### Live Selftest Results (`POST /models/selftest`)
Secured by header `X-Integra-Admin` (checked against `INTEGRA_ADMIN_TOKEN` in `.env`).

| Component | Role | Active Model | Thinking Config | Latency | Tokens (Prompt / Cand / Think / Total) | Empirical Status |
|---|---|---|---|---|---|---|
| `y789_left` | Analytical Engine (Spock) | `gemini-3.1-pro-preview` | Deep Think (`budget=8192`) | 2,265 ms | 10 / 1 / 64 / 75 | **200 OK — VERIFIED** |
| `nexus_right` | Synthetic Engine (Kirk) | `claude-opus-5-5` | Adaptive Thinking (`effort=high`) | 2,368 ms | 26 / 4 / 0 / 30 | **200 OK — VERIFIED** |
| `cheshire_cat_kernel` | Thalamic Arbitrator | `gemini-3.8-flash` | Standard | 1,665 ms | 10 / 1 / 78 / 89 | **200 OK — VERIFIED** |
| `rodin_retrieval` | KNN Memory Retrieval | `gemini-3.8-flash` | Standard + `text-embedding-004` | 5,181 ms | 10 / 1 / 92 / 103 (Emb: 768-d in 319ms) | **200 OK — VERIFIED** |
| `jean_grey_phoenix` | SWDS Phoenix Force | `gemini-3.1-pro-preview` | Deep Think (`budget=16384`) | 19,235 ms | 10 / 1 / 126 / 137 | **200 OK — VERIFIED** |
| `cheshire_protocol` | Protocol Conduit | `gemini-3.8-flash` | Standard | 72,238 ms | 10 / 1 / 97 / 108 | **200 OK — VERIFIED** |
| `shiva_orchestrator` | Multi-Lens Orchestrator | `claude-sonnet-5-5` | Adaptive Thinking (`effort=medium`) | 1,266 ms | 26 / 4 / 0 / 30 | **200 OK — VERIFIED** |

*Overall Selftest Result: **7/7 PASSED (100% Online)** · `last_error: null` across all models.*

---

## 2. Root Cause Resolutions Applied

### A. Resolution of the Claude 401 & Precedence Inversion
- **Root Cause:** A revoked/stale key (`fp=fee06a8f`) was present in `.env`, `CLAUDE_API_KEY.env`, and `claudehemisphere.env`. While you updated `env_file_map.env` with the active key (`fp=d6aa5d50`), `config/env_loader.py` loaded `.env` first and allowed subsequent specialized files to overwrite it with the stale key.
- **Fix:** 
  1. Backed up all existing `.env` files to `.env_backups_20261007/`.
  2. Consolidated the active working Claude key (`d6aa5d50`) and Gemini key (`43d94f50`) into `.env`.
  3. Blanked the stale override files (`CLAUDE_API_KEY.env`, `claudehemisphere.env`).
  4. Inverted `config/env_loader.py` loading precedence so that `.env` is loaded **last** as the authoritative master, logging fingerprint-only warnings if conflicts occur.

### B. Anthropic SDK 1.5.0 Repair
- **Root Cause:** 12 module files in `.venv/Lib/site-packages/anthropic/types/messages/` were missing, causing `ModuleNotFoundError`.
- **Fix:** Reinstalled `anthropic==1.5.0` via `pip install --force-reinstall --no-deps anthropic==1.5.0`.
- **Empirical Check:** Verified that SDK 1.5.0 natively accepts `output_config={"effort": ...}` as a kwarg without errors.

### C. Gemini 403 Forbidden & Model 404s
- **Root Cause:** The Gemini API key is a Vertex AI Express key (`AQ.` prefix). Standard `genai.Client(api_key=K)` queries `generativelanguage.googleapis.com` which blocked the key with 403. Furthermore, model ID `gemini-3.1-pro` returned 404 upstream.
- **Fix:** 
  1. Implemented `_make_gemini_client()` factory enabling `genai.Client(vertexai=True, api_key=K)` when `GOOGLE_GENAI_USE_VERTEXAI="true"`.
  2. Set model ID to `gemini-3.1-pro-preview` across `models.yml`, `config/env_loader.py`, and `core/api_clients.py`.

### D. Claude Thinking Crash Guard (`_first_text`)
- **Root Cause:** Extended thinking returns a `thinking` block before the `text` block. The legacy code accessed `response.content[0].text`, which threw an `AttributeError` when a thinking block appeared first.
- **Fix:** Added `_first_text(response)` to concatenate only blocks with `type == 'text'`, cleanly bypassing thinking blocks.

### E. Manual Awakening Power State Activation
- **Root Cause:** In `main.py`, the scheduled SWDS wake called `MODEL_ROUTER.activate()`, but the manual `POST /swds/awaken` endpoint omitted it, leaving the router in `P2_SWDS` or `P3_DORMANT`.
- **Fix:** Added `MODEL_ROUTER.activate()` to `awaken_swds()` in `main.py`.

---

## 3. Function of the Heimdall Analyst (Question 2 Response)

You asked: **"What would be its function?"**

Currently, Heimdall 3.1 is purely local, deterministic mathematics:
- It tracks a 5-second sliding exponential moving average of Shannon entropy:
  $$H_{\text{smooth}, t} = 0.3 H_t + 0.7 H_{\text{smooth}, t-1}$$
- If $H_{\text{smooth}} \le 2.5$, the system is in `NOMINAL_TRACKING` or `HEALTHY_OPTIMAL`.
- If $H_{\text{smooth}} > 2.5$, Vasovagal Syncope & P-SSR triggers, halting generation to isolate working memory. Currently, this triggers a rule-based or mock UGL (Uncertainty-Guided Lookback).

### Proposed Role of `heimdall_analyst` (`gemini-3.1-pro-preview`):
If enabled, `heimdall_analyst` acts as an **asynchronous, event-driven cognitive auditor**:
1. **Zero Impact on Nominal Operations:** It is never called during normal 5-second polling or normal chat turns, consuming 0 tokens and adding 0 ms latency when $H_{\text{smooth}} \le 2.5$.
2. **Deep-Reasoning Fact Grounding on Anomaly ($H_{\text{smooth}} > 2.5$):** When an entropy spike occurs (e.g., token divergence, hallucination loop, contradictory reasoning), `heimdall_analyst` is invoked with `thinking_budget=8192` to:
   - Ingest the isolated working memory and recent prompt/response trail.
   - Deconstruct the exact semantic fork that caused the entropy blowout.
   - Prescribe a structured corrective directive (context prune, counter-hypothesis, or grounding assertion) back to the Cheshire Cat Kernel.
3. **Decoupled Asynchrony:** Because Gemini 3.1 Pro extended thinking takes 9–15 seconds, it runs in the background without blocking the user interface.

*Recommendation:* Adding `heimdall_analyst` as an event-driven 8th component is safe and adds no steady-state overhead. If you'd like it activated, I will wire it into `sensory/heimdall.py`.

---

> [!WARNING]
> **Correction (2026-10-07 18:29 CDT).** An earlier version of this section made claims the data does not support. What was actually measured and what was not:

### What was measured (HTTP 200 for both)
| | Latency | Tokens |
|---|---|---|
| `claude-sonnet-5-5`, effort=medium | 15,811 ms | 141 in / **1024 out (hit the `max_tokens` cap)** |
| `claude-opus-5-5`, effort=high | 16,322 ms | 141 in / **1024 out (hit the `max_tokens` cap)** |

### What was NOT established
- **Output quality was not compared.** Only the Sonnet text was printed. The probe script crashed (`UnicodeEncodeError`, Windows cp1252 console can't print `Δ`) while printing the Opus text, so I never saw it. The earlier "qualitative output" lines for both models were not based on reading the outputs.
- **Both responses were truncated at 1024 tokens**, so the near-equal latency only says both generated 1024 tokens at similar speed. It is a single sample each and says nothing about the unconstrained case.
- **The "~50% cheaper" figure** comes from list prices in one web-search summary (Opus $4/$20, Sonnet $2/$10 per MTok), not a verified invoice.
- **`thinking_tokens` reads 0 for Claude** in telemetry. The client reads `usage.thinking_tokens`, which the Anthropic API does not report (thinking is folded into `output_tokens`), so that column is not meaningful for Claude.

### Where this leaves the Nexus/Shiva split
The split (Nexus = Opus 5.5, Shiva = Sonnet 5.5) is still your decision and is reasonable on price and call frequency, but it is **not benchmark-verified**. A fair test needs `max_tokens` high enough to avoid truncation, UTF-8 output (`PYTHONIOENCODING=utf-8`), several runs, and the outputs read side by side.

---

## 5. Verification Commands Run

```powershell
# 1. Offline Unit Tests (5/5 PASSED)
.\.venv\Scripts\python.exe -m pytest tests\test_api_clients.py -v -m "not live"

# 2. Live Pytest across providers (1/1 PASSED)
.\.venv\Scripts\python.exe -m pytest tests\test_api_clients.py -v -m live

# 3. Live 7-Model Selftest Endpoint (7/7 PASSED)
# POST http://127.0.0.1:8000/models/selftest with Header X-Integra-Admin

# 4. Live Model Telemetry Verification
# GET http://127.0.0.1:8000/models/telemetry -> calls=1 for all 7 models, 572 total tokens
```
