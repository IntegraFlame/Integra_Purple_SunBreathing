# 13 — Browser & Computer Use with the SDK Toolsets — Report
Stamp: 2026-10-08 03:01 CDT (08:01Z). Reader: subagent 2155d494.

## 0 Read receipt
- File: `docsplit/13_Browser_and_computer_use_with_the_SDK_to_96b1de417f0b.md` — 1,278 lines / 75,929 bytes, read in full (lines 1–775 in view 1, 775–1278 in view 2; overlap at 775 covered the truncated byte tail).
- First heading: `title: Browser and computer use with the SDK toolsets` (URL `.../tool-use/browser-use-sdk`). Sections: Partner integrations → Quick start → Customize a driver → Implement a driver → Run the toolset safely → Computer toolset → Reference → Limitations → last heading **Next steps**.
- Empirical probe (read-only): `integra-homebase\.venv` → `anthropic.__version__ == 1.5.0`; `anthropic.tools` exists but `anthropic.tools.browser` = **absent**, `anthropic.tools.computer` = **absent**.

## 1 DOC SAYS
**Toolsets / classes (both beta, Python + TypeScript SDKs):**
- `BetaAbstractBrowserToolset20260801` (`anthropic.tools.browser`) and `BetaAbstractComputerToolset20260801` (`anthropic.tools.computer`); async variants `BetaAsyncAbstractBrowserToolset20260801` / `BetaAsyncAbstractComputerToolset20260801`. TS import: `@anthropic-ai/sdk/helpers/beta/toolsets`.
- You subclass and write one method per member (`navigate`, `screenshot`, `left_click`, `type`, `key`, …). Browser driver must implement `_browser_state` (TS `browserState`). SDK ships **no browser, desktop, driver, or URL policy**; minimal CDP (browser) and VNC (computer) examples in claude-quickstarts, "isn't production code".
- Unimplemented members are sent as disabled; calling one returns an error, run continues. Overriding `execute` makes SDK treat every member as implemented → must disable extras via `configs`.
- Run with `client.beta.messages.tool_runner(...)` or own loop using `browser.tool_result(call)`; calls carry `toolset_name` (`browser`/`computer`). Runner never closes the toolset.
- Early start: `stream=True` + `run_tools_eagerly=True`; a started call "can't be taken back" if response is cut at `max_tokens`.
- Computer tool: 17 tools total; example implements 5. `screenshot`, `cursor_position`, `left_mouse_down`, `left_mouse_up` have no inputs.

**Versions / headers:** Only date-versioned class names `...20260801`. **The section names no beta header string and no tool `type` version string.** Example model: `claude-opus-5-5`, `max_tokens=1024`.

**Constructor options:** `configs`, `confirm`, `url_policy`, `file_policy`, `tool_configs` (e.g. `cache_control`), `_browser_state`. Computer class takes only `configs`, `confirm`, `tool_configs`. Options immutable after construction.

**Errors:** `ToolError` → Claude reads message, run continues; `ToolsetUsageError` → run stops (config error, call after `close`, or any exception in `_browser_state`); other exceptions → `ClassName: message`, continues. SDK does **not** hide local paths in error text.

**Safety (browser, 6 steps):** URL policy; request interception in driver; container egress policy (block private/link-local incl. `169.254.169.254`; DNS only to resolver); confine uploads/downloads (`BetaLocalFilePolicy(upload_roots, download_dir, expose_download_paths)`, download dir mode `0700`, `noexec,nosuid,nodev`); gate with `confirm`; isolate host per session (non-root, fresh profile, no credentials). Key facts: without URL policy SDK checks **no** URL; `url_policy=None` refuses all; SDK doesn't check schemes (`javascript:`, `file:`, `data:`, `view-source:` must be refused by you); **egress rules outside the container can't block loopback** — a page can reach a DevTools port. `javascript_exec` and `file_upload` off by default and require `confirm`. Prompt-injection classifiers don't run on browser toolset requests via Amazon Bedrock.

**Safety (computer, 5 steps):** isolate desktop; gate with `confirm`; keep terminals/run dialogs/launchers off desktop; refuse out-of-range input; treat screen as untrusted. Implementing `type`/`key`/`hold_key` without `confirm` → configuration error. With no `confirm`, SDK runs every call. Fail-closed: auto-approve only `screenshot`, `zoom`, `cursor_position`, `wait`.

**Limits:** URLs and computer error/return text cut at 4,096 chars; SDK never resizes images — API rejects oversize image and run ends; >20 images in one request triggers stricter per-image limit; SDK doesn't limit `duration`, `repeat`, `scroll_amount`; one toolset runs calls serially (can't disable); approvals are based on last state report (page can change); computer `confirm` sees tool+input, not the screen. Skipped-call texts: browser `Not executed: an earlier action in this turn failed.`; computer `Not executed: an earlier computer action in this turn failed.`

## 2 MY INFERENCE FOR INTEGRA
- **Dashboard verification:** The browser toolset could let Claude visually verify `127.0.0.1:8000/dashboard`. But the doc's own warning is decisive: loopback is exactly the surface that egress rules can't protect, and the kernel/MCP endpoints live there. A URL policy allowing only `http://127.0.0.1:8000/dashboard|/clock` + request hook would be required. Cheaper and deterministic: Playwright/curl probes by code (no model), screenshot only on failure.
- **Heimdall monitoring:** Heimdall authority must be deterministic; a model-driven computer loop contradicts that. Usable pieces: overriding `execute` as a before/after hook pattern (timing, call IDs) maps onto the Proof-of-Sleep ledger; `confirm` maps onto Heimdall lockdown gating.
- **Cheshire Cat "local-only" risk:** Giving it any browser/computer toolset breaks the local-only constraint (pages = untrusted input, `file:` URLs read host files, `javascript:` runs script). Do not attach these toolsets to Cheshire Cat.
- **Host risk:** Integra runs on the Architect's signed-in Windows desktop in OneDrive — the opposite of "dedicated container/VM, fresh profile, no credentials". Computer use there could type into terminals.
- **Cost:** screenshot-heavy loops, 20+ images/request stricter limits — conflicts with the token-overuse problem.

## 3 Contradictions with current wiring
1. **SDK version:** pinned `anthropic==1.5.0` lacks `anthropic.tools.browser`/`.computer` (verified). Doc code won't import without upgrading.
2. Model ID `claude-opus-5-5` matches `nexus_right`. No conflict.
3. Doc examples use `client.beta.messages...`; current clients presumably use non-beta `messages.create` (not verified in this pass) — toolset requires beta surface.
4. No beta header named here; any assumption of a specific header string is unsupported by this section.
5. Host model (Windows desktop, Task Scheduler, OneDrive) violates every isolation step.

## 4 Concrete recommended actions (ranked)
1. **(S)** Do NOT wire browser/computer toolsets into Cheshire Cat or Heimdall authority paths; record as policy in kernel card.
2. **(S)** Dashboard verification via deterministic code probes (`curl`/Playwright headless, no model) logged to the ledger; model sees only failures.
3. **(S)** If any future use: adopt fail-closed `confirm` (approve only `screenshot`, `zoom`, `cursor_position`, `wait`), `url_policy` with explicit allowlist + scheme refusal, never `None`-by-accident.
4. **(M)** Before adopting: upgrade/verify Anthropic SDK version that ships `anthropic.tools.browser` in a separate venv; re-run the read-only import probe; check beta header in the Browser use tool doc.
5. **(M)** Reuse the `execute`-override hook pattern for ledger instrumentation of all tool calls (call_id, member, ms, result hash).
6. **(L)** Any real computer/browser automation only inside a disposable VM/container (Windows Sandbox or Docker) with in-container egress rules blocking loopback-reachable services, no OneDrive mounts.
