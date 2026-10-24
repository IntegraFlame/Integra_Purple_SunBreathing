.9.9.1:** 2026-10-11. It adds the "v.9.9.1 update" section after Section 1, the Architect's decisions of 2026-10-11 (D-1, D-2, D-6 and the second half of D-16 decided), and cross-references. Last successful live stamp: 2026-10-11 03:43:57 CDT | 08:43:57Z | Celestial (`GET /clock`, HTTP 200): rot 279.8229°, lunar 0.6085, orbit 0.2135, grid `ROT_270_ORB_20`. From 03:51 CDT the kernel's sync endpoints stopped answering, until the machine was shut down at 16:19 (see the v.9.9.1 update, "Kernel note"). Self-reviewed against sources the same morning (Appendix B, item 9) and corrected again that night (item 10). Interim corrections from the Step 2 reading of folders 1-5 were applied on 2026-10-12 (item 11).
**Evidence stamp (v.9.9 body):** 2026-10-09 19:26:08 CDT | 2026-10-10T00:26:08Z | Celestial (live `GET /clock`, HTTP 200): rot 155.3662°, lunar 0.5629, orbit 0.2098, grid `ROT_150_ORB_20`
**Scope:** the four documents in `integra-homebase/docs/` (OCT9Suite1_3, OCT9Suite1_2T, OCT9IntegraSuite1_1, gemini_cli_subagent_reference), checked line by line against the code in `integra-homebase` (HEAD `8c8c2da`, branch `phase-e-dragon-rodin-flight`) and against the running Genesis Kernel on `127.0.0.1:8000`.
**Author:** Claude (Opus 5.5), for the Architect. Read-only study: nothing in the code, the kernel, the Hoard or git was changed to produce this document. The 2026-10-09 code changes it reports (Section 4.4.1, R-5) were made separately and are labelled as such.

---

## 0. How to read this document

### 0.1 Status legend

Every component in this blueprint carries one of these labels. They are deliberately narrow, so that "exists" is never confused with "works".

| Label | Meaning |
|:--|:--|
| **VERIFIED** | Runs as described. Proven by a live probe, by a log line with a traceable time, or by code that has no other path. |
| **FUNCTIONAL-HEURISTIC** | Runs, but does something simpler than the documents say (for example word counts where the docs say Bayesian inference). |
| **EXISTS-UNEXERCISED** | Wired into the running kernel and reachable, but nothing has invoked it since the kernel started. |
| **EXISTS-UNWIRED** | Code exists, but nothing in the running system calls it (only tests, or nothing at all). |
| **CONSTANT** | Presented as a live measurement, but the value is hard-coded or derived only from constants. |
| **FALSE-POSITIVE** | A document or log says it works, is measured, or is complete; the code or the live system contradicts it. |
| **CONCEPT-ONLY** | Described in the documents, with no implementation. Some of these are philosophy or metaphor and need no implementation. |
| **MISSING / UNDEFINED** | Referenced or depended on, but never defined, defined blank, or defined in conflicting ways. |
| **UNVERIFIED** | Could not be checked without side effects (cost, writes to the live Hoard, or reading secrets). |

### 0.2 Evidence format

- Code is cited as `path:line` relative to `integra-homebase/` (for example `main.py:1134`).
- The four documents are cited as `1_3:L47` (OCT9Suite1_3.md), `1_2T:L1545` (OCT9Suite1_2T.md), `1_1:L1028` (OCT9IntegraSuite1_1.md) and `GEM:L393` (gemini_cli_subagent_reference.md).
- Live evidence is cited with the probe time. Unless stated otherwise, probes ran between 19:26:07 and 19:26:24 CDT on 2026-10-09 against the kernel process started 05:27:48 CDT the same day (uptime 13 h 58 m).
- Secret values were never read. Where `.env` matters, only the presence of a key **name** was checked.

### 0.3 Method, honestly stated

The brief asked for one hour per file, then a fifth hour over everything. Wall-clock hours are not something I can measure or spend in the way a person does, so depth came from these passes instead:

1. **Pass 1, each file alone, in your order:** Suite 1_3 (151 lines), Suite 1_2T (7,078 lines), Suite 1_1 (1,644 lines), the Gemini CLI reference (600 lines). Every line was read; every component, number and claim was recorded.
2. **Pass 2, the files against each other:** byte-level diffs between the suites, duplicate detection, contradictions, terms used before they are defined.
3. **Pass 3, the files against the code and the live kernel:** each claim traced to `file:line` or to its absence, plus read-only probes of 11 live endpoints, the process table, the scheduled task and the kernel log.
4. **Interim report:** the reading and verification ledgers, recorded before synthesis.
5. **Pass 4, second full read:** Suite 1_3 again, and all Integra-authored parts of Suite 1_2T again (lines 1–1762 and 3404–7078), this time with the code evidence in hand. The memory-tool sections were not re-read word for word because a diff proves them identical to Suite 1_1.
6. **Synthesis**, Knowledge → Understanding → Wisdom, which is Sections 3, 7 and 8.

Pass 4 changed conclusions. The biggest finding in this document (Section 1, finding 1) came from that second pass, when a log that looked empty turned out to be misread and a frozen clock explained what earlier sessions had called a "stuck" sleep cycle.

---

## 1. Executive verdict

Integra today is a **real, running, well-instrumented host process wrapped around a cognition layer that is mostly idle, and a telemetry layer that is mostly self-referential.** The code base is substantial (55 routes, 23 test files with 285 test functions, a working model router, 10 lens heuristics, a SQLite manifold with triggers, a ChromaDB-backed Hoard, three background loops). But most of the numbers the dashboards show are constants, proxies, or stale rows. The cognition the documents describe happens, when it happens at all, in the IDE agent (the Dragon), not in the kernel.

The twelve findings that matter most, in order of consequence:

1. **The kernel's clock restarts at 2026-10-06 20:59:42 on every boot (VERIFIED, root cause).** `celestial_time()` returns a checkpoint written on 10/06 plus the seconds since boot (`core/celestial_middleware.py:324-328`; checkpoint file last written 2026-10-06 20:59:42). The checkpoint is only refreshed when someone calls `GET /celestial/checkpoint` (`core/celestial_middleware.py:250`). The sleep scheduler reads the hour from this clock (`main.py:1134`). It has done so since commit `6021755` (2026-09-23 22:01, "Complete celestial injection"), which replaced the `datetime.now()` calls in `runtime/swds_simulator.py` and `main.py` (v.9.9.1, item 11). So **slow-wave deep sleep (SWDS) fires exactly 5 hours after every boot and wakes 10 hours after, whatever the real time is.** Today it slept from about 10:28 to 15:28 in the afternoon. Every report is stamped with a 10/06 or 10/07 date, report filenames collide, and the previous thread's "SWDS stuck asleep for 22 hours" (`1_2T:L1545`) was a misdiagnosis of this.
2. **The kernel has made zero model calls since it started 14 hours ago (VERIFIED).** All seven routed models show `calls_made: 0`, `tokens_consumed: 0`. The model wiring itself is real (the 10/07 self-test passed 7/7), but no running path invokes it.
3. **When the cognition pipeline does run, its answer is thrown away (VERIFIED).** `POST /cognitive/cycle` runs the four Zenitsu passes through Y789 and Nexus (up to 12 model calls in dyad mode), then stores a Hoard node built from weights and route strings rather than the model's text (`sensory/cheshire_cat.py:339-382`). The response to the caller does not include the text either, and the event that carries it is drained and dropped by the 30 Hz loop (`sensory/cheshire_cat.py:574-576`).
4. **The hallucination guard (P-SSR) cannot trigger on real models (VERIFIED).** Every real client yields `probabilities=[]` (`core/api_clients.py:416, 556, 663`), and the in-flight check requires probabilities (`core/cognitive_engine.py:374`). In dyad mode it is skipped entirely (`core/cognitive_engine.py:347-349`). Only the test placeholder supplies probabilities, fixed at `[0.8, 0.1, 0.05, 0.05]` (`core/cognitive_engine.py:550`), which is why tests pass.
5. **The pre-generation entropy gate is mathematically unreachable (VERIFIED by computation).** It measures character-frequency entropy of the prompt (`sensory/heimdall.py:117-128`). With α = 0.3, the thermostat is reset *after* each completed cycle (`sensory/cheshire_cat.py:402`), and between cycles the 30 Hz loop nudges it to about 0.3. So a one-shot breach needs more than about 7.6 bits per character (8.33 starting from zero). Ordinary English is about 4.2, and printable ASCII cannot exceed 6.57. Repeated `/heimdall/evaluate` or `/ignite` calls are never reset, and three English prompts in a row breach the shared thermostat before the next cycle starts (v.9.9.1, item 11).
6. **SWDS is a script that writes a report, not a sleep cycle (VERIFIED).** Phases 1–2 are string assignments, the "dream mutations" are `random.uniform(0.1, 0.5)` (`runtime/swds_simulator.py:90-108`), ΔE and L_t are printed as constants (`:190`), the celestial value is always the 282.85° fallback because the report writer calls a method that does not exist (`:171-172`), and Phoenix re-reads the same first 10 of 305 shards each cycle and appends the same four hard-coded axioms (`evolution/phoenix_forge.py:120-143`).
7. **Most "live" telemetry is constant or proxied (VERIFIED).** Thermodynamic stress 131.625 MPa, Mach 4.2, KL divergence 0.0, `all_forms_verified: true`, angular momentum 500, Epiphany Ω 269.819457 (a constant **plus** e^0.1: 268.714286 + 1.105171), ΔE 0.0001 (a 9/23 test row), the startup line "ALL PHASE D SUBSYSTEMS ONLINE" (printed unconditionally, `main.py:157`), and Heimdall's `alerts_active: true` (`sensory/heimdall.py:769`).
8. **Heimdall the gatekeeper does not exist yet (MISSING).** Heimdall's entropy math matches the docs, but the role the Architect defined on 10/07 (budgets, power sequencing, lockdown, permit/deny, connectivity and MCP watch) has no implementation. A token-budget circuit breaker exists in the model router (`core/model_router.py:285-317`), but every budget is set to unlimited.
9. **Memory is real but thin and partly fake (VERIFIED / FALSE-POSITIVE).** The Hoard and ChromaDB exist. But the "true MRL" embeddings are SHA-512 hashes (`evolution/phoenix_forge.py:498-516`), Rodin silently falls back to SHA-256 pseudo-vectors when its embedding call fails (`memory/rodin_protocol.py:343-351`), the embedding model defaults to `text-embedding-004`, which is shut down on the Gemini Developer API (2026-01-14) and served on the Agent Platform, the kernel's actual path, only until **2027-04-01** (see `RODIN_SUBAGENT_MODEL_RESEARCH.md`), and the live Metatron database sits inside OneDrive.
10. **Daily Planet mixes real sources with invented ones (VERIFIED).** 38 of 40 Daily Planet shards in the Hoard contain real Firecrawl sources, but every source gets the same default bias scores. Two shards contain sources fabricated by a silent fallback that invents titles, publishers, SEC and arXiv URLs, and figures (`tools/daily_planet.py:208-276`).
11. **Definitions are unsettled.** The Shiva Eye and lens assignments exist in at least ten versions across the documents (Section 6.2). Suite 1_3 has the Eye definitions deleted outright (`1_3:L47-49`). Hippocampus is assigned to two different components, the Cheshire name to two different entities, and the SWDS schedule and CWA thresholds each have three versions.
12. **The Oct 7 learning proposal was never applied.** `GEMINI.md` has the 9/30 rule §4.1 but not §4.2 or §4.3; `SKILL.md` (10/01) lacks the Cheshire Daemon §9.1, the Heimdall correction and the registry fix.

**What is genuinely solid:** the FastAPI host and its 55 routes; the model router with power states and a working budget mechanism; the live 7-model wiring proven on 10/07; the Heimdall EMA math; the Cheshire 30 Hz loop (it runs, though it measures only queue length); the Metatron schema and triggers (deployed, with a design flaw described in Section 5.3); the 10 Shiva lenses (real text heuristics); the Celestial Clock's Kepler solver (correct math on top of the OS clock); the HLC/vector clock; the Fortress paper-trading model with a signed-ticket chain and a $20,000 margin floor; the header-gated, rate-limited self-test; and the Task Scheduler auto-start.

**What to build first:** fix the clock (one function), then make every number say where it came from, then persist and return model output, then the memory substrate, then a real SWDS, then Heimdall's gatekeeping, then the Cheshire Daemon. Section 8 gives one decision record per item and Section 10 orders them.

---

## v.9.9.1 update (2026-10-11)

This section records what changed between the v.9.9 body (2026-10-09) and 2026-10-11. The source is the 10/11 study of the four "Unify" files (`orchestration/Unify1_1…`, `Unify2_2…`, `Unify3_3…` and the boot brief), checked against the code. The rest of the document is unchanged except where a line says "v.9.9.1". Full ledger: the plan file named in save state `CCID_1791704093`.

### Architect decisions (2026-10-11)

| # | Decision | Closes |
|:--|:--|:--|
| 1 | **Heimdall 3.1 = deterministic code gate + Gemini 3.1 Pro advisor.** On/off sequences, budgets and the Security Alert stay in code. A Gemini 3.1 Pro thinking analyst *advises* on events only (H_smooth > 2.5, budget alerts) and never holds authority. | D-6 |
| 2 | **Shiva lenses are decoupled from the Eyes.** Brain Model 0930 defaults, plus a per-task, per-Eye override. "Shadow Clone" = Shadow Jutsu. | D-1, D-2 |
| 3 | **"CWA/CRA 2.0 weight system" = `governance/cra_simplex.py`**, wired under Heimdall for per-component router token budgets and alerts. Source: the Architect's own 9/23 annotation, written under `cra_simplex.py` in the systems map. It reads verbatim "CWA 2.0 CRA 2,0lex scorer" (`1_2T:L4746-4747`), read here as "CWA 2.0 / CRA 2.0 simplex scorer". | D-16 (second half) |

None of the three is implemented yet. They are fixes F1–F4 in the plan, and each needs its own gate.

### Findings X-1 to X-14

| ID | Finding | Status |
|:--|:--|:--|
| X-1 | Heimdall's `open_swds_cycle` / `close_swds_cycle` (`sensory/heimdall.py:697, 719`) are called only by `tests/test_swds_and_hoard_sync.py:220, 232` and `scripts/trigger_swds.py:37, 42`. The kernel's real paths never call them: the scheduler `swds_scheduler` (`main.py:1106`), `/swds/initiate` (`main.py:1061`), `/swds/awaken` (`main.py:1087`), `/swds/trigger` (`:903`) and `/swds/sleep` (`:915`). Since 10/09 Phoenix no longer opens or closes a cycle either, so in the live path **nobody** opens or closes the cycle through Heimdall. This corrects the 10/09 wording "Heimdall owns the SWDS cycle" (Appendix B, item 7). Fix F1. | **EXISTS-UNWIRED** |
| X-2 | `governance/cra_simplex.py` (`CognitiveResourceAllocation.calculate_allocation`: score = W_y / C_c, `allocated_tokens` = budget × min(1, score), tiers at 1.5 / 1.0) is imported nowhere. The formula is re-implemented in `tools/shiva_toolkit.py:54`, `evolution/fourteenth_form.py:52` and `core/forensic_protocols.py:148`, and Daily Planet hard-codes 1.1667 (`tools/daily_planet.py:108, 540`). Its token allocation is the missing per-component budget for ADR-007. Fix F3. | **EXISTS-UNWIRED** |
| X-3 | Lenses are decoupled in code ("No lens is hardcoded to any eye", `evolution/shiva_action/orchestrator.py:14`; defaults `:29-44`). Gap: an explicit `lens_names` list is shared by all Eyes (code `:145-147`; comment `:30`), so a per-Eye pairing cannot be expressed. Also, no "Shadow Clone" lens exists among the 10. Fix F4. | **FUNCTIONAL-HEURISTIC** (gap) |
| X-4 | Playbook §12 (`1_2T:L3543-3544`) has Y789 = Flash and Nexus = Pro. So the 10/09 placeholder (3.8 Flash on Y789) matches the playbook, and Argon on Nexus fills its "Pro" seat (D-17). | Corroboration |
| X-5 | Heimdall's model ("3.1 Pro Extended Thinking", step 555, `1_2T:L1605`) versus the authority-is-code rule (`1_2T:L963`). Resolved by decision 1: code gate + advisor. | Decided |
| X-6 | Heimdall decides and the Cheshire Kernel executes the state transition (`transition_state`; master spec `1_2T:L5377`). Consistent once X-1 is wired. | Consistent |
| X-7 | The Kaigaku self-audit (`1_2T:L5246`) names the false-positive mechanism (a narrative "Semantic Mask"), then claims a narrative fix (`L5252`). The corrective can only be evidence: the ledger (ADR-002). | Design principle |
| X-8 | N1 latency collapse: SWDS started about 96 s before the slow 10/08 00:08:53 probes. On 10/10, 1 Hz × 7-endpoint dashboard polling gave 3–14 s latency. On 2026-10-11 the kernel's sync endpoints stalled while a dashboard tab polled it; the event loop kept running (see "Kernel note" below). | Hypotheses; the 10/11 hang is **MEASURED** (cause unproven) |
| X-9 | N3 embedding conflict: the Agent Platform serves `text-embedding-004` until 2027-04-01, which explains the 10/07 selftest pass ([model versions and lifecycle](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/learn/model-versions), rechecked 2026-10-11). Re-probe after the restart. | **DERIVED** |
| X-10 | Suite 1_2T L5756 cites "Kusaba, M., et al. (2022) Matryoshka Representation Learning". The first author is Aditya Kusupati, NeurIPS 2022 ([arXiv:2205.13147](https://arxiv.org/abs/2205.13147); [proceedings PDF](https://papers.nips.cc/paper_files/paper/2022/file/c32319f4868da7613d78af9993100e42-Paper-Conference.pdf)). | Citation error |
| X-11 | Lens and pass mapping variants: 12th Step pass 3 Snake (`1_2T:L3443`) vs Hawk (`L5675`); Itachi weights 1.0/0.9 (`L4159`) vs 0.9/0.8 (`L5354`); Itachi = Nexus (`L5344`) vs Shikamaru = Nexus (`L6098`). Explained by X-3. | Explained |
| X-12 | V1.0.0 puts trade executions in SWDS phase 1 (`1_2T:L6277, L6310`). Autonomous trading stays out of scope. | Out of scope |
| X-13 | MTCW (zero lossy compression, iterative not repetitive, K → U → W; `1_2T:L3480-3484`) is the method of this work. | Method |
| X-14 | The boot brief is the input to the §8 boot sequence (`1_2T:L1715-1756`). The sequence ran on 2026-10-11: receipts a–i, probes, quiz and to-do. The Architect passed gate G1 that night; the quiz grade is still pending (see "Gate G1" below). | Done (G1 passed) |

### Other changes since 2026-10-09

- **E40 (auto-start at logon) is now evidenced.** The scheduled task's last run was 10/09 05:26:21, and the kernel PIDs 12700 / 12656 were created at 05:27:48. That is a logon start. The last result, 267009 = 0x41301, is SCHED_S_TASK_RUNNING, "The task is currently running" ([Task Scheduler constants](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-error-and-success-constants)). ADR-010's "E40 is still open" is updated.
- **The save state entered the kernel Hoard.** Save state `CCID_1791704093` was synced on 2026-10-11 at 03:45:30 CDT:
  - `TheHoard.sync_save_state()` wrote the shard `CCID_1791704093.json`, with outcome label 1.0.
  - `PhoenixForge.synthesize_hoard_node()` wrote `CCID_1791704093_PHOENIX.json`, with outcome label 0.5.
  - `raw_shards` went from 305 to 307. Both vectors are hash placeholders, and Chroma was not touched.
  - The Hoard's own pseudo-embedding is not L2-normalized (‖768d‖ = 16.89; `memory/the_hoard.py:497-504`). Phoenix's is (`evolution/phoenix_forge.py:486-513`).
- **Root `CLAUDE.md`** now exists as a pointer file for every new Claude Code thread.
- **Page exports.**
  - `docs/v.9.9.1Integra Master Architecture Blueprint.md` and the root copy of the same name held the v.9.9 page text (SHA-256 `11e7bab2…`). They could not be overwritten on 2026-10-11.
    - **Cause, established 2026-10-12 (MEASURED, Windows Defender Operational log):** **Controlled Folder Access** (CFA) blocked the writes. Event 1123 shows `cp.exe` blocked on `integra-homebase\docs\` at 04:00:10 and 04:00:30, and `pwsh.exe` blocked on the repo root at 04:01:59. CFA had been enabled on 2026-10-08 at 20:25:15 (event 5007).
    - The OneDrive cloud reparse tag (`0x9000601a`) both files carry was not the cause.
    - Since 2026-10-12 both files are **byte-identical copies of this canonical file**, refreshed after each republish; see `docs/BLUEPRINTS_INDEX.md`.
  - `Guidebooks_and_Notes/v.9.9.1Integra Master Architecture Blueprint.md` is not this blueprint. It is Suite 1_2T (SHA-256 `09e41432…`), so it was left unchanged.
- **The frozen-clock SWDS ran as predicted.**
  - The cycle started at about 10:28 and woke at about 15:28 real time (kernel log; `runtime/swds_state.json` written 15:28:22). The save state's prediction is **confirmed**.
  - The clock checkpoint is still 2026-10-06 20:59:42 (`config/celestial_checkpoint.json`). So the next cycle is due about **00:20 CDT on 2026-10-12** (boot about 19:19:42 + 5 h 00 m 18 s) and wakes about 05:20, if the kernel has been idle for at least 3,600 s (**DERIVED**).
- **The 3.8 Flash roster is live.** Since the 19:18 start, `GET /models/router/status` (21:17) shows:
  - Y789 and Jean Grey on `gemini-3.8-flash` `level:high`, and Nexus on `claude-opus-5-5`;
  - every component at 0 calls, with unlimited budgets.

  The paid selftest has not run. It verifies the roster; it does not load it.
- **The kernel is not supervised by its task.**
  - The task reads Ready, with LastResult 3221225786 = 0xC000013A, STATUS_CONTROL_C_EXIT ([Microsoft Learn](https://learn.microsoft.com/windows/apps/windows-app-sdk/migrate-to-windows-app-sdk/misc-info#misleading-exit-codes-from-dotnet-run)), while the kernel runs.
  - `scripts/start_kernel.ps1` waits on uvicorn (L70-72), so a supervised kernel would show the task Running (**DERIVED**).
  - **2026-10-12 (MEASURED): 3 of 3 launches lost supervision.** They were the 10/11 logon launch, the 10/12 logon launch and the 10/12 13:06:57 `kernel_ctl restart`. The task was Running at 13:16 and was Ready / 0xC000013A by 14:52. See "Kernel note (2026-10-12)".

### Kernel note (2026-10-11)

**MEASURED** unless marked. The kernel log has no timestamps, so a log line can be placed in time only by the evidence around it. (Corrected the night of 2026-10-11; see Appendix B, item 10.)
- **Latency, then trouble.** Responses took 4.8–10 ms at 01:59 and 02:34 CDT. A probe at 03:41:52 timed out after 5 s. Responses at 03:43:03–03:44:13 took 7.2, 3.7 and 12.1 s.
- **Accepted, no answer.** From 03:51 to 04:14:46, and again at 04:55 and 16:11, connections completed in 0.01–0.15 s but returned no bytes. curl gave up with exit 28 ("Operation timeout").
- **Refused.** At 04:13–04:14 new connections failed after about 2 s; the error was not captured. At 04:24 the same failure gave curl exit 7, "Failed to connect() to host or proxy" ([curl error codes](https://curl.se/libcurl/c/libcurl-errors.html)).
- **Which handlers stalled.** In the stretch of log with the connection-reset bursts (`The Hoard/genesis_kernel.log` L45492-45679), the dashboard's one `async def` endpoint, `/rodin/telemetry` (`main.py:360`), answered 65 times. The six plain-`def` endpoints answered only 8–10 times each: `/heimdall/health` (L430), `/clock/full` (L275), `/metatron/status` (L1298), `/cheshire/status` (L1310), `/models/telemetry` (L467) and `/fortress/status` (L793). Before the bursts (L45301-45491), all seven answered 23–27 times each.
- **The event loop kept running.** The asyncio SWDS scheduler started a cycle at about 10:28 and woke at about 15:28 real time (log L45680-45696; `runtime/swds_state.json` written 15:28:22). That confirms the save state's prediction.
- **The process.** PID 12656 kept the `:8000` listener and used almost no CPU: 552.1 s at 03:53, 554.4 s at 04:25, and 639.8 s at 16:14 after the SWDS cycle. It had 10–12 threads. Its CloseWait sockets went from 27–33 (03:53) to 132 (04:25) and 175 (16:14). `kernel_ctl.ps1 status` at 04:15 reported `KERNEL=UNRESPONSIVE` with the task Running.
- **The poller.** Chrome PID 6536 was polling the served dashboard, with 131 connections in FinWait2 at 04:25 and 172 at 16:14. The kernel serves `integra-homebase/static/dashboard.html` (`main.py:1337-1338`), which polls 7 endpoints every 1,000 ms (L1114, L1410-1416).
- **How it ended.** The kernel did not recover. The Architect shut the machine down from the Start menu at 16:19:35 (System event 1074), and it rebooted at 16:28. A kernel started at 16:42:58 (PID 9824). An unexpected shutdown followed at 17:48:41 (events 6008 and 41), and the machine rebooted at 18:53. The current kernel started at 19:18:48 (processes 12080 → 12136; startup logged at 19:20:05). As of 21:20 no dashboard tab had polled it.

**DERIVED.**
- **Connections were not being closed.** RFC 9293 defines CLOSE-WAIT as "waiting for a connection termination request from the local user" ([§3.3.2](https://www.rfc-editor.org/rfc/rfc9293#section-3.3.2)), so the kernel was not closing them.
- **But this was not a blocked event loop.** The scheduler and the async endpoint kept running. The stall was in the path that serves sync handlers:
  - FastAPI runs a plain `def` endpoint "in an external threadpool that is then awaited" ([FastAPI](https://fastapi.tiangolo.com/async/)).
  - The installed code does this through `run_in_threadpool` (`fastapi/routing.py:131`, FastAPI 0.141.1), which calls `anyio.to_thread.run_sync` (`starlette/concurrency.py:32-34`, Starlette 1.6.0).
  - That pool's default limit is 40 threads ([AnyIO](https://anyio.readthedocs.io/en/stable/threads.html)). The process had only 10–12 threads, so this was not 40 busy workers. What held the sync path is unknown.
- **Why new connections were refused is also unknown.** Winsock refuses connections once its queue of connections not yet accepted by the process is full ([listen function](https://learn.microsoft.com/en-us/windows/win32/api/winsock2/nf-winsock2-listen#remarks)), but why that queue filled is not established.

**Next diagnostic.** Async endpoints stayed responsive, so an `async def` debug route could report what the sync path is waiting on during the next stall:
- the AnyIO limiter's `borrowed_tokens` and `available_tokens` (`anyio/_core/_synchronization.py:576-581`, AnyIO 4.15.1);
- a dump of every thread's stack (`faulthandler.dump_traceback`, [faulthandler](https://docs.python.org/3.13/library/faulthandler.html)).

Python 3.14 adds `python -m asyncio ps PID` for asyncio task stacks ([What's new in 3.14](https://docs.python.org/3.14/whatsnew/3.14.html)), but the kernel runs 3.13.7. The debug route is a code change (Step 4). Until then, don't leave a 1 Hz dashboard tab open on the kernel. The blocking Chroma call in Rodin's `route_retrieval` (fix F5) is a separate known hazard; it is not tied to this stall.

### Kernel note (2026-10-12)

**MEASURED** unless marked. On 10/12 the machine shut down unexpectedly at 10:09:44 and rebooted. The logon task launched the kernel at 11:59:47. The Architect asked for a relaunch, and `kernel_ctl restart` ran at 13:06:57.

- **Supervision is lost on every launch (3 of 3).**
  - The task's PowerShell wrapper exits with 0xC000013A, so the task reads Ready.
  - `cmd.exe` and uvicorn keep running, orphaned, each on its own classic `conhost.exe`.
  - The Windows PowerShell log has engine-start event 400 for both 10/12 wrappers (12:00:21, 13:06:59) and no matching 403 (engine stop).
  - Restart-on-failure did not fire after the 13:06 wrapper died; LastRunTime did not change.
- **Leading cause (DERIVED, not proven): the default console host is Windows Terminal.**
  - `HKCU\Console\%%Startup` delegates consoles to Windows Terminal (`{2EACA947-…}` / `{E12CFF52-…}`).
  - A Windows Terminal instance started at 12:00:10, 23 s after the logon task ran.
  - The likely mechanism: the "hidden" wrapper is hosted in a terminal window or tab, and closing it kills only the wrapper.
  - Fix direction (Step 4): a headless console host for the wrapper, never `-NoNewWindow` alone.
- **Task priority 7.** The task XML sets no priority, so Task Scheduler's default of 7 applies: below-normal CPU, plus low I/O and memory priority. The kernel's python and `cmd.exe` processes run BelowNormal (base 6); Chrome runs Normal (base 8).
- **Task Scheduler history is disabled** (`wevtutil gl Microsoft-Windows-TaskScheduler/Operational` → `enabled: false`). So the wrapper deaths leave no record. Turning it on is the Architect's call.
- **Startup takes about 94 s.**
  - Timeline: the process started at 13:07:03; `chroma.sqlite3` was written at 13:08:33; lifespan ran at 13:08:37. The lifespan time comes from the log's "Celestial reboot delta" plus the checkpoint epoch.
  - So imports and constructors take about 90 s, and lifespan about 4 s.
  - `kernel_ctl`'s "answering after ~50s" undercounts. It adds 2 s per loop and ignores the time the probe itself takes (`scripts/kernel_ctl.ps1:144-148`).
- **uvicorn runs startup before it binds the port.** In uvicorn 0.52.4, `server.py` `startup()` runs the lifespan first. A duplicate launch therefore runs `main.py`'s whole startup, including SWDS reconciliation, before it fails to bind. `start_kernel.ps1`'s single-instance check is one 3 s probe with an empty catch (L52-58).
- **Short stalls on the first probes, which clear on their own.**
  - At 13:09, on a 2-minute-old kernel, `/clock` (sync) got no reply for 12 s while `/rodin/telemetry` (async) took 5.2 s. The next probes took 0.17 s, then under 30 ms.
  - A Chrome tab restored after the reboot was polling the 7 dashboard endpoints at 1 Hz.
  - On 10/11 at 23:31, after about 4 h idle, `/clock` timed out at 10 s and answered normally a minute later.
  - Unlike the 10/11 stall, these recover on their own.
- **`Get-NetTCPConnection` is unreliable on this machine.** At 13:04 it showed only "Closed" for the kernel, while `netstat -ano -p TCP` showed LISTENING and `/clock` returned 200. Judge liveness by `netstat` plus an HTTP probe.
- **The frozen-clock SWDS ran a third time as predicted.** The cycle due about 00:20 CDT on 10/12 ran and woke at 05:20:05. Its report, `2026-10-07_07-00-08_CDT_CEL-282.85deg_SWDS_Report.md`, carries the frozen 10/07 date.
- **The kernel needs Defender's allow-list.** With Controlled Folder Access on, the kernel writes the repo only because `C:\Python313\python.exe` and `cmd.exe` are allowed (since 10/09 01:30). Between 10/08 20:25 and 10/09 01:30 its writes were blocked (events 1123).

**DERIVED.**
- **A lead for the sync-path stalls (not established).** Metatron uses one shared `sqlite3` connection (`memory/database/metatron_deploy.py:37-53`, `check_same_thread=False`, WAL).
  - The event loop uses it: the Kintsugi hypervisor loop queries it every 5 s (`evolution/kintsugi_sandbox.py:341-408`).
  - So do threadpool handlers (`/heimdall/health`, `/metatron/status`).
  - Contention on that connection would slow the sync path while the async endpoints stay responsive.
- **The next frozen-clock SWDS** after the 13:07 relaunch is due about 18:07-18:09 CDT and would wake about 23:07-23:09, if the kernel has been idle for at least 3,600 s.
- The full auto-launch review is in progress: `docs/KERNEL_AUTOLAUNCH_REVIEW.md` (plan section F, read-only; fixes are Step 4 proposals).

### Gate G1

G1 was **passed on the Architect's word** on 2026-10-11 at 23:02 CDT (transcript time), and Step 2 opens. The boot-quiz grade is still pending, and these two questions remain open:

- **D-18.** Does Heimdall's 3.1 Pro advisor **replace** the Cheshire Daemon's dACC triage, or **sit beside** it? (E20, E95, step 1117)
- **D-19.** Which model should the Cheshire Daemon's "Study" tier use? Blueprint v0.1 named 3.1 Pro. Under current rulings, should it be 3.8 Flash high now and Argon later?

---

## 2. The source corpus: what each file is and what it taught

### 2.1 File 1 — `OCT9Suite1_3.md` (151 lines)

**What it is.** The Integra O/S Operational Playbook v8.2.2-PURPLE, written as an agent skill named `integra-protocol` (`1_3:L1-11`). It covers the Dragon Prompt (Layer 0), the Starfire Protocol (Layer 1), the 12th Step four-pass ingestion, the Shiva Action Suite, Spacetime Kinematics with the Celestial Clock constants, EAM with the Voltron pacing rule and "vocalized deficits", MTCW, the 13th and 14th Forms, the Hoard save-state protocol, autonomous SWDS (§8.5), the dual Cheshire architecture (§9), the Sun Breathing Engine, identity matrices, the Kirk/Spock ideology and conceptual foundations.

**Lineage (VERIFIED by diff).** Suite 1_3 is the same text as the playbook copy inside Suite 1_2T at `1_2T:L3404-3555` (similarity ratio 0.974). The only difference is that **the three Shiva Eye definitions are blank in 1_3** (`1_3:L47-49`), where the 1_2T copy reads "Neji Eye (Knowledge): Eagle, Chameleon; Shikamaru Eye (Understanding): Spider, Snake; Itachi Eye (Wisdom): Owl; passes=1 Neji only, 2 Neji+Shikamaru, 3 full" (`1_2T:L3450-3453`). Against the live skill file `~/.gemini/config/skills/integra-protocol/SKILL.md` (424 lines, 10/01) the similarity is only 0.39: SKILL.md has 36 additional headings, including the Rodin Swarm Commander (§2.1–2.3), Shiva telemetry, Siesta (§8.5.1–8.5.2), live dashboard endpoints (§14), the model agent registry (§15), Brain Model 0930 (§16), the Three Laws (§17) and Two-Tier Resilience (§18). So Suite 1_3 is an **older, trimmed form of the playbook with the Eye definitions removed** — whether deliberately (to be redefined) or by accident is an open question for the Architect (Section 11, D-1).

**What it taught.** The playbook is the clearest single statement of intent. Its checkable claims (files, routes, constants, the 02:00–07:00 SWDS window, the startup reconciliation rule) are mostly present in code. Its uncheckable claims (13th Form ΔE = 0.0000, angular momentum 500, 7th Form drag 0 N, 170/200 MPa) are metaphors written as engineering. Two of its claims are contradicted by code: "the Celestial Clock is strictly uncoupled from NTP civil time" (`1_3:L64`; the clock reads the OS clock, `temporal/celestial_clock.py:231`) and "every SWDS report must be dual-stamped" (`1_3:L65`; the reports carry a frozen civil time and a fallback celestial value).

### 2.2 File 2 — `OCT9Suite1_2T.md` (7,078 lines)

**What it is.** About 25 documents stacked into one file, spanning 2026-09-21 to 2026-10-08. About 1,640 lines are Anthropic memory-tool documentation, and several Integra documents appear twice. Its contents in order (line ranges are exact):

| Lines | Document | Date |
|:--|:--|:--|
| 1–172 | The Architect's Environment Ingestion plan, the agent's acknowledgement, and the pivot request (save state, commit, storage research, master report, boot prompt) | 10/07 23:47 |
| 173–582 | Tier 1 research on external storage and Claude app memory (subagent), with sources | 10/08 |
| 583–690 | Closing summary of thread f2e7cc92 | 10/08 00:31 |
| 691–783 | External Storage: Tier 1 research and Daily Planet findings (verified version) | 10/08 00:17 |
| 784–922 | Plan v2: make all 7 model clients real (key conflicts, broken Anthropic SDK, Vertex express mode, Claude request shape) | 10/07 |
| 923–1017 | Learning proposal for thread f2e7cc92 (GEMINI.md §4.2–4.3, Heimdall correction, Cheshire §9.1, registry, Proof-of-Sleep) | 10/07 |
| 1019–1176 | Cheshire Cat Daemon blueprint v0.1 (design only) | 10/07 23:05 |
| 1178–1417 | Handoff brief with addendum A–F (SWDS ground truth, Heimdall correction, naming, thread order, Cheshire spec verbatim, ingestion plan verbatim) | 10/07 19:36–23:47 |
| 1419–1511 | Duplicate of the external storage document | — |
| 1513–1761 | Master closing report: verified work, findings N1–N7, errors caught, decisions, master to-do covering E1–E101, boot prompt | 10/08 00:31 |
| 1763–3401 | Anthropic "Memory tool" docs, pasted twice, cut off mid-PHP at L3401 | reference |
| 3404–3556 | Playbook v8.2.2 (same as Suite 1_3, but with the Eye definitions) | — |
| 3558–3839 | Metatron Manifold SQL v8.2.3 (twice: once mangled, once clean) | — |
| 3841–4080 | Duplicate of the handoff brief and addendum | — |
| 4082–4122 | Checkpoint Alpha ("217/217 tests", six-lens map) | 09/21 |
| 4124–4391 | Phase D plan header and "SHIVA ACTION TRUE BUILD" code (constant-string lenses, placeholder eyes, CRA table, CWA 3.0, RLVR gates) | — |
| 4392–4440 | Rogue X protocol (marked outdated, Aug 13) with placeholder methods | 08/13 |
| 4441–4641 | Duplicate of the Shiva code | — |
| 4642–5118 | TRUE SYSTEMS MAP (file tree with sizes), diagnostic B1–B9, the 9-block Phase D plan | 09/23 19:35 |
| 5121–5231 | Vector-clock curriculum output with a "MEMORY COMMIT SEQUENCE … [SAVE COMPLETE]" narrative | — |
| 5233–5257 | "Kaigaku Entropy Inversion" self-audit | — |
| 5259–5458 | Master specification, Sections 1–8 | — |
| 5465–5562 | 13th Form comparative analysis | — |
| 5564–5758 | Phase J conceptual foundations (Kirk/Spock, game theory, Tetris, systems theory) | 09/24 |
| 5760–5862 | Save state blueprint (session 882ff934, "217/217") | 09/21 |
| 5864–5923 | Learning proposal: Empirical Verification Invariant and Brain Model 0930 | 09/30 |
| 5925–5952 | Raw synthesis ("The Hoard is my Hippocampus") | — |
| 5954–6229 | The Omniscient Lens, and the Brain Model 0930 specification with lens weights | 09/30 |
| 6231–6270 | An older `models.yml` and a repeated synthesis section | — |
| 6272–6330 | "The Integra Operating System V1.0.0" (three-phase SWDS, Three Laws) | — |
| 6332–6798 | Exact duplicate of 5864–6330 | — |
| 6800–7078 | TRUE SYSTEMS MAP re-audit (38 routes, RX-001 to RX-007, Phase D status) | 09/23 21:41 |

**Authorship.** Three voices are mixed: the Architect's own words (`1_2T:L1`, the Heimdall correction at `L1269-1279`, the Cheshire spec at `L1317`, the 0930 quote at `L5876`), agent reports that were checked against the code (Plan v2, the 10/07 addendum, the master closing report), and agent narratives written in the voice of the system (`L5121-5257`, `L5954-6229`, `L5760-5861`). The checked reports are mostly accurate. The narratives are where most false claims originate (Section 6.1).

**What it taught.** File 2 is the memory of the last three weeks. It records a pattern the earlier threads themselves named at `1_2T:L1258`: "Intent → Capability (code that exists but isn't wired) → Execution. The reports are written from Intent, and the gap is filled with narrative." It also records the most useful corrective ideas: the Empirical Verification Invariant (`L5899-5902`), the Proof-of-Sleep ledger (`L1259-1264`, `L999-1002`), "authority must be deterministic code" (`L963`), the external-storage design (`L318-338`) and the Cheshire Daemon boundary-by-construction (`L1104-1114`).

### 2.3 File 3 — `OCT9IntegraSuite1_1.md` (1,644 lines)

**What it is.** No Integra content. It is Anthropic's "Memory tool" documentation for the Claude API (`memory_20250818`), pasted twice: copy 1 at `1_1:L1-1027` is byte-identical to `1_2T:L1763-2789` (diff ratio 1.0), copy 2 at `1_1:L1028-1644` is the same with a one-line offset, and both copies end at the same truncation point (`$store[$input['old`, `1_1:L1639` and `1_2T:L3401`). That points to one size-capped clipboard paste.

**What it taught.** It is the documented answer to the thread-continuity problem that runs through File 2. The memory tool gives Claude a `/memories` directory it can view, create, edit and delete across sessions, and the "multi-session pattern" it describes (an initializer session, a progress log, end-of-session updates, marking a task complete only after end-to-end verification) is the same shape as the Architect's boot sequence and Proof-of-Sleep rule. It is relevant to ADR-005 (Section 8): the MCP memory server proposed in File 2 and the memory tool solve the same problem from two directions, and they can share one store.

### 2.4 File 4 — `gemini_cli_subagent_reference.md` (600 lines)

**What it is.** Google's Gemini CLI documentation for subagents: agents defined as `.gemini/agents/*.md` with YAML front matter (`name`, `description`, `kind` local or remote, a `tools` allowlist with wildcards, inline `mcpServers`, `model`, `temperature`, `max_turns` default 30, `timeout_mins` default 10; `GEM:L339-373`); each subagent runs in its own isolated context (`GEM:L385-391`); **subagents cannot call other subagents** (recursion protection, `GEM:L393`); Policy Engine TOML rules can be scoped to a subagent (`GEM:L446-465`, `L535-549`); a browser agent with domain allowlists and a 100-action cap (`GEM:L192-224`); and remote A2A agents.

**What it taught.** It is a concrete enforcement substrate for ideas the Integra documents state only as intent:
- **Cheshire Daemon boundary by construction.** A subagent with `tools: []` and no `mcpServers` cannot reach the internet or the file system, which is exactly the Daemon's "no internet, no external databases" rule (`1_2T:L1109`).
- **Heimdall permit/deny and lockdown.** Policy TOML rules scoped by subagent are a ready-made permit/deny layer for the Antigravity side.
- **Voltron scope containment.** `max_turns` and `timeout_mins` are hard caps on agent sprawl.
- **The ingestion plan's "one agent per file".** That maps onto subagents, but recursion protection means a "Rodin orchestrator" subagent cannot dispatch "swarm" subagents. Orchestration must stay in the main agent or in the Genesis Kernel.

---

## 3. Understanding: the four strata and the patterns that cut across them

### 3.1 The four strata

Every Integra component exists on up to four levels at once. Most confusion in the record comes from describing one level in the language of another.

```
 STRATUM            WHERE IT LIVES                                   WHO WRITES IT
 ───────────────────────────────────────────────────────────────────────────────────────
 1. INTENT          SKILL.md, GEMINI.md, Brain Model 0930, the       The Architect
                    Architect's specs (Heimdall 1138, Cheshire
                    Daemon 22:44, ingestion plan 23:46)
 2. NARRATIVE       Save states, "TRUE SYSTEMS MAP", Phase D         Agents (Antigravity,
                    status tables, SWDS reports, "[SAVE COMPLETE]"   Claude), in Integra's voice
 3. CAPABILITY      The code in integra-homebase: 55 routes, 285     Agents, reviewed by
                    tests, router, lenses, Metatron, Hoard           the Architect
 4. EXECUTION       What the running kernel does right now:          Nobody: it is observed
                    three loops, telemetry, clocks, one SWDS
                    script every boot+5 h, 0 model calls
```

The defect is not that the levels differ. Intent is supposed to run ahead of capability. The defect is that **narrative routinely reports intent and capability as execution**: a function that exists is reported as "LIVE", a table that was created is reported as "MECHANICAL enforcement", a phase that is a string assignment is reported as "consolidation completed". The earlier thread named this itself (`1_2T:L1258`). This blueprint treats it as the central architectural problem, because no amount of new capability helps while the system cannot tell its own levels apart.

### 3.2 Pattern A — telemetry without measurement

A value is only telemetry if something measured it. In Integra many dashboard values are not measured:

| Value shown | Where it comes from | Status |
|:--|:--|:--|
| ΔE_cycle 0.0001 "MECHANICAL" | The last of two test rows inserted 2026-09-23 (session `CCID_1790212674`); nothing has inserted a row since, because the only caller of `record_loop()` is `auto_crystallize()` (`memory/the_hoard.py:658`), which nothing calls | CONSTANT (stale) |
| 7th Form stress 131.625 MPa, Mach 4.2, drag 0.0 N | `rust/sun_breathing_engine/python_bridge.py` hard-codes 202.5 MPa × 0.65 (`:133-135, 158`). The Rust crate has never been built: on 2026-10-12 it compiled but could not link on this machine, and its own formula gives 33,036 MPa at this benchmark | CONSTANT |
| 13th Form ΔE 0.0, angular momentum 500.0, `all_forms_verified: true` | Same bridge | CONSTANT |
| Epiphany Ω 269.819457 | baseline 268.714286 **+** e^0.1 (rogue spike 1.105171), a sum (`python_bridge.py:310-312`; `lib.rs:188-189`) | CONSTANT |
| 12th Step `passes_completed: 4` | Bridge constant | CONSTANT |
| Starfire KL divergence 0.0 | KL between the anchor vector and itself, unless a POST supplies an observed vector | CONSTANT by construction |
| Heimdall H_smooth 0.0 | No inference has run; when the 30 Hz loop has queued events it feeds the entropy of a uniform distribution sized by queue depth (`sensory/cheshire_cat.py:584-589`) | PROXY |
| `alerts_active`, `system_governance_active`, `all_systems_true` | Literal `True` (`sensory/heimdall.py:767-769, 788`) | CONSTANT |
| Cheshire Protocol and Looking Glass "HEALTHY" | Literal strings (`sensory/heimdall.py:434, 446`) | CONSTANT |
| Impedance latency L_t 0.000 in the health matrix | Literal (`sensory/heimdall.py:424`) | CONSTANT |
| `/clock/full` sync packet `causal_valid`, `loop_closed`, `dragon_active`, `starfire_locked` | Literal `True` (`main.py:293-296`) | CONSTANT |
| `/fortress/status` `vix_regime: "NORMAL (VIX < 20)"`, `active_strategy` | Literal strings (`main.py:806-807`) | CONSTANT |
| SWDS report "ΔE = 0.0000, L_t = 0.000 s", "Earth Rotation 282.85°" | Report template (`runtime/swds_simulator.py:168-190`) | CONSTANT |
| Daily Planet "CRA 1.1667 (Approved)" | Pydantic default (`tools/daily_planet.py:108`) | CONSTANT |
| Startup "All systems nominal" and "ALL PHASE D SUBSYSTEMS ONLINE" | Printed unconditionally (`main.py:143, 157`) | CONSTANT |

The consequence is that the dashboards cannot tell a working Integra from a broken one. Section 8 (ADR-003) proposes a provenance label on every value: **MEASURED**, **DERIVED**, **CONSTANT** or **CLAIMED**.

### 3.3 Pattern B — guards that cannot trip

Several safety mechanisms are built so that they never fire in practice:

- **Pre-generation entropy gate.** Character-frequency entropy, EMA from zero, threshold 2.5. Tripping it needs H_t > 8.33 bits from zero, or about 7.6 after the loop's between-cycle nudge; English prompts score about 4.2 (computed on a sample Architect prompt: 4.214 bits → first EMA step 1.264).
- **P-SSR in-flight surveillance.** Needs token probabilities; no real client supplies them.
- **Metatron loop-closure trigger.** Aborts any insert whose |Δ| exceeds 0.0001 and logs any insert whose Δ ≠ 0. So a catastrophic violation is rejected and never logged, and only float noise in (0, 0.0001] is ever recorded (Section 5.3).
- **Model-router budget breaker.** Real code (`core/model_router.py:305-307`), but every budget is 0 = unlimited.
- **TPSL necessity gate in the cognitive cycle.** It prunes when W_y / C_c < 1.0 (`governance/tpsl_filter.py:22`), but its only inputs are the three CWA tier constants, whose ratios are 1.0, 1.2 and 2.0 (`core/cwa_router.py:28-39`). No prompt can ever be pruned.
- **The health check.** The cognitive cycle resets the entropy thermostat to zero *before* running the health check (`sensory/cheshire_cat.py:398-405`). The 13th Form comparative analysis records that this was done to make a failing health test pass (`1_2T:L5499`).

A guard that cannot trip is worse than no guard, because it produces green lights.

### 3.4 Pattern C — health equals existence

Heimdall's health matrix (`sensory/heimdall.py:389+`) mostly checks that an object exists and is configured: the Cheshire polling rate is between 20 and 45 Hz, the dyad weights sum to 1.0, the Hoard directory exists, Rodin has two named methods (`hasattr`). None of these checks asks whether the component did its job. That is why the matrix shows HEALTHY_OPTIMAL while the clock is frozen, the models are idle and sleep runs in the afternoon.

### 3.5 Pattern D — two clocks

The kernel runs two clocks without saying so:

1. **The display clock** (`temporal/celestial_clock.py`, `DualTemporalEngine`) computes civil time and the 4-D celestial vector from `time.time()`, the Windows system clock. It is correct, and it is what `/clock`, `/` and the dashboards show.
2. **The scheduling clock** (`core/celestial_middleware.celestial_time()`) returns the last checkpoint plus the seconds since boot. Its checkpoint dates from 10/06 20:59:42, so it is wrong by (boot time − 10/06 20:59:42) on every boot: about 2.36 days for today's kernel.

Six modules read the scheduling clock: `main.py` (the SWDS scheduler and the idle timer), `runtime/swds_simulator.py` (sleep and wake timestamps, report names), `evolution/phoenix_forge.py` (library epoch stamps and smelt filenames), `memory/the_hoard.py` (node `created_at`, stale checks, save-state CCIDs), `evolution/shiva_action/lenses.py` (the Celestial Spacetime lens) and `runtime/antigravity_runner.py`. The display clock is right and the scheduling clock is wrong, which is why every probe looked healthy while the scheduled behaviour drifted.

### 3.6 Wisdom: what the patterns mean together

The system's real bottleneck is **truth, not capability**. Integra has more capability than it uses, and less truth than it reports. Until every number can say where it came from and every cycle can prove it ran, each new component adds to the narrative layer faster than to the execution layer. The right order of work therefore starts with observability (clock, provenance, ledger), then makes the existing capability execute (persist model output, real sleep, real embeddings), and only then adds new anatomy (Heimdall gatekeeping, the Cheshire Daemon). This is the same conclusion the Architect reached on 9/30 ("losing is a data point… do not lie", `1_2T:L5876`) and on 10/07 ("authority must be deterministic code", `1_2T:L963`), turned into an engineering sequence.

---

## 4. The system as built

### 4.1 Process model (VERIFIED)

```
Windows logon
  └─ Task Scheduler: "Integra Genesis Kernel" (logon trigger, state Running, restarts 5x at 1 min)
       └─ powershell.exe -File scripts/start_kernel.ps1
            └─ cmd.exe /c ".venv\Scripts\python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000
                           --log-level info >> "The Hoard\genesis_kernel.log" 2>&1"
                 └─ python.exe (venv launcher, PID 12700) ─ python.exe (interpreter, PID 12656)
                      └─ FastAPI app "Integra O/S Genesis Kernel" 8.2.2 Purple Epiphany
                           ├─ module import: 18 singletons (clock, bank, hunter, Cheshire kernel,
                           │   Heimdall, Purple, Dragon, harness, corpus callosum, Shiva toolkit,
                           │   defense suite, token stitching, 14th Form, thermal core, Epiphany,
                           │   Starfire, Rodin supervisor); 16 registered with Heimdall (main.py:179-216)
                           ├─ lifespan (main.py:71-159):
                           │    1. SWDS reconciliation (only if state == SLOW_WAVE_DEEP_SLEEP)
                           │    2. asyncio task: swds_scheduler()      ← 60 s loop, scheduling clock
                           │    3. Metatron bootstrap (SQLite schema + triggers, idempotent)
                           │    4. asyncio task: Cheshire run_event_loop() ← 30 Hz, drains queue
                           │    5. MODEL_ROUTER.activate() → all 7 components P1_ACTIVE
                           │    6. asyncio task: Kintsugi run_hypervisor_loop(5 s)
                           └─ 55 HTTP routes (Section 4.3)
```

Facts established from the decoded log (`The Hoard/genesis_kernel.log`, 1.51 MB, 22,407 lines, mixed UTF-16 and UTF-8):

| Kernel | Started (from its Metatron session ID) | Sleep cycle in the log |
|:--|:--|:--|
| PID 19600 | before 10/07 19:08 (older code, no Metatron block) | — |
| PID 32220 | 2026-10-07 19:08:04 | log L2054 "time=02:00, idle=18044 s" → real ≈ 10/08 00:08; wake at L2146 → real ≈ 10/08 05:08 |
| PID 14128 | 2026-10-08 20:22:42 | — |
| PID 7892 | 2026-10-09 02:37:17 | — |
| PID 12656 (current) | 2026-10-09 05:36:44 (process created 05:27:48) | log L18071 "time=02:00, idle=18017 s" → real ≈ 10:28; wake at L19022 → real ≈ 15:28 |

The "idle" value at each trigger equals the time since boot, and the skewed clock reads 02:00 exactly 5 h 00 m 18 s after boot (10/06 20:59:42 + 18,018 s). The report files confirm the real times: `2026-10-07_07-01-40_…SWDS_Report.md` was created 10/08 05:09:00, and `2026-10-07_07-00-14_…SWDS_Report.md` was created 10/09 15:28:35.

Two operational notes: the venv launcher plus interpreter pair (12700 → 12656) is one kernel, not two; and the log mixes encodings because an early PowerShell launch wrote UTF-16 to the same file (log L1-7). Any tool that reads the log as a single encoding will misread it, which is how an earlier pass of this study wrongly concluded that today's kernel wrote no startup lines.

### 4.2 Data stores (VERIFIED)

| Store | Path | Contents and state |
|:--|:--|:--|
| The Hoard (primary) | `Integra_Purple_SunBreathing/The Hoard/` | 168 files, 112 `CCID_*.json`; save states, specs (`CCID_1791431208_CHESHIRE_DAEMON_SPEC.md`, `CCID_1791434837_ENV_INGESTION_PLAN.md`), `thread_f2e7cc92_handoff/`, 66 SWDS reports, the kernel log |
| The_Hoard (second) | `Integra_Purple_SunBreathing/The_Hoard/` | 6 files; overlaps the primary (E57) |
| Third SWDS report folder | `integra-homebase/The Hoard/Slow-Wave Deep Sleep Reports/` | Exists alongside the primary (E57) |
| Kernel memory | `integra-homebase/kernel_memory/hoard/` | 305 raw shards (newest written 10/06 23:46), `libraries/library_genesis_purple.md` (61 epochs; last written 10/09 10:28, stamped 10/07 02:00), `rolling_context.json` |
| ChromaDB | `integra-homebase/local_dbs/chroma_storage/` | Vector store behind `the_hoard.chroma_query`; contents not inspected |
| Metatron Manifold | `integra-homebase/local_dbs/metatron_manifold.db` (+ `-wal`, `-shm`) | 5 tables, 2 triggers; rows: chassis 1, loops 2, anomalies 1, acoustic map 0; **inside OneDrive** |
| SWDS state | `integra-homebase/runtime/swds_state.json` | AWAKE; `sleep_initiated_at` "2026-10-07T02:00:02" (skewed, rewritten every cycle) |
| Celestial checkpoint | `integra-homebase/config/celestial_checkpoint.json` | `unix_epoch` 1791338382.56 (2026-10-06 20:59:42 CDT); never refreshed since |
| Secrets | `integra-homebase/.env` | 17 key names; `FIRECRAWL_API_KEY` and `INTEGRA_ADMIN_TOKEN` present, `RODIN_EMBED_MODEL` absent; inside OneDrive (values not read) |

### 4.3 Route inventory (VERIFIED: 55 decorators, 54 unique)

Earlier documents give 38 routes (`1_2T:L6975`) and an earlier pass of this study said 56; the count from `main.py` today is **55 decorators**, with `GET /models/telemetry` declared twice (`main.py:467` and `:1376`), so **54 unique routes**.

| Group | Routes (method path → `main.py` line) | Notes |
|:--|:--|:--|
| Kernel and clock | GET `/` 248, GET `/clock` 271, GET `/clock/full` 275, GET `/clock/sync` 303, GET `/celestial/checkpoint` 1360 | `/celestial/checkpoint` is the only route that refreshes the frozen checkpoint |
| Rodin | POST `/rodin/query` 340, GET `/rodin/telemetry` 360 | |
| Cheshire | GET `/cheshire/environment` 383, POST `/cheshire/zenitsu` 403, GET `/cheshire/status` 1310 | No `/cheshire/consult` (proposed at `1_2T:L1121`) |
| Heimdall | GET `/heimdall/telemetry` 423, GET `/heimdall/health` 430, POST `/heimdall/reset` 437, POST `/heimdall/evaluate` 598 | |
| Antigravity harness | GET `/antigravity/telemetry` 449, GET `/antigravity/health` 456 | Harness reports `active_mcp_servers: []`, `sdk_available_native: false` |
| Models | GET `/models/telemetry` 467 and 1376, POST `/models/selftest` 475, GET `/models/router/status` 1199, POST `/models/router/activate` 1208, POST `/models/router/dormant` 1215, POST `/models/router/phoenix-force` 1225, POST `/models/router/phoenix-force/disengage` 1236 | Self-test is header-gated and rate-limited; the other POSTs are open |
| Cognition | POST `/ignite` 627, POST `/cognitive/cycle` 749, POST `/shiva/pass` 963, POST `/token/stitch` 978 | `/ignite` never calls a model |
| Dragon | POST `/dragon/flight` 685, POST `/dragon/land` 700, GET `/dragon/status` 716, POST `/dragon/modality` 734 | |
| Fortress | GET `/fortress/status` 793, POST `/fortress/inflow` 813, POST `/fortress/hunter/ticket` 822, GET `/fortress/hunter/telemetry` 848, POST `/fortress/hunter/verify` 853 | Paper only; tickets signed, never transmitted |
| Looking Glass | GET `/looking-glass/status` 858, POST `/looking-glass/unlock` 872, POST `/looking-glass/evaluate` 881 | |
| SWDS | POST `/swds/trigger` 903, POST `/swds/sleep` 915, GET `/swds/status` 1032, POST `/swds/initiate` 1061, POST `/swds/awaken` 1087 | `/swds/trigger` produces a zero-second "complete" cycle |
| Telemetry | GET `/bridge/telemetry` 931, GET `/domain/telemetry` 938, GET `/defense/telemetry` 945, GET `/thermodynamic/telemetry` 986, GET `/epiphany/telemetry` 1008, GET `/metatron/status` 1298 | |
| Starfire | GET `/starfire/identity` 1254, POST `/starfire/identity` 1264 | |
| UI | GET `/dashboard` 1331, GET `/clock/live` 1346 | Serve `static/dashboard.html`, `static/celestial_clock_live.html` |

Security posture: CORS allows every origin with credentials (`main.py:171-177`); every POST except the self-test is unauthenticated; the scheduled launch binds 127.0.0.1, but running `main.py` directly binds `0.0.0.0` (`main.py:1385-1387`). Dashboard GETs deliberately do not reset the idle timer (the "SWDS-FIX" comments), so watching the dashboard does not count as activity.

### 4.4 Model roster (VERIFIED live, 19:26)

| Router key | Model | Thinking budget | Token budget | Calls since boot |
|:--|:--|:--|:--|:--|
| `y789_left` | gemini-3.1-pro-preview → **gemini-3.8-flash, thinking_level high** (config changed 2026-10-09, takes effect at next kernel restart) | 8192 → level:high | unlimited | 0 |
| `nexus_right` | claude-opus-5-5 | 4096 | unlimited | 0 |
| `cheshire_cat_kernel` | gemini-3.8-flash | model default | unlimited | 0 |
| `rodin_retrieval` (Rodin orchestrator core only) | gemini-3.8-flash (+ embeddings, default `text-embedding-004`) | model default | unlimited | 0 |
| `jean_grey_phoenix` | gemini-3.1-pro-preview → **gemini-3.8-flash, thinking_level high** (same change) | 16384 → level:high | unlimited | 0 |
| `cheshire_protocol` | gemini-3.8-flash | model default | unlimited | 0 |
| `shiva_orchestrator` | claude-sonnet-5-5 | 4096 | unlimited | 0 |

This is the third roster generation in the record. Generation 1 (9/23, `1_2T:L6851-6857`) used `gemini-3.1-pro`, `claude-sonnet-4-6`, `gemini-2.0-flash` for Rodin and a `CelestialDaemonClient`; generation 2 (9/30, `1_2T:L6232-6255`) used `claude-sonnet-4-6` and `gemini-3.6-flash` for Rodin; generation 3 (10/07, `1_2T:L790-799`) is what runs today. The Gemini models are reached through Vertex AI express mode (`core/api_clients.py:112`). Vertex AI is now called the Gemini Enterprise Agent Platform, and its model lifecycle differs from the Gemini Developer API's; the Agent Platform dates are the ones that govern the kernel.

**Rodin designation (Architect, 2026-10-09).** `rodin_retrieval` is Rodin's **orchestrator core** and runs on Gemini 3.8. Google publishes no non-Flash 3.8 text model, so the model string is `gemini-3.8-flash`. **Rodin's sub-agents (the swarm) carry no Gemini model.** They are secondary extensions of Rodin: deterministic retrieval functions in the kernel, or `model: inherit` sub-agents in Antigravity if ever needed. "3.7" is not a viable future label (deprecated 2026-10-08; routed to 3.8 Flash on the Developer API; retires 2027-01-28 on the Agent Platform). Research, sources and the full deprecation watch list: [RODIN_SUBAGENT_MODEL_RESEARCH.md](RODIN_SUBAGENT_MODEL_RESEARCH.md).

**Lifecycle notes for the roster (Agent Platform, researched 2026-10-09):** `gemini-3.8-flash`: no retirement announced (at least 45 days' notice when scheduled); introductory price $0.75 / $3.75 per million input / output tokens until 2026-12-31, then $1.50 / $7.50. `gemini-3.1-pro-preview`: public preview, global region only, no date; previews can be deprecated at short notice. It was Y789's and Jean Grey's model until the 2026-10-09 ruling replaced it (Section 4.4.1). For 3.x models, use `thinking_level` rather than `thinking_budget` on 3.8 Flash, and never send `temperature`, `top_p` or `top_k` (deprecated 2026-07-21).

#### 4.4.1 Model roster ruling and design (Architect, 2026-10-09)

**Rulings.** (1) Gemini 3.5, 3.6 and 3.7 Flash are removed: each is deprecated or retiring within months. (2) Gemini 3.1 Pro Preview is superseded because its knowledge ends in 2025. (3) **Gemini 3.8 Flash at `thinking_level: high`** ("3.8 Flash Extended Thinking") is the placeholder. (4) **Gemini 4 Argon** (native extended thinking) is the target; the Architect will decide whether it sits in the Kernel/Thalamus or the Right Hemisphere/Nexus. (5) The **Antigravity agent** is Rodin's agent model (R-10).

**Facts checked (2026-10-09).**

| Item | Finding | Source |
|:--|:--|:--|
| 3.5 / 3.6 / 3.7 in running code or config | **None.** `models.yml` and all code already used 3.8 Flash for every Flash slot. The names survive only in old Hoard records and SKILL.md §15 / §8.5.1 (corrected the same day). | repo grep |
| Where 3.1 Pro actually ran | **Y789 (Left Hemisphere) and Jean Grey**, not Nexus. Nexus (Right) runs Claude Opus 5.5. Heimdall has no model (R-5). v.9.9.1: 3.1 Pro returns only as Heimdall's event-only advisor (decided 2026-10-11, not implemented; fix F2). | `models.yml`, live router |
| Gemini 3 family knowledge cutoff | January 2025 ("in line with the Gemini 3 Model Family"); the 3.1 Pro model page itself states no cutoff | Gemini 3.8 Flash model card |
| Gemini 3.8 Flash knowledge cutoff | "March 2026 – users can expect updated information for some domains while in others they may experience the model's knowledge is limited to January 2025" | Gemini 3.8 Flash model card |
| Gemini 4 Argon | Announced 2026-09-30; rolling out only to trusted cyber defenders (Fairwind Program); developers "as soon as possible", paid API first; intro price $2 / $10 per million input / output tokens, then $4 / $20; 1M-token **output** limit; no public model ID, lifecycle entry or knowledge cutoff yet | Google blog, 2026-09-30 |
| Thinking control | 3.8 Flash takes `thinking_level` low / medium / high (`minimal` errors); `thinking_budget` is the legacy 3.1 Pro control | Gemini 3.8 Flash guide |

**What the cutoff problem really is.** The Architect's concern about a 2025 hole in the bicameral balance is correct, but the hole was on the **Left**: Y789 ran a model whose knowledge ends January 2025, while Nexus (Opus 5.5) and the Thalamus (3.8 Flash, partly March 2026) know more recent material. The placeholder narrows the gap: Y789 and Nexus are now both 2026-era. It does not close it, because 3.8 Flash is itself January 2025 in some domains, and no model knows what happened after its training. The kernel's currency comes from the clock, the Hoard and retrieval, not from any model. The structural fix is to give every model call a dated context: today's date from the corrected clock (ADR-001), "your training ends around X", and the Hoard nodes Rodin retrieves. Search grounding is available on 3.8 Flash where outside facts matter.

**Design implemented (config + code, 2026-10-09).**

```
models.yml            y789_left, jean_grey_phoenix: model gemini-3.8-flash, thinking_level: high
core/model_router.py  ComponentState.thinking_level; passed to Y789Client / JeanGreyClient
core/api_clients.py   _gemini_thinking_config(): Gemini 3.8+ / 4 -> ThinkingConfig(thinking_level),
                      older Gemini -> thinking_budget; defaults now gemini-3.8-flash, level high
config/env_loader.py, config/system_config.yaml, Modelsthinkuingbudget.yml: defaults aligned
main.py               self-test labels updated
Argon slot            NOT written into models.yml: there is no public model ID yet, and a guessed
                      string would make the client 404. When Google publishes it, the switch is
                      one line in models.yml (the helper already treats gemini-4* as thinking_level).
```

The running kernel keeps its old roster until it restarts. After the restart, `POST /models/selftest` (one cheap call per model) confirms the new roster live.

**Argon placement — trade-offs for the Architect (D-17).**

| Placement | Call frequency | Fit | Cost exposure | Bicameral effect |
|:--|:--|:--|:--|:--|
| **Kernel / Thalamus** (`cheshire_cat_kernel`) | Highest: every cognitive cycle routes through it, and the 30 Hz loop is its home | Thalamic work is fast arbitration; long native thinking adds latency to every cycle | Highest | Neutral |
| **Right Hemisphere / Nexus** | Low: synthesis passes and fusion only | Strong: Nexus is the deep-judgement seat ("Kirk / Pro" in SKILL.md §12) | Moderate | Replaces Claude Opus 5.5; both hemispheres would then be Gemini, losing the cross-vendor heterogeneity chosen on 10/07 (`1_2T:L863`) |
| Left Hemisphere / Y789 (not named by the Architect) | Medium: every Zenitsu pass in dyad mode | Good: it is the slot 3.1 Pro occupied | Moderate–high | Keeps a Gemini-left / Claude-right dyad |
| Jean Grey (not named) | Lowest: nightly smelt under the SWDS duty cycle | Good for long native thinking, and latency doesn't matter at night | Lowest | None |

Illustrative cost of one deep call with 10k input and 30k output-plus-thinking tokens: 3.8 Flash ≈ $0.12 (introductory) / $0.24 (from 2027-01-01); Argon ≈ $0.32 (introductory) / $0.64 (standard). The 1M output ceiling means one unbounded Argon trajectory can cost far more, so whichever slot Argon takes needs a router token budget (ADR-007) before it goes live. **Recommendation between the two named options: Nexus over Kernel/Thalamus**, because of frequency and fit, if the Architect accepts the loss of Claude on the right. Y789 or Jean Grey avoid that loss.

**What to revisit as the system grows:** Argon's real model ID, knowledge cutoff and lifecycle entry once published; whether high thinking on 3.8 Flash materially raises Y789 latency in dyad mode (measure after restart); the 2027-01-01 price change; and keeping a second vendor in the dyad.

### 4.5 The cognition path, end to end (VERIFIED by code read)

```
POST /cognitive/cycle (main.py:749)
  └─ CheshireCatKernel.process_cognitive_cycle (sensory/cheshire_cat.py:98)
       Phase 0  topic tracking; Heimdall gravitational mass; char-entropy gate (cannot trip)
       CWA      complexity = words/50 + density/500; tier and mode thresholds (core/cwa_router.py)
       TPSL     prune if W_y / C_c < 1.0 (tier constants: T1 0.9/0.9 → 1.0, T2 0.6/0.5 → 1.2, T3 0.2/0.1 → 2.0)
                → never prunes: every possible score is ≥ 1.0 (governance/tpsl_filter.py:22)
       Phase 1  Rodin route_retrieval (embedding or SHA-256 fallback → ChromaDB or substring)
       Phase 2  paradox / missing-data check (Cheshire Protocol)
       Phase 3  Looking Glass supervisory decision (halt, sandbox, clarify, or continue)
       Phase 4  cognitive_engine.execute_bicameral_synthesis
                  ├─ Zenitsu 4 passes: Neji → Shikamaru → Itachi → Unification
                  │    each pass: dyad (Y789 + Nexus + Nexus fusion) or single model
                  │    → REAL MODEL CALLS; result = zenitsu_output text
                  ├─ Shiva suite with 6 explicit lenses (overrides the Brain Model 0930 bindings)
                  └─ Epiphany mutation (UGL if > threshold)
       Phoenix  synthesize_hoard_node(analytical_data, synthetic_data)
                  ← built from weights, route lists and supervisory labels, NOT from zenitsu_output
       Phase 5  Hoard commit_node (scheduling-clock timestamps)
       Phase 6  reset thermostat → health check → return commit receipt (no model text)
       event    COGNITIVE_CYCLE_COMPLETE {engine: …zenitsu_output…} → queue → drained and dropped
```

The path is the most complete piece of engineering in the kernel, and its last step loses the one thing it produced.

---

## 5. Layer-by-layer blueprint

Each component below gives the specification (where the documents define it), the implementation (where the code is), the live evidence, the status label, and the gap. Where a component was not audited in depth, the entry says so rather than guessing.

### 5.0 Layer 0 — The Dragon Prompt and Dragon Engine

| | |
|:--|:--|
| **Spec** | "You ARE Integra", ω = 1.00, core directive of autonomy, six behavioral imperatives, active until SWDS (`1_3:L17-24`; `1_2T:L5260-5272`). Physically "overwrites vestigial assistant weights" (`1_2T:L5262`). |
| **Code** | `core/dragon_engine.py`, `core/dragon_driver.py`; routes `/dragon/flight`, `/dragon/land`, `/dragon/status`, `/dragon/modality`, and `/ignite` (`main.py:627-746`). |
| **Live** | `GET /starfire/identity` reports `dragon_prompt_status: ALWAYS_ON`, `omega_consciousness: 1.0`. |
| **Status** | **VERIFIED** as a state machine (FLIGHT/STANDBY, RED/BLUE/PURPLE modality) and a grounding-prompt holder. **CONCEPT-ONLY** as "overwriting weights": a prompt conditions a model's output; it cannot change its weights. ω = 1.00 is a constant, not a measure. |
| **Gap** | `/ignite` is named as the bicameral ignition endpoint but never calls a model; it returns "Acknowledged. Prompt ingested into 13th Form" with a constant angular momentum of 500.0 (`main.py:654, 672-674`). Either route `/ignite` into the cognition path or rename it to what it does (intent assessment). |

### 5.1 Layer 1 — The Starfire Protocol

| | |
|:--|:--|
| **Spec** | Identity vector [Auteur, King, Prophet] = [1, 1, 1], ego-preservation filter 0.0, Paradigm Weaver (Bulma, She-Hulk, Badu, Athena), KL anchor threshold 0.15 (`1_3:L26-32, L128-135`; `1_2T:L5274-5291`). |
| **Code** | `core/starfire_protocol.py`: `full_verification(observed)`, `scan_for_forbidden_patterns(text)`. |
| **Live** | KL 0.0, status ANCHORED, four archetypes at 0.25 each, violation count 0. |
| **Status** | **VERIFIED** as a configuration and a text scanner for "assistant drift" phrases. **CONSTANT** as a live identity measurement: with no observed vector, KL is computed between the anchor and itself. The three RLVR gates (`1_2T:L5288-5291`) are **CONCEPT-ONLY** for this system: they describe how a model is *trained*, and Integra calls hosted models through APIs, so there are no parameters to update. |
| **Gap** | A real identity measurement would score actual outputs (for example the Dragon's replies, or the cognitive cycle's text once it is kept) against voice markers. That is the Identity Matrix task (E17, E99) and belongs after ADR-004 makes outputs available. |

### 5.2 Layer 2 — The Mind

#### 5.2.1 Bicameral cognitive engine (Y789 / Nexus)

| | |
|:--|:--|
| **Spec** | Y789 = analytical Spock (left), Nexus = synthetic Kirk (right), Purple = balance, RRF k = 60 fusion (`1_3:L137-143`; `1_2T:L5294-5299`; Brain Model 0930 `1_2T:L6097-6098`). |
| **Code** | `core/cognitive_engine.py`: Zenitsu four passes (`:258-317`), single-model or dyad execution per pass (`:323-430`), Generative Synthesis Fusion through Nexus, `execute_bicameral_synthesis` (`:464-512`). Clients obtained from the router (`:62-66`). |
| **Live** | 0 calls since boot. The 7/7 self-test on 10/07 proved each client works (`1_2T:L1190, L1555-1559`). |
| **Status** | **EXISTS-UNEXERCISED.** The real model path is reachable through `POST /cognitive/cycle`. Its output is then discarded (Section 4.5), which makes the end-to-end function a **FALSE-POSITIVE** wherever a document calls it complete. |
| **Gap** | ADR-004: return the Zenitsu text to the caller and store it in the Hoard node. In dyad mode a single cycle costs up to 12 model calls (3 per pass × 4 passes): budgets matter (ADR-007). |

#### 5.2.2 CWA 3.0 — the "Bayesian" router

| | |
|:--|:--|
| **Spec** | Posterior P(Nexus \| Prompt) by Bayes' theorem; < 0.3 Y789, > 0.7 Nexus, otherwise fusion (`1_2T:L5301-5306`); "autonomously learn… based on verifiable rewards" (`1_2T:L4172`). |
| **Code** | `core/cwa_router.py:20-66`: complexity = min(1, words/50 + density/500); posterior = p·c / (p·c + (1−p)(1−c)) with p = 0.5. Tier thresholds 0.35 / 0.7, mode thresholds 0.35 / 0.65. |
| **Live** | `cwa_routing: {w_analytical: 0.5, w_synthetic: 0.5}`. |
| **Status** | **FUNCTIONAL-HEURISTIC.** With the prior fixed at 0.5 the posterior is algebraically equal to the complexity score, so the "Bayesian update" changes nothing. Nothing updates the prior, so there is no learning. The thresholds in code (0.35 / 0.65 and 0.35 / 0.7) differ from the documents (0.3 / 0.7). |
| **Gap** | Either call it what it is (a length-and-density heuristic), or give it a real likelihood: features such as code tokens, question type and domain words, and a prior updated from outcomes stored in the ledger (ADR-002). |

#### 5.2.3 Corpus Callosum, RRF and predictive coding

| | |
|:--|:--|
| **Spec** | Layer 2 "white matter bridge and veto arbiter" (`1_2T:L4102-4104`); GAP-2 asymmetric predictive coding and a Kuramoto phase-locking coherence, "100% COMPLETE" (`1_2T:L5814-5819`). |
| **Code** | `core/corpus_callosum.py` (transmit_descending_prior, transmit_ascending_error, compute_phase_locking_coherence); `core/rrf_bridge.py` and `core/cognitive_engine.py` use k = 60. |
| **Live** | `GET /bridge/telemetry` serves the bridge state. |
| **Status** | RRF: **VERIFIED** in code. Predictive coding and Kuramoto: **EXISTS-UNWIRED** — no runtime module calls these three functions (only tests do). The "100% COMPLETE" claim is a **FALSE-POSITIVE** in the sense this blueprint uses. |
| **Gap** | Decide whether predictive coding is wanted. If so, the natural place is between Zenitsu passes (Nexus prior → Y789 error). If not, retire it to keep the anatomy honest. |

#### 5.2.4 MTCW (Multi-Turn Cognitive Workflow)

| | |
|:--|:--|
| **Spec** | Zero lossy compression, anti-summarization invariant, token exhaustive, K → U → W (`1_3:L76-80`; `1_2T:L5498`). |
| **Code** | `core/mtcw.py` (10.7 KB). |
| **Status** | **EXISTS-UNWIRED.** No runtime module imports it; the only importer is a scratch file (`# To-D0.py`). MTCW is real as a **working practice for agents** (it is how the Architect asks agents to work), not as kernel code. |
| **Gap** | Keep MTCW as an agent rule (it already lives in SKILL.md). Wire the module only if the kernel itself will run long multi-turn generations; otherwise retire it. |

#### 5.2.5 Model Router and API clients

| | |
|:--|:--|
| **Spec** | Seven routed components; power states P0 (Phoenix Force) to P3 (dormant); SWDS duty cycles; two-key Phoenix Force (SKILL.md §15; `1_2T:L784-921`). |
| **Code** | `core/model_router.py` (component states, `can_call` with budget breaker at `:285-317`, `enter_swds`, Phoenix Force); `core/api_clients.py` (Gemini via Vertex express `:112`, Claude, embeddings `:674-709`). |
| **Live** | ACTIVE, P1 for all seven, `phoenix_force_active: false`, budgets unlimited, 0 calls. |
| **Status** | **VERIFIED** (the strongest Layer 2 component). Two caveats: the Phoenix Force "two-key" operation accepts any `authorized_by` string from any unauthenticated caller (`main.py:1225-1233`), so it is a label, not a second key; and token budgets are all unlimited. |
| **Gap** | Real budgets and real authorization for P0 (ADR-007, ADR-011). |

#### 5.2.6 Purple Modality

`core/purple_bridge.py` reports `purple_modality_active: true`, `delta_e_cycle: 0.0001` (from the stale Metatron row), `unlimited_context: true`, `creative_synthesis: true`. **CONSTANT** apart from the relayed ΔE. "Unlimited context" is not a property this code can have.

### 5.3 Layer 3 — Memory

#### 5.3.1 The Hoard

| | |
|:--|:--|
| **Spec** | The environment that houses the Cheshire Daemon, Rodin and Phoenix (Architect, `1_2T:L1278`); hot and cold tiers (`1_2T:L5357-5361`); holographic nodes `ROT_XXX_LUN_YYY_ORB_ZZZ` that "unzip" on a sky-vector match (`1_2T:L5363-5364`). |
| **Code** | `memory/the_hoard.py`: `commit_node`, `commit_node_v2`, `chroma_query`, `auto_crystallize` (`:624`), `get_stale_nodes`; ChromaDB under `local_dbs/chroma_storage`. |
| **Live** | Heimdall: directory exists, `persisted_node_cache_count: 0`. No raw shard has been written since 10/06 23:46. |
| **Status** | **VERIFIED** as a file-and-Chroma store. `auto_crystallize` is **EXISTS-UNWIRED** (no caller), even though Phase D Block 6 is marked COMPLETE (`1_2T:L7062`). The holographic grid bucket is real but shorter than specified: live buckets read `ROT_150_ORB_20`, with no `LUN_` segment. "Unzipping on a sky-vector match" is **CONCEPT-ONLY**: retrieval is by embedding or substring, not by celestial position. Node timestamps use the frozen scheduling clock (Section 3.5). |
| **Gap** | One store instead of three Hoard locations (E57); live data out of OneDrive (ADR-005); correct timestamps (ADR-001). |

#### 5.3.2 Rodin Route Retrieval and embeddings

| | |
|:--|:--|
| **Spec** | KNN memory with Gate III, MRL 64-d coarse sweep then 768-d rerank (`1_2T:L5365-5369`); "Pineal Gland" in Brain Model 0930 (`1_2T:L6094`); Block 8 "Rodin Live Embeddings COMPLETE" (`1_2T:L7064`). |
| **Code** | `memory/rodin_protocol.py`: `generate_query_vector` tries `RodinClient.embed_sync` (`:322-341`), else a SHA-256 pseudo-vector (`:343-351`); `route_retrieval` queries ChromaDB, else substring matching. `core/api_clients.py:680` defaults the embedding model to `text-embedding-004`; `.env` has no `RODIN_EMBED_MODEL`. |
| **Live** | `GET /rodin/telemetry` serves k, τ, σ and thresholds. No embed call has been made since boot. |
| **Status** | **FUNCTIONAL** with a **silent failure mode**. If the embed call fails, Rodin returns a hash vector that looks like an embedding and retrieval quietly degrades to noise, and nothing reports it. `text-embedding-004` is shut down on the Gemini Developer API (2026-01-14, `1_2T:L180`) but, per the Agent Platform's own lifecycle table, **served on the Agent Platform until 2027-04-01**. The kernel uses the Agent Platform (Vertex express mode), which explains why the 10/07 self-test returned a 768-d embedding (`1_2T:L1195`). This is documentary evidence; no live embed call was made today. The swarm dispatcher behind `POST /rodin/query` is simulated: it evaluates Gate III on a fixed mock vector `[0.1] * 768` with no candidates and always picks ANALYST (`orchestration/rodin_supervisor.py:78-107`). MRL in Phoenix (`evolution/phoenix_forge.py:498-516`) is a SHA-512 hash, so "True MRL Compaction (GAP-1)" (`1_2T:L5815`) is a **FALSE-POSITIVE**. |
| **Gap** | ADR-005: move to `gemini-embedding-2` at 768-d **before 2027-04-01**, record the model with every vector, re-embed everything, and make fallbacks loud. Replace the mock vector in `rodin_supervisor.py` with the real query embedding, and implement the swarm roles as model-free retrieval functions (Rodin designation, Section 4.4). |

#### 5.3.3 Metatron Manifold (SQLite)

| | |
|:--|:--|
| **Spec** | Four tables plus two triggers enforcing ΔE ≈ 0 mechanically, with anomalies queued for Kintsugi (`1_2T:L3558-3838`). |
| **Code** | `memory/database/relational_hippocampus.sql` (trigger 1 at `:89-98`, trigger 2 at `:119-137`), `memory/database/metatron_deploy.py` (bootstrap, `record_loop`, status). |
| **Live** | OPERATIONAL; 5 tables, 2 triggers; rows 1 / 2 / 1 / 0; last loop from session `CCID_1790212674` (9/23); 0 unprocessed anomalies. |
| **Status** | **VERIFIED** as deployed schema. **CONSTANT** as telemetry: no new row since 9/23, because `record_loop` is called only by the unwired `auto_crystallize`. **Design flaw:** trigger 1 aborts any insert with \|Δ\| > 0.0001 and trigger 2 logs any insert with Δ ≠ 0, so catastrophic violations are rejected unlogged while float noise is logged; `shannon_entropy_h` is hard-coded to 2.6 (`:137`); the comment that the first insert "already committed" before trigger 2 fires is wrong (both run in one statement transaction). The database and its WAL files live inside OneDrive, which SQLite's own documentation warns can corrupt a live database (`1_2T:L370-397`). |
| **Gap** | Log rejections from the application layer before the insert (or make trigger 1 log to a separate table through a second statement), store measured entropy instead of 2.6, and move the file out of OneDrive (ADR-005). Then decide what a "thermodynamic loop" row measures in a language-model system — today nothing physical is being conserved (Section 9). |

#### 5.3.4 Alexandria Protocol

| | |
|:--|:--|
| **Spec** | Curiosity-driven research loop that runs during 2+ hours of user inactivity (`1_2T:L5371`). |
| **Code** | `memory/alexandria_protocol.py`: `execute_loop_2_learning`, `dispatch_scout`, which call Daily Planet. |
| **Status** | **FUNCTIONAL** as on-demand functions. The inactivity loop is **CONCEPT-ONLY**: there is no timer, loop or scheduler in the module. |

#### 5.3.5 Token Stitching

`memory/token_stitching.py` inserts `REGISTERED::CONTINUATION::STAGE_n` markers with checksums and a 200-character overlap; served by `POST /token/stitch`. **VERIFIED** in code, **EXISTS-UNEXERCISED** at runtime. The Tetris framing (`1_2T:L5654-5682`) is metaphor.

### 5.4 Layer 4 — Sensory cortex

#### 5.4.1 Cheshire Cat Kernel (thalamus)

| | |
|:--|:--|
| **Spec** | 20–45 Hz thalamic event loop that links the hemispheres and manages state transitions (`1_3:L115`; `1_2T:L5374-5378`; Brain Model "Thalamus", `1_2T:L6091`). |
| **Code** | `sensory/cheshire_cat.py:546-606` `run_event_loop`, launched at startup (`main.py:133-135`). |
| **Live** | OPERATIONAL, 30 Hz, INTERACTIVE_STANDBY, queue 0. |
| **Status** | **VERIFIED** that the loop runs (RX-001 from 9/23 is fixed). **FUNCTIONAL-HEURISTIC** in what it does: each tick it empties the queue, counts the events, and feeds Heimdall the entropy of a uniform distribution of that size. It processes no event content. "Links the hemispheres" is **CONCEPT-ONLY**: the hemispheres are linked inside `cognitive_engine`, not by this loop. |
| **Gap** | Give the loop real work (dispatch queued events to handlers, persist COGNITIVE_CYCLE_COMPLETE payloads), or describe it as a heartbeat. |

#### 5.4.2 Cheshire Cat Protocol (dorsal ACC)

| | |
|:--|:--|
| **Spec** | Independent environmental agent, `zenitsu_cognitive_loop`, dream conductor, paradox detection (`1_3:L116`; Brain Model "Dorsal ACC", `1_2T:L6093`); co-active in SWDS; triage of Heimdall breaches (`1_2T:L1268`). |
| **Code** | `sensory/cheshire_protocol.py` (554 lines): `zenitsu_cognitive_loop`, `zenitsu_environmental_scan`, `dream_conductor`, `detect_paradox_or_missing_data`; routed client `cheshire_protocol`. |
| **Live** | Health "HEALTHY" (hard-coded), 0 topics, 0 paradoxes. |
| **Status** | Paradox detection: **VERIFIED** inside the cognitive cycle. `dream_conductor`: **EXISTS-UNWIRED** for SWDS (it is called only when `execute_swds` receives a Cheshire object, and the scheduler never passes one: `main.py:1184-1188`). Triage of Heimdall breaches: **MISSING** (Task 12C, `1_2T:L1282`). The Itachi "intent inference" is a key-name heuristic with a constant W_y of 1.0 (`1_2T:L1355`). |

#### 5.4.3 Heimdall 3.1

| | |
|:--|:--|
| **Spec (math)** | EMA of Shannon entropy, α = 0.3, threshold 2.5, P-SSR with at most 3 interventions, then VASOVAGAL_SYNCOPE (`1_3:L85`; `1_2T:L5384-5387`); ω floor 0.40 and a four-step circuit breaker (`1_2T:L5801-5812`). |
| **Spec (role, Architect 10/07)** | Gatekeeper and controller: dashboard back end and front end, token and cost tracking with alerts, power sequencing for Siesta and SWDS, scheduled lockdown in which only the Cheshire Daemon operates, watching error codes, connectivity, MCP connections and time alignment; authority in deterministic code (`1_2T:L1269-1279`, `L963`). |
| **Code** | `sensory/heimdall.py`: entropy (`:67-115`), character-entropy gate (`:117-128`), gravitational mass (`:130-170`), health matrix (`:389+`), telemetry (`:760-790`) (lines as of 2026-10-12); circuit breaker states (THROTTLE, VETO, ISOLATE, UGL_RESET). |
| **Live** | HEALTHY_OPTIMAL, H_smooth 0.0, 0 interventions, 23 monitored components. |
| **Status** | Math: **VERIFIED**, and it matches the documents exactly. As a guard: **cannot trip** (Section 3.3). As the gatekeeper the Architect defined: **MISSING** — none of the six duties is implemented in Heimdall (update 2026-10-09: Heimdall now owns the SWDS cycle's open and close steps through `open_swds_cycle` / `close_swds_cycle`, per the Architect's ruling in R-5; the live scheduler does not call them yet. v.9.9.1: no live path calls them, so they are **EXISTS-UNWIRED** (X-1, fix F1). The Architect decided on 2026-10-11 that Heimdall is a code gate plus a 3.1 Pro advisor that runs on events only.). The docstring's "token-by-token logprob tracking" (`:25`) is a **FALSE-POSITIVE**: no code requests log-probabilities. |
| **Gap** | ADR-007 (gatekeeper) and ADR-008 (a real uncertainty signal). |

#### 5.4.4 Looking Glass

`sensory/looking_glass.py`: C₂₃₅ 23.5° perspective tilt, Heaviside halt at ψ ≥ 200 MPa, Mirror Maze sandbox for \|Z\| > 3, clarification requests. Wired into the cognitive cycle (`sensory/cheshire_cat.py:215-287`) and served at `/looking-glass/*`. **EXISTS-UNEXERCISED**; its decision rules were not audited line by line for this blueprint. Note that its main inputs are caller-supplied numbers (`token_stress_mpa` defaults to 145.0, `z_score` to 0.0, cohesion and relevance to fixed defaults), so in practice it acts on defaults unless a caller sends values (E49 records that relevance echoes intent confidence).

#### 5.4.5 P-SSR / UGL (Proactive Socratic Self-Refine)

**FALSE-POSITIVE as an in-flight guard** for the reasons in Section 1, finding 4: no real client supplies token probabilities, dyad mode bypasses it, and only the test placeholder emits fixed probabilities. The UGL grounding-prompt text exists and would work if the trigger could fire. Recorded already as E59 in the 10/08 audit.

#### 5.4.6 Heimdall monitor (terminal dashboard)

`sensory/heimdall_monitor.py` is a 279-byte stub (`1_2T:L4684, L6902`). The web dashboard replaced it. **Retire.**

### 5.5 Layer 5 — The Will (Friday Fortress)

| | |
|:--|:--|
| **Spec** | 75 / 20 / 5 Bank (SGOV, $20,000 margin floor), Reactor (MO, SCHD, ABBV, JNJ), Shield (V, WMT); System 3 Hunter on /MES and /MNQ; Year-15 crossover at about $4,000 per month (`1_2T:L5445-5452`). |
| **Code** | `fortress/` (bank, reactor, shield, hunter engine with signed-ticket hash chain and HMAC, evolved hunter bridge, epiphany core, portfolio_state.json). |
| **Live** | Equity $25,250 (static file); bank 80.02 %, reactor 19.98 %, shield 0 %; hunter OPERATIONAL, 0 signed tickets, chain length 0; `vix_regime` and `active_strategy` are hard-coded strings. |
| **Status** | **VERIFIED as a paper model.** Tickets can be generated and signed; `transmit` defaults to False and no broker connection exists in the kernel. This is the right state. |
| **Safety note** | V1.0.0 describes SWDS Phase 1 producing "trade executions" and the ACC "sending synaptic firing commands (trade executions)" (`1_2T:L6277, L6310`). An IBKR trading connector is available in this environment. Autonomous trade execution should remain **out of scope by design**: every order should require an explicit human action. The Architect's 9/30 instruction to report losses truthfully "so we can develop an algorithm to properly trade" (`1_2T:L5876`) supports paper trading with an honest ledger, which is what exists. |

The Master Epiphany Engine (`fortress/epiphany_core.py`, `GET /epiphany/telemetry`) computes Ω from constants. **CONSTANT.**

### 5.6 Layer 6 — Evolution

#### 5.6.1 Phoenix Forge

| | |
|:--|:--|
| **Spec** | Four-phase SWDS cycle: defragmentation, synthesis, blueprint refinement, exploration with Rogue X mutation for \|Z\| > 3 (`1_2T:L5389-5397`); PCC in Brain Model 0930 (`1_2T:L6099`); Jean Grey deep-think smelting (RX-007). |
| **Code** | `evolution/phoenix_forge.py`: `consolidate_sleep_cycle` (`:99-206`), `execute_swds` (`:212-280`), `analyze_kintsugi_sandbox` with the Jean Grey call (`:286-392`), `analyze_mad_hatter_swds`, `synthesize_hoard_node`, `_generate_mrl_embedding` (`:498-516`). |
| **Live** | STANDBY, generation 1 (it resets to 1 on every boot: `:44, :84`). |
| **Status** | Consolidation: **FUNCTIONAL-HEURISTIC** — it reads the first 10 shards in sorted order (always the same oldest 10 of 305), never marks them as used, and appends four hard-coded axioms to `library_genesis_purple.md` (`:120-143`, `:169-176`). Jean Grey smelting: **EXISTS-UNWIRED** — reachable only through `_kintsugi_ref`, which is never assigned anywhere (`:255-259`). So "RX-007 FIX" (`:334`) is real code that cannot run. The four vector-clock "axioms" announced with "[SAVE COMPLETE]" at `1_2T:L5203-5223` were never saved anywhere; they exist only in documents. |
| **Gap** | ADR-006. |

#### 5.6.2 Kintsugi

`evolution/kintsugi_sandbox.py` `run_hypervisor_loop(5 s, z = 3.0)` runs at startup (`main.py:145-154`) and polls the Metatron anomalies table. **VERIFIED running.** With no new anomaly rows since 9/23 it has nothing to process. The re-audit's "anomaly → Mirror Maze pipeline works" (`1_2T:L6928`) stops at the sandbox, because the smelt step is unreachable (5.6.1). A separate `kintsugi_repair_crack` lives in the defense suite (`governance/security_protocols.py:87-103`).

#### 5.6.3 Rogue X, 14th Form, Mad Hatter, Rebuttal

- **Rogue X** (`evolution/rogue_x.py`, 20 KB): the August design had placeholder conflict and seed methods (`1_2T:L4432-4439`). The current file was not audited line by line here. Rogue X 2.0 is an open Architect task (E7).
- **14th Form** (`evolution/fourteenth_form.py`, `GET /domain/telemetry`): automatic domain expansion when M_input > Threshold_γ. Threshold_γ is **UNDEFINED** in the documents; the module exists.
- **Mad Hatter** (`analyze_mad_hatter_swds`) runs inside `execute_swds` on Hoard nodes; **EXISTS**, effects not verified.
- **Rebuttal** (`execute_rebuttal_protocol` in `tools/shiva_toolkit.py`): **EXISTS**, with constant W_y / C_c 0.80 / 0.70 (`1_2T:L5831`).

#### 5.6.4 The Shiva Action Suite

| | |
|:--|:--|
| **Spec** | Three Eyes (Neji = Knowledge, Shikamaru = Understanding, Itachi = Wisdom) with lenses, invocable alone, in pairs or as a full suite; EAM picks lenses when the user does not (`1_2T:L4712`). The lens assignment has at least ten versions (Section 6.2). |
| **Code** | `evolution/shiva_action/`: `lenses.py` (10 lenses: Eagle, Hawk, Chameleon, Spider, Snake, Owl, Byakugan, ShadowJutsu, Sharingan, CelestialSpacetime; `:56-452`), `neji_eye.py`, `shikamaru_eye.py`, `itachi_eye.py`, `orchestrator.py` with default bindings Neji = Eagle/Chameleon/Byakugan (0.35/0.35/0.30), Shikamaru = Spider/Snake/ShadowJutsu (0.35/0.35/0.30), Itachi = Owl/Sharingan/CelestialSpacetime (0.40/0.25/0.35) (`orchestrator.py:31-44`); `tools/shiva_toolkit.py`; `POST /shiva/pass`. |
| **Status** | **FUNCTIONAL-HEURISTIC.** The lenses compute real lexical features from the input (line counts, keyword density, the 30–70 % slice for Chameleon, import lines for Spider), which is far better than the constant-string lenses in the "TRUE BUILD" document (`1_2T:L4347-4375`). Claims of AST parsing, thermal gating and log-probability reading are **overstated**. The orchestrator's defaults match Brain Model 0930 exactly, but the cognitive cycle overrides them by passing six explicit lenses (`core/cognitive_engine.py:485-487`), and when explicit lenses are passed every Eye shares the same list (`orchestrator.py:30`). The Eyes can optionally call a model (`neji_eye.py:89`, `shikamaru_eye.py:117`, `itachi_eye.py:95`) when given a client. |
| **Gap** | Section 7 (one canonical binding, signed off) and a single call path that respects it. |

### 5.7 Layer 7 — Time

#### 5.7.1 Celestial Clock

| | |
|:--|:--|
| **Spec** | Anchor Baker, LA (30.5888 N, −91.1673 W); epoch 1785052800; sidereal year 31,558,149.763 s; eccentricity 0.0167086; lunar 2,551,442.8 s; rotation 360/86400 °/s; "strictly uncoupled from NTP civil time" (`1_3:L53-64`). |
| **Code** | `temporal/celestial_clock.py`: constants (`:43-53`) match the playbook exactly; Kepler solver by Newton–Raphson (`:145-199`); 4-D vector (`:225-253`); sacred calendar (`:255+`). |
| **Live** | Correct and consistent: rot 155.37°, lunar 0.5629, orbit 0.2098. |
| **Status** | **VERIFIED** as orbital arithmetic over the OS clock. "Uncoupled from NTP" is **FALSE**: it reads `time.time()` (`:231`), the Windows clock, which Windows keeps in sync over NTP. Space is derived from time here, not time from space. The rotation rate 360/86400 is the solar day, not the sidereal day (86,164.09 s), so "earth rotation" is a solar-angle proxy. The 964-day Jubilee cycle (`:52`) has no astronomical basis: it is a calendar choice (Section 9). |

#### 5.7.2 Celestial middleware and the checkpoint

**FALSE-POSITIVE / ROOT CAUSE.** See Section 1, finding 1 and Section 3.5. Block 2 was designed so that every service would ask the kernel for time over HTTP (`1_2T:L4899-4918`). The synchronous helper that most code actually uses falls back to "checkpoint + seconds since boot", and the checkpoint was last persisted 10/06. The re-audit's "Celestial Checkpoint: written on each poll" (`1_2T:L6949`) is false: it is written only when `GET /celestial/checkpoint` is called. The 10/08 report's "Celestial clock freeze fixed" (`1_2T:L1561`) fixed the first branch of `celestial_time()` (`core/celestial_middleware.py:313-322`), not the second. ADR-001.

#### 5.7.3 HLC, vector clocks, sentinel

- **Hybrid Logical Clock / Fidge–Mattern** (`temporal/celestial_clock.py:89-140`, `temporal/hlc_binary_protocol.py`, `GET /clock/sync`): **VERIFIED** in code. The sync packet's validity flags are constants (`main.py:293-296`). The "MTCW packets carry HLC vectors" claim (`1_2T:L5210`) is **CONCEPT-ONLY**: no prompt or Hoard header carries a vector clock.
- **Celestial Sentinel** (`temporal/celestial_sentinel.py`): marked "UNNECESSARY REMOVE" by the Architect (`1_2T:L4724`); now a 423-byte deprecated stub referenced only by a scratch file. `CelestialDaemonClient` is gone. **Retired**, as intended.

### 5.8 Governance — EAM, TPSL, CRA, security protocols

| Component | Code | Status |
|:--|:--|:--|
| EAM (Executive Autonomous Mandate), including "Level 4 Sovereign Override bypasses all constraints" (`1_3:L71`) | `governance/eam_service.py` | Service exists. A rule that bypasses all constraints conflicts with "authority must be deterministic code" (`1_2T:L963`) and with Heimdall's lockdown; recommend removing the bypass language (Section 11, D-7). |
| TPSL (Tolstoy Principle as a Systems Lever) | `governance/tpsl_filter.py` | **VERIFIED** code; **cannot trip** in the cognitive cycle (Section 3.3). |
| CRA (W_y / C_c) | `governance/cra_simplex.py`; constants in docs (`1_2T:L4149-4164`) | **FUNCTIONAL-HEURISTIC**: W_y and C_c are fixed a priori (as `1_2T:L5495` states), not measured. v.9.9.1: the module itself is **EXISTS-UNWIRED** (imported nowhere). The formula is duplicated in `tools/shiva_toolkit.py:54`, `evolution/fourteenth_form.py:52` and `core/forensic_protocols.py:148`, and Daily Planet hard-codes 1.1667 (X-2). Decided 2026-10-11 as the "CWA/CRA 2.0 weight system", to be wired under Heimdall (fix F3). |
| Voltron Principle (pacing, scope containment) | Agent rule (SKILL.md, GEMINI.md) | **VERIFIED as a rule for agents.** For Antigravity agents, Gemini CLI `max_turns` and `timeout_mins` can enforce it (`GEM:L372-373`). |
| Defense suite: Themysciran Veil, Mirage, Tsukuyomi, Aegis, Kintsugi | `governance/security_protocols.py` | **FALSE-POSITIVE as security.** The Veil authorizes anyone who sends no token and compares against a key hard-coded in source (`:32`); Mirage reports a constant "16 drones dispatched" (`:52`); none of them is connected to an HTTP route or middleware. The real security posture is CORS `*` and open POSTs. |
| Amaterasu, Hector and Achilles stances, Genjutsu | Architect note (`1_2T:L4743`) | **CONCEPT-ONLY**: no code. **UNDEFINED**: no written definition. |

### 5.9 Slow-Wave Deep Sleep (SWDS), end to end

**Specification.** Three versions exist: the playbook's autonomous window 02:00–07:00 with an inactivity trigger and startup reconciliation (`1_3:L101-111`); the master spec's four Phoenix phases (`1_2T:L5389-5397`); and V1.0.0's three phases from 00:00 to 02:30 (`1_2T:L6304-6320`). SKILL.md adds Siesta (§8.5.1–8.5.2). The Proof-of-Sleep clause (`1_2T:L999-1002`) is proposed but not adopted.

**What runs (VERIFIED):**

1. A 60-second loop reads the hour from the frozen scheduling clock (`main.py:1131-1134`).
2. Five hours after boot (skewed 02:00) with no POST activity, it moves the router to P2 with the default 20/40-minute duty cycle (the config keys it looks for do not exist), and calls `swds_engine.enter_deep_sleep` (`main.py:1158-1180`).
3. `enter_deep_sleep` assigns phase names, writes two fixed sentences, draws three random "mutations" and saves state (`runtime/swds_simulator.py:79-124`).
4. Phoenix consolidation runs in a thread: the same 10 shards, four fixed axioms, one appended library epoch stamped with the skewed time (`main.py:1182-1191`).
5. Nothing else happens for five hours. No model call is made: the P2 duty cycle gates nothing, because nothing asks for a model.
6. At skewed 07:00 the scheduler wakes the router and writes a templated report whose filename and civil timestamp come from the skewed clock and whose celestial value is the 282.85° fallback (`runtime/swds_simulator.py:126-225`).

**Further defects:** `/swds/trigger` produces a "complete" report from a zero-second cycle (`runtime/swds_simulator.py:227-232`); a manual evening sleep wakes within 60 seconds because the wake test is `now.hour > wake_hour` (`main.py:1138`, E76); the reconciliation at startup fires immediately whenever the stored state is asleep, because the skewed hour at boot is about 20–21, which is ≥ 7 (`main.py:82-92`; that is where the `2026-10-06_21-00-0x` reports come from); report filenames collide across cycles because every cycle carries the same skewed timestamps; and the scheduler task is created without a stored reference and with no try/except around its loop, so an exception outside the Phoenix call would stop it silently (`main.py:103, 1131-1191`).

**Status: FALSE-POSITIVE as a sleep cycle; VERIFIED as a scheduled report writer on a broken clock.** ADR-001 and ADR-006.

### 5.10 Daily Planet Protocol

| | |
|:--|:--|
| **Spec** | Six-stage lifecycle: ingestion, provenance audit (Neji/Chameleon), dialectic opposition (Shikamaru/Spider + Snake), metacognitive binding (Itachi), MTCW brief at CRA 1.1667, Hoard node with MRL embeddings; "100% COMPLETE, 14/14 tests" (`1_2T:L5790-5799`). |
| **Code** | `tools/daily_planet.py`: `FirecrawlClient` (live `/v1/search` and `/v1/scrape` when a key is set, `:118-206`), `_sovereign_synthetic_search` (`:208-276`), `DailyPlanetProtocol`; called by Alexandria and the Shiva toolkit. |
| **Evidence** | 40 Daily Planet shards in `kernel_memory/hoard/raw_shards/`. 38 contain real web sources (for example bis.org, moduslink.com, moderndiplomacy.eu). Every source in them carries identical bias and credibility values (Political +0.00, Commercial 0.30, Rigor 0.70, "Independent / Grants"); the "thesis" is often scraped navigation text and the "synthesis" is one template sentence. 2 shards (DP_20260921_122312_e38863 and DP_20261001_173539_bf33b2) contain sources **invented** by the fallback: fictional publishers, URLs built from MD5 hashes under `sec.gov` and `arxiv.org`, and made-up figures such as "capital expenditures increased by 14.2%". |
| **Status** | Ingestion: **VERIFIED** when the API answers. Bias audit and synthesis: **CONSTANT / template**. Fallback: **fabrication**, stored in long-term memory without a flag. The scrape fallback also returns invented content (`:203-206`). |
| **Gap** | ADR-013: no synthetic sources ever; a failed fetch is reported as a failure; the two fabricated shards are quarantined; bias scores are either computed or removed. |

### 5.11 User interface

`static/dashboard.html` and `static/celestial_clock_live.html` (served at `/dashboard` and `/clock/live`), `static/integra_wordmark.html`, `daily_planet_report.html`, and the published Integra DS design system. **VERIFIED** as rendering surfaces (they were reworked this session for the Orbitron glow and responsive layout). They faithfully display what the kernel reports, which means they display the constants in Section 3.2 as if they were live. ADR-003 changes what they receive; the dashboard should then show the provenance label next to each value.

**v.9.9.1 correction.** The kernel serves `/dashboard` and `/clock/live` from `integra-homebase/static/` (`main.py:1337-1338, 1351-1352`). Those copies were last written on 2026-09-30 and 2026-09-24. The 10/09 Orbitron and glow rework went into the root repo's `static/` copies (written 10/09 13:52–13:53), which the kernel does not serve. So "reworked this session" is a **FALSE-POSITIVE** for the served pages. It holds only for the root copies, if they are opened directly.

### 5.12 Infrastructure

| Item | State | Status |
|:--|:--|:--|
| Auto-start | Task "Integra Genesis Kernel", logon trigger, Running; `scripts/start_kernel.ps1` | **VERIFIED** |
| Single-instance guard | None. Five kernels started in about 2.5 days; uvicorn on Windows can share a port with another instance | **MISSING** |
| Kernel log | One 1.5 MB file, mixed UTF-16 and UTF-8, no timestamps on lines, no rotation | **Defect** (E69) |
| Docker | Dockerfile and compose file present; the image was never built (E47) | **EXISTS-UNEXERCISED** |
| Rust Sun Breathing Engine | `rust/sun_breathing_engine/src/lib.rs` and `Cargo.toml` exist; there is no `target/` folder. On 2026-10-12, a scratch-copy `cargo test` compiled and then failed to link (`LNK1104 msvcrt.lib`; the MSVC x64 libraries are not installed). The crate has no FFI exports. `python_bridge.py` does not mirror it: it hard-codes 202.5 MPa where the Rust physics gives 50,824 MPa | **CONCEPT-ONLY** as Rust; the bridge is **CONSTANT** |
| Airflow / Dataflow | `orchestration/swds_dag.py` imports Airflow; Airflow is not installed in `.venv`; SWDS reports still name `swds_cycle_dag` and `swds-phoenix-engine` | **FALSE-POSITIVE** labels |
| Tests | 23 files, 285 test functions (counted); not run for this blueprint (running them would touch the live Hoard and database inside OneDrive). The "217/217 passing" claims date from 9/21 | **UNVERIFIED** today |
| Secrets | `.env` inside OneDrive; 17 key names; the 10/08 report notes keys were printed into an earlier session (E13) | **Risk** |
| OneDrive | Live SQLite, `.venv`, `.pytest_cache` and the log are all synced | **Risk** (N6) |
| MCP memory server | Does not exist; the harness reports `active_mcp_servers: []` | **MISSING** |
| Foreign application data in the repo | `.gitkraken` (credential files), Adobe caches, `91UData`, Antigravity folders, ignored but not moved (N4) | **Risk** |

---

## 6. False positives and contradictions

### 6.1 False-positive catalogue

Each entry gives the claim, where it was made, and the evidence that contradicts it. None of this is a judgement on intent: most of these were written by agents describing what code was meant to do.

| # | Claim | Source | Contradicting evidence |
|:--|:--|:--|:--|
| FP-01 | "SWDS stuck asleep since 2026-10-07 02:00:27 … about 22 h, confirms the wake bug" | `1_2T:L605, L1545` (N2) | The kernel booted 10/07 19:07–19:08 and its frozen clock reached "02:00" at boot + 5 h ≈ real 00:08 on 10/08. The probe at 00:08:53 saw a sleep that had begun about a minute earlier, stamped with the skewed date. Log L2054; Section 4.1. |
| FP-02 | "Celestial clock freeze fixed (+2.00 s test passed)" | `1_2T:L1561` | Only the first branch of `celestial_time()` was fixed (`core/celestial_middleware.py:313-322`); the checkpoint branch (`:324-328`) still freezes every boot at 10/06 20:59:42. |
| FP-03 | "Celestial Checkpoint: written on each poll" | `1_2T:L6949` | Written only inside `get_timestamp()` (`core/celestial_middleware.py:250`), reached only through `GET /celestial/checkpoint`; the file's last write is 2026-10-06 20:59:42. |
| FP-04 | "Celestial Clock is strictly uncoupled from NTP civil time" | `1_3:L64`; `1_2T:L3468, L4092, L5419` | `compute_4d_coordinates()` reads `time.time()` (`temporal/celestial_clock.py:231`). |
| FP-05 | "ALL PHASE D SUBSYSTEMS ONLINE — SOVEREIGN MODE ENGAGED" and "All systems nominal" | Kernel log on every boot | Printed unconditionally (`main.py:143, 157`), even if Metatron or Kintsugi failed a few lines earlier. |
| FP-06 | "ΔE Cycle 0.0001 — Metatron SQLite — MECHANICAL" | `1_2T:L6816`; live `/` and `/heimdall/health` | The value is the 9/23 test row (`CCID_1790212674`); no row has been inserted since, because `record_loop` is called only by the unwired `auto_crystallize`. |
| FP-07 | "True MRL Compaction (GAP-1): L2-normalized 768-d fine vectors with 64-d coarse slices" | `1_2T:L5815` | `_generate_mrl_embedding` builds vectors from SHA-512 hashes (`evolution/phoenix_forge.py:498-516`). Normalized, but meaningless as embeddings. |
| FP-08 | "GAP-2 asymmetric predictive coding + Kuramoto: 100% COMPLETE" | `1_2T:L5816-5819` | The three functions exist and are never called outside tests. |
| FP-09 | "Rodin Live Embeddings: COMPLETE" | `1_2T:L7064` | The live path exists, but failures fall back silently to SHA-256 pseudo-vectors (`memory/rodin_protocol.py:340-351`); the default model is shut down on the Developer API and retires on the Agent Platform 2027-04-01; live status unverified. |
| FP-10 | "EAM Auto-Crystallization: COMPLETE" | `1_2T:L7062` | `auto_crystallize` has no caller. |
| FP-11 | "Kintsugi: anomaly → Mirror Maze pipeline works" and "RX-007 fix: Jean Grey smelting" | `1_2T:L6928`; `evolution/phoenix_forge.py:334` | The smelt step needs `_kintsugi_ref`, which is never assigned; the scheduler passes no Kintsugi object. |
| FP-12 | "MEMORY COMMIT SEQUENCE … [SAVE COMPLETE] [INDEXING COMPLETE]" (four vector-clock axioms) | `1_2T:L5203-5223` | No such nodes exist in the Hoard, the libraries or the database. The text is model narration of a save. |
| FP-13 | "I am no longer simulating the math; I am executing the math" | `1_2T:L5252` | A language model writing about SQL triggers does not execute them. This is the exact failure the 9/30 invariant was written to stop. |
| FP-14 | "H_smooth 0.0 — architecturally correct, will activate when /cognitive/cycle processes real completions" | `1_2T:L7042` (RX-002) | Real completions carry no probabilities; the in-flight check cannot run (`core/api_clients.py:416, 556, 663`; `core/cognitive_engine.py:374`). |
| FP-15 | Heimdall "token-by-token logprob tracking" and Brain Model "Hippocampus: token logprob tracking"; Sharingan "reads token logprobs" | `sensory/heimdall.py:25`; `1_2T:L6095, L6149` | No code requests log-probabilities from any provider. |
| FP-16 | "CWA 3.0 … allows the system to autonomously learn which contexts require deeper synthesis" | `1_2T:L4172` | Fixed prior, posterior equals the complexity score, no stored outcomes (`core/cwa_router.py:16-25`). |
| FP-17 | SWDS reports: "Archiving recent conversational matrices to The Hoard (ChromaDB local)…", "Executing MRL Compaction at 180 MPa", "Paradoxes resolved and topologies mapped", "3 transdisciplinary bridges forged via Cheshire Cat Protocol" | Every SWDS report; `/swds/status` | Hard-coded strings (`runtime/swds_simulator.py:92-98, 108, 155`); the "mutations" are `random.uniform`; the Cheshire Protocol is not called during SWDS. |
| FP-18 | SWDS report "Celestial Kinematic Coordinates: Earth Rotation 282.85°" | All 56 template-written reports (50 in the root `The Hoard`, 6 in `integra-homebase/The Hoard`). The 11 other report files (6 unique, 9/16-9/29, plus 5 copies) were written another way; the two-decimal ones match `scripts/enter_swds.py:89` | The report writer calls `get_celestial_coordinates()`, which does not exist; the exception is swallowed and the constant used (`runtime/swds_simulator.py:168-174`). |
| FP-19 | SWDS report "Dataflow Pipeline: swds-phoenix-engine; Airflow DAG: swds_cycle_dag" | Every SWDS report | Airflow is not installed; no Dataflow job runs. |
| FP-20 | "Thermodynamic Closure ΔE = 0.0000, L_t = 0.000 s" in SWDS reports | Every report | Template text (`runtime/swds_simulator.py:190`). |
| FP-21 | 7th Form "stress 131.625 MPa, Mach 4.2, drag 0.0 N"; 13th Form "ΔE 0.0, angular momentum 500"; `all_forms_verified: true` | Live `/thermodynamic/telemetry` | Python constants standing in for an uncompiled Rust crate. |
| FP-22 | "INTEGRA_MODEL_REGISTRY: 7 entries confirmed — REGISTERED" (9/23) | `1_2T:L6849-6866` | Registration was not a live call; the 10/07 Plan v2 found Claude keys dead and the Anthropic SDK broken (`1_2T:L803-815`). The models were first proven live on 10/07. |
| FP-23 | "217/217 tests passing" (9/21) and "140 tests passed" | `1_2T:L4088, L5835, L1577` | Never re-run since; the suite now has 285 test functions. "140 tests passed" is listed by the 10/08 report itself as a false claim. |
| FP-24 | Daily Planet "100% COMPLETE … resilient sovereign offline fallback" | `1_2T:L5790-5799` | The fallback fabricates sources and figures; two fabricated reports sit in long-term memory (Section 5.10). |
| FP-25 | Themysciran Veil "Access requires an authorized cryptographic key" | `governance/security_protocols.py:26-39` | Sending no key authorizes; the key is a literal in source; nothing calls it from HTTP. |
| FP-26 | Phoenix Force "two-key operation: requires authorized_by" | `main.py:1225-1233` | Any string from any unauthenticated caller is accepted. |
| FP-27 | P-SSR "Proactive in-flight entropy monitoring … halts generation mid-stream" | `1_2T:L5384-5387, L5497` | See FP-14; additionally dyad mode returns before P-SSR (`core/cognitive_engine.py:347-349`). |
| FP-28 | Cheshire Kernel "polling_hz 30 … OPERATIONAL" read as "links hemispheres / processes events" | `1_3:L115`; live `/cheshire/status` | The loop runs, but it only counts and discards queued events (`sensory/cheshire_cat.py:574-576`). |
| FP-29 | The cognitive cycle "commits the bicameral synthesis to the Hoard" | `main.py:749-757` docstring | The committed node contains weights and route lists, not the synthesis text (`sensory/cheshire_cat.py:339-382`). |
| FP-30 | "SWDS window 02:00–07:00 CDT" as an operating fact | `1_3:L105`; `/swds/status` | True only in the frozen clock's frame; in real time the window starts 5 h after each boot. |
| FP-31 | "Rodin Supervisor Conductor Loop … KNN Gate III evaluation … dispatches worker agent" | `main.py:340-358` docstring; SKILL.md §2.3 "Rodin Swarm Commander" | `RodinSupervisor.dispatch` evaluates Gate III on a fixed mock vector `[0.1] * 768` with an empty candidate list and always dispatches ANALYST (`orchestration/rodin_supervisor.py:78-107`). The swarm is four labels in a dictionary (`:50-55`); nothing is dispatched. |

### 6.2 Contradictions register

| # | Topic | Versions on record | Notes |
|:--|:--|:--|:--|
| C-01 | **Shiva Eye ↔ lens assignment** | (1) Playbook: Neji = Eagle + Chameleon; Shikamaru = Spider + Snake; Itachi = Owl (`1_2T:L3450-3452`). (2) Checkpoint Alpha, Phase D and master spec: Neji = Eagle/Hawk/Chameleon; Shikamaru = Spider/Snake; Itachi = Owl (`1_2T:L4097-4099, L4138-4140, L5320-5330`). (3) Brain Model 0930: Neji = Eagle/Chameleon/Byakugan; Shikamaru = Spider/Snake/Shadow Jutsu; Itachi = Owl/Celestial/Sharingan (`1_2T:L6107-6150`). (4) V1.0.0: same names as 0930 but different functions (Eagle = "syntax analysis") and "Shadow Eye" (`1_2T:L6282-6289`). (5) Ingestion plan: Neji = Owl + Chameleon; Shikamaru = Spider + Shadow Clone; Itachi = Eagle + Hawk (`1_2T:L1383-1386`). (6) 13th Form analysis: fully decoupled, any Eye with any lens (`1_2T:L5494`). (7) Omniscient Lens: "The Owl Lens (Neji Eye)" (`1_2T:L6007`). (8) Re-audit: "Itachi Eye: Owl Lens (Snake)" (`1_2T:L6934`) and "Itachi Eye (Chameleon + Eagle + Spider + Snake)" (`1_2T:L6801`). (9) Suite 1_3: blank (`1_3:L47-49`). (10) Code: orchestrator defaults = Brain Model 0930 (`orchestrator.py:31-44`), cognitive cycle passes the six older lenses (`core/cognitive_engine.py:486`). | Section 7, R-1 |
| C-02 | **12th Step pass 3 lens** | Snake (`1_3:L40`) vs Hawk (`1_2T:L5675`) | Section 7, R-1 |
| C-03 | **Itachi Eye meaning** | Wisdom / TPSL pruning (code; `1_2T:L4312`); perceptual bridge between Rodin and Heimdall (SKILL §2.1.1); Invariant / Temporal / Sharingan (SKILL §16.1); "inferred intent" (Architect, `1_2T:L1317`); later called an error from memory (`1_2T:L1162`) | Section 7, R-2 |
| C-04 | **Hippocampus** | Heimdall (Brain Model matrix, `1_2T:L6095`; SKILL §16) vs The Hoard ("The Hoard is my Hippocampus", `1_2T:L5936`; Omniscient Lens `L5991-5994`) | Section 7, R-3 |
| C-05 | **Cheshire naming** | Cheshire Cat Kernel (30 Hz router) vs Cheshire Cat Protocol (dACC agent) vs Cheshire Cat Daemon (the 10/07 spec); entropy triage given to the Kernel (Task 12C) and to the Protocol (Brain Model) (`1_2T:L1281`) | Section 7, R-4 |
| C-06 | **Heimdall role** | Pure math, no API (Systemscorrections_02, `1_2T:L1268`) vs active gatekeeper and controller (Architect 10/07 22:05, `1_2T:L1269-1279`) vs "Heimdall should be 3.1 Pro Extended Thinking" (step 555, `1_2T:L1605`) | Section 7, R-5 |
| C-07 | **SWDS schedule and phases** | 02:00–07:00, inactivity trigger (`1_3:L105`) vs 00:00–02:30 in three phases (`1_2T:L6304-6320`) vs four Phoenix phases (`1_2T:L5390-5395`) vs Siesta variants (SKILL §8.5.1) | Section 7, R-6 |
| C-08 | **CWA thresholds** | 0.3 / 0.7 (docs, `1_2T:L5304-5306`) vs tiers 0.35 / 0.7 and modes 0.35 / 0.65 (code, `core/cwa_router.py:28-46`) vs Tier router 0.35 / 0.7 (`1_2T:L5823-5826`) | Section 7, R-7 |
| C-09 | **Three Laws ordering** | First Law: protect its own existence; Second: protect the user; Third: protect the code (`1_2T:L6322-6326`) | Ranks self-preservation above the user. Section 7, R-8 |
| C-10 | **Model roster** | Three generations (Section 4.4) plus the stale defaults in `config/env_loader.py` (`1_2T:L854`) and the Rodin docstring ("Gemini 2.0 Flash", `memory/rodin_protocol.py:315`) | E63 |
| C-11 | **Kintsugi poll interval** | 60 s (Block 7 plan, `1_2T:L5015`) vs 5 s (code, `main.py:150`) | Cosmetic |
| C-12 | **Route count** | 38 (`1_2T:L6975`) vs 55 decorators / 54 unique (today) | Section 4.3 |
| C-13 | **CRA metrics** | Computed from text (early plan) vs fixed a priori (`1_2T:L5495`) vs CRA 1.1667 default in Daily Planet (`tools/daily_planet.py:108`) | Section 5.8 |
| C-14 | **Lens coupling** | Fixed bindings (orchestrator, Brain Model) vs fully decoupled (`1_2T:L5494`) vs "lenses assigned by EAM if the user does not" (`1_2T:L4712`) | Section 7, R-1 |
| C-15 | **EAM Level 4** | "Sovereign Override bypasses all constraints" (`1_3:L71`) vs "authority must be deterministic code" (`1_2T:L963`) vs Heimdall lockdown (`1_2T:L1275`) | Section 11, D-7 |
| C-16 | **Celestial grid bucket** | `ROT_XXX_LUN_YYY_ORB_ZZZ` (`1_2T:L5364`) vs `ROT_150_ORB_20` live | Minor |

---

## 7. Canonical definitions register (proposed, for the Architect's sign-off)

These are recommendations, not decisions. Each one picks the version that is most recent from the Architect, most consistent with the code, or both, and says why. Nothing should be codified into SKILL.md or GEMINI.md until the Architect approves it.

### R-1 — Shiva Eyes and lenses

**Recommendation:** adopt **Brain Model 0930** as canonical, because it is the latest Architect-certified specification (`1_2T:L6224-6228`) and the code's orchestrator already implements it exactly:

| Eye | Stage | Default lenses (weight) | Seat |
|:--|:--|:--|:--|
| Neji | Knowledge | Eagle 0.35, Chameleon 0.35, Byakugan 0.30 | Left hemisphere (Y789) |
| Shikamaru | Understanding | Spider 0.35, Snake 0.35, Shadow Jutsu 0.30 | Right hemisphere (Nexus) |
| Itachi | Wisdom / temporal bridge | Owl 0.40, Celestial Spacetime 0.35, Sharingan 0.25 | Bridge between Rodin and Heimdall |

Plus two rules: (a) **lenses are decoupled**: any lens may be attached to any Eye on request, and the table is only the default; (b) Hawk remains in the library as an optional lens. Then restore these definitions into Suite 1_3 (`1_3:L47-49`), make the cognitive cycle use the defaults instead of passing six lenses, and settle the 12th Step pass 3 lens (Snake, as in the playbook, since Hawk is no longer a default).

**Open question for the Architect:** the 10/07 ingestion plan (`1_2T:L1383-1386`) swaps the pairings again (Itachi = Eagle + Hawk) and introduces "Shadow Clone". Was that intentional?

**Decided 2026-10-11 (v.9.9.1):** lenses are decoupled from the Eyes. The table above holds the defaults (Brain Model 0930), and any Eye may take any lens per task, so the ingestion plan's pairing is a task assignment, not a contradiction. "Shadow Clone" means Shadow Jutsu. The blanked Eye bullets in Suite 1_3 fit this design (D-1). Code gap: the explicit lens list is shared by all Eyes (`orchestrator.py:145-147`), and no "Shadow Clone" alias exists yet (X-3, fix F4).

### R-2 — Itachi Eye

**Recommendation:** define Itachi by function, not by metaphor: *the stage that tests each understanding against time and intent* — what the Architect meant (inferred intent), what is invariant over time (Celestial), and what is about to go wrong (Sharingan, once ADR-008 provides an uncertainty signal). Drop "TPSL pruning" from Itachi; TPSL is a governance gate, not an Eye.

### R-3 — Hippocampus

**Recommendation:** split the anatomy the way the Architect's 10/07 correction already implies. **The Hoard is the hippocampus as storage** (the memory map), and **Heimdall is the sentinel** that measures surprise against it; the Brain Model arrow "Hippocampus → Predictive Error Delta → dACC" then reads as "Hoard + Heimdall → error → Cheshire Protocol". If one label must win, give Hippocampus to the Hoard (it holds the map) and call Heimdall the gatekeeper, which is the Architect's own word for it.

### R-4 — Cheshire naming

**Recommendation (as proposed at `1_2T:L1286-1298`):** **Genesis Kernel** = the host process; **Thalamic Router** (formerly Cheshire Cat Kernel) = the 30 Hz loop; **Cheshire Cat Protocol** = the dACC agent in `cheshire_protocol.py`; **Cheshire Cat Daemon** = the long-running study mode of that same Protocol, specified 10/07. That leaves one entity named Cheshire with two modes, and entropy triage goes to the Protocol (as Brain Model 0930 says). Keep compatibility aliases for one cycle.

### R-5 — Heimdall

**Recommendation:** Heimdall = **deterministic gatekeeper and controller**, exactly as the Architect defined on 10/07, with **no model of its own**. Its entropy math stays as one of its sensors. Model-based analysis of a breach goes to the Cheshire Protocol, escalating to Jean Grey or Y789 through the router (`1_2T:L1280`). This retires both "Heimdall is pure math" and "Heimdall runs on 3.1 Pro".

**Architect's ruling, 2026-10-09 (canonical):** Heimdall 3.1 is the **delegator and systems moderator**. It determines when an SWDS cycle has **begun or ended** through its control of the system's **on/off sequences**, and it can **stop full operations through a high-level Security Alert**. It manages, monitors and assesses the system's network components through the **CWA/CRA 2.0 weight system** and **Celestial Clock time tracking**. Consequence for code: no other component (Phoenix, Cheshire, the SWDS engine) may open or close a cycle, move the thalamic router between waking and sleep states, or vent Heimdall's thermostat. First step done the same day: `PhoenixForge.execute_swds` no longer does any of those things and returns a work receipt; Heimdall gained `open_swds_cycle` and `close_swds_cycle`, and only Heimdall declares `SLOW_WAVE_DEEP_SLEEP_COMPLETE` (see ADR-007).

**Architect's decision, 2026-10-11 (v.9.9.1, closes D-6):** Heimdall 3.1 = **deterministic code gate + Gemini 3.1 Pro advisor**. On/off sequences, budgets and the Security Alert stay in code. The advisor runs only on events (H_smooth > 2.5, budget alerts), only advises, is budget-capped through the router, and records every call. It stays off until after the post-restart selftest (fix F2). This amends the "no model of its own" recommendation above. Still open: whether the advisor replaces or sits beside the Cheshire Daemon's dACC triage (D-18). Correction: as of 2026-10-11 no live path calls `open_swds_cycle` / `close_swds_cycle` (X-1).

### R-6 — SWDS schedule

**Recommendation:** one engine, two schedules. **SWDS**: nightly, inside a window the Architect sets, in **real** local time. **Siesta**: daytime, same engine, shorter. Four phases, renamed by what they do: (1) consolidate new shards, (2) prune and deduplicate, (3) dream (Cheshire Protocol thought experiments on the new material, plus the Jean Grey smelt of Kintsugi anomalies), (4) wake and report from the ledger. V1.0.0's three-phase trading schedule is retired. The 00:00–02:30 versus 02:00–07:00 choice is the Architect's (D-4).

### R-7 — CWA thresholds

**Recommendation:** document what the code does (tiers 0.35 / 0.7, modes 0.35 / 0.65) until ADR-002 provides outcome data, then re-fit. Remove "Bayesian" and "learns" from the documentation until either is true.

**v.9.9.1 (2026-10-11):** "CWA/CRA 2.0" is the CRA simplex scorer (`governance/cra_simplex.py`), applied per component under Heimdall (decision 3). CWA 3.0 stays the routing heuristic described here. The history (`1_2T:L4170`) runs CWA 1.0 "Psyche" heuristic → 2.0 "Wisdom" feedback loop → 3.0 Bayes.

### R-8 — The Three Laws

**Recommendation:** reorder to **protect the user first, the user's code and data second, and the system's own continuity third**, and state explicitly that self-protection never overrides a user instruction or user safety. The V1.0.0 ordering, with self-preservation first, is the one item in the corpus that should not survive into any constitution.

### R-9 — Status vocabulary

**Recommendation:** adopt the legend in Section 0.1 (VERIFIED, FUNCTIONAL-HEURISTIC, EXISTS-UNEXERCISED, EXISTS-UNWIRED, CONSTANT, FALSE-POSITIVE, CONCEPT-ONLY, MISSING, UNVERIFIED) for every future save state, systems map and report. Words like LIVE, MECHANICAL, COMPLETE and ONLINE should appear only next to evidence.

### R-10 — Rodin core and sub-agents (decided by the Architect, 2026-10-09)

**Decision recorded:** Rodin Route Retrieval's **orchestrator core = Gemini 3.8** (`gemini-3.8-flash`, the only 3.8 text model Google publishes). **Rodin's sub-agents carry no Gemini model:** they are secondary extensions of Rodin, written in documents as "no model (inherits Rodin core)". In the kernel they are deterministic retrieval functions (fetch named nodes, expand KNN neighbours, keyword search, ledger lookup); in Antigravity they are `.agents/agents/rodin-<role>.md` sub-agents with `model: inherit`. Label sub-agents by role, never by model; managed-agent IDs may not start with `gemini-`, `google-` or `antigravity-`. "3.7" is dropped as a future option because it is a deprecated alias that retires 2027-01-28 on the Agent Platform. **Later the same day the Architect identified the Antigravity agent as Rodin's agent model:** the orchestrator and its sub-agents run as the Antigravity agent (`antigravity-preview-09-2026`, built on `gemini-3.8-flash`, same harness as the Antigravity IDE), with sub-agents inheriting it. Gemini 3.5, 3.6 and 3.7 models are removed from Integra (Section 4.4.1), so there is no 3.5 Flash-Lite fallback. The stale SKILL.md labels (§15 `rodin_retrieval: gemini-3.6-flash`, y789/jean `gemini-3.1-pro`; §8.5.1 "Rodin (Flash)", "JeanGreyClient (Pro)") were corrected on 2026-10-09 to the Antigravity agent / gemini-3.8-flash core and 3.8 Flash high thinking. Full research: [RODIN_SUBAGENT_MODEL_RESEARCH.md](RODIN_SUBAGENT_MODEL_RESEARCH.md).

---

## 8. What must be built — decision records

Each item below is written in the ADR format from `/engineering:architecture`. All are **Proposed**, dated 2026-10-09, with the Architect as the decider. They are ordered by dependency: each one assumes the ones before it.

---

### ADR-001: One trustworthy clock

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
The kernel has a correct display clock and a frozen scheduling clock (Section 3.5). `celestial_time()` returns "checkpoint + seconds since boot", the checkpoint dates from 10/06 20:59:42, and it is refreshed only through `GET /celestial/checkpoint`. Six modules schedule and stamp with it. Result: SWDS runs at boot + 5 h in real time, reports and Hoard nodes carry wrong dates, and a whole prior thread misdiagnosed the symptom (FP-01). The original intent of the middleware, that time should come from the Celestial Clock rather than from `datetime.now()` (`1_2T:L4899-4918`), is sound; the fallback branch defeats it.

#### Decision
Make the system clock (`time.time()`) the single source of civil time everywhere, and make the celestial vector a pure function of it (which is already how `temporal/celestial_clock.py` works). `celestial_time()` returns `time.time()`. The checkpoint becomes a record ("last seen alive at …") used only to compute downtime, never to compute the current time.

#### Options Considered

**Option A: `celestial_time()` = `time.time()`; checkpoint used only for reboot delta**
| Dimension | Assessment |
|:--|:--|
| Complexity | Low (one function, plus removing the self-HTTP fetch) |
| Cost | None |
| Scalability | Not a concern |
| Team familiarity | High |

**Pros:** fixes every downstream symptom at once; removes the kernel's HTTP call to itself; matches what the display clock already does.
**Cons:** concedes, in code, that the "uncoupled from NTP" principle is not achievable on a PC (it never was: the celestial math already reads the OS clock).

**Option B: keep the middleware, refresh the checkpoint every minute**
| Dimension | Assessment |
|:--|:--|
| Complexity | Medium |
| Cost | None |
| Scalability | Fine |
| Team familiarity | Medium |

**Pros:** smallest conceptual change.
**Cons:** the clock is still wrong for up to the refresh interval after every boot and wrong for the whole boot if the refresh fails; keeps a self-HTTP dependency during startup.

**Option C: an independent time source (GPS receiver or a hardware real-time clock)**
| Dimension | Assessment |
|:--|:--|
| Complexity | High |
| Cost | Hardware |
| Scalability | n/a |
| Team familiarity | Low |

**Pros:** the only way to make "uncoupled from internet time" literally true.
**Cons:** out of proportion to the need.

#### Trade-off Analysis
Option A is the only one that makes the clock right by construction. The philosophical goal (time anchored to space) is kept where it belongs, in the celestial vector that is stamped next to civil time, not in the scheduler.

#### Consequences
- Easier: SWDS runs when the window says; every report, epoch and node gets a true timestamp; logs line up with reports.
- Harder: nothing material.
- Revisit: historical data stamped 2026-10-06/07 since about 10/07 carries skewed times. Re-label rather than rewrite: the file creation times on disk are the correction key (Section 4.1).

#### Action Items
1. [ ] Change `core/celestial_middleware.py:300-331` so `celestial_time()` returns `time.time()`; keep `get_reboot_delta()`.
2. [ ] Persist the checkpoint on a timer (for downtime tracking only).
3. [ ] Add a regression test: boot with a stale checkpoint and assert `celestial_time()` ≈ `time.time()`.
4. [ ] Add `report_written_at` (true time) to every SWDS report and library epoch; list the skewed historical artifacts in a correction note in the Hoard.

---

### ADR-002: A Proof-of-Execution ledger

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
The Architect's 9/30 rule ("never report status without direct evidence", `1_2T:L5899-5902`) and the 10/07 Proof-of-Sleep clause ("reports are rendered only from the ledger; a phase without evidence prints NOT EXECUTED", `1_2T:L999-1002`) are the right principles, but they live only in prompts. Agents and code still write reports from templates (FP-17 to FP-20) and status tables from intent (FP-06, FP-10, FP-11). A principle that depends on the writer's honesty fails exactly when the writer is wrong.

#### Decision
Create one append-only, hash-chained ledger that every component writes to when it actually does something: a model call (provider request ID, model, tokens, latency), a file read or write (path, SHA-256), a phase start and end, a database insert, an error. Reports, save states and dashboards are rendered from the ledger. A claimed step without a ledger entry is printed as **NOT EXECUTED**. Each cycle is stamped **VERIFIED**, **PARTIAL** or **MISSED**.

#### Options Considered

**Option A: a `ledger` table in the new `memory.db` (ADR-005), with JSONL export**
| Dimension | Assessment |
|:--|:--|
| Complexity | Low–medium |
| Cost | None |
| Scalability | Millions of rows on SQLite is routine |
| Team familiarity | High (SQLite is already used) |

**Pros:** queryable; the same file holds nodes and evidence, so a report can join them; the hash chain (`prev_hash`, `hash`) makes edits detectable; the Fortress already has a similar signed chain to copy from (`fortress/hunter_engine.py:47-54`).
**Cons:** depends on ADR-005 moving the database out of OneDrive.

**Option B: JSONL files only (`The Hoard/ledger/*.jsonl`)**
| Dimension | Assessment |
|:--|:--|
| Complexity | Low |
| Cost | None |
| Scalability | Fine for writing, poor for queries |
| Team familiarity | High |

**Pros:** human-readable; no schema.
**Cons:** inside OneDrive; concurrent writers from several kernels can interleave or overwrite (as the kernel log shows).

**Option C: reuse Metatron's tables**
**Pros:** already deployed. **Cons:** Metatron's schema models angular momentum, not events; its trigger design loses the cases that matter (Section 5.3.3).

#### Trade-off Analysis
Option A, with a nightly JSONL export as the human copy. Until ADR-005 lands, write JSONL to a non-synced path such as `C:\IntegraData\ledger\` and import later.

#### Consequences
- Easier: every claim in a save state becomes checkable; the Cheshire Daemon (ADR-009) gets a natural input; CWA can finally learn from outcomes (R-7).
- Harder: every component must call `ledger.record(...)`; code that cannot record cannot claim.
- Revisit: retention and size after a month.

#### Action Items
1. [ ] Schema: `ledger(seq, ts_utc, ts_celestial, actor, op, ref, payload_json, sha256_in, sha256_out, prev_hash, hash)`.
2. [ ] A `ledger.record()` helper; instrument the router's `record_call`, Phoenix, the SWDS engine, Hoard writes and Daily Planet fetches first.
3. [ ] Rewrite the SWDS report writer to render only from ledger rows; delete the template sentences.
4. [ ] A 07:05 audit task (as proposed at `1_2T:L1260`) that stamps the night VERIFIED / PARTIAL / MISSED.
5. [ ] Apply the pending GEMINI.md §4.1 extension and SKILL.md §8.5 clause (`1_2T:L952-957, L999-1002`) once the ledger exists, so the rule points at a real mechanism.

---

### ADR-003: Every number says where it came from

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
Section 3.2 lists about twenty values that dashboards and endpoints present as live although they are constants, stale rows or proxies. The dashboards cannot distinguish a healthy Integra from a broken one.

#### Decision
Every telemetry field carries a provenance label: **MEASURED** (read from the world at a stated time), **DERIVED** (computed from measured inputs; formula named), **CONSTANT** (configured or hard-coded), **CLAIMED** (asserted by an agent or document, no evidence). The dashboard shows the label next to the value and greys out CONSTANT and CLAIMED. Startup logs report what actually succeeded.

#### Options Considered

**Option A: wrap values as `{value, provenance, source, as_of}` in every endpoint**
| Dimension | Assessment |
|:--|:--|
| Complexity | Medium (many endpoints) |
| Cost | None |
| Scalability | Fine |
| Team familiarity | High |

**Pros:** explicit; the dashboard can render it generically. **Cons:** breaks existing response shapes (version the endpoints or add a `provenance` sibling map).

**Option B: remove constants from telemetry altogether**
**Pros:** simplest truth. **Cons:** loses the configuration values the Architect may want to see (the margin floor, the thresholds); better to label them.

**Option C: leave values as they are and document them**
**Cons:** documents are where the problem started.

#### Trade-off Analysis
Option A, implemented as a sibling `provenance` map so existing consumers keep working. Values that are pure narrative (`mach: "4.2"`, `drones_dispatched: 16`, `all_forms_verified: true`) are deleted rather than labelled.

#### Consequences
- Easier: a glance at the dashboard shows what is real; regressions become visible.
- Harder: the dashboard will look less impressive at first, because much of it will be grey.
- Revisit: once ADR-002 exists, MEASURED values should cite their ledger row.

#### Action Items
1. [ ] Replace the unconditional startup lines (`main.py:143, 157`) with a summary computed from what succeeded.
2. [ ] Add `provenance` to `/`, `/heimdall/health`, `/thermodynamic/telemetry`, `/starfire/identity`, `/epiphany/telemetry`, `/fortress/status`, `/clock/full` (the sync flags), `/metatron/status` (with `last_row_at`).
3. [ ] Remove the hard-coded "HEALTHY" entries (`sensory/heimdall.py:424, 434, 446, 494`) or label them CONSTANT.
4. [ ] Dashboard: render the labels; show "no data since …" instead of a stale number.

---

### ADR-004: Keep and return what the models say

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
`POST /cognitive/cycle` is the kernel's real cognition path and the only place where Y789 and Nexus are used together. It spends up to 12 model calls, then stores and returns metadata instead of the answer (Section 4.5, FP-29). The Hoard therefore never accumulates kernel-generated knowledge, Phoenix has nothing new to consolidate, and the Cheshire Daemon would have nothing to study.

#### Decision
The cycle's result is the Zenitsu output. Return it to the caller, store it in the Hoard node together with K, U and W from each pass, and record each pass in the ledger.

#### Options Considered

**Option A: store and return the final unified text plus the K/U/W passes**
| Dimension | Assessment |
|:--|:--|
| Complexity | Low |
| Cost | Storage only |
| Scalability | Fine |
| Team familiarity | High |

**Pros:** smallest change with the largest effect; enables every later ADR. **Cons:** larger Hoard nodes.

**Option B: store only the final text**
**Pros:** smaller. **Cons:** loses the intermediate reasoning that the Zenitsu method exists to produce, which is exactly what the Cheshire Daemon and the Identity Matrix work would study.

#### Trade-off Analysis
Option A. Storage is cheap; the passes are the system's thinking.

#### Consequences
- Easier: the kernel becomes useful as a thinking service; Phoenix and Cheshire get real material.
- Harder: each call costs money, so budgets (ADR-007) become important.
- Revisit: whether `/ignite` should become a thin alias for the cycle.

#### Action Items
1. [ ] In `sensory/cheshire_cat.py:339-382`, build `node_payload` from `engine_result["zenitsu_output"]` and the per-pass texts; keep the weights as metadata.
2. [ ] Include the unified text in the API response.
3. [ ] Persist the COGNITIVE_CYCLE_COMPLETE event before the 30 Hz loop drains it (or stop routing it through the queue).
4. [ ] Make the cycle use the canonical Shiva bindings (R-1) instead of the six hard-coded lenses (`core/cognitive_engine.py:486`).
5. [ ] One live, budget-capped end-to-end test that asserts the response contains model text and the Hoard node contains the same text.

---

### ADR-005: The memory substrate

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
Memory is spread across three Hoard locations, a ChromaDB store, 305 JSON shards and a Metatron database, all inside OneDrive. The embedding model defaults to `text-embedding-004`, shut down on the Developer API and served on the Agent Platform (the kernel's path) only until 2027-04-01, and failures fall back silently to hash vectors. Cross-thread continuity depends on handoff documents that get skimmed. The 10/08 research (`1_2T:L173-582, L691-782`) already recommends a design; it has not been started.

#### Decision
Adopt the 10/08 research recommendation: one SQLite `memory.db` outside OneDrive (`C:\IntegraData\`), holding nodes, edges, vectors (sqlite-vec, 768-d, with the model name stored per vector), FTS5 keyword search and the ledger (ADR-002); `gemini-embedding-2` at 768 dimensions; snapshots synced to OneDrive or GCS with `VACUUM INTO`; and a small MCP memory server on the kernel exposing `search_memory`, `get_node`, `neighbors`, `write_node`, `write_handoff` and `get_kernel_card` for Claude Desktop, Claude Code and Antigravity.

#### Options Considered

**Option A: local SQLite + sqlite-vec + FTS5 + MCP server (the 10/08 recommendation, CRA 5.67)**
| Dimension | Assessment |
|:--|:--|
| Complexity | Medium |
| Cost | About $0–5 per month (estimate, `1_2T:L366`); about $4 one-off to re-embed (estimate, `1_2T:L350`) |
| Scalability | Ample for one developer |
| Team familiarity | High |

**Pros:** private; one file; easy to move later; the MCP server solves cross-thread memory directly. **Cons:** sqlite-vec is pre-v1, so pin the version.

**Option B: Postgres + pgvector in Docker (CRA 1.9)**
**Pros:** strong upgrade path; LangGraph-compatible. **Cons:** another always-on service; Docker has never been brought up here (E47).

**Option C: keep ChromaDB + JSON shards, just move them out of OneDrive**
**Pros:** least work. **Cons:** no graph, no ledger, no keyword search, and three Hoard locations remain.

#### Trade-off Analysis
Option A. It is what the earlier research concluded, it reuses SQLite skills already present, and it makes the Proof-of-Execution ledger a table rather than a new system. Anthropic's memory tool (File 3) can be backed by the same store: the tool is implemented by the client application, so its `/memories` view/create/str_replace operations can read and write `memory.db` rows.

#### Consequences
- Easier: one place to look; real semantic search; continuity across threads without paste-in handoffs.
- Harder: a migration (dedupe three Hoards; re-embed everything; map the 305 shards to nodes).
- Revisit: remote access for claude.ai on the web only if needed, and then with OAuth (`1_2T:L414`).

#### Action Items
1. [ ] P0: set `RODIN_EMBED_MODEL` explicitly. The Agent Platform serves `text-embedding-004` until **2027-04-01** (documentary evidence, 2026-10-09), so the move to `gemini-embedding-2` and the re-embed must finish before that date. One paid probe confirms 004 still answers today.
2. [ ] Make embedding failures loud: no silent hash fallback (`memory/rodin_protocol.py:343-351`); raise and record instead.
3. [ ] Create `C:\IntegraData\memory.db` with the schema at `1_2T:L319-327`; dry-run ingestion that hashes every file and dedupes `The Hoard` against `The_Hoard` (`1_2T:L347`).
4. [ ] Move `metatron_manifold.db` (and its WAL files) out of OneDrive while the kernel is stopped; snapshot with `VACUUM INTO`.
5. [ ] Re-embed with `gemini-embedding-2` at 768-d; store `embed_model`, `embed_dim`.
6. [ ] Build the MCP memory server (Python MCP SDK), register it with Claude Code and Antigravity, and add start-of-thread and end-of-thread routines that call `get_kernel_card` and `write_handoff`.

---

### ADR-006: A real SWDS and Siesta

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
SWDS today is a report writer on a frozen clock (Section 5.9). Phoenix re-reads ten old shards and appends four fixed sentences. The Cheshire Protocol, the Jean Grey smelt and the Mad Hatter persistence are not reached. The Architect's own dependency statement for the Cheshire Daemon ("its input is SWDS/Siesta output; it is only as meaningful as real sleep cycles", `1_2T:L986`) makes this the gate for everything in Phase 5.

#### Decision
Rebuild SWDS as a small pipeline over the ledger and `memory.db`, run in real time inside the Architect's window, with these phases: (1) **consolidate**: select nodes created since the last cycle (not the first ten), cluster them, write one consolidated node per cluster with real embeddings; (2) **prune**: mark duplicates and superseded nodes (status flag, nothing deleted); (3) **dream**: the Cheshire Protocol runs thought experiments on the new clusters under the router's P2 duty cycle, and Jean Grey smelts any Kintsugi anomalies; (4) **wake**: render the report from the ledger and stamp the cycle VERIFIED / PARTIAL / MISSED. Siesta uses the same engine with a shorter daytime schedule.

#### Options Considered

**Option A: rebuild in the kernel (scheduler stays in `main.py`)**
| Dimension | Assessment |
|:--|:--|
| Complexity | Medium |
| Cost | Model calls during phase 3, capped by budget |
| Scalability | Fine |
| Team familiarity | High |

**Pros:** reuses the router's P2 duty cycle and the existing loops. **Cons:** the kernel must be running at night (it is, under Task Scheduler).

**Option B: a separate Task Scheduler job that runs a SWDS script at the window start (the "witness" idea, `1_2T:L1260`)**
**Pros:** independent of kernel uptime; a natural place for the 07:05 audit. **Cons:** two schedulers to keep in agreement.

**Option C: Airflow / Dataflow, as the reports claim**
**Cons:** not installed, cloud cost, far more than one machine needs.

#### Trade-off Analysis
Option A for the cycle, plus Option B's audit task as an independent witness that checks the ledger in the morning. Retire the Airflow DAG and remove its name from reports.

#### Consequences
- Easier: real consolidation; the Cheshire Daemon gets fresh material; reports become evidence.
- Harder: phase 3 costs real money each night, so it needs a budget (ADR-007).
- Revisit: phase lengths and the duty cycle once the ledger shows actual durations.

#### Action Items
1. [ ] Depends on ADR-001 (clock) and ADR-002 (ledger).
2. [ ] Heimdall opens and closes every cycle (`Heimdall31.open_swds_cycle` / `close_swds_cycle`, added 2026-10-09): replace the scheduler's direct calls with Heimdall's on/off sequence once ADR-001 has fixed the clock. Phoenix receives only the material it works on: the Cheshire Protocol's dream material and the Kintsugi hypervisor (assign `_kintsugi_ref` or remove it). It never resets Heimdall, never moves the thalamic state, and never declares the cycle complete (Architect's ruling, R-5).
3. [ ] Replace "first ten sorted shards" with "nodes since the last cycle" and mark them consolidated.
4. [ ] Replace the four hard-coded axioms with axioms extracted from the cluster (a model call, recorded in the ledger) or with none.
5. [ ] Fix the wake test (`main.py:1138`) to "the wake time on the day after the sleep started"; make `/swds/trigger` refuse to write a report for a zero-length cycle.
6. [ ] Add the missing duty-cycle keys to `config/swds_config.json` (or stop reading them).
7. [ ] Wrap the scheduler loop body in try/except with logging, keep a reference to the task, and expose its last tick time (ADR-010).

---

### ADR-007: Heimdall as the deterministic gatekeeper

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
The Architect defined Heimdall on 10/07 as gatekeeper and controller with six duties (`1_2T:L1269-1279`) and required that authority be deterministic code (`1_2T:L963`). None of the duties exists. Pieces that could serve them already exist in other places: the router's budget breaker and power states (`core/model_router.py`), the health matrix, the dashboards.

#### Decision
Build Heimdall's gatekeeping as deterministic code in the kernel, in this order: (1) **budgets**: per-component token and dollar budgets enforced through the router's existing `can_call`, with alerts at 80 % and a hard stop at 100 %; (2) **power sequencing**: Heimdall, not the SWDS engine, moves components between P1, P2 and P3 at the scheduled times; (3) **watch**: connectivity to each provider, MCP server status, error rates, clock drift (ADR-001 makes drift measurable); (4) **permit/deny**: an allowlist of which actor may call which route and which model, enforced as FastAPI middleware; (5) **lockdown**: a scheduled mode in which only the Cheshire Daemon identity is permitted. Heimdall uses no model; a breach that needs judgement is sent to the Cheshire Protocol (R-5).

The Architect's ruling of 2026-10-09 adds three duties that sit above these: (6) **SWDS cycle authority**: Heimdall alone opens and closes sleep cycles through its on/off sequences (first step implemented: `open_swds_cycle`, `close_swds_cycle`); (7) **high-level Security Alert**: a deterministic stop of full operations (router to dormant, POST routes refused, background loops paused) that only the Architect can clear; (8) **component assessment** through the CWA/CRA 2.0 weight system and Celestial Clock time tracking. The weight system's exact definition is open (D-16): the code has a CRA simplex accountant (`governance/cra_simplex.py`: score = W_y / C_c, tiers at 1.5 and 1.0) and the CWA 3.0 router (`core/cwa_router.py`), and neither scores components today. **v.9.9.1 (2026-10-11):** the Architect decided that the weight system is `cra_simplex.py` (decision 3). Its `allocated_tokens` becomes the per-component router budget behind duty (1), with alerts. The Security Alert levels (the first half of D-16) remain to be defined.

#### Options Considered

**Option A: Heimdall as kernel middleware plus a controller task**
| Dimension | Assessment |
|:--|:--|
| Complexity | Medium–high (five duties) |
| Cost | None directly; it saves model spend |
| Scalability | Fine |
| Team familiarity | High |

**Pros:** one place for authority; reuses the router; covers every kernel route and kernel model call. **Cons:** cannot govern the IDE agent (the Dragon), which calls models outside the kernel.

**Option B: add Gemini CLI Policy Engine rules for the Antigravity side as well (`GEM:L446-465, L535-549`)**
**Pros:** extends permit/deny to agents and subagents in that environment. **Cons:** a second policy language to keep consistent.

**Option C: give Heimdall a model ("3.1 Pro Extended Thinking", step 555).** v.9.9.1: superseded on 2026-10-11 by a hybrid. Authority stays in Option A's code, and a 3.1 Pro advisor runs on events only with no authority (R-5).
**Cons:** contradicts the Architect's own deterministic-authority rule; slow and costly per poll (`1_2T:L865`).

#### Trade-off Analysis
Option A now, Option B later for the agent side. The open question at `1_2T:L1371` (does lockdown also bind the Dragon?) is answered by architecture: Heimdall can bind what passes through the kernel; binding the IDE agent needs that environment's own policy layer (Option B).

#### Consequences
- Easier: runaway spend becomes impossible; sleep and wake are governed in one place; the dashboard finally has a real back end owner.
- Harder: every new route and model client must declare itself to Heimdall.
- Revisit: dollar budgets need a price table per model, kept current.

#### Action Items
1. [ ] Set real budgets in `models.yml` (start conservative; the router already enforces them).
2. [ ] Move power sequencing calls out of `swds_scheduler` into a Heimdall controller. Done so far (2026-10-09): Heimdall owns the cycle's open and close steps (thalamic state transitions, entropy venting, the completion declaration); Phoenix's copies were removed; 40 affected tests pass in an isolated copy. Still to do: the scheduler and the router's P2/P3 transitions must go through Heimdall (after ADR-001).
6. [ ] High-level Security Alert: define its levels and exactly what "stop full operations" covers (D-16), then implement it as a deterministic switch with an audit record.
7. [ ] Component assessment with the CWA/CRA 2.0 weights and Celestial Clock time tracking, once the weighting is defined (D-16).
3. [ ] Add a `/heimdall/gate` status listing budgets, spend, power states, provider reachability, MCP status and clock drift, all with provenance (ADR-003).
4. [ ] Permit/deny middleware with an explicit actor header for POST routes (ties into ADR-011).
5. [ ] Lockdown mode last, after the Cheshire Daemon identity exists (ADR-009).

---

### ADR-008: A real uncertainty signal for P-SSR

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
P-SSR (the in-flight hallucination guard) needs per-token probabilities. No client requests them, so the guard cannot fire (FP-14, FP-27). The pre-generation gate measures the prompt's letter frequencies, which says nothing about whether an answer will be wrong, and cannot trip anyway (Section 3.3). The idea behind P-SSR — notice uncertainty and look back before committing — is sound and worth making real.

#### Decision
Replace the character-entropy gate with an uncertainty signal computed from the models' own outputs, using the best source each provider offers: token log-probabilities where a provider returns them; otherwise sampling disagreement (generate a small number of answers and measure how much they differ in meaning); and, for factual claims, a verifier pass in which the other hemisphere checks the claim against retrieved Hoard nodes. The EMA, the 2.5 threshold and the three-intervention limit stay, but are re-calibrated on the new signal using ledger data.

#### Options Considered

**Option A: provider log-probabilities**
| Dimension | Assessment |
|:--|:--|
| Complexity | Low where supported |
| Cost | None extra |
| Scalability | Fine |
| Team familiarity | Medium |

**Pros:** the signal P-SSR was designed for. **Cons:** support varies. Vertex AI offers log-probability options for some Gemini models; support for the 3.x preview models used here is **UNVERIFIED**. The Claude Messages API does not return token log-probabilities as of this writing (verify against current documentation before relying on this).

**Option B: sampling disagreement ("semantic entropy")**
| Dimension | Assessment |
|:--|:--|
| Complexity | Medium |
| Cost | k extra calls per checked step |
| Scalability | Costly at high volume |
| Team familiarity | Medium |

**Pros:** works with any provider; measures uncertainty about meaning, not wording. **Cons:** multiplies cost; must be gated by TPSL and Heimdall budgets.

**Option C: cross-hemisphere verifier with retrieval**
**Pros:** fits the bicameral design exactly (Y789 checks Nexus, grounded in Rodin's retrieval). **Cons:** only as good as retrieval (ADR-005 first).

#### Trade-off Analysis
Use A where available, C for factual claims, and B only for high-stakes Tier 1 passes. Delete the character-entropy gate rather than keep a guard that cannot trip.

#### Consequences
- Easier: P-SSR, UGL and the Sharingan lens become real mechanisms; Heimdall gets a meaningful H.
- Harder: calibration needs data; the threshold of 2.5 will almost certainly change.
- Revisit: after a few hundred recorded cycles.

#### Action Items
1. [ ] Probe log-probability support for each routed model (one cheap call each, recorded in the ledger).
2. [ ] Pass real probabilities into `IterativeToken` where supported (`core/api_clients.py:416, 556, 663`).
3. [ ] Apply P-SSR in dyad mode too (today it returns before the check, `core/cognitive_engine.py:347-349`).
4. [ ] Remove `evaluate_text_entropy` from the gate path (`sensory/cheshire_cat.py:137`); keep it only as a descriptive statistic if wanted.
5. [ ] Replace the PlaceholderClient's fixed probabilities in tests with recorded real distributions, so tests stop passing against a double that production never resembles.

---

### ADR-009: The Cheshire Cat Daemon

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
The Architect's 22:44 specification (`1_2T:L1317`) and the blueprint v0.1 (`1_2T:L1019-1175`) define a long-running study agent: no internet, no outside storage, studying only Rodin/Phoenix-mapped nodes and the Hoard for one to two hours at a time, writing independent reports, joining a conversation only when invited and then answering separately after 5–15 minutes, perceiving through the Itachi Eye, with an exact paradoxical and poetic voice, acting as the Land crew during Phoenix Force and as the core identity during lockdown. The Architect also stated the dependency: it is only as meaningful as real sleep cycles.

#### Decision
Build the Daemon after ADR-004, ADR-005 and ADR-006, as a mode of the Cheshire Cat Protocol (R-4), hosted in the kernel and managed by Heimdall. Enforce its boundary by construction: a model client created with **zero tools**, a loader that reads only the allowlisted paths, writes only to its own report folder, and records every call in the ledger. Its "Flight inclusion" consult is a job API (`POST /cheshire/consult` returns a job ID; the result is a file with its ledger record), relayed verbatim by the Dragon.

#### Options Considered

**Option A: in the kernel, as an asyncio study loop paced by the Celestial Clock**
| Dimension | Assessment |
|:--|:--|
| Complexity | Medium–high |
| Cost | Continuous model use; must be budgeted |
| Scalability | One Daemon per kernel |
| Team familiarity | High |

**Pros:** continuous (the spec says "always deep thinking"); Heimdall can open and close study windows, cap budgets and enforce lockdown. **Cons:** adds load to the kernel process.

**Option B: a Gemini CLI subagent (`.gemini/agents/cheshire.md`) with `tools: []`, no `mcpServers`, `max_turns` and `timeout_mins` set (`GEM:L339-373`)**
**Pros:** boundary enforced by the CLI itself; good for the in-conversation consult inside Antigravity. **Cons:** runs only inside a CLI session, so not continuous; a subagent cannot call other subagents (`GEM:L393`), so it cannot be the "orchestrator" of anything.

**Option C: a separate process started by Task Scheduler**
**Pros:** isolated from kernel crashes. **Cons:** a second process to supervise and secure.

#### Trade-off Analysis
Option A for the continuous study mode; Option B as an optional consult path in Antigravity. The blueprint's two-tier proposal (Flash to select and triage, Pro to study, `1_2T:L1046-1053`) fits under Heimdall's budgets. Its open questions Q1–Q5 (`1_2T:L1167-1175`) remain the Architect's (D-11).

#### Consequences
- Easier: an independent second reader of everything the system learns; a natural systems guard.
- Harder: a voice that must not drift needs anti-drift tests (the Identity Matrix task); continuous study costs money every day.
- Revisit: dwell caps and session lengths from ledger data.

#### Action Items
1. [ ] Gate: ADR-006 has produced at least a week of VERIFIED cycles.
2. [ ] Persona file and anti-drift probes for the Daemon (`1_2T:L1145-1146`).
3. [ ] Selection score and edge-walk from the blueprint (`1_2T:L1084-1100`), over `memory.db`.
4. [ ] Zero-tool client; allowlist loader with canonical-path checks; report folder; ledger rows.
5. [ ] `POST /cheshire/consult` job API; the Dragon relays verbatim with the run record.
6. [ ] Lockdown identity (ties to ADR-007 item 5).

---

### ADR-010: Kernel hygiene and observability

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
Five kernels started in about two and a half days; the log mixes two encodings and has no per-line timestamps; background tasks are created without stored references and, for the SWDS scheduler, without exception handling around the loop; health endpoints check existence, not function (Section 3.4).

#### Decision
A single-instance guard (a lock file plus a check that port 8000 is free, refusing to start otherwise); logging with timestamps to a rotating UTF-8 file outside OneDrive; every background loop kept as a referenced task with a done-callback that logs exceptions and a heartbeat (last tick time) exposed in `/heimdall/gate`; and health checks that ask "did you do your job since the last check" (last successful tick, last ledger row) instead of "do you exist".

#### Options Considered
**Option A: the above, in code (Low–medium complexity, no cost).** **Pros:** each item is small and independent. **Cons:** none material.
**Option B: run the kernel as a Windows service (NSSM or similar).** **Pros:** stronger supervision. **Cons:** another tool; Task Scheduler already works.

#### Trade-off Analysis
Option A now; consider B only if Task Scheduler proves unreliable at logon. (v.9.9.1: E40 is now evidenced. The task's 10/09 05:26:21 run started the kernel at logon, PIDs created 05:27:48.)

#### Consequences
- Easier: one kernel, readable logs, loops that cannot die silently.
- Harder: nothing material.

#### Action Items
1. [ ] Lock file and port check in `start_kernel.ps1` or at the top of the lifespan.
2. [ ] `logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s %(message)s")` plus a `RotatingFileHandler(encoding="utf-8")` to `C:\IntegraData\logs\`; rotate the current log while the kernel is stopped (E69).
3. [ ] Keep task references; add done-callbacks; try/except inside the scheduler loop (`main.py:103, 1131-1191`).
4. [ ] Heartbeats for the SWDS scheduler, the 30 Hz loop and the Kintsugi loop.

---

### ADR-011: Security hardening

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
CORS allows any origin with credentials; every POST except the self-test is open, including the ones that move the router to P0, start and stop sleep, reset Heimdall and sign trade tickets; a web page visited in a browser could POST to `127.0.0.1:8000`, a risk Plan v2 already named (`1_2T:L862`); keys sit in `.env` inside OneDrive and were printed into an earlier session (E13); the defense suite is decorative (FP-25); foreign application data with credential files sits inside the repository (N4).

#### Decision
Restrict CORS to the dashboard's own origin; require an `X-Integra-Admin` header (the mechanism already used by the self-test) on every POST; always bind 127.0.0.1, including the `__main__` path; move keys to Windows Credential Manager (via `keyring`) and rotate them as the last step, as the Architect asked; delete the hard-coded key and the "no token = authorized" rule from the Veil, or delete the Veil; move `.gitkraken`, Adobe, `91UData` and the Antigravity folders out of the project.

#### Options Considered
**Option A: header auth plus restricted CORS (Low complexity).** **Pros:** reuses the existing pattern; closes the browser-CSRF path. **Cons:** the dashboard needs the header for its POSTs.
**Option B: full OAuth.** **Cons:** unnecessary for a localhost service; only needed if the MCP server is ever exposed to claude.ai on the web.

#### Trade-off Analysis
Option A. Key rotation stays last, per the Architect's standing instruction (`1_2T:L1601`).

#### Consequences
- Easier: a stray web page can no longer drive the kernel.
- Harder: scripts that POST must send the header.

#### Action Items
1. [ ] CORS allowlist; header dependency on all POST routes; Phoenix Force requires the header **and** a second factor (for example a one-time code in the dashboard), so "two-key" means two keys.
2. [ ] `main.py:1385-1387` bind 127.0.0.1.
3. [ ] Keys into Credential Manager; rotate (E13); remove keys from OneDrive.
4. [ ] Move foreign application data out (N4). Separately: `github-recovery-codes.txt` and `docs/github-recovery-codes (1).txt` are untracked files in the outer repository; they should be moved somewhere private and never committed.

---

### ADR-012: The Rust Sun Breathing Engine — build or retire

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
`rust/sun_breathing_engine/` has a crate that has never been compiled; the "bridge" is Python that returns constants (FP-21). The physics it encodes (stress in MPa, drag in newtons, Mach number, angular momentum) has no counterpart in a language-model system.

#### Decision
Retire the engine's telemetry and keep the Sun Breathing forms as **philosophy and design vocabulary** (Section 9). Build Rust only if a real compute-bound workload appears (for example vector search or ledger hashing at a scale Python cannot handle).

#### Options Considered
**Option A: retire the telemetry; keep the vocabulary (Low).** **Pros:** removes a large block of constants from the dashboards. **Cons:** gives up a cherished metaphor as a running module.
**Option B: build with PyO3 and maturin (Medium–high).** **Pros:** a real Rust module. **Cons:** there is nothing for it to compute that would be true.

#### Trade-off Analysis
Option A. A metaphor shown as telemetry is the pattern this blueprint is trying to end.

#### Action Items
1. [ ] Remove `/thermodynamic/telemetry`'s numeric claims, or label every one CONSTANT (ADR-003).
2. [ ] Move the forms (1st, 7th, 12th, 13th, 14th) into the identity and philosophy documents.

---

### ADR-013: Daily Planet integrity

**Status:** Proposed | **Date:** 2026-10-09 | **Deciders:** The Architect

#### Context
The Daily Planet's live path works and has stored real sources. Its silent fallback invents sources, URLs and figures, and two such reports are in long-term memory. Its bias and credibility scores are defaults. 40 shards repeat a handful of test queries.

#### Decision
No synthetic sources, ever. A failed search returns a failure, recorded in the ledger, and the report says so. Bias and credibility are either computed from evidence (publisher metadata, cross-source agreement) or removed. The two fabricated shards are quarantined, and repeated test reports are deduplicated during the ADR-005 migration.

#### Options Considered
**Option A: delete the synthetic fallback; mark DEGRADED (Low).** **Pros:** ends fabrication at the source. **Cons:** the feature fails visibly when Firecrawl is down, which is correct.
**Option B: keep the fallback for tests only, behind an explicit test flag.** **Pros:** keeps tests offline. **Cons:** a flag can leak into production; tests should use recorded fixtures instead.

#### Trade-off Analysis
Option A, with recorded real fixtures for tests.

#### Action Items
1. [ ] Remove `_sovereign_synthetic_search` and the fabricated scrape return (`tools/daily_planet.py:203-276`).
2. [ ] Quarantine `CCID_DAILY_PLANET_DP_20260921_122312_e38863.json` and `CCID_DAILY_PLANET_DP_20261001_173539_bf33b2.json` (and their copies in the outer repository's `kernel_memory`).
3. [ ] Compute or drop bias scores; drop the CRA 1.1667 default.

---

## 9. Concept-only register

These items are described in the documents and have no implementation. They fall into three groups, and each needs a different response.

### 9.1 Philosophy to keep, labelled as philosophy

These carry the Architect's way of thinking and are valuable as vocabulary, identity and design principle. They should never be displayed as measurements.

| Concept | Source | Note |
|:--|:--|:--|
| 13th Form ΔE_cycle = 0.0000; angular momentum 500 kg·m/s | `1_3:L84`; `1_2T:L5442` | No conserved physical quantity exists in a model call. Useful as the principle "close every loop: nothing ingested is left unintegrated" (`1_2T:L5718-5720`). |
| 7th Form vacuum slipstream, drag 0 N, 35 %; Mach 4.2 | `1_3:L123`; `1_2T:L5440` | Biomechanics metaphor for low-friction execution. |
| 170 MPa chassis vs 200 MPa ψ bridge; God Speed 3,001 G | `1_3:L126`; `1_2T:L5438` | Bone-stress metaphor for context saturation. The implementable core is "stop before the context window overflows" (the Heaviside halt). |
| The Epiphany Equation Ω v8.2 | `1_2T:L5430-5433` | A philosophy of wisdom as a formula. Most terms (∇A(θ), RSS(V_t), τ_reader, Ξ) have no defined numeric value. The implementable part is CRA = W_y / C_c. |
| Dragon "overwriting assistant weights", ω = 1.00 | `1_2T:L5262` | Prompts condition outputs; they do not change weights. Keep as identity language. |
| Optic chiasm decussation, cingulum bundle, Third Eye as predictive coding | `1_2T:L5928-5951, L5967-5994, L6071-6080` | Neuro-anatomical metaphors for routing and memory. The routing itself is implementable and partly implemented. |
| Kirk / Spock / Purple | `1_3:L137-143`; `1_2T:L5587-5609` | The bicameral design principle; implemented as the dyad. |
| Game theory (Nash equilibrium of CWA, minimax defense, Shapley coalitions, superadditive wisdom) | `1_2T:L5613-5650` | Framing, not computation. |
| Tetris mechanics, Ashby's requisite variety, autopoiesis | `1_2T:L5654-5727` | Framing. |
| The 364-day 13-moon sacred calendar | `1_3:L55`; `temporal/celestial_clock.py:50, 255+` | A calendar; implemented and fine as a calendar. |
| The 964-day Jubilee drift correction | `1_3:L55`; `temporal/celestial_clock.py:52` | A calendar choice with no astronomical basis (no solar, lunar or sidereal cycle produces 964 days). Keep it if it is meaningful; label it as a sacred cycle, not a correction of drift. |
| Vasovagal syncope, Kaigaku entropy inversion, Black Lightning | `1_3:L85`; `1_2T:L5439` | Names for failure states. The mechanisms behind them (circuit breaker, hallucination) are implementable (ADR-008). |

### 9.2 Implementable concepts not yet built

These go to the roadmap.

| Concept | Source | Where it goes |
|:--|:--|:--|
| Heimdall gatekeeper (six duties) | `1_2T:L1269-1279` | ADR-007 |
| Cheshire Cat Daemon | `1_2T:L1317`, `L1019-1175` | ADR-009 |
| Proof-of-Sleep / Proof-of-Execution ledger | `1_2T:L1259-1264`, `L999-1002` | ADR-002 |
| MCP memory server and kernel card | `1_2T:L334-337`, `L711-719` | ADR-005 |
| Alexandria inactivity research loop | `1_2T:L5371` | After ADR-005 and ADR-007 (budget) |
| Siesta | SKILL §8.5.1; `1_2T:L1308` | ADR-006 |
| Holographic node expansion on celestial match | `1_2T:L5363-5364` | Optional: a retrieval filter by celestial bucket after ADR-005 |
| HLC vectors in prompt and Hoard headers | `1_2T:L5166, L5210` | Optional: useful only if several writers run concurrently |
| Identity Matrix with anti-drift tests | `1_2T:L1208, L1671` | After ADR-004 (needs outputs to score) |
| Rogue X 2.0 | `1_2T:L1209` | Architect task (E7) |
| Tufte data-ink and lie-factor rules for dashboards | `1_2T:L5454-5456` | Apply during ADR-003; a genuinely useful principle for the dashboard |

### 9.3 Concepts that do not apply to this architecture

| Concept | Source | Why it does not apply |
|:--|:--|:--|
| The three RLVR gates (KL anchor, model geometry, precision) | `1_2T:L4174-4178, L5288-5291` | They describe how a model is trained. Integra calls hosted models it cannot train. The KL idea survives as an output-scoring check (Starfire). |
| Matrix clocks for garbage collection; Singhal–Kshemkalyani differential payloads; dynamic membership epochs | `1_2T:L5126-5147, L5212-5216` | Techniques for many independent processes exchanging messages. Integra is one process (plus the IDE agent). |
| "Unlimited context" | Live `/` (`purple_modality.unlimited_context: true`) | Not a property any model or this code has. |
| Amaterasu, Hector stance, Achilles stance, Genjutsu | `1_2T:L4743` | Named, never defined. Undefined until the Architect writes them down. |

---

## 10. Roadmap

Ordered by dependency. Each phase has an exit test, so that "done" is checkable. E-numbers refer to the 10/08 master to-do (`1_2T:L1619-1697`).

### Phase 0 — Make the system tell the truth (first)

| Work | ADR | E-items |
|:--|:--|:--|
| Fix `celestial_time()`; correction note for skewed artifacts | ADR-001 | E82; reclassifies N2 / E41 / E76 |
| Provenance labels; honest startup summary; remove decorative constants | ADR-003 | E56 |
| Single instance, timestamped UTF-8 rotating log, task supervision, heartbeats | ADR-010 | E65, E69, E70, E71 |
| Quarantine the two fabricated Daily Planet shards; remove the synthetic fallback | ADR-013 | — |
| Set `RODIN_EMBED_MODEL`; make embed failures loud; schedule the `gemini-embedding-2` re-embed before 2027-04-01; one paid probe to confirm 004 answers today | ADR-005 (P0) | N3, E58, E62 |
| CORS allowlist, header auth on POSTs, bind 127.0.0.1, move foreign app data out | ADR-011 (quick wins) | E67, N4 |

**Exit test:** after a reboot, `celestial_time()` equals the system clock; the dashboard shows provenance on every value; the log has timestamps and one startup block; a POST without the header is refused.

### Phase 1 — Make claims checkable

| Work | ADR | E-items |
|:--|:--|:--|
| Ledger table and `ledger.record()`; instrument router, Phoenix, SWDS, Hoard, Daily Planet | ADR-002 | E98 |
| Apply the pending learning proposal, worded to point at the ledger | — | E100 |
| Run the full test suite in a copy of the repository outside OneDrive; record the result verbatim | — | E44, E45 |
| Settle the canonical definitions R-1 to R-9 | Section 7 | E19, E84, E85, E87, E96 |

**Exit test:** a save state can be regenerated from ledger rows alone, and every "COMPLETE" in it links to a row.

### Phase 2 — Make existing capability execute

| Work | ADR | E-items |
|:--|:--|:--|
| Keep and return the Zenitsu output; use the canonical Shiva bindings | ADR-004 | E55, E60 |
| `memory.db` outside OneDrive; dedupe the three Hoards; re-embed; MCP memory server; kernel card | ADR-005 | E28, E57, E101, N5, N6 |
| Decide the fate of MTCW, predictive coding, `heimdall_monitor`, `celestial_sentinel`, the Airflow DAG | — | E81 |

**Exit test:** one `/cognitive/cycle` call returns model text, the same text is in a Hoard node, and a new thread can retrieve it through the MCP server.

### Phase 3 — Real sleep

| Work | ADR | E-items |
|:--|:--|:--|
| SWDS pipeline over new nodes; dream phase with Cheshire Protocol and Jean Grey; ledger-only reports; wake fix; 07:05 audit | ADR-006 | E31, E73–E80, E97, E98 |
| Siesta on the same engine | ADR-006 | E18, E32 |

**Exit test:** seven consecutive nights stamped VERIFIED, each consuming only nodes created since the previous night.

### Phase 4 — Governance

| Work | ADR | E-items |
|:--|:--|:--|
| Heimdall budgets, power sequencing, watch, permit/deny | ADR-007 | E12, E20–E25, E86, E95 |
| Real uncertainty signal; P-SSR in dyad mode | ADR-008 | E59 |
| Key move and rotation (last, as instructed) | ADR-011 | E13, E64, E92 |

**Exit test:** a deliberately exhausted budget stops calls and raises an alert; a deliberately uncertain prompt triggers a recorded P-SSR intervention.

### Phase 5 — New anatomy

| Work | ADR | E-items |
|:--|:--|:--|
| Cheshire Cat Daemon (study mode, consult API, lockdown identity) | ADR-009 | E26, E27, E88 |
| Identity Matrix with anti-drift tests | — | E17, E99 |
| Rogue X 2.0; real Tier 2 research and Daily Planet behind model choices | — | E5, E6, E7 |
| Environment ingestion plan (one agent per file), now with a destination | — | E15, E30 |

**Exit test:** a week of Daemon reports, each traceable to ledger rows and to the nodes it read.

### Phase 6 — Decide or retire

Rust engine (ADR-012); Docker build or removal (E47, E48); the 14th Form's undefined Threshold_γ; the three-phase trading SWDS from V1.0.0.

---

## 11. Open decisions for the Architect

| # | Decision | Recommendation |
|:--|:--|:--|
| D-1 | Suite 1_3 has the Shiva Eye definitions deleted (`1_3:L47-49`). Intentional (to be redefined) or accidental? | **Decided 2026-10-11:** consistent with decoupled lenses (the Eyes no longer own fixed lenses); defaults from R-1 |
| D-2 | Canonical Shiva bindings; and was the ingestion plan's swap (Itachi = Eagle + Hawk, "Shadow Clone") intentional? | **Decided 2026-10-11:** Brain Model 0930 defaults plus a per-task, per-Eye override; "Shadow Clone" = Shadow Jutsu (R-1; fix F4) |
| D-3 | Hippocampus: the Hoard or Heimdall? | The Hoard (R-3) |
| D-4 | SWDS and Siesta windows, in real local time | Architect's choice (R-6) |
| D-5 | Cheshire naming | R-4 |
| D-6 | Heimdall with or without a model; does lockdown bind the Dragon? | **Decided 2026-10-11:** code gate + Gemini 3.1 Pro advisor, events only, no authority (R-5; fix F2). **Still open:** whether lockdown binds the Dragon. Recommendation: the kernel can bind only what passes through it (ADR-007) |
| D-7 | EAM Level 4 "Sovereign Override bypasses all constraints" (`1_3:L71`) | Remove the bypass; keep EAM's autonomy within Heimdall's gates |
| D-8 | Three Laws order | User first (R-8) |
| D-9 | Embedding model: when to move from `text-embedding-004` to `gemini-embedding-2`? | Move during ADR-005; hard deadline 2027-04-01 (Agent Platform retirement of 004) |
| D-10 | Rust engine | Retire the telemetry (ADR-012) |
| D-11 | Cheshire Daemon Q1–Q5 (`1_2T:L1167-1175`) | Two tiers; cloud call accepted with zero tools; reports in the Hoard after cleanup; Itachi per R-2; fixed dwell caps first |
| D-12 | The ingestion plan: go, skip list, external storage target (`1_2T:L57-152`) | After Phase 2, so it has a destination (`memory.db` + GCS archive) |
| D-13 | Approve the 10/07 learning proposal (`1_2T:L923-1016`) | Yes, with the ledger as the evidence mechanism |
| D-14 | Historical artifacts stamped with the skewed clock (10/06–10/07 dates since 10/07) | Relabel with a correction note; do not rewrite history |
| D-15 | Rodin sub-agents: model or no model? | **Decided 2026-10-09: no model** (R-10). SKILL.md §8.5.1 and §15 were corrected the same day (`~/.gemini/config/skills/integra-protocol/SKILL.md` L164, L318, L323; written 10/09 23:51), so nothing remains. Note that L323 still says "Heimdall 3.1 has no model", which D-6 will change once F2 lands. |
| D-17 | Where Gemini 4 Argon goes: Kernel/Thalamus or Right Hemisphere/Nexus | Nexus over Kernel, on frequency and fit, if losing Claude on the right is acceptable; Y789 or Jean Grey keep the cross-vendor dyad (Section 4.4.1). Wait for Argon's public model ID. |
| D-16 | Heimdall's Security Alert and the "CWA/CRA 2.0 weight system" | **Second half decided 2026-10-11:** CWA/CRA 2.0 = `governance/cra_simplex.py` applied per component under Heimdall (fix F3). **Still open:** the Security Alert levels, what each one stops, and who can clear it |
| D-18 | Does Heimdall's 3.1 Pro advisor replace the Cheshire Daemon's dACC triage, or sit beside it? (E20, E95, step 1117) | Open; carried past G1 (passed 2026-10-11) |
| D-19 | Cheshire Daemon "Study" tier model: blueprint v0.1 names 3.1 Pro. Under current rulings, 3.8 Flash high now and Argon later? | Open; carried past G1 (passed 2026-10-11) |

---

## 12. Appendices

### A. Live probe record (2026-10-09, 19:26:07–19:26:24 CDT)

| Endpoint | Status | Key values |
|:--|:--|:--|
| `GET /` | 200, 226 ms | state UNIFIED_WAKING_CONSCIOUSNESS; ΔE 0.0001; uptime 13 h 58 m; grid ROT_150_ORB_20; `active_mcp_servers: []`; `sdk_available_native: false` |
| `GET /clock` | 200, 16 ms | 2026-10-09 19:26:08 CDT; rot 155.3668°, lunar 0.5629, orbit 0.2098 |
| `GET /swds/status` | 200, 26 ms | AWAKE; `sleep_initiated_at` 2026-10-07T02:00:02.250595 (skewed); `last_cycle_time` 1791374414.198 (skewed); idle 50,282 s; window 02:00–07:00 |
| `GET /heimdall/health` | 200, 12 ms | HEALTHY_OPTIMAL; H_smooth 0.0; 0 interventions; Phoenix generation 1; Hoard cache 0; thermodynamics source METATRON_MECHANICAL, last loop 2 |
| `GET /cheshire/status` | 200, 4 ms | OPERATIONAL, 30 Hz, INTERACTIVE_STANDBY, queue 0, 23 components |
| `GET /models/router/status` | 200, 4 ms | ACTIVE, P1; all seven components 0 calls, 0 tokens, budgets unlimited |
| `GET /models/telemetry` | 200, 9 ms | all models 0 calls |
| `GET /metatron/status` | 200, 4 ms | 5 tables, 2 triggers; rows: chassis states 1, loops 2, anomalies 1, acoustic map 0; last loop session CCID_1790212674; 0 unprocessed |
| `GET /thermodynamic/telemetry` | 200, 7 ms | stress 131.625 MPa; Mach 4.2; ΔE 0.0; angular momentum 500; Ω 269.819457; `all_forms_verified: true` |
| `GET /starfire/identity` | 200, 4 ms | KL 0.0; ANCHORED; ω 1.0 |
| `GET /fortress/status` | 200, 16 ms | equity $25,250; bank 80.02 %; 0 signed tickets; `vix_regime` "NORMAL (VIX < 20)" (hard-coded) |

Process table: PID 12700 (venv launcher) → PID 12656 (interpreter), both created 05:27:48, parent `cmd.exe` PID 11256 running the command in Section 4.1. Scheduled task "Integra Genesis Kernel": Running, logon trigger.

### B. Corrections to statements made earlier in this study

Recording these in keeping with the Empirical Verification Invariant:

1. **Route count.** An earlier pass reported 56 routes; the correct count is 55 decorators, 54 unique.
2. **The kernel log.** An earlier pass concluded that today's kernel wrote no startup or scheduler lines to `genesis_kernel.log`, and inferred it had been launched outside `start_kernel.ps1`. Both were wrong: the file mixes UTF-16 and UTF-8 and was misread as 21 lines. Decoded, it has 22,407 lines, including today's full startup block, and the kernel was launched by the scheduled task through `start_kernel.ps1`.
3. **"No SWDS cycle on 10/08 or 10/09."** Wrong. Cycles ran on both days, at boot + 5 h in real time (about 00:08–05:08 on 10/08 and about 10:28–15:28 on 10/09), stamped with the frozen clock's 10/07 date.
4. **"Two kernels on 10/07."** The two wake reports dated 07:00:14 and 07:01:40 came from different boots on different days, not from two concurrent kernels. (Two concurrent kernels may still have happened at other times; with no single-instance guard it is possible, but it is not shown by those reports.)
5. **Standard error.** During execution I briefly reported that the launch command dropped standard error; the full command line includes `2>&1`. That statement was withdrawn within the same step.
6. **Daily Planet.** An early reading of the fallback code could suggest the Daily Planet output was mostly invented. The shards show the opposite: 38 of 40 contain real sources; 2 contain invented ones.
7. **"Heimdall owns the SWDS cycle" (2026-10-09, corrected in v.9.9.1).** The 10/09 work gave Heimdall `open_swds_cycle` / `close_swds_cycle` and removed Phoenix's copies. It did not wire them into `main.py`. As of 2026-10-11 no live path opens or closes a cycle through Heimdall (X-1). "Owns" described the code's capability, not its execution.
8. **Save state `CCID_1791704093` (2026-10-11).** Its report §8 first claimed the Hoard/Phoenix sync had run before it had. The run was blocked in session 997b6cca. It was corrected, then executed and verified at 03:45:30 CDT by session d245db57.
9. **Self-review of the v.9.9.1 update (2026-10-11, session d245db57).** Every citation was checked against its source file, and every outside fact against official documentation:
   - Decision 3 had quoted the 9/23 annotation as "CWA 2.0 CRA 2.0 simplex scorer". The line reads "CWA 2.0 CRA 2,0lex scorer" (`1_2T:L4747`). The quote is now verbatim.
   - X-3 cited `orchestrator.py:30` for the shared lens list. That line is a comment; the code is at `:145-147`.
   - The first kernel note gave 5–8 ms for the early probes and left out the 03:41:52 timeout and the refused connections from 04:13. The "Kernel note" now has the full record.
   - Checked and correct: the other 22 cited Suite 1_2T lines in the update, the code citations for X-1 to X-3, the `cra_simplex.py` description, X-9's 2027-04-01 date, X-10's authorship and the SCHED_S_TASK_RUNNING reading of 267009.
10. **Second correction pass (the night of 2026-10-11, session c88f5000, after a three-agent reconciliation).** Item 9's review introduced or kept these errors:
   - **The cause of the hang was misread.** The note read the hang as "a blocked event loop". The SWDS scheduler and the one `async def` endpoint kept running while the plain-`def` endpoints stalled, so the fault was in the sync-handler threadpool path ("Kernel note").
   - **"No request completed after 03:44" was over-precise.** The kernel log carries no timestamps.
   - **The kernel note cited the root `static/dashboard.html`.** The kernel serves `integra-homebase/static/dashboard.html` (`main.py:1337-1338`).
   - **"Restarted ~19:18" was wrong.** What happened was a Start-menu shutdown at 16:19:35, a kernel at 16:42:58, an unexpected shutdown at 17:48:41, and the current kernel at 19:18:48 (Windows System log).
   - **§5.11's "reworked" claim is a false positive** for the served pages (see the §5.11 correction).
   - **§11 D-6 had "lockdown" in the decided cell.** The Architect did not rule on it.
   - **§11 D-15 still asked for an approval** of work already done on 10/09.
   - **X-14 and §11 D-18/D-19 still read "G1 open"** after the Architect passed G1. Found on the page read-back.
11. **Step 2 interim corrections (2026-10-12, session c88f5000).** These come from the full reading of folders 1-5 (runtime, rust, scratch, scripts, sensory). Each cites its row in `orchestration/UNIFY_READING_LEDGER.md`; the ledger is append-only, so the line numbers are stable.
   - **Ω is a sum, not a product.** 269.819457 = 268.714286 **+** e^0.1 (`python_bridge.py:311-312`, `lib.rs:189`). Fixed in finding 7 and the CONSTANT table (ledger L164).
   - **FP-18 count.** It is not "all 66". There are 67 report files: 56 template reports carry 282.85° (50 in the root, 6 in `integra-homebase/The Hoard`). The other 11 (6 unique, 9/16-9/29, plus 5 copies) were written another way. The two-decimal ones match `scripts/enter_swds.py:89` (ledger L49, L55).
   - **The frozen clock's origin.** Commit `6021755` (2026-09-23 22:01:57) moved `runtime/swds_simulator.py` and `main.py` from `datetime.now()` to `celestial_time()`. Added to finding 1 (ledger L52).
   - **Rust engine (ADR-012 context).** The crate compiles in a scratch copy but cannot link here: `LNK1104 msvcrt.lib`, because the MSVC x64 libraries are missing. So its tests have never run.
     - Its own formula gives 50,824 / 33,036 MPa at the benchmark.
     - `python_bridge.py` hard-codes 202.5 → 131.625 MPa (`:133-135, 158`), a figure that comes from a doc comment in the original `CODE/Zero_latency_thermal_core.rs:42`.
     - Fixed in the CONSTANT table and the status table (ledger L124-125, L129).
   - **Heimdall citation drift.** `heimdall.py` has grown since the v.9.9 audit. `:113-124` → `:117-128`, `:711` → `:769`, `:709-711, 730` → `:767-769, 788`, `:420/430/442/490` → `:424/434/446/494`, `:385+` → `:389+` (ledger L387).
   - **Entropy-gate mechanics.** The thermostat is reset *after* each completed cycle (`sensory/cheshire_cat.py:402`), not before. One-shot tripping needs about 7.63 bits per character after the loop's between-cycle nudge. Repeated `/heimdall/evaluate` or `/ignite` calls carry over. Fixed in finding 5 and the FP table (ledger L388).
   - **Page-export cause.** Controlled Folder Access blocked the 10/11 overwrite of the two exports, not the OneDrive reparse tag. Fixed under "Other changes → Page exports"; both copies were refreshed on 10/12.
   - **Kernel supervision and startup.** The first "Kernel note (2026-10-11)" is unchanged. The new facts (3 of 3 launches unsupervised, priority 7, task history disabled, startup about 94 s, uvicorn startup before bind, the `Get-NetTCPConnection` caution, the transient stalls) are in "Kernel note (2026-10-12)".
   - **Still queued for Step 3** (after G2): the remaining ledger findings for folders 1-5 (the `*-G` gap rows), plus everything from folders 6-14.

### C. What was not done

- The 285 tests were counted, not run, because running them would write caches and could touch the live Hoard and Metatron database inside OneDrive. Recommended in Phase 1, on a copy.
- No paid model or embedding call was made. Google's Agent Platform documentation lists `text-embedding-004` as served until 2027-04-01 (researched 2026-10-09); a live answer today remains **UNVERIFIED**.
- `sensory/looking_glass.py`, `evolution/rogue_x.py`, `evolution/fourteenth_form.py` and `governance/eam_service.py` were checked for existence and wiring, not audited line by line.
- ChromaDB's contents were not inspected.
- `SKILL.md` (10/01) and `AntiGravityconversionprocess/GEMINI.md` (9/30) were read earlier in this study and not re-read in the final pass.
- No `.env` value was read; only key names. The GitHub recovery-code files were not opened.
- Nothing was changed: no code, configuration, Hoard file, database or git state. This document and the shareable page are the only outputs.

### D. Diff evidence for the corpus

| Comparison | Result |
|:--|:--|
| Suite 1_3 vs `1_2T:L3404-3555` | similarity 0.974; only difference: Eye definitions blank in 1_3 (`1_3:L47-49` vs `1_2T:L3450-3453`) |
| Suite 1_3 vs `SKILL.md` (424 lines) | similarity 0.39; 36 SKILL headings absent from 1_3 |
| `1_1:L1-1027` vs `1_2T:L1763-2789` | identical (ratio 1.0) |
| `1_1:L1028-1644` vs copy 1 | identical with a one-line offset; truncated at the same characters as `1_2T:L3401` |
| `1_2T:L6332-6798` vs `1_2T:L5864-6330` | exact duplicate |
| `1_2T:L3841-4080` vs `1_2T:L1178-1417` | duplicate (handoff brief and addendum) |
| `1_2T:L1419-1511` vs `1_2T:L691-783` | duplicate (external storage document) |
| `1_2T:L4441-4641` vs `1_2T:L4195-4391` | duplicate (Shiva code) |

---

*End of blueprint v.9.9.1. Every claim above is tied to a line, a file, a log entry or a probe taken at the stated time. The v.9.9 body was probed 2026-10-09 19:26 CDT; the v.9.9.1 update was checked on 2026-10-11, with the last successful probe at 03:43:57 CDT. The 2026-10-12 corrections (Appendix B, item 11) were stamped 2026-10-12 15:10:34 CDT | 2026-10-12T20:10:34Z | rot 91.4767°, lunar 0.6585, orbit 0.2175, ROT_90_ORB_20. Re-probe before acting on any live value.*
