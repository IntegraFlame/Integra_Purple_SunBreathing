# 14/15 — Tool combinations + Programmatic Tool Calling (PTC) report
Stamp: 2026-10-08 ~03:00 CDT (08:00Z). Reader: subagent 0ac53ba0. (Written here because the write tool would not allow the parent's scratch dir.)

## 0 Read receipt
- **14_Tool_combinations_7fac033c403a.md**: 108/108 lines, 6,335 bytes, one view. First heading: "Research agent: web_search + code_execution". Last heading: "Next steps".
- **15_Programmatic_tool_calling_3749ce3c3e94.md**: 1,593/1,593 lines, 63,941 bytes, two views (1–800, 800–1593). First heading: "Quick start". Last heading: "Next steps", after "Data retention".

## 1 DOC SAYS
**Tool combinations (doc 14).** The doc calls these "starting points, not prescriptions." It gives patterns, not a compatibility matrix, so it does not list any invalid pairs.
- Research: `web_search_20260209` + `code_execution_20260521`. Code execution runs server-side.
- Coding: `text_editor_20250728` (name `str_replace_based_edit_tool`) + `bash_20250124`. Both run on the client. The doc recommends a constrained working directory and a command allowlist.
- Cite-then-fetch: `web_search_20260209` + `web_fetch_20260209`. Claude searches, then fetches only the 2–3 relevant results.
- Long-running: `memory_20250818` (name `memory`) alongside any other tools. Memory is "orthogonal": it does not change how the other tools behave.
- `computer_toolset_20260801` and `browser_toolset_20260801` take no `name`. You switch individual actions off through `configs`. Computer use is the slowest option.

**PTC mechanics (doc 15).**
- Status GA. **ZDR: not-eligible.** Platforms:
  - GA on the Claude API and on Claude Platform on AWS.
  - **Not available on Amazon Bedrock or Google Cloud.**
  - Microsoft Foundry only with a "Hosted on Anthropic" deployment.
- Requires the code execution tool, version `code_execution_20260120` or later. You can check support through Models API `capabilities.code_execution.supported`.
- Supported models include `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, opus-4-5…4-8 and sonnet-4-5/4-6. Haiku 4.5 accepts the tool but does not support PTC.
- **`allowed_callers`** values:
  - `["direct"]` is the default.
  - `["code_execution_20260120"]` limits the tool to code execution.
  - Both values together are allowed but not advised.
  - `20260120` and `20260521` are interchangeable here. Responses always tag the caller as `code_execution_20260120`.
  - The doc says it is **not a security boundary**: the client must still handle a direct `tool_use` for any tool.
- **Flow:**
  1. Claude writes Python, where each tool is an **async function** that takes one dict and returns a string. Parallel calls are possible with `asyncio.gather`.
  2. When the code calls a tool, the API pauses with `stop_reason:"tool_use"`. The `tool_use` block has `caller:{type, tool_id:"srvtoolu_…"}`.
  3. The client sends back a message that contains **only `tool_result` blocks**, with no text. Results must be **string/text only**; images and documents are rejected. The request must also carry the **`container` ID**, which is mandatory while a call is pending, and the **same `tools` array**.
  4. When the code finishes, the response contains a `code_execution_tool_result` with `stdout`, `stderr` and `return_code`.
- **Limits:**
  - A pending call times out after about **4 min**. The example shows `TimeoutError … 270s`.
  - Idle containers are reclaimed after about **5 min**. A container can be reused for at most **30 days** after creation.
  - Container data is retained for up to 30 days.
- **Incompatible features:** `strict: true` tools, forcing via `tool_choice` (returns 400 if the named tool lacks `"direct"`), and `disable_parallel_tool_use: true`.
- A recursive `$ref` gives `400 Circular $ref detected`.
- **Tools that cannot be called from code:** MCP-connector tools, and the computer/browser toolsets.
- Rate limits: each programmatic call counts as a separate invocation.
- **Token figures:**
  - Results from programmatic calls are **not added to context** and **do not count toward input/output tokens**. Only the final code output and Claude's response count.
  - Pricing is the same as code execution.
  - Calling 10 tools directly costs about 10× the tokens.
  - 75-tool benchmark: about −38% billed input tokens, with no change in accuracy.
  - τ²-bench (sequential workflows with 1–2 calls): **about +8% cost**, no gain.
  - Requests with 10–49 tools: typically 20–40% savings.
  - BrowseComp/DeepSearchQA: +11% performance with −24% input tokens.
- **Fit:**
  - Strong: fan-out work, large results that can be filtered, agentic search.
  - Weak: strictly sequential reasoning chains, a few small calls on the first turn, steps that need user feedback.
  - The doc's advice: "measure billed input tokens with and without `allowed_callers`."
- **Alternatives:** client-side direct execution (unsandboxed, injection risk), a self-managed sandbox, or Anthropic-managed execution.

## 2 MY INFERENCE FOR INTEGRA
- **Environment ingestion / Rodin swarm.** PTC fits the **inventory pass** well: walk files, hash, size/type, find duplicates between `The Hoard` and `The_Hoard`, check against the ledger. Expose `list_dir`, `stat_file`, `hash_file`, `read_file_chunk` and `write_metadata_node` as custom tools with `allowed_callers:["code_execution_20260120"]`. One script fans out over hundreds of files and returns only a manifest. **Caveat:** PTC lets the model filter content *without reading it*. That is effectively skimming, which the Architect has banned. The semantic pass (one reader per file writing a metadata node) must stay a direct model read of the full text. Use PTC only for deterministic metadata and for verification ("did node X record the right sha256 and byte count?").
- **Shiva lenses.**
  - Neji (boundary/noise stripping): PTC data filtering, e.g. scanning logs for errors.
  - Shikamaru (dependency graph): fan-out across many files to build a graph of imports and edges.
  - Itachi (temporal): sequential reasoning that depends on time, which the doc lists as a weak fit, so keep it on direct calls.
- **Heimdall token budgets.** Results from programmatic calls never appear in `usage`, so token-based dashboards will **undercount the data Claude actually processed**. Container/code-execution charges are separate. Heimdall must:
  1. Log every programmatic `tool_use` and `tool_result` locally in the Proof-of-Sleep ledger. Results never enter the transcript, so the ledger is the only evidence.
  2. Track code-execution cost as its own line item.
  3. Enable PTC per workload only after an A/B test of billed tokens.
- **Cheshire Cat study sessions.** These are sequential, deep-thinking chains, a weak fit (+8%). Do not use PTC there. It also conflicts with "local only": code and tool results go to Anthropic containers that are retained for 30 days.
- **Memory tool.** `memory_20250818` could provide cross-thread continuity alongside the planned MCP memory server. The storage model is in a separate doc that I did not read.

## 3 Contradictions with current wiring
1. **Google Cloud: not available.** If Claude is ever routed through Vertex (the project already uses Vertex Express for Gemini), PTC is unavailable there. Only the direct Claude API works. Confirm how `core/api_clients.py` reaches Claude.
2. **Planned MCP memory server.** If it is attached through the Anthropic MCP connector, its tools **cannot be called programmatically**. They would need duplicate definitions as plain custom tools.
3. **Response parsing.** The client code joins text blocks only. PTC responses add `server_tool_use`, `tool_use` with a `caller`, and `code_execution_tool_result`; the stdout lives in that last block, so the current logic would drop the evidence. The client loop must also pass `container`, resend the identical `tools` array, and send tool-result-only messages.
4. **SDK pin `anthropic==1.5.0`.** Unverified whether it exposes typed `allowed_callers`, `container` and `caller`. I am not claiming it lacks them; this needs a probe.
5. **Kernel latency of 5–43 s per endpoint.** This is within the 4-min tool timeout. However, a slow `hash_file` or `read` over OneDrive, or a stalled kernel, could exceed about 270 s and raise a `TimeoutError` inside the script.
6. **Privacy.** ZDR is not eligible and container data is kept for 30 days. This conflicts with sending The Hoard or other private content through PTC under the "local only" doctrine.
7. **No `strict: true`.** Any Integra tool schemas that rely on strict structured outputs cannot also be PTC-callable.

## 4 Concrete recommended actions (ranked)
1. **(S)** Probe the Claude transport: confirm direct `api.anthropic.com`, not Vertex. Call the Models API and record `capabilities.code_execution.supported` for opus-5-5 and sonnet-5-5.
2. **(S)** Patch response handling to iterate every block type and to log `server_tool_use`, `caller.tool_id` and `code_execution_tool_result.stdout/stderr/return_code` to the ledger. This is needed whether or not PTC is adopted.
3. **(M)** Build a PTC client loop:
   - Persist `container` with `expires_at`.
   - Resend an identical `tools` array.
   - Send tool-result-only messages, with string results.
   - Apply a 200 s per-tool watchdog (under the 270 s limit).
   - Handle direct `tool_use` even for code-only tools.
4. **(M)** Ingestion v1 inventory pass through PTC (manifest of hashes and duplicates). Keep the semantic per-file read on direct calls, and record the full byte count read per file to enforce no-skim.
5. **(M)** Heimdall: add a separate code-execution cost meter and a "programmatic results bytes" counter. A/B test billed input tokens with and without `allowed_callers` before turning PTC on by default.
6. **(L)** For private and Cheshire workloads, use the "self-managed sandboxed execution" alternative: a local sandbox with no egress, running the same async-function pattern, so data never leaves the machine.
7. **(S)** Audit tool schemas for `strict: true` and recursive `$ref` before marking them PTC-callable.
