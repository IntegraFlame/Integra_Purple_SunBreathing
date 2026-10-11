# 10 — Prompt Caching Report
Stamp: 2026-10-08 ~03:05 CDT (08:05Z). Reader: subagent 1908efd4.
(Intended path was the parent's scratch/voltron/10_prompt_caching_report.md. The tool refused to write outside my own artifact dir, so this copy lives in my dir.)

## 0 Read receipt
- File: `docsplit/10_Prompt_caching_1235fda1dd3e.md`. Read all **3,358 lines / 163,632 bytes** (lines 1–3358 across 7 views, no gaps). Source tag: `Claudecode5Untitled-3.md lines 4134-7490`.
- First heading: title "Prompt caching" → first `##` "How prompt caching works". Last heading: `## FAQ`, final accordion "Why am I seeing 'TypeError: Cannot read properties of undefined (reading 'messages')'?".
- About 60% of the file is the same example repeated in 9 languages (cURL/CLI/Py/TS/C#/Go/Java/PHP/Ruby). I read all of it. None of the repeats add facts.
- Also read `integra-homebase/core/api_clients.py` in full (1,050 lines) to check §3 against the code.

## 1 DOC SAYS
- **Two modes.** (a) Automatic caching: top-level `"cache_control": {"type":"ephemeral"}`. The breakpoint goes on the last cacheable block and moves forward as the conversation grows. (b) Explicit caching: `cache_control` on individual blocks. Prefix order is `tools` → `system` → `messages`. `"ephemeral"` is the only cache type.
- **TTL.** 5 min by default. Reading the entry refreshes it at no extra cost. 1 h is available with `"ttl": "1h"`. The lifetime is counted **from the start of the request**, so generation time uses up part of the TTL. When mixing TTLs, longer TTLs must come before shorter ones. Billing is split at positions A (read), B (1h write) and C (5m write).
- **Multipliers.** 5m write = 1.25× base input. 1h write = 2×. Read = 0.1×, **except Opus 5.5 / Sonnet 5.5 = 0.05×** and Fable/Mythos 5.1 = 0.025×. These stack with the Batch discount and data residency.
- **Prices ($/MTok: base / 5m write / 1h write / hit / output).**
  - Opus 5.5: 4 / 5 / 8 / 0.20 / 20
  - Sonnet 5.5: 2 / 2.50 / 4 / 0.10 / 10
  - Opus 5: 5 / 6.25 / 10 / 0.50 / 25
  - Haiku 5.5 (≤100k): 0.10 / 0.125 / 0.20 / 0.01 / 0.50
- **Minimum cacheable length.** 512 tokens for Fable 5.1, Mythos 5.1, Opus 5.5, Opus 5, Sonnet 5.5, Fable 5, Mythos 5 and Haiku 5.5. 1,024 for Opus 4.8, Sonnet 5, Sonnet 4.6 and 4.5. 2,048 for Opus 4.7. 4,096 for Opus 4.6, Opus 4.5 and Haiku 4.5. If the prompt is too short, caching is **silently skipped**: there is no error and both cache fields are 0.
- **Breakpoints.** At most **4** (an automatic breakpoint uses one of the slots). A write happens only at a breakpoint. Reads look back at most **20 blocks**. A run of `tool_use` or `tool_result` blocks counts as 1 position. Breakpoints cost nothing.
  - If 4 explicit breakpoints are already set and you add automatic caching, you get a 400.
  - If the automatic TTL differs from an explicit TTL on the last block, you get a 400.
- **Pre-warming.** Send `max_tokens: 0`. The response has empty `content`, `stop_reason:"max_tokens"`, and you pay the cache write but no output.
  - Rejected when combined with: `stream:true`, `thinking.type:"enabled"`, `output_config.format`, `tool_choice` set to tool/any, or use inside Message Batches.
  - You must use an **explicit** breakpoint on the shared prefix, and the **same thinking config and effort** as the real calls.
- **What invalidates the cache.**
  - Changing tool definitions invalidates everything.
  - Toggling web search or citations, or changing `speed`, invalidates system and messages.
  - Changing `tool_choice` or adding/removing images invalidates messages.
  - Changing **thinking params or `output_config.effort`** always invalidates messages, and on some models also tools and system. Setting effort explicitly to the model's default counts the same as omitting it.
  - Dropped thinking blocks invalidate from that point on.
  - Matching requires 100% identical bytes. Unstable JSON key order breaks it.
  - On Opus 5.5 and Sonnet 5.5 you can append a `{"role":"system"}` message to `messages` without breaking the cache. Sonnet 5 does not support this.
  - Thinking blocks can't carry `cache_control`, but they get cached as part of earlier turns and count as input when read.
- **Usage fields.** `cache_creation_input_tokens`, `cache_read_input_tokens`, `input_tokens` (counts **only tokens after the last breakpoint**), `cache_creation.{ephemeral_5m_input_tokens, ephemeral_1h_input_tokens}`, `output_tokens`, `iterations[]`, `service_tier`, `inference_geo`.
  - total input = read + creation + input.
  - Cache hits are not counted against rate limits.
- **Isolation, Batches, misc.**
  - Caches are isolated **per workspace** on the Claude API. On Bedrock and Google Cloud they are isolated per org.
  - A cache entry only becomes available once the first response begins, so parallel calls launched together won't hit it.
  - With Batches, hits are best-effort. Recommended pattern: send one request that writes the shared prefix with a 1h breakpoint, then submit the rest.
  - There is no way to clear the cache manually.
  - Caching is no longer a beta: use `client.messages.create`, not `client.beta.prompt_caching`.

## 2 MY INFERENCE FOR INTEGRA
- **Identity / kernel-card caching (Nexus, Shiva).** Every call is a single turn: `messages=[1 user]`, plus a `system` string.
  - The only reusable prefix is the system/identity text. Make it a list block with an explicit `cache_control` on it.
  - **Do not use top-level automatic caching here.** It would put the breakpoint on the user message, which changes every call. That is the "common mistake" in the doc: you pay 1.25× on every call and never get a read.
  - The kernel card must be ≥512 tokens and **byte-stable**: no timestamps, no dual-clock stamps, no telemetry numbers in the cached block.
  - Put changing data (clock, Heimdall state) after the breakpoint, or in a mid-conversation `role:"system"` message.
  - Cost example: a 4k-token Opus 5.5 kernel card. Uncached it costs $0.016 per call. A cache hit costs $0.0008, which is 20× cheaper.
- **Cheshire Daemon long study loops (1–2 h).** This only applies if the Daemon runs on Claude. The proposed Gemini 3.1 Pro does not use Anthropic caching.
  - A growing study transcript fits the multi-turn pattern. Put one breakpoint on the identity and memory-node pack, and a moving breakpoint on the last turn.
  - Use **1h TTL** if calls are more than 5 min apart. Deep-thinking generations eat into the TTL, which is measured from request start.
  - If a single turn adds more than 20 blocks (e.g., many tool results), add a second breakpoint.
  - Keep `effort` fixed for the whole session. Changing it breaks the cached message prefix.
- **SWDS batch + 1h cache.** For a night run of many consolidation calls with a shared prefix (instructions plus a node pack):
  1. Send one request with a 1h breakpoint to write the prefix.
  2. After it completes, submit the rest as a Batch.
  - `max_tokens:0` pre-warm **cannot** be used inside Batches; it has to be a separate non-batch call.
  - Every call's `usage` should go into the Proof-of-Sleep ledger. A non-zero `cache_read_input_tokens` is hard evidence that a model call actually happened.
- **Heimdall cost accounting.** Cost per call = Σ(field × price).
  - Opus 5.5: `input×4 + eph5m×5 + eph1h×8 + cache_read×0.20 + output×20`, all ÷1e6.
  - Sonnet 5.5: the same formula with 2 / 2.5 / 4 / 0.10 / 10.
  - Alerts:
    - hit-ratio = read/(read+creation+input) below a target.
    - both cache fields = 0 when caching was expected. That means the prefix is under 512 tokens or a prefix byte changed.
    - repeated creation with no reads, which means the breakpoint sits on varying content.

## 3 Contradictions with current wiring (api_clients.py)
1. **No `cache_control` anywhere.** `NexusClient` and `ShivaOrchestratorClient` pass `system` as a plain string (L484–485, L958–959). Caching is off, so the system prompt is paid at full price on every call.
2. **Telemetry undercounts once caching is on.** `_extract_anthropic_tokens` (L180–189) reads only `input_tokens`, `output_tokens` and `thinking_tokens`.
   - The doc says `input_tokens` excludes cached tokens, so prompt totals and cost would drop artificially.
   - `thinking_tokens` is **not a usage field listed in this doc**. Check whether it always reads 0.
   - `cache_*` fields and `cache_creation.*` are ignored.
3. **Streaming and non-streaming config mismatch.** `NexusClient.generate_iterative` (L543–550) sends **no thinking/effort**, while `generate` sends adaptive thinking + effort. The thinking config is rendered into the prompt, so the two paths cannot share cache entries. They also behave differently.
4. **Dual-clock injection risk.** The constitution says to stamp timestamps on outputs. If those stamps are ever put into the `system` string, the cache is invalidated on every call. I did not verify where the system prompts are built. Needs a check.
5. **SDK pin `anthropic==1.5.0`.** The doc only says prompt caching needs no beta namespace. Whether 1.5.0 accepts a top-level `cache_control` kwarg is **unverified** (`extra_body` would work around it). Block-level `cache_control` inside `system` list dicts is plain JSON and should pass.
6. **Pricing assumptions.** The brief has no Anthropic price table. Any $ figure Heimdall uses must come from the 5.5 rows above. Note that the 0.05× hit rate on Opus/Sonnet 5.5 is not the generic 0.1×.
7. **Workspace isolation.** Both Claude clients send the same `ANTHROPIC_WORKSPACE_ID`, which is fine. Splitting workspaces later would split the caches.

## 4 Concrete recommended actions (ranked)
1. **(S)** Extend `_extract_anthropic_tokens` and `ModelTokenTelemetryHub` to record `cache_read_input_tokens`, `cache_creation_input_tokens`, `ephemeral_5m/1h`, and `total_input = read+creation+input`. Add a per-model $ calculator using the 5.5 rows. Run this before enabling caching so the baseline is honest.
2. **(S)** Convert `system` to `[{"type":"text","text":KERNEL_CARD,"cache_control":{"type":"ephemeral"}}]` for Nexus and Shiva. Use a byte-stable, ≥512-token card. Then probe once and check the `usage` cache fields on a real call. Do not claim caching works without that evidence.
3. **(S)** Make `generate_iterative` send the same thinking/effort kwargs as `generate`.
4. **(S)** Audit where system prompts are built. Move timestamps, clock data and telemetry after the breakpoint, or into a mid-conversation `role:"system"` message (Opus/Sonnet 5.5 only).
5. **(M)** Cheshire Daemon (if it runs on Claude):
   - 1h-TTL breakpoint on identity + memory pack, plus a moving breakpoint on the last turn.
   - Fixed effort for the session.
   - Log every call's `usage` to the ledger.
6. **(M)** SWDS rebuild: one request writes the 1h prefix, then a Batch runs the remaining calls. Reports are rendered from the logged `usage` fields.
7. **(M)** Heimdall alerts: hit-ratio floor; "creation>0 and read=0 repeatedly"; "both cache fields 0 when caching was expected".
8. **(L)** Optional pre-warm job (`max_tokens:0`, non-stream, not batched, same thinking/effort) when the kernel starts or Siesta ends. Only worth it if the 1h TTL is used; at 5m it would need a call every ≤5 min.
