# 09 — Token Counting: Report

## 0 Read receipt
- File: `docsplit/09_Token_counting_03d4c2753dc5.md` — read lines 1–1456 in full (45,008 bytes), in two view_file calls (1–800, 800–1456).
- Source marker: `Claudecode5Untitled-3.md lines 2677-4133`. Page title "Token counting".
- First heading seen: `## How to count message tokens`. Last heading seen: `## Next steps`.
- Cross-checked (read-only) against: `integra-homebase/core/model_router.py` L295–320, L460–530; `core/api_clients.py` L470–520; grep of `core/*.py` for token/usage/budget terms.

## 1 DOC SAYS
- **Endpoint:** `POST https://api.anthropic.com/v1/messages/count_tokens`, headers `x-api-key`, `anthropic-version: 2023-06-01`, `content-type: application/json`. Python: `client.messages.count_tokens(...)`; CLI: `ant messages count-tokens`.
- **Params:** "accepts the same structured list of inputs for creating a message": `model`, `system`, `messages`, `tools`, `thinking` (example: `{"type": "adaptive"}`), images, PDFs. The examples do not pass `max_tokens`.
- **Response:** `{ "input_tokens": N }`. Example values: 14 (basic), 403 (one tool), 1028 (image), 88 (thinking multi-turn), 2188 (PDF).
- **Status:** GA. ZDR-eligible (except "Covered Models"). Available on Claude API, Claude Platform on AWS, Bedrock, Google Cloud, and Microsoft Foundry. Works with "all active models".
- **Estimate only:** "The token count is an **estimate**". Actual usage "might differ by a small amount". Counts can include tokens Anthropic adds for system optimization, and "**You are not billed for system-added tokens**."
- **Tokenizer:** Claude 4.7+ and Mythos Preview use a newer tokenizer that produces "approximately 30 percent more tokens". Fable 5.1, Mythos 5.1, Fable 5 and Mythos 5 share the Opus 4.7 tokenizer. The endpoint counts with the tokenizer of the `model` you pass. The doc says to recount against the target model and "don't reuse token counts measured on the older model".
- **Not supported (`invalid_request_error`):** server tools (web search, web fetch, code execution, tool search; the advisor tool is the only server tool allowed), the MCP connector, and `image`/`document` blocks with a `url` or `file` source. Send images and PDFs as base64 instead. For server-tool or MCP requests, use the Messages API `usage` object.
- **Tools:** client tools and the advisor tool are supported. For the advisor tool, the count "covers the executor's first sampling call only".
- **Images:** `"oversized_image": "error"` blocks are rejected at count time, the same way Messages rejects them.
- **Thinking:** thinking from previous assistant turns counts on models that keep all prior turns. Models that keep only the last turn strip it, so it does **not** count. Thinking in the current assistant turn **does** count.
- **PDFs:** base64 only, with the same PDF requirements as Messages.
- **Cost / rate limits:** "**free to use**". RPM depends on tier: Start 5,000; Build 10,000; Scale 20,000. These limits are "separate and independent" from message-creation limits.
- **Caching:** the endpoint does not use prompt caching. `cache_control` is accepted, but caching only happens during actual message creation.
- **Output tokens:** the doc does not cover counting output or thinking-generation tokens before a call. It only counts input.

## 2 MY INFERENCE FOR INTEGRA
- **Heimdall token tracking:** the right setup has two layers. (a) **Pre-flight:** call `count_tokens` before every Claude call (nexus_right, shiva_orchestrator) and log the result as `input_tokens_est`. (b) **Post-hoc:** keep `usage` from the response as the billing truth, which is what `_extract_anthropic_tokens` already reads. Excess alerts: flag drift where |actual − est| / est > ~5%, and flag any pre-flight estimate above a per-call cap *before* spending. The endpoint is free and has its own RPM, so pre-flight calls do not eat into generation quota. The cost is one extra network round trip per call, which matters given the kernel's current latency problem.
- **Context-saturation limit (ψ = 200 MPa):** in code this is a metaphorical constant (`forensic_protocols.py` `FRACTURE_LIMIT_MAX_MPA = 200.0`; `corpus_callosum.py` "psi >= 200 MPa"). Nothing ties it to a real token count. A deterministic mapping would be ψ = 200 × (`input_tokens` from count_tokens + `max_tokens`) / model context window. That makes the "Heaviside halt" a measurable gate rather than a narrative one.
- **Router budgets:** `ModelRouter` Gate 2 (L305) refuses a call only once `tokens_consumed >= token_budget`. A single large call can therefore overshoot the cap. A pre-flight count lets the gate check `consumed + est_input + max_tokens > budget` before the call goes out.
- **Streaming estimate is biased low for Claude 5.x:** `RoutedClient.generate_iterative` uses "~4 chars/token" (L475). The doc says the 4.7+ tokenizer yields about 30% more tokens, so this heuristic likely under-counts Claude spend. That is my inference, not measured. Also, the heuristic counts streamed output characters only, so input tokens are missing entirely.
- **Proof-of-Sleep ledger:** each SWDS/Cheshire step can store both `input_tokens_est` (count_tokens) and the actual `usage`. Phases with no recorded usage print NOT EXECUTED.
- **Gemini clients (5 of 7):** this doc does not cover them. They would need Gemini's own `count_tokens`.

## 3 Contradictions with current wiring
- **No contradiction:** model ID `claude-opus-5-5` and `thinking: {"type": "adaptive"}` match the doc examples exactly.
- **Gap:** grep found no `count_tokens` usage anywhere in `core/*.py`, so there is no pre-flight counting today.
- **Gap:** the chars/4 streaming estimator conflicts with the doc's tokenizer guidance. It probably reflects older-tokenizer assumptions.
- **Gap:** ψ = 200 MPa is not derived from tokens, while the doc gives a direct way to measure input size.
- **Unverified:** whether pinned `anthropic==1.5.0` exposes `messages.count_tokens`. The doc does not name an SDK version, so this needs a probe.
- **Not covered by the doc:** whether Opus 5.5 / Sonnet 5.5 keep all prior thinking turns or only the last. This changes multi-turn input counts.
- **Constraint:** if any Claude call ever uses server tools (web search, web fetch, code execution) or the MCP connector, count_tokens will error. Those calls must fall back to `usage`.

## 4 Concrete recommended actions (ranked)
1. **(S)** Probe that `anthropic==1.5.0` has `client.messages.count_tokens` by making one live call with `claude-opus-5-5` and `claude-sonnet-5-5`. Record the returned `input_tokens` in the ledger as evidence.
2. **(M)** Add a pre-flight gate in `RoutedClient` for Claude components: if `count_tokens` + `max_tokens` would exceed the remaining budget, refuse with `BUDGET_WOULD_EXCEED`. Log est vs actual to `TOKEN_TELEMETRY`.
3. **(S)** Replace the chars/4 streaming estimate for Claude. Use `count_tokens` for input, plus the final stream `usage` if the SDK's stream exposes `message_delta` usage. Otherwise scale chars/4 by ×1.3 and mark it ESTIMATED.
4. **(M)** Heimdall alerts: per-call est > cap → pre-spend alert; |actual − est| > 5% → drift alert; daily $ from actual `usage` only.
5. **(M)** Redefine ψ in code as context-utilization percent from measured tokens (count_tokens + `max_tokens`) relative to the model's context window. Keep 200 MPa as the display scale only.
6. **(S)** Make the counter fail-safe: on `invalid_request_error` (server tools, MCP, URL/file sources), fall back to post-hoc `usage` and never block the call on a counting error.
7. **(L)** Add the matching Gemini `count_tokens` pre-flight for the 5 Gemini components, so Heimdall gets a uniform measured view.
