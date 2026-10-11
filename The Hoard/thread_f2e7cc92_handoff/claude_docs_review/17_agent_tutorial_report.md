# 17 — Tutorial: Build a tool-using agent (report)

## 0 Read receipt
- File: `docsplit/17_Tutorial_Build_a_tool_using_agent_d58a2423bd6a.md`: 4672 lines / 169,312 bytes. I read every line (lines 1–4672, across 7 views).
- First heading: `## Ring 1: Single tool, single turn` (title "Tutorial: Build a tool-using agent"). Last heading: `## Next steps` (cards: Define tools, Tool Runner, Troubleshooting).
- Every ring has code tabs for cURL, ant CLI, Python, TypeScript, C#, Go, Java, PHP, and Ruby. Every example uses `model: "claude-opus-5-5"`, `max_tokens: 1024`, `anthropic-version: 2023-06-01`.

## 1 DOC SAYS
**Ring 1: single call.** The request sends a `tools` array. Each tool has a name, a description, and an `input_schema` (JSON Schema). The example schema has a nested object `recurrence`, an array `attendees`, and `required: [title,start,end]`. Rings 1–2 set `tool_choice: {type:"auto", disable_parallel_tool_use:true}`.
- If Claude needs a tool, the response has `stop_reason: "tool_use"` and a `tool_use` block containing `name`, a unique `id`, and a structured `input`.
- Quote: "A response may contain text blocks before the tool_use block, so filter by type rather than assuming position."
- Your code runs the tool and appends the assistant's full `response.content` to history. It then sends a **user** message whose content is `[{type:"tool_result", tool_use_id:<id>, content:<string>}]`. The Python example passes `json.dumps(result)` as the content.
- The final response has `stop_reason: "end_turn"` and natural-language text.

**Ring 2: agentic loop.** The loop is `while response.stop_reason == "tool_use":` → run tool → append `{"role":"assistant","content":response.content}` → append the user `tool_result` → call again. Keep one running `messages` list ("Every turn sees the complete prior context"). The model decides how many times the loop runs.

**Ring 3: multiple tools, parallel calls.** Adds a second tool, `list_calendar_events(date)`, and drops `disable_parallel_tool_use`. Claude "might return several tool_use blocks in a single response". Your code must iterate over **every** `tool_use` block and "send back all results together in one user message." Links to the Parallel tool use doc.

**Ring 4: errors.** When a tool fails, don't crash. Return a `tool_result` with `content: str(exc)` and `is_error: true`. Claude "can retry with corrected input, ask the user for clarification, or explain the limitation."
- Demo: more than 10 attendees raises "Too many attendees (max 10)".
- Quote: "The `is_error` flag is the only difference from a successful result."
- Unknown tool names also raise and come back with `is_error`.

**Ring 5: Tool Runner (beta).** Entry point per SDK:
- Python: `client.beta.messages.tool_runner(...)`
- TypeScript: `toolRunner`
- Java: `client.beta().messages().toolRunner()`
- PHP: `$client->beta->messages->toolRunner()`
- C#: `client.Beta.Messages.ToolRunner()`
- Go: `client.Beta.Messages.NewToolRunner()`

Quote: "Error wrapping, result formatting, and conversation management are handled internally."

Helpers build the schema from the function signature:
- Python: `from anthropic import beta_tool` + `@beta_tool`. Docstring `Args:` lines become parameter descriptions. Call `.until_done()`.
- TypeScript: `betaZodTool` (zod).
- Go: `toolrunner.NewBetaToolFromJSONSchema` + `runner.All(ctx)`.
- Java: tool classes + `.addBeta("structured-outputs-2025-11-13")`.
- C#/PHP: `BetaRunnableTool`. Ruby: `Anthropic::BaseTool`.

Raised exceptions or returned errors become `is_error` results. There is no cURL/CLI equivalent. The doc says this takes "roughly half the lines" and gives the same output as Ring 3.

**What the doc does not cover (a gap, not a claim):**
- `stop_reason` values other than `tool_use`/`end_turn` (e.g. `max_tokens`)
- thinking blocks
- iteration caps or token budgets
- retrying failed API calls

The example loops exit on *any* stop reason other than `tool_use`. The Python final-text step uses `next(...)`, which raises if there is no text block.

## 2 MY INFERENCE FOR INTEGRA
**Cheshire Daemon study loop: write the Ring-4 loop by hand; don't use the Tool Runner.** Writing the Proof-of-Sleep ledger needs control over each step, so a hand-written loop is the right fit:
1. Code, not the model, picks the target node IDs to study and puts them in the first user message.
2. Tools are a local-only allowlist: `search_memory(query,k)`, `get_node(id)`, `neighbors(id)`, `read_hoard(path)` (paths limited to one Hoard root), `write_study_note(node_ids,text)`, `end_session(summary)`. Isolation comes from having no network tools at all. The dispatcher also returns `is_error` for any unknown tool name.
3. Each iteration: call the model → write a ledger row {ts, session_id, iter, response.id, model, stop_reason, usage in/out/thinking, tool name, sha256(input), sha256(result), is_error} → run **all** tool_use blocks → send one user message with all results → repeat.
4. Exit classes:
   - `end_turn` = OK.
   - `max_tokens` or any other stop reason = logged FAULT.
   - Hitting a cap (max iterations, Heimdall token budget, 1–2 h wallclock) = logged CAPPED.

   Session state is rebuilt from the ledger, so a crashed session can resume.
5. The 5–15 min delayed reply is a separate loop run that reads the conversation plus the daemon's own notes.

If Cheshire runs on Gemini 3.1 Pro, the same skeleton applies, but the wire format differs (functionCall/functionResponse). The loop therefore has to sit behind a provider-neutral adapter.

**Ledger-driven SWDS.**
- A deterministic code orchestrator runs the phases.
- Any phase that needs reasoning runs the same agent loop with phase-specific tools (`read_shard(id)`, `write_consolidated_node`, `link_nodes`).
- Code picks shards with a rotating cursor over all 305, instead of the same 10 every time.
- The report is built only from ledger rows. A phase with zero rows prints `NOT EXECUTED`; FAULT/CAPPED rows are shown as-is.

**Kernel files that would change or be added** (the integra-homebase grep was run):
- `core/api_clients.py`: it has zero hits for `stop_reason`, `tool_use`, `tool_result`, or `is_error`, so the clients are single-shot today. Add a tool-capable call that returns raw content plus usage.
- New: `core/agent_loop.py`, `core/ledger.py`, `runtime/cheshire_daemon.py`.
- Rewrite `runtime/swds_simulator.py`. The grep found no model or tool calls in it, which matches the HOLLOW finding. Its callers also need review: `pipelines/swds_pipeline.py`, `orchestration/swds_dag.py`, `scripts/enter_swds.py`, `scripts/trigger_swds.py`, `config/swds_config.json`.
- Existing Cheshire code to check before building a parallel daemon: `sensory/cheshire_cat.py`, `sensory/cheshire_protocol.py`, `config/cheshire_identity.json`.
- `models.yml`: add a cheshire study entry.
- `main.py`: scheduler plus ledger/status endpoints.
- Heimdall budget hook reusing `_extract_anthropic_tokens` (api_clients.py:180).

## 3 Contradictions with current wiring
1. **There is no tool-use support** in `core/api_clients.py`. The doc's core protocol (the `stop_reason` loop, `tool_use_id` matching, `is_error`) is missing.
2. **Async vs sync:** the kernel uses `AsyncAnthropic` (api_clients.py:453/931), but every doc example uses sync `anthropic.Anthropic()`. This doc doesn't show whether an async Tool Runner exists.
3. **SDK pin `anthropic==1.5.0`:** Ring 5 needs `from anthropic import beta_tool` and `client.beta.messages.tool_runner`. Neither has been verified in the pinned version.
4. **Silent-success hazard:** the doc loop treats any stop other than `tool_use` as finished. Copying it into SWDS would bring back the fake-success problem whenever output is cut off at `max_tokens`. The kernel sets max_tokens=8192; with adaptive thinking, truncation is a real risk.
5. **Model IDs:** the doc's `claude-opus-5-5` matches nexus_right, so no conflict. The doc shows no `thinking`/`output_config.effort` params. Once those are added, the full `response.content` (including thinking blocks) must be sent back unchanged. The doc's append-the-whole-content pattern already does this. Any code that rebuilds assistant turns from joined text would break it.
6. **Provider mismatch:** the proposed Cheshire model is Gemini, but this doc is Anthropic-only.

## 4 Concrete recommended actions (ranked)
1. **S**: Probe the pinned SDK: `python -c "import anthropic; from anthropic import beta_tool; print(anthropic.__version__, hasattr(anthropic.AsyncAnthropic().beta.messages,'tool_runner'))"`. The result decides Ring 4 vs Ring 5; I recommend Ring 4 either way because of the ledger hooks.
2. **M**: `core/ledger.py`: an append-only, hash-chained JSONL/SQLite ledger with `append(event)`, `verify_chain()`, `rows(session)`.
3. **M**: `core/agent_loop.py`: a provider-neutral Ring-4 loop that:
   - filters blocks by type
   - runs all tool_use blocks and returns one results message
   - sets `is_error` on exceptions and unknown tools
   - classifies stop_reason explicitly
   - enforces caps (iterations, tokens, wallclock)
   - writes to the ledger at every step
4. **M**: Cheshire tool sandbox: allowlisted local tools plus a path allowlist, and a unit test that no network-capable tool is registered. Start with `disable_parallel_tool_use: true` so ledger order is deterministic.
5. **S**: Heimdall budget gate, checked between iterations using each response's `usage`.
6. **L**: Replace `runtime/swds_simulator.py` with ledger-driven phases and a report renderer that reads only the ledger (`NOT EXECUTED` for empty phases). Fix the shard cursor.
7. **S**: Test fixture: a mocked response with a thinking block first and a `max_tokens` stop. The loop must log FAULT, not report success.
