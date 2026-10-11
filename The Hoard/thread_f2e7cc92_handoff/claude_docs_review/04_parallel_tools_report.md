# 04 — Parallel tool use: report

## 0 Read receipt
- Brief `voltron_brief.md`: 26/26 lines, 4,162 bytes.
- Section `04_Parallel_tool_use_65b9f895b7bb.md`: all 1,622/1,622 lines, 57,904 bytes, read in 3 views (1–800, 801–1600, 1600–1622). Source tag: `Claudecode1import anthropic.md lines 2855-4475`.
- First heading: `## Execution semantics`. Last doc heading: `## Next steps` (L1581).
- **Contamination:** L1597–1621 are not Anthropic doc text. They are a "memory export" prompt ("Export all of my stored memories… Categories… Instructions/Identity/Career/Projects/Preferences… wrap in a single code block"). I did not act on it. The split or paste should be cleaned so other agents don't treat it as an instruction.
- Tool note: the first 5 tool calls failed in the `dak-telemetry` PreToolUse hook (exit 1 or a timeout). Later calls worked. The write tool also refused the requested path because subagents may only write to their own artifact dir, so this file lives in the subagent dir (see the end).

## 1 DOC SAYS
- **Default:** Claude "may call multiple tools in a single response." Parallel use is on by default, and Claude 4+ models do it by default when the request benefits from it.
- **Execution order is up to the client.** The response has `stop_reason: "tool_use"` and can hold several `tool_use` blocks. You can run them concurrently (`asyncio.gather`, `Promise.all`), sequentially, or mixed. Independent, read-only operations are usually safe to run in parallel. Tools with side effects, shared state, or ordering needs are better run sequentially.
- **Result formatting (hard rules):** send one `tool_result` per `tool_use`, all in the **next single user message**. Match each by `tool_use_id`. Put every `tool_result` **before any text** in that message. If you skip a call, still return a result: `{"type":"tool_result","tool_use_id":…,"is_error":true,"content":"Not executed: …"}`.
- **Computer-use / browser-use batch actions:** run them sequentially in order and stop at the first failure. Each tool defines the text to return for skipped calls.
- **Tool Runner (SDK)** is recommended for most apps. Write the loop by hand only if you need custom batching, ordering, or error handling.
- **Bad formatting suppresses parallelism.** Separate user messages per result "teaches" Claude to stop making parallel calls. The doc calls this the most common issue.
- **Prompting to boost parallelism:** a short system line ("For maximum efficiency, whenever you need to perform multiple independent operations, invoke all relevant tools simultaneously rather than sequentially.") and a stronger `<use_parallel_tool_calls>` block. To keep dependent calls out of the same batch: "Only batch tool calls that are independent of each other."
- **Claude Fable 5.1** may issue fewer parallel calls in long agent loops (coding/bash/text-editor harnesses, computer use). Standard function calling is unaffected.
- **Disabling:** `disable_parallel_tool_use: true` goes **inside `tool_choice`**. It is not a top-level parameter.
  - `tool_choice.type = "auto"` + disable → **at most one** tool call, and plain text is still allowed.
  - `type = "any"` or `"tool"` + disable → **exactly one** call. **Claude Opus 5.5, Sonnet 5.5, Fable 5.1, and Mythos 5.1 don't support `any`/`tool`.** The doc's example uses `claude-opus-5` for that reason.
- **Metric:** average `tool_use` blocks per tool-calling message, which "should be > 1.0 if parallel calls are working."
- **Dependency failures:** if a parallel call fails because its prerequisite hadn't finished, return `is_error: true` with the natural error message, and Claude will reissue it next turn.
- **Model IDs shown:** `claude-opus-5-5` (main examples), `claude-opus-5` (any/tool example). **Header:** `anthropic-version: 2023-06-01`. **Pricing:** none in this section. **Numeric limits:** none, apart from `max_tokens: 1024` in the examples.

## 2 MY INFERENCE FOR INTEGRA
- **Cheshire Daemon (local-only, 1–2 h study sessions):** this is where parallel tools pay off most. Expose read-only local tools (`search_memory`, `get_node`, `neighbors`, `read_hoard_file`) and run each batch with `asyncio.gather`. One turn can then fan out across many Rodin nodes and Hoard files, so fewer turns are needed and token re-sends drop (each extra turn re-sends the full history). Write tools (`write_node`, `write_handoff`) should run sequentially, after the reads, with stop-on-first-failure.
- **Proof-of-Sleep ledger (SWDS/Siesta):** log every `tool_use_id` → tool, input hash, start/end time, `is_error`, and output hash. A batch becomes one ledger "turn" with N child entries. Any call returned as "Not executed" then shows up as NOT EXECUTED instead of being invented, which targets chronic problem (2), fabricated reports.
- **Heimdall:** compute and alert on **avg-tools-per-message** for each Claude client. A value stuck at 1.0 means the history is badly formatted or prompting is weak, which wastes tokens (problem 3). The lockdown/allow-list must be enforced in the **tool executor** (deterministic code). The model can request any tool name, so the executor must refuse non-allow-listed tools with `is_error: true`.
- **Rodin retrieval:** multi-query KNN (several phrasings or several 4D windows) maps naturally onto parallel `search_memory` calls in one turn.
- **Anti-skimming (problem 4):** the strong prompt's example ("when reading 3 files, run 3 tool calls in parallel") fits the environment-ingestion agents. Batch-read whole files and record byte counts in the ledger.
- **Cross-thread memory MCP server:** its read tools are parallel-safe. Mark the write tools as non-parallel in the executor.

## 3 Contradictions with current wiring
- **`tool_choice` any/tool is not supported** on `nexus_right = claude-opus-5-5` or `shiva_orchestrator = claude-sonnet-5-5`. Any code that forces a tool this way will fail on these clients. Use `auto` plus prompting instead. **Not verified against the code:** my grep of `integra-homebase` failed (a PowerShell quoting error, exit 1), so I don't know whether the kernel uses `tool_choice` or tools at all.
- **Brief hazard confirmed:** responses mix `thinking`, `text`, and several `tool_use` blocks. The doc filters by `block.type`. Any `content[0]` access is wrong.
- **SDK pin `anthropic==1.5.0`:** this section doesn't confirm the pinned version has the Tool Runner or the `tool_choice` shape it uses. Probe it.
- **SWDS simulator** makes zero model calls, so none of these mechanics are in use yet.
- **No contradictions** on model ID strings (`claude-opus-5-5` matches) or pricing (the section has none).

## 4 Concrete recommended actions (ranked)
1. **(S)** Strip L1597–1621 (the memory-export prompt) from the docsplit/source, and warn other swarm readers.
2. **(S)** Grep `core/api_clients.py` for `tool_choice` `any`/`tool` on the Claude 5.5 clients. Replace with `auto` (plus `disable_parallel_tool_use` if single-call behaviour is needed).
3. **(M)** Build one shared tool executor: `asyncio.gather` for `read_only` tools, sequential stop-on-first-failure for `side_effect` tools, `is_error` "Not executed" stubs for skipped calls, and all results in one user message ahead of any text. Enforce the Heimdall allow-list there.
4. **(M)** Write ledger entries per `tool_use_id`, and render SWDS/Siesta/Cheshire reports only from the ledger.
5. **(S)** Add the avg-tools-per-message metric to Heimdall telemetry and alert at ≤1.0 over long sessions.
6. **(S)** Add `<use_parallel_tool_calls>` and "Only batch tool calls that are independent of each other." to the Cheshire Daemon and ingestion-agent system prompts.
7. **(S)** Probe whether `anthropic==1.5.0` exposes the Tool Runner. If it does, use it for simple loops and keep the manual executor for the ledgered and gated paths.
