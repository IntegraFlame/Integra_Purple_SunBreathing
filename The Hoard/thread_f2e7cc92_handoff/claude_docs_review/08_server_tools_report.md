# 08 — Server tools: report
(Written here because write_to_file blocked the parent scratch path `...f2e7cc92.../scratch/voltron/08_server_tools_report.md`.)

## 0 Read receipt
- File: `docsplit/08_Server_tools_041d1f2e09f0.md` — **1122/1122 lines, 45,917 bytes read** (views 1–800, 800–1122). Source: Claudecode5Untitled-3.md lines 1556–2676.
- First heading: `## The server_tool_use block`. Last heading: `## Next steps` (cards: Troubleshooting, Web search, Web fetch, Code execution, Tool search).
- Also read: voltron_brief.md (26 lines). Ran a read-only grep of `integra-homebase/core/*.py` and `integra-homebase/*.py` for `pause_turn|stop_reason|web_search|web_fetch|server_tool|allowed_domains|content[0]`. Only hit: an api_clients.py:121 comment about `content[0].text`. **No server-tool or stop_reason handling found.**

## 1 DOC SAYS
**Tools named in the section** (it covers shared mechanics only and sends readers to the tool reference for individual tools):
- `web_search_20250305` (basic; ZDR-eligible; example uses `max_uses: 10`)
- `web_fetch_20250910` (basic; ZDR-eligible; example uses `max_uses: 5`)
- `web_search_20260209` / web_fetch `_20260209`+ (dynamic filtering through internal code execution; **not ZDR-eligible by default**)
- `code_execution_20260120`+ (required if you add code_execution next to the `_20260209` web tools; older versions are rejected)
- Tool search tool (link card only). MCP connector `mcp_tool_use` acts like `server_tool_use`.

**Mechanics:**
- `server_tool_use` block ids start with `srvtoolu_`. The API runs these tools itself, so no `tool_result` is needed. The result block (e.g. `web_search_tool_result`) is matched by `tool_use_id`, **not by position**.
- **`pause_turn`**: the server-side agentic loop can pause on long turns. To continue, re-send the assistant content as-is with the **same tools**. A missing tool causes a validation error. A turn can pause again, so cap the number of continuations like any retry loop.
- **Mixed server + client tools**: the API skips the server tool and returns `stop_reason: "tool_use"` (not `pause_turn`). You can only spot this by finding a `server_tool_use` id that has no result block. The follow-up user message must contain **only** `tool_result` blocks. Adding text gives a 400 (`...found without a corresponding web_fetch_tool_result block`). Dropping the tool gives a 400 (``...but no `web_fetch` tool was provided``). The deferred result becomes the **first block** of the next response.
- Programmatic tool calling: the same response shape, but `caller` names the code_execution block, and you must pass back the `container` id.
- **`allowed_callers`**: `"direct"`, `"code_execution_20260120"`, or both. `_20260209` defaults to code-exec caller only, and earlier versions default to `["direct"]`. Setting `["direct"]` turns off dynamic filtering, which makes the tool ZDR-usable. Models without programmatic tool calling *require* `["direct"]`.
- **Domain filtering**: `allowed_domains` OR `blocked_domains`, never both. No scheme. Subdomains are included automatically. A specific subdomain matches only that subdomain. Search supports subpaths; fetch matches the domain only, and a path entry never matches. Wildcards are allowed only in the path (`example.com/*`), never `*.example.com`. Invalid entries give a 400. A request-level allow list must be a subset of the org-level Console list. Use ASCII only because of homograph attacks. Managed Agents allows at most 64 entries per list and has no `max_uses`/`citations`/`cache_control`.
- ZDR caveat: website publishers may keep URL parameters.
- **Streaming**: `server_tool_use` streams as `content_block_start` + `input_json_delta`. The result arrives whole in one `content_block_start`.
- **Batch**: all server tools support it, with a higher per-turn iteration limit. Hitting the limit returns `pause_turn`.
- **Pricing: this section gives NO pricing numbers.** It also gives no per-tool limits beyond the `max_uses` examples.

## 2 MY INFERENCE FOR INTEGRA
- **Daily Planet / Tier 1 research** (I'm assuming this is the web-research tier; the brief doesn't define it): run research through nexus_right/shiva (Claude) with `web_search` + `web_fetch`, `max_uses` set, and a curated `allowed_domains` list. For the nightly bulk enrichment ("checking documents against current sources"), the Batch API fits. Either way, a `pause_turn` loop is needed.
- **Cheshire Daemon local-only boundary**: server tools run on Anthropic's side, so they would break "no internet". The guard has to be deterministic code: the daemon's request builder must reject any tool whose `type` starts with `web_search`, `web_fetch`, `code_execution`, or `mcp`, and Heimdall should treat any `srvtoolu_` / `mcp_tool_use` block in a Cheshire response as a lockdown breach. Domain filters are not a boundary for Cheshire. Leaving the tools out entirely is the only control. (If Cheshire runs on Gemini, the same rule applies to Google Search grounding.)
- **Heimdall**: log each server tool call (`srvtoolu_` id, name, query/URL) to the Proof-of-Sleep/usage ledger. Show `pause_turn` counts and continuation caps on the dashboard. Alert on 400s from tool-list drift. Use ASCII-only domain lists.
- **Rodin / Hoard**: keep fetched documents (`web_fetch_result` → `document.source.data`) as provenance-stamped nodes (URL, fetch time, tool_use_id). That lets "Alexandria Verification" cite real retrievals instead of making them up.
- **Kernel code**: the existing "join text blocks only" fix is necessary but not enough. With server tools, content contains `server_tool_use` and `*_tool_result` blocks, and the deferred result is block 0.

## 3 Contradictions with current wiring
1. **No `pause_turn` / `stop_reason` handling** in core (grep found none). Turning on any server tool today would silently return partial turns, which could be reported as complete answers. That is the fabrication risk.
2. Doc examples use `claude-opus-5-5` (matches nexus_right) and **`claude-opus-4-8`** for the mixed example. No `claude-sonnet-5-5` appears in this section, so I can't confirm it here.
3. `anthropic==1.5.0`: the doc doesn't give SDK versions. Whether `WebSearchTool20260209` / `allowed_callers` types exist in 1.5.0 is **unverified**. Raw dict tools would avoid the problem.
4. Pricing assumptions for web search/fetch can't be checked from this section.

## 4 Recommended actions (ranked)
1. **(S)** In api_clients.py, add a stop_reason dispatcher: `pause_turn` → re-send with the same tools (cap ≈3–5). `tool_use` → client results only. Any other unexpected value → log and flag as INCOMPLETE. Never return a paused turn as final.
2. **(S)** Add a deterministic Cheshire tool allowlist (empty server-tool set), plus a Heimdall response scan for `srvtoolu_`/`mcp_tool_use` that triggers a breach alert.
3. **(S)** Add ledger fields per call: stop_reason, continuation count, server tool ids/names/queries/URLs.
4. **(M)** Build the Tier 1 research path: `web_search_20250305` + `web_fetch_20250910` (ZDR-eligible, `direct` default), `max_uses` budgets, a curated ASCII `allowed_domains` list, and fetched docs written to The Hoard with provenance.
5. **(M)** Probe whether the SDK 1.5.0 types support `_20260209` + `allowed_callers` before adopting dynamic filtering. Record whether ZDR matters for the org.
6. **(L)** Run nightly SWDS source-verification as Batch jobs with server tools, with `pause_turn` follow-ups logged to the ledger.
