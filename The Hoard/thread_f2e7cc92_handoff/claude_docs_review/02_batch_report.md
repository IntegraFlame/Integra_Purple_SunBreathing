# 02 — Batch processing report (Message Batches API)
Note: written here because the tool refused the parent's directory (`f2e7cc92-…\scratch\voltron\`); the tool only allows this agent's own artifact directory.

## 0 Read receipt
- voltron_brief.md: 26/26 lines, 4,162 bytes.
- 01__preamble__43754e3dee92.md: 38/38 lines, 1,138 bytes. It is a Python `client.messages.batches.create` example using `claude-haiku-5-5` and `claude-sonnet-5-5`, with `max_tokens` 100.
- 02_Batch_processing_14ee6edfdc40.md: 1,901/1,901 lines, 77,396 bytes. Read in 3 views: 1–800, 801–1400, 1401–1901.
  - First heading: "title: Batch processing" / "# Message Batches API".
  - Last heading: "## Next steps" (cards: Search results, Prompt caching).

## 1 DOC SAYS
- **Mechanics:** `POST /v1/messages/batches` takes `requests[]`. Each request is `{custom_id, params}`, where `params` holds standard Messages params.
  - Requests are processed asynchronously and independently. A failure in one request does not affect the others.
  - `processing_status` goes `in_progress` → `ended`. After a cancel it goes `canceling` → `ended`, and the batch may hold partial results.
  - The response includes `request_counts` {processing, succeeded, errored, canceled, expired}, plus `created_at`, `expires_at`, `ended_at`, `cancel_initiated_at` and `results_url`.
- **Limits:**
  - Up to 100,000 requests or 256 MB per batch, whichever is reached first. Exceeding the size gives 413 `request_too_large`.
  - Most batches finish in under 1 h. Results become available when all requests are done or after 24 h. Requests not finished within 24 h expire.
  - Results are kept for 29 days from `created_at` (not `ended_at`). Batches are scoped to a Workspace.
  - Batch rate limits are separate and "do not affect" Messages API rate limits.
  - Batches "may go slightly over" the Workspace spend limit.
- **`custom_id` format:** `^[a-zA-Z0-9_-]{1,64}$`, and it must be unique within the batch.
- **Not allowed in a batch:** `stream: true`, `speed` (fast mode) and `max_tokens: 0` (cache pre-warm). The minimum is `max_tokens` ≥ 1.
- **Allowed in a batch:** vision, tool use (including all server tools: web search, web fetch, code execution, MCP connectors, advisor, tool search), system prompts, multi-turn, extended thinking, and most betas.
- **Validation timing:** `params` are validated asynchronously, so errors only show up after the whole batch ends. The doc advises a dry run with the sync Messages API first.
- **Results:**
  - Delivered as `.jsonl` in arbitrary order. Match on `custom_id`.
  - Types are `succeeded`, `errored`, `canceled` and `expired`. The last three are not billed.
  - For retries: `errored` with `invalid_request_error` means fix the request first; any other error can be retried as-is.
  - Stream results with `client.messages.batches.results(id)`.
- **Other endpoints:** list (paginated, `limit`), retrieve, cancel, and `DELETE /v1/messages/batches/{id}` (an in-progress batch must be canceled first).
- **Pricing:** 50% of standard prices, applied to input, output and "any special tokens". Batch prices per MTok (input / output):

  | Model | Input | Output |
  |---|---|---|
  | Fable 5.1 / Mythos 5.1 / Fable 5 / Mythos 5 | $5 | $25 |
  | Opus 5.5 | $2 | $10 |
  | Opus 5 / 4.8 / 4.7 / 4.6 / 4.5 | $2.50 | $12.50 |
  | Opus 4.1 / 4 (retired) | $7.50 | $37.50 |
  | Sonnet 5.5 / 5 | $1 | $5 |
  | Sonnet 4.6 / 4.5 / 4 | $1.50 | $7.50 |
  | Haiku 5.5, prompts ≤100k tokens | $0.05 | $0.25 |
  | Haiku 5.5, prompts >100k tokens | $0.25 | $1.25 |
  | Haiku 4.5 | $0.50 | $2.50 |
  | Haiku 3.5 (retired) | $0.40 | $2 |

- **Caching:** batch and cache discounts stack. Cache hits are best-effort, with typical hit rates of 30–98%.
  - Put identical `cache_control: {type: "ephemeral"}` blocks in every request. The default lifetime is 5 min.
  - A Tip recommends the 1-hour cache duration for batches.
- **Server tools:** the batch loop runs more iterations per turn and can return `stop_reason: "pause_turn"`, which you continue with a follow-up request. `web_search` is throttled per org and retried automatically.
- **Extended output (beta):** header `output-300k-2026-03-24` raises `max_tokens` to 300,000 in batches only. The standard limit is 128k.
  - Applies to Opus 5.5 / 5 / 4.8 / 4.7 / 4.6, Sonnet 5.5 / 5 / 4.6 and Haiku 5.5.
  - Available on the Claude API and Claude Platform on AWS, not on Bedrock, Google Cloud or Foundry.
  - One 300k generation can take over 1 h.
  - Python: `client.beta.messages.batches.create(betas=[...])`.
- **Model IDs in the doc:** `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`. Header `anthropic-version: 2023-06-01`.
- **Python types in the doc:** `anthropic.types.message_create_params.MessageCreateParamsNonStreaming` and `anthropic.types.messages.batch_create_params.Request`.
- **Retention and immutability:** data is stored up to 29 days. A submitted batch cannot be modified; you have to cancel it and resubmit.

## 2 MY INFERENCE FOR INTEGRA
- **SWDS:** batches suit the planned rebuild well — no latency requirement, 50% cheaper, and each request gets a `custom_id`.
  - Make each SWDS step one batch request with `custom_id = swds-YYYYMMDD-<phase>-<seq>`, which stays within 64 characters.
  - Write the submit, `batch_id`, every poll, and each result line to the Proof-of-Sleep ledger, including `usage` and `message.id`.
  - Mark phases with no `succeeded` line as NOT EXECUTED. The `request_counts` field and per-line result types give the ledger hard evidence.
  - The 24 h expiry means a cycle can overrun the wake time. The ledger needs a PENDING/EXPIRED state, and wake must not block on results.
- **Siesta:** batches are risky for a short daytime cycle. "Most <1 h" is not a guarantee, so use sync calls or accept carry-over into the next window.
- **Cheshire Cat Daemon:**
  - Study sessions (1–2 h, many calls) can be batched if the steps don't depend on each other.
  - Multi-step chains need one batch per round, with the output of round N feeding round N+1. Expect latency of minutes to hours per round.
  - The 5–15 min delayed reply cannot rely on batch timing; use the sync API.
  - Its "local only" rule limits what it reads. Batches do not violate that, but they keep prompts and outputs on Anthropic servers for up to 29 days. Use `DELETE` once results are in the ledger.
  - Do not give it server tools (web_search, MCP connectors) in batch params. Those would break "local only".
  - The proposed Cheshire model is Gemini, so this applies only if Claude is chosen.
- **Heimdall cost tracking:**
  - Add a batch price table (×0.5) and the Haiku 5.5 price tier at 100k tokens.
  - Read `usage` from each `succeeded` line. Bill $0 for errored, canceled and expired.
  - Heimdall needs its own budget gate before submitting, because the Workspace spend cap can be overrun.
  - Power-down and lockdown must account for batches still running server-side. Either cancel them or explicitly allow them; record either choice in the ledger.
- **Rodin / Phoenix / environment ingestion:**
  - The one-agent-per-file ingestion (metadata nodes) is a strong batch fit: hundreds of independent requests with a shared cached system prompt. Use the 1 h cache.
  - Phoenix re-reading 305 shards nightly can be one batch, with `custom_id` = shard hash prefix.
- **Hoard:** store raw result `.jsonl` lines as immutable evidence alongside the generated nodes.
- **Kernel code:**
  - Batch results have the same content-block shape as sync responses, so the "thinking block first" hazard applies. Join the `text` blocks only.
  - Handle `pause_turn`.

## 3 Contradictions with current wiring
1. **Opus 5.5 price:** the doc's batch price of $2/$10 implies a standard price of $4/$20 per MTok (my inference). Any Heimdall table that assumes older Opus prices ($5/$25, or $15/$75) is wrong. The cost logic must also distinguish batch from sync, which it does not appear to do today.
2. **SDK pin:** we pin `anthropic==1.5.0`. I have not verified that 1.5.0 exposes `messages.batches.results` streaming, `beta.messages.batches` with `betas=`, or the `batch_create_params.Request` import path. It needs a probe.
3. **Cheshire latency:** the 5–15 min reply plan conflicts with batch latency (up to 24 h).
4. **Effort parameters:** the doc never mentions `thinking:{type:"adaptive"}` or `output_config.effort` in batch params. It only says "extended thinking" and standard params are supported. This is not a contradiction, but it is unverified; do a sync dry run first, as the doc advises.
5. **Extended output:** 300k output is unavailable on Google Cloud. If any Claude calls go through Vertex, the beta will not work there.
6. **`max_tokens: 0`:** if anything pre-warms the cache with `max_tokens: 0`, it fails inside a batch.

## 4 Concrete recommended actions (ranked)
1. Probe anthropic 1.5.0 for the batch create/retrieve/results/cancel/delete methods and the beta `betas=` parameter, then submit a 2-request test batch. Effort: S.
2. Add batch pricing (×0.5, the Haiku 5.5 tier, $0 for non-succeeded results) and a pre-submit budget gate to Heimdall. Effort: S.
3. Build a `BatchRunner` in the kernel. Effort: M. It should:
   - generate `custom_id` from ledger IDs;
   - sync dry-run one request;
   - submit, then poll every 60 s;
   - stream `.jsonl` results to the ledger and The Hoard;
   - retry non-`invalid_request` errors;
   - `DELETE` the batch after it is archived.
4. Rebuild SWDS and Phoenix consolidation on `BatchRunner`, with the 1 h shared-prefix cache and PENDING/EXPIRED ledger states. Wake must not block on results. Effort: M.
5. Run the environment ingestion as batches of ≤10k files each, with a shared cached instruction prompt. Effort: M.
6. Heimdall lockdown policy for batches still running: cancel or allow them, and log the choice. Effort: S.
7. Keep Cheshire's 5–15 min replies on sync calls. Batch only its overnight study rounds, with no server tools. Effort: L (depends on the daemon build).
