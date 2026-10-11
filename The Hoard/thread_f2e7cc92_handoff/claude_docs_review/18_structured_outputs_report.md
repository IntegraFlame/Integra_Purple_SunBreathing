# 18 — Structured outputs: report

## 0 Read receipt
- File: `docsplit/18_Structured_outputs_66d768f34cc5.md` — 2832 lines / 105,928 bytes, read in full (views 1–800, 801–1500, 1501–2200, 2201–2832).
- First heading: frontmatter `title: Structured outputs` → `## Why use structured outputs`. Last heading: `## Next steps` (CardGroup: Citations, Strict tool use, Tool use, Pricing).
- Source marker: `Claudecode6Untitled-5.md lines 12057-14886`. Status `ga`, ZDR eligible (excludes "Covered Models").

## 1 DOC SAYS
**Two features.** (a) JSON outputs via `output_config.format` = `{"type":"json_schema","schema":{...}}`; result arrives as valid JSON in the response's **text** content block. (b) Strict tool use via `strict: true` on a tool (separate page). Usable independently or together in one request ("JSON outputs control what Claude says; strict tool use validates how Claude calls your functions").

**Supported models (frontmatter):** claude-fable-5-1, claude-mythos-5-1, claude-fable-5, claude-mythos-5, claude-mythos-preview, **claude-opus-5-5**, claude-opus-5, claude-opus-4-8/4-7/4-6, **claude-sonnet-5-5**, claude-sonnet-5, claude-sonnet-4-6, claude-sonnet-4-5-20250929, claude-opus-4-5-20251101, claude-haiku-5-5, claude-haiku-4-5-20251001. Platforms: Claude API, Claude Platform on AWS, Google Cloud, Microsoft Foundry all GA; Amazon Bedrock only on the legacy integration (Opus 4.6 and earlier models).

**Python SDK helpers.** `client.messages.parse(model=..., max_tokens=..., messages=..., output_format=PydanticModel)` → `response.parsed_output` (the "recommended method"; SDK transforms schema, sends it as `output_config.format`, validates response). `transform_schema()` (in `anthropic` package; accepts dict or Pydantic) returns the transformed schema without sending. Raw path: `client.messages.create(..., output_config={"format": {...}})` then `next(b.text for b in response.content if b.type == "text")` + `json.loads`.

**SDK transformation:** removes unsupported constraints (`minimum`, `maximum`, `minLength`, `maxLength`), appends them to field descriptions, adds `additionalProperties: false` to all objects, filters string formats, then (if helper validates) checks response against the ORIGINAL schema. TS `jsonSchemaOutputFormat()` transforms but does NOT validate.

**Schema support:** basic types incl. null; `enum` (scalars only); `const`; `anyOf`/`allOf` (`allOf`+`$ref` not supported); `$ref`/`$def`/`definitions` (no external); `default`; `required`; `additionalProperties` must be `false`; formats `date-time, time, date, duration, email, hostname, uri, ipv4, ipv6, uuid`; array `minItems` only 0 or 1. **Not supported:** recursive schemas, numeric/string length constraints, other array constraints → 400. Regex: no backrefs, lookaround, `\b`, large `{n,m}`.

**Hard limits (per request, across all strict schemas):** 20 strict tools; 24 optional parameters total; 16 union-type params (`anyOf` or `"type":["string","null"]`). Internal grammar-size limit → 400 "Schema is too complex for compilation."; compilation timeout **180 s**.

**Performance/cost:** first use of a schema compiles a grammar (extra latency); cached 24 h from last use; invalidated by schema structure change or tool-set change (not by `name`/`description` edits). Injected extra system prompt adds input tokens; changing `output_config.format` invalidates prompt cache for that thread.

**Invalid-output cases:** `stop_reason:"refusal"` (200, billed, may not match schema); a property asking for "thinking or step-by-step reasoning" may trigger a `reasoning_extraction` refusal — ask for a short explanation instead. `stop_reason:"max_tokens"` → truncated/invalid JSON; retry higher. Enum/const **capitalization not guaranteed** — compare case-insensitively.

**Property ordering:** required props first (schema order), then optional.

**Compat:** works with Batch (50% discount), token counting, streaming, combined strict tools. Incompatible with Citations (400) and message prefilling. **Thinking:** grammar applies only to Claude's direct output — not tool calls, tool results, or thinking; "allowing Claude to think freely while still producing structured output in the final response."

**Beta migration:** top-level `output_format` deprecated; requires `structured-outputs-2025-11-13` header or 400. Python SDK **v1.0+** raises `TypeError` for `output_format={...}` on `client.beta.messages.create()`/`count_tokens()`. (Note: `messages.parse(output_format=Model)` is still the documented helper signature.)

**Retention:** schema cached up to 24 h; no PHI in property names, enums, consts, patterns.

## 2 MY INFERENCE FOR INTEGRA
- **Memory nodes (Rodin/Hoard):** define one Pydantic `MemoryNode` (id uuid, ccid, created_at `date-time`, source_path, sha256 `pattern ^[a-f0-9]{64}$`, summary, tags[], edges[]) and generate via `messages.parse`. Kills `JSON_PARSE_FAILED` fallbacks. No recursion allowed → edges must be flat `{target_id, relation}` lists, not nested nodes.
- **Proof-of-Sleep ledger:** model output should only fill the *content* fields (findings, consolidation summary). Ledger provenance (timestamp, request_id, usage tokens, file hashes) must be written by deterministic code from the API response, never by the model. Structured outputs guarantee shape, not truth.
- **Save states / Heimdall telemetry:** Heimdall records are produced by code, so schema-constrained decoding is unnecessary there; use Pydantic validation locally. Use structured outputs only where an LLM emits records (SWDS reports, Cheshire study notes, environment-ingestion metadata nodes).
- **Effort + thinking:** our `output_config.effort` lives in the SAME `output_config` object as `format`. Adaptive thinking remains compatible (grammar excludes thinking). Don't put a "reasoning" field in schemas (refusal risk).
- **Cost:** keep a small, stable set of schemas (grammar cache 24 h; prompt-cache invalidation on format change). Environment ingestion at volume → Batch API (50%) with one fixed schema.
- Keep optional fields ≤24 and nullable unions ≤16 across a request; prefer all-`required` with explicit null/empty defaults.

## 3 Contradictions with current wiring
1. `core/api_clients.py` L153–154 `_claude_thinking_kwargs` returns `"output_config": {"effort": chosen_effort}`. Adding `format` naively (e.g., a second `output_config=` kwarg or dict overwrite) would drop effort or raise a duplicate-kwarg error — must deep-merge.
2. L20–42 `clean_json_payload` regex-strips ```json fences and falls back to `{"error":"JSON_PARSE_FAILED"}` — this is the exact failure class structured outputs eliminate; currently still the parsing path (inferred from grep; full call-site audit not done).
3. Text extraction joins text blocks only (L121 comment) — consistent with doc (JSON is in the text block). OK, but must also check `stop_reason` for `refusal`/`max_tokens` before trusting JSON; no evidence that's done (not verified).
4. SDK `anthropic==1.5.0` ≥ v1.0 → `output_config` path is correct; any legacy `output_format=` on `beta.messages.create` would TypeError. Model IDs `claude-opus-5-5`, `claude-sonnet-5-5` are on the supported list — no contradiction.
5. Gemini clients (y789, Cheshire, Rodin) are out of scope for this doc; they need Gemini's own `response_schema`.

## 4 Concrete recommended actions (ranked)
1. **(S)** Make `_claude_thinking_kwargs` accept an optional `output_format` and merge into one `output_config` dict `{effort, format}`.
2. **(S)** After every Claude call, gate on `stop_reason`: `refusal` → ledger entry REFUSED; `max_tokens` → retry with higher `max_tokens`; never write such JSON to The Hoard.
3. **(M)** Create `schemas/` Pydantic models: `MemoryNode`, `SleepPhaseResult`, `IngestionMetadata`, `CheshireStudyNote`; call via `client.messages.parse(output_format=...)`; retire `clean_json_payload` for Claude paths.
4. **(S)** Case-insensitive enum normalization in validators; avoid enum values differing only by case.
5. **(M)** Ledger writer stamps provenance (request id, usage, hashes) from code; model-filled fields only for content.
6. **(L)** Environment ingestion via Message Batches + single fixed schema (50% cost, cached grammar).
