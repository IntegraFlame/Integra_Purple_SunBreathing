# 07 — Code execution tool: report

## 0 Read receipt
- Brief: `voltron_brief.md`, 26/26 lines, 4,162 bytes.
- Doc: `07_Code_execution_tool_dd86ecd0d119.md`, 1,556/1,556 lines, 62,800 bytes. I read it in two views (L1–800 and L801–1556).
- First heading seen: title "Code execution tool", then "## Tool versions". Last heading seen: "## Next steps".
- No project files were modified.
- I could not write to the requested path in the parent's brain directory: write_to_file is restricted to this subagent's own artifact directory.

## 1 DOC SAYS
- **Status:** `ga`. **ZDR: `not-eligible`**. Container data (artifacts, uploaded files, outputs) is retained for up to 30 days. Files that code execution creates in the Files API persist until you explicitly delete them.
- **Platforms:**

  | Platform | Code execution |
  |---|---|
  | Claude API | GA |
  | Claude Platform on AWS | GA |
  | Microsoft Foundry | GA, but only with a "Hosted on Anthropic" deployment |
  | **Amazon Bedrock** | **not available** |
  | **Google Cloud** | **not available** |

- **Models:** includes `claude-opus-5-5`, `claude-sonnet-5-5`, `claude-haiku-5-5`, opus-5/4-8/4-7/4-6/4-5, sonnet-5/4-6/4-5, haiku-4-5, and fable/mythos 5 and 5-1. Every supported model accepts all three tool versions. On Haiku 4.5, programmatic tool calling and REPL persistence are missing, so the newer versions behave like `code_execution_20250825` there.
- **Tool versions** (none needs an `anthropic-beta` header):
  - `code_execution_20250825`: Bash and file operations.
  - `code_execution_20260120`: adds REPL state persistence and programmatic tool calling.
  - `code_execution_20260521`: same runtime as 20260120. The difference is that the tool description tells Claude about the **90 s wall-clock limit per Python cell**. A cell that hits the limit returns a non-zero `return_code` with a `detection_timeout` message.
  - The latest version is `20260521`.
  - `web_search_20260209` and `web_fetch_20260209` require `code_execution_20260120` or later.
  - The legacy `code_execution_20250522` is Python-only and uses the header `code-execution-2025-05-22`.
- **Tool definition:** `{"type": "...", "name": "code_execution"}`. Both fields are fixed and there are no other parameters. It provides two sub-tools: `bash_code_execution` and `text_editor_code_execution`.
- **Capability probe:** read `capabilities.server_tools.code_execution.supported` from the Models API. Do not use the top-level `capabilities.code_execution`, which reports programmatic-tool-calling ability instead.
- **Response blocks:**
  - A `server_tool_use` block (id `srvtoolu_…`), followed by a `bash_code_execution_tool_result` containing `stdout`, `stderr`, `return_code`, and `content[]` (one `file_id` per file).
  - `text_editor_code_execution_{view,create,str_replace}_result` blocks.
  - A top-level `container` object with `id` and `expires_at`.
- **Errors:** `unavailable`, `execution_time_exceeded`, `invalid_tool_input`, `too_many_requests`; `output_file_too_large` (bash only); `file_not_found` (editor only).
- **Stop reason:** `pause_turn` means the API paused a long turn. Send the response back as-is to let Claude continue.
- **Mixing with client tools:** if Claude calls a client tool alongside code execution, the code execution result is withheld until you return your `tool_result` blocks.
- **Runtime:** Python 3.11, Linux x86_64, 5 GiB RAM, 5 GiB disk, 1 CPU. The doc gives no number for the maximum execution time per invocation.
- **Network and isolation:** no internet and no outbound connections. Fully isolated, scoped to the request's workspace.
- **Libraries:** pre-installed only (pandas, numpy, scipy, sklearn, statsmodels, matplotlib, seaborn, pyarrow, pdf/office libraries, sympy, and others). CLI tools include `rg`, `fd`, `sqlite`, and `7zip`. Nothing can be installed at runtime.
- **Files:**
  - Uploads go in through the Files API plus a `container_upload` content block.
  - Only files at the top level of `$OUTPUT_DIR` (a fresh directory per bash call) are returned.
  - Claude cannot see the returned `content` list, so prompt it to `cp` into `$OUTPUT_DIR` and then `ls` it.
  - Image, video, and audio outputs get a C2PA manifest on download, which changes their size and checksum. Text, PDF, and office files are not signed.
- **Containers:**
  - A container is new on each request unless you pass the top-level `container` parameter.
  - Containers are checkpointed after about 5 min idle and restorable within **30 days of creation**. `expires_at` is a shorter rolling value, not the 30-day limit.
  - An expired container returns an error; send the request again without `container` to get a new one.
- **Pricing:**
  - Free (tokens only) when `web_search_20260209` or `web_fetch_20260209` (or later) is in the request.
  - Otherwise billed by execution time: **minimum 5 min**, **1,550 free hours/org/month**, then **$0.05/hour per container**.
  - **Including files bills execution time even if the tool is never called.**
  - Batch API pricing is the same.
  - Usage appears at `usage.server_tool_use.code_execution_requests`.
- **Streaming:** sub-tool input arrives as `input_json_delta`. Each result block arrives whole in a single `content_block_start`.

## 2 MY INFERENCE FOR INTEGRA
- **SWDS/Siesta:**
  - Every execution yields `srvtoolu_` IDs, `return_code`, `stdout`/`stderr`, and a container ID. These map directly onto Proof-of-Sleep ledger rows.
  - A phase that claims computation but has no `bash_code_execution_tool_result` with `return_code: 0` should print NOT EXECUTED.
  - SWDS analytics such as Hoard dedupe stats or shard coverage (10 of 305) can run in the sandbox. However, local Python on the kernel is free, keeps the data local, and can be logged deterministically, so the sandbox adds cost and egress for little gain.
- **Cheshire Daemon local-only boundary:** **the tool is incompatible with this boundary.**
  - The sandbox has no internet, but it is Anthropic-hosted. Uploading Hoard or Rodin nodes sends data off-machine.
  - The tool is not ZDR-eligible, and data is retained for up to 30 days.
  - Cheshire must never get this tool. The Daemon should do its "computation" through kernel-local functions only.
- **Heimdall:**
  - Meter `usage.server_tool_use.code_execution_requests` per call.
  - Estimate container-hours as at least 5 min per call, plus the hidden cost of any request that carries `container_upload`.
  - Alert well below 1,550 h/month.
  - Treat `too_many_requests`, `unavailable`, and `pause_turn` as health signals.
  - Track open container IDs and their 30-day lifetime.
  - Audit Files API outputs, because they persist until deleted.
- **Rodin:** sqlite-vec cannot be installed in the sandbox: there is no network and it is not in the pre-installed list. Only the plain `sqlite` CLI is there. Vector retrieval has to stay on the kernel.
- **Hoard:**
  - Hash files after download. C2PA changes image checksums, so a hash taken inside the container will not match.
  - Text, MD, and JSON files are unchanged by signing.
  - Downloaded outputs should be filed as nodes stamped with their source `file_id`, container ID, and `srvtoolu_` ID.
- **Kernel code:**
  - Response parsing must tolerate `server_tool_use`, `*_tool_result`, and `container` blocks.
  - It must loop on `pause_turn`.
  - Any multi-environment prompt (kernel shell plus sandbox) needs the doc's "state does NOT persist between environments" system-prompt clause.

## 3 Contradictions with current wiring
1. **Platform risk:** the tool is "not available" on Google Cloud. If any Claude call is routed through Vertex (Integra holds Vertex credentials), code execution, and with it the dynamic filtering in web_search/web_fetch 20260209, will not work. Claude must use the direct Claude API. Needs a probe.
2. **SDK pin `anthropic==1.5.0`:** the doc does not state a minimum SDK version. Whether 1.5.0 has types for `code_execution_20260521`, the `container` parameter, and `bash_code_execution_tool_result` is unverified. Probe before use.
3. **Parsing hazard:** joining only text blocks is safe, but kernel code that does not handle `pause_turn` will return truncated turns as if they were complete. With client tools, the withheld code execution result can be mistaken for a finished turn. This fits the brief's "fabricated reports" pattern.
4. **Python 3.11 (sandbox) vs 3.13 (kernel):** code that Claude writes for the sandbox is not guaranteed to match the kernel interpreter.
5. **Cost assumptions:** pricing is per container-hour with a 5-minute minimum, so many tiny calls (for example, Cheshire "many calls per study session") would each bill at least 5 min. Attaching files bills time even when the tool goes unused.

## 4 Concrete recommended actions (ranked)
1. **(S)** Hard-deny `code_execution`, web_search, and web_fetch in the Cheshire Daemon's tool list in code. The ZDR status (not eligible) and the 30-day retention break the local-only boundary.
2. **(S)** Write a probe script: call the Models API for `claude-opus-5-5` and `claude-sonnet-5-5`, read `capabilities.server_tools.code_execution.supported`, and confirm the endpoint is api.anthropic.com, not Vertex. Log the result to the ledger.
3. **(S)** Add `pause_turn` continuation and server-block-aware parsing to `core/api_clients.py`. Never treat a response without a final text block as complete.
4. **(M)** Heimdall meter: record `code_execution_requests`, estimated container-minutes (minimum 5), and container IDs and creation times. Alert at, say, 50% of 1,550 h. Run a weekly Files API cleanup.
5. **(M)** Proof-of-Sleep schema: add fields for `srvtoolu_id`, `container_id`, `return_code`, a stdout hash, and output `file_id`s. Render reports only from these.
6. **(L)** Optional: use the sandbox only for non-sensitive SWDS analytics. Pin `code_execution_20260521` so Claude budgets around the 90 s cell limit. Default to local kernel Python instead.
