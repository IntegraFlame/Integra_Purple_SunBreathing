# 05 — Anthropic Memory Tool: Report

## 0. Read receipt
- `voltron_brief.md`: all 26 lines, 4,162 bytes.
- `05_Memory_tool_782fafb29fed.md`: all 615 lines, 22,976 bytes. First heading: "Use cases". Last heading: "Implement the memory handler". The file stops partway through line 614, in the PHP `rename` case (`$store[$input['old`).
- `06_Memory_tool_36c165d57e7c.md`: all 1,027 lines, 40,781 bytes. First heading: "Use cases". Last heading: "Next steps".
- Diff check: I ran a scripted line-by-line comparison of lines 2–613. **0 differences.**

## 1. DOC SAYS
- **What it is:** a tool that runs on your side. Claude asks for file operations under `/memories`, and your application carries them out and returns a `tool_result`. `/memories` is only a prefix. Your handler maps it onto real storage, such as a directory or database keys. A later conversation sees the same memory if it sends the same `tools` entry and your handler serves the same store.
- **Tool entry (the whole configuration):** `{"type": "memory_20250818", "name": "memory"}`. `name` must be `memory`, and you do not define an input schema. No beta header is needed, but the SDK helpers and tool runners live in the beta namespace.
- **Models:** "all Claude 4 and later models". The examples use `claude-opus-5-5`, `max_tokens` 2048 or 1024, and `anthropic-version: 2023-06-01`.
- **Python helper:** `from anthropic.tools import BetaLocalFilesystemMemoryTool`, `BetaLocalFilesystemMemoryTool(base_path="./memory")`, `client.beta.messages.tool_runner(model, max_tokens, messages, tools=[memory])`, `runner.until_done()`. To use your own storage, subclass `BetaAbstractMemoryTool`. TypeScript uses `betaMemoryTool` with `max_iterations: 10`. Java uses `BetaMemoryToolHandler`. Go, Ruby and PHP have no helper, so they run the loop by hand on `stop_reason == tool_use`.
- **Commands and parameters:**
  - `view`: `path`, plus optional `view_range` `[start,end]` (`-1` means to end of file).
    - A directory view lists 2 levels deep with human-readable sizes, tab-separated. It skips dotfiles and `node_modules`.
    - A file view returns 1-indexed line numbers, 6 characters wide and right-aligned, then a tab. Files over 999,999 lines return an error.
    - `view` can also show `.jpg`, `.jpeg` and `.png`. Text views are truncated above **16,000 characters**, so Claude follows up with ranged views.
    - A first `view` on an empty store is not an error.
  - `create`: `path`, `file_text`. The reference behavior returns the error "already exists". However, Claude's own tool description says create "creates or overwrites", so overwriting is also a valid choice.
  - `str_replace`: `path`, `old_str`, optional `new_str` (if omitted, `old_str` is deleted). It errors if the text is not found or appears more than once ("Multiple occurrences … in lines: …"). A directory path returns "does not exist".
  - `insert`: `path`, `insert_line` (text goes after that line; `0` means the top of the file), `insert_text`. Valid range is `[0, n_lines]`.
  - `delete`: removes directories recursively. Must reject the `/memories` root.
  - `rename`: `old_path`, `new_path`. Never overwrites an existing destination. Must reject the root as `old_path`.
- **Errors:** return `is_error: true` with the message in `content`.
- **System prompt added automatically by the API:** "IMPORTANT: ALWAYS VIEW YOUR MEMORY DIRECTORY BEFORE DOING ANYTHING ELSE … ASSUME INTERRUPTION: Your context window might be reset at any moment …". You can optionally add a "keep organized / do not create new files unless necessary" line, and you can limit memory to one topic.
- **Security (your responsibility):**
  - Strip sensitive data before writing.
  - Cap file sizes and cap how much `view` returns; let Claude page with `view_range`.
  - Expire files that have not been accessed in a long time.
  - Block path traversal: paths must start with `/memories`; resolve to canonical form (`pathlib.Path.resolve()` + `relative_to()`); reject `../` and `..\\`; catch URL-encoded `%2e%2e%2f`.
- **Context editing and compaction:**
  - Context editing clears specific tool results on the client side.
  - Compaction summarizes the whole conversation on the server as it nears the context limit.
  - The doc recommends using both: compaction keeps context small, and memory "preserves the information that must survive summarization".
- **Pattern for multi-session software projects:**
  - An initializer session first creates a progress log, a feature checklist and a pointer to the startup script.
  - Each later session starts by reading these files.
  - Each session ends by updating the progress log.
  - Work one feature at a time, and mark a feature complete only after end-to-end verification.
- Includes a zero data retention (ZDR) note.

## 2. Diff between the two versions
- Lines 2–613 are byte-identical. Line 1 is only the provenance comment: 05 came from `Claudecode1import anthropic.md` lines 4476–5090, and 06 from `Claudecode4Untitled-2.md` lines 1–1026.
- **05 is the same page cut off, not an older version.** It ends at the source-span boundary, partway through the PHP example.
- **Everything below is only in 06 (lines 614–1027):**
  - The rest of the PHP example and the full Ruby example.
  - The paragraph listing SDK example files.
  - **The entire "Tool commands" spec**: return strings, the 16K truncation, image views, create-overwrite, the root-deletion ban.
  - **Prompting guidance**, including the exact system prompt the API adds.
  - **Security considerations**, including path traversal.
  - **Error handling** (`is_error`).
  - **Context editing / compaction** sections.
  - **The multi-session pattern.**
  - "Next steps".
- Anyone who read only 05 missed every rule and security requirement.

## 3. MY INFERENCE FOR INTEGRA
- **One store with three access paths.** The memory tool reaches only Claude agents called through the API by the kernel. A Claude chat thread in claude.ai or a Project cannot call your handler; the doc never mentions claude.ai. For your thread-to-thread continuity, the access path is still the planned **MCP memory server**. The memory tool and the MCP server should be two front ends on **one backend**:
  - SQLite `nodes`/`edges`/`ledger`, outside OneDrive.
  - Gemini clients would get the same handler exposed as a Gemini function declaration.
- **Proposed `/memories` layout:**
  - `kernel_card.md` (small, always the first read)
  - `progress_log.md`
  - `feature_checklist.md`
  - `handoff/<thread_id>.md`
  - `cheshire/study_state.md`
  - `swds/last_cycle.md`
  - Files stay small, because the 16K-character truncation forces ranged reads.
- **The Hoard:** a subclass of `BetaAbstractMemoryTool` writes each `create` / `str_replace` as a node version in SQLite, and the uncompressed JSON save state goes to The Hoard. The listing format skips dotfiles, so hidden `.meta` sidecar files (hash, CCID, last-access time) stay out of Claude's view.
- **Rodin:** `view` is lookup by path, not semantic search. Rodin's KNN search stays a separate capability, offered through MCP `search_memory`. Optionally, a virtual `/memories/index.md` could be generated from the Rodin graph.
- **Proof-of-Sleep ledger:** every memory command becomes a hash-chained ledger row (time, model call ID, command, path, hash before/after). This gives an audit trail of who wrote each memory and when. The doc's "mark complete only after end-to-end verification" rule matches the planned anti-fabrication rule (phases with no ledger entries print NOT EXECUTED).
- **Cheshire Daemon:** the tool's client-side design fits "local only". The doc's "ASSUME INTERRUPTION" protocol fits 1–2 h study sessions that save state. But the daemon is planned on Gemini 3.1 Pro, which needs the same handler through function calling; native support exists only on Claude.
- **Skimming:** a capped `view` plus ledger-logged `view_range` coverage can prove which lines of a file were actually read.

## 4. Contradictions with current wiring
1. **Model ID matches.** The doc uses `claude-opus-5-5`, the same as `nexus_right`.
2. **SDK: no contradiction (checked).** anthropic **1.5.0** (`anthropic-1.5.0.dist-info`) has `anthropic/tools/memory.py`, which exports both `BetaLocalFilesystemMemoryTool` and `BetaAbstractMemoryTool`. I have not run it end to end.
3. **The current client is (inferred) single-shot text-joining.** Memory needs a tool-use loop: tool_use → tool_result → resend. The thinking-block-first hazard also applies to tool_use blocks, which code that only joins text will drop.
4. **The automatic prompt "ALWAYS VIEW … BEFORE ANYTHING ELSE"** adds at least one round trip and extra input tokens to every memory-enabled call. That works against problem (3), token overuse. Enable memory only for long-running agents, not every routed call.
5. **"Memory expiration: periodically delete"** conflicts with The Hoard's permanent storage. Archive to GCS cold storage instead of deleting.
6. **"create overwrites" allowed** conflicts with the append-only ledger. Choose the reference error behavior, or keep versions.
7. **No native Gemini support.** 5 of the 7 routed clients are Gemini.
8. **OneDrive path:** the default `./memory` relative path inside the project would sit under OneDrive's sync. Use an absolute path outside OneDrive.

## 5. Concrete recommended actions (ranked)
1. **(M)** Build the `IntegraMemoryTool(BetaAbstractMemoryTool)` handler. Back it with SQLite outside OneDrive. Include traversal guards (`resolve()`+`relative_to()`, `..\\`, `%2e%2e`), root-delete/rename bans, size caps, and **no overwrite on create**. Log every operation to the hash-chained ledger.
2. **(S)** Write the initializer files `kernel_card.md`, `progress_log.md` and `feature_checklist.md`. Mark items complete only after verification.
3. **(M)** Expose the same backend through the planned MCP memory server (`get_kernel_card`, `write_handoff`, `search_memory`, …) so Claude chat threads get continuity. This is the actual fix for problem (1).
4. **(M)** Add a tool-use loop to `core/api_clients.py` for `nexus_right` / `shiva_orchestrator` only. Handle `tool_use` blocks alongside thinking and text blocks.
5. **(S)** Write a Gemini function declaration that mirrors the 6 commands, so the Cheshire Daemon and Phoenix use the same store.
6. **(S)** Write a test: run the doc's Python example against a temporary directory and confirm with the ledger and a file hash.
7. **(L)** Pair the memory tool with compaction for long kernel sessions. Read the separate compaction and context-editing docs first; this doc only links to them.
