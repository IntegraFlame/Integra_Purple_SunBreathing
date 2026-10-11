# 03 — Define tools: report
Written 2026-10-08 ~02:58 CDT (07:58Z). No project files were modified.

## 0 Read receipt
- **Brief:** `voltron_brief.md`, all 26 lines (4,162 bytes).
- **Doc section:** `03_Define_tools_0ce73ae4d067.md`, all 916 lines (39,077 bytes), read as lines 1–800 and then 800–916.
- **Source:** "Claudecode1import anthropic.md" lines 1939–2854. Page URL: https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools
- **First heading seen:** "## Prerequisites". **Last heading seen:** "## Next steps", which links to the Handle tool calls, Tool Runner (SDK) and Tool reference pages.
- **Sections in between:** Specifying client tools · Tool use system prompt · Best practices for tool definitions · Providing tool use examples (Basic usage; Requirements and limitations) · Controlling Claude's output (Forcing tool use; Model responses with tools).

## 1 DOC SAYS
**How tools are declared**
- Tools go in the top-level `tools` array.
- A user-defined tool has four fields:
  - `name`, which must match the regex `^[a-zA-Z0-9_-]{1,128}$`
  - `description`
  - `input_schema` (a JSON Schema object)
  - `input_examples` (optional)
- The page names other optional properties but defers their details to the Tool reference page: `cache_control`, `strict`, `defer_loading`, `allowed_callers`.
- Anthropic-schema tools (bash, text editor) are declared with a date-versioned `type`.
- Computer use and browser use are "client toolsets": a single entry with no `name`. That entry accepts `cache_control` and `allowed_callers`, and `defer_loading` is set per member tool.

**System prompt the API builds**
- When `tools` is present, the API builds its own system prompt in this order: preamble, formatting instructions, tool JSON schemas, the user's system prompt, then the tool configuration.
- That prompt says the output "is parsed with regular expressions".

**Best practices**
- Descriptions are "by far the most important factor". Aim for at least 3–4 sentences each, covering what the tool does, when to use it and when not to, what each parameter means, and caveats.
- Use `input_examples` for complex, nested or format-sensitive inputs.
- Merge related operations into fewer tools with an `action` parameter.
- Prefix tool names with the service, e.g. `github_list_prs`. The doc says this matters especially when using tool search.
- Tool responses should return only high-signal fields and stable identifiers (slugs or UUIDs).
- **Ask for an explanation, not reasoning.** A parameter that asks for the model's thinking or step-by-step reasoning "may lead to a `reasoning_extraction` refusal".

**`input_examples`**
- Every example must validate against `input_schema`. An invalid example returns **400**.
- Not supported on server tools (web search, code execution) or on the computer use and browser use toolsets.
- Token cost: about 20–50 tokens per simple example, about 100–200 per complex nested one.

**`tool_choice` options**
- `auto` is the default when tools are provided.
- `any` means some tool must be used.
- `tool` forces one named tool.
- `none` is the default when no tools are provided.

**Restrictions on forced tool use (`any` / `tool`)**
- Manual extended thinking (`thinking: {type: "enabled"}`) does not allow `any` or `tool`; requesting them is an error.
- Adaptive thinking on its own does not block forced tool use. The doc names Claude Opus 5 and Claude Haiku 5.5 as supporting it with thinking on.
- **Claude Opus 5.5, Claude Sonnet 5.5, Claude Fable 5.1 and Claude Mythos 5.1 return a 400 for `any` or `tool`**, whatever the thinking settings.
  - The doc's alternative is `auto` plus strict tool use (`strict: true`), or structured outputs.
  - `none` still works on these models.
- With `any` or `tool`, the API prefills the assistant turn, so no natural-language text appears before the `tool_use` blocks.
- If you want an explanation alongside the call, use `auto` and put the instruction in the user message.
- Tip: on models that support forced use, `any` combined with `strict: true` guarantees both that a tool is called and that the input matches the schema.

**Caching**
- Changing `tool_choice` invalidates cached **message** blocks. Tool definitions and the system prompt stay cached.

**Response shape**
- With `auto`, Claude often emits a `text` block and then a `tool_use` block (`id` such as `toolu_…`, `name`, `input`).
- Code must not rely on the exact phrasing or format of that text.

**What the section does not cover**
- **Pricing:** none.
- **SDK version:** none.
- **Model IDs that appear:** `claude-opus-5-5` (input_examples samples) and `claude-opus-5` (forced-tool samples). SDK constants: `ClaudeOpus5_5`, `CLAUDE_OPUS_5_5`, `ModelClaudeOpus5`.
- Java passes `input_examples` through `putAdditionalProperty`, meaning there is no typed field for it in that SDK.

## 2 MY INFERENCE FOR INTEGRA
- **MCP memory server for cross-thread continuity.** The doc's guidance applies directly:
  - Namespace the tools, e.g. `rodin_search`, `rodin_get_node`, `rodin_neighbors`, `hoard_write_node`, `hoard_write_handoff`, `kernel_get_card`.
  - Or merge them into `rodin_memory(action=…)` plus `hoard_write(action=…)`.
  - Give each tool a description of at least 3–4 sentences stating what it does not return, e.g. "returns node metadata only, not full file text".
  - Responses should return node IDs (CCID or UUID), the 4D stamp and a short excerpt, not whole JSON dumps. This targets problem (3), token overuse.
- **Proof-of-Sleep ledger (SWDS/Siesta).**
  - Any tool that records a step, e.g. `ledger_append`, must not have a field like `reasoning` or `thought_process`; that risks a `reasoning_extraction` refusal.
  - Use `explanation` or `evidence` (file hashes, call IDs) instead.
  - Set `strict: true` so ledger entries are always schema-valid. Combined with ledger-only rendering, this addresses problem (2), fabricated reports.
- **Cheshire Cat Daemon ("local only").**
  - Enforce the restriction through the tool list, in code. Heimdall builds the `tools` array from a fixed allowlist: Rodin and Phoenix node reads, cache read, Hoard read. No web or MCP tools are passed.
  - The restriction should not depend on prompt instructions.
  - For the delayed riddle reply, use `tool_choice: none`. It works on every model.
- **Long Cheshire study sessions (1–2 h, many calls).** Keep `tool_choice` the same for the whole session. Changing it flushes the cached message prefix and raises cost.
- **Heimdall.** It can log the `tool_use` `id` (`toolu_…`) of every call into the ledger, giving verifiable model-call evidence.
- **Kernel code.** The response parser must loop over all content blocks by `type` (`thinking`, `text`, `tool_use`). Neither `content[0]` nor "join the text blocks" is safe:
  - With `auto`, a `text` block often comes before `tool_use`.
  - Under adaptive thinking, a `thinking` block can come first.

## 3 Contradictions with current wiring
1. **Forced tool use on the brief's Claude models.** `nexus_right = claude-opus-5-5` and `shiva_orchestrator = claude-sonnet-5-5` are both models the doc says return **400** for `tool_choice` `any` or `tool`. Any kernel or SWDS code that forces a tool on these clients will fail. Grep `core/api_clients.py` and the callers for `tool_choice`.
2. **Text-join parsing.** The brief says the code "joins text blocks only". If tools are used, that path silently drops `tool_use` blocks.
3. **Model ID drift.** The doc's forced-tool samples use `claude-opus-5`, which is not in `models.yml`. The doc says Opus 5 (not 5.5) and Haiku 5.5 do support forced use with adaptive thinking. If the Orchestrator needs guaranteed tool calls, those are candidates, but that is a routing decision.
4. **SDK unknown.** The section names no SDK version. Whether `anthropic==1.5.0` accepts `input_examples` and `strict` as typed parameters is **unverified**; probe before relying on them.
5. **No contradiction found** on thinking shape: the brief's `{type:"adaptive"}` is the mode that does not block forcing. Manual `enabled` does block it.

## 4 Concrete recommended actions (ranked)
1. **(S)** Grep `integra-homebase` for `tool_choice` and `content[0]`. Remove `any`/`tool` from Opus 5.5 and Sonnet 5.5 calls and replace them with `auto` + `strict: true`. Make the parser walk blocks by `type`.
2. **(S)** In the Proof-of-Sleep ledger tool schemas, rename any `reasoning` or `thinking` fields to `explanation` or `evidence`, and set `strict: true`.
3. **(M)** Write the MCP memory server tool set as namespaced tools with 3–4+ sentence descriptions, `input_examples` only on complex tools (budget 100–200 tokens each), and compact ID-based responses.
4. **(M)** Have Heimdall build the Cheshire `tools` array in code from an allowlist, use `tool_choice: none` for reply turns, and keep `tool_choice` fixed within a study session to protect the prompt cache.
5. **(S)** Make a probe call on `anthropic==1.5.0` with `input_examples` and `strict` and log the result to the ledger. Only after that, decide whether to add a `claude-opus-5` route for forced-tool workloads.
