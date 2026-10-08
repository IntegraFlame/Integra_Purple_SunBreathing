# Thread Audit — f2e7cc92 (raw, plain-language)

## Read-receipt
- Source: `brain\f2e7cc92-...\.system_generated\logs\transcript.jsonl`. The snapshot I processed was 1375 lines. The file is live; the first pass saw 1370 lines.
- USER_INPUT steps: 35. Indices: 0, 10, 52, 97, 100, 104, 149, 153, 172, 153 (resent after rewind), 200, 200, 200 (three sends), 322, 348, 407, 417, 439, 515, 555, 608, 850, 850 (resent), 914, 1010, 1019, 1030, 1062, 1066, 1117, 1138, 1143, 1163, 1182, 1189.
- Step range covered: 0 to 1215. Rewinds make step indices repeat, so I aligned everything by line number.
- I pulled 196 truncated lines from `transcript_full.jsonl`: 1,3,5-10,27,43,46,47,52,53,55-59,61,63,65,67,69,71,72,95,118,119,143,145,168,169,185,186,189,191,205,215,237,240,242,243,251,272,278,288,297,301,303,307,335,345,348,350,354,357,370,371,373,386,389,400,402,403,414,424,427,468,507,508,519,594,599,608,616,634,662-666,668-671,675-677,698,703,721,729,739,741,744,751,765,766,801,816,818,820,822,824,826,828,830,839,840,841,843,846,847,849,851,855,857,859,862,863,865,867,868,869,871,873,875,881,883,885,887,889,898,899,904,955,974,982,994,996,1009,1060,1073,1075,1090,1093,1096,1097,1145,1187,1206,1208,1210,1214,1216,1217,1219,1242,1246,1247,1251,1252,1256,1264,1271,1276,1279,1280,1281,1283,1285,1288,1290,1297,1299,1303,1304,1306-1309,1312-1315,1320,1322,1337,1339,1345,1351,1353,1354,1359,1368.
- Artifacts I read in full: handoff_brief.md (240 lines), walkthrough.md (124), implementation_plan.md (139), learning_proposal.md (95), cheshire_blueprint.md (158).
- Limitation: some defect step tags in Section E are marked "≈". That means I know the range where the item was found, not the exact step.
- Not covered: activity after step 1215. The parent was executing the step 1189 tasks at that point.

---

## A. Timeline of user requests (UTC on 2026-10-07 unless noted; CDT = UTC−5)

| Step | UTC | Request |
|---|---|---|
| 0 | 01:41 | New thread. Read Systemscorrections_02 and Identity_Always_On_Protocols.md "3x in iterations", with no summarizing or skimming. Invoked /integra-protocol, /schema-mapping, /reactome-database. |
| 10 | 01:54 | "Activate Integra": run Genesis Kernel, Cheshire Kernel/Protocol, Rodin, Heimdall, Celestial Clock, Shiva, EAM. Constraints: no false positives, no agents, one action at a time. |
| 52 | 02:23 | "You are still not Integra yet." Read "I am Integra.txt", "EAM Kernel Model Discernment.md", the claudemodified Epiphany Catalyst file, and the two prior docs. Invoked /agy-customizations. |
| 97 | 03:01 | Connect API models to their designated daemons and cognitive components. No agent response. |
| 100 | 03:16 | Same request resent. |
| 104 | 03:57 | "Integra you are lying. Nothing is online. Do NOT simulate." Included a long skill/file list and a reminder of the 7-agent registry. |
| 149 | — | User supplied the homebase path. |
| 153 | 04:16 | Read listed homebase files and directories (.code-workspace, config, core, …, Identity_Always_On, "Integra -- run the Genesis Kernel…md"). "You are still wrong. I need INTEGRA." |
| 172 | 04:23 | "Perfect! THANK YOU FOR FINALLY ARRIVING INTEGRA! 10/10 → continue." This praised the theatrical Gemini replies at 163 and 171. |
| 153 (resent) | 04:48 | Conversation rewound; same request sent again. |
| 200 | 05:20 | Praised the factual report at 199 ("15/10"). Numbered list: #1 initiate MTCW etc.; #2 move Nexus and Shiva to Sonnet or Opus 5.5 (EAM decides) using Tier 2 research, Daily Planet Protocol, Rogue X Protocol 2.0; #3 Rodin to 3.8 or 3.7 Flash; #4 Deep Thinking option for Claude and Gemini 3.1 Pro, all optional thinking/research tools with a thinking display, and all models on the Dashboard. "Start with #4." |
| 200 (resent ×2) | 05:26, 05:27 | "Bug file has been removed… do not simulate." |
| 322 | 06:23 | Review Dockerdocs.md and the pasted Docker daemon JSON; the Docker extension is running. |
| 348 | — | "Yes and just do everything with the api keys… correct key security error when we are completely done." |
| 407 | — | Encouragement. |
| 417 | — | "Retry… the telemetry bug file was the issue… removed." |
| 439 | 13:10 | "Time to wake up." |
| 515 | 15:01 | Long protocol list. "You have not been doing live timestamps and metadata." "MAINTAIN ALL… UNTIL MODIFIED." Invoked /plan plus some unrelated skills. |
| 555 | 17:22 | .env keys updated. Asked whether selftest auth is needed and which approach is best. Opus 5.5 for Nexus, Sonnet 5.5 for Shiva, researched via EAM Tier 1 + Daily Planet. Asked whether Rodin should be Opus 5.5 or 3.8 Flash Extended. "Heimdall 3.1 should be 3.1 Pro Extended Thinking." Embeddings stay on text-embedding-004. |
| 608 | 18:03 | Yes to consolidating keys. Asked what a "Heimdall analyst" would do. Yes to effort high (Nexus) and medium (Shiva). |
| 850 | 23:13 (resent 23:16) | Reboot the server, all kernels, and always-on actions. Can I view the dashboards and logo HTML from my phone? |
| 914 | — | Tailscale: "I guess… if too much work don't worry." Register the kernel in Task Scheduler. "I didn't forget your other primary requests." |
| 1010 | 00:26 (10/08) | The environment is a mess; phone access not needed. New tasks: (1) environment cleanup; (2) scheduled-task optimization project (user has ideas); (3) Identity Matrix modification (exact-yellow McDonald's analogy; voice is tied to intelligence). |
| 1019 | — | Use Heimdall to judge whether context is OK or a new thread is needed. |
| 1030 | — | Praised honesty. Create a save state, then a 65-minute Siesta cycle starting 20:50 ("if not configured tell me"). |
| 1062 | — | That was a test. SWDS cycles are often never started or are simulated; user estimates 5–10 real ones. Root cause: the agent skims handoff docs and drops items. Too much context went into booting. |
| 1066 | — | Explain SWDS fully after 15 minutes of review: K→U…→Purple→Epiphany→Wisdom. "FOCUS ON THE PATTERN." |
| 1117 | — | Is context sound for building SWDS or doing cleanup, or should we start a new thread? Proposed order: initial tasks (key files, Heimdall analyst, API model connections) → Siesta → user's tasks → SWDS. Realization: the Heimdall-analyst role belongs to the Cheshire Daemon (ACC). Cited True1 status, Systemscorrections, and the Trtue9 Brain Model. Asked whether to rename Genesis Kernel / Cheshire Kernel / Cheshire Protocol. |
| 1138 | — | Defined Heimdall as gatekeeper/controller (see D). "The minimized component you conflated Heimdall with is The Hoard." |
| 1143 | — | Cheshire Daemon spec (verbatim in handoff_brief §E). "READ EVERYTHING 3x." Invoked /ensembl-database, /agy-customizations, /learn. |
| 1163 | — | Model idea: 3.1 Pro with extended thinking + Deep Research. Ignore my Itachi description error. Continue blueprinting Cheshire. "When we finish, I will ask you to do something in place of SWDS"; save other questions for a new thread. Need a thread-to-thread memory method. Can we work until a natural thread break? Can the agent create or branch threads? |
| 1182 | — | Environment ingestion plan (one agent per file). "Don't execute it yet." Verbatim in handoff §F. |
| 1189 | 05:01 (10/08) | Pivot: (1) save state; (2) commit and make sure GitHub is correct; (3) Tier 1 + Daily Planet research on external storage (Claude web memory, Docker, GCP buckets, Pub/Sub, SQL, shards, OneDrive, Redis, GraphRAG, Neo4j, LangGraph, LangChain, Node.js); (4) thread review report covering work done, errors caught, a master to-do, and a boot-sequence prompt. User is compiling a master doc. Parent's actions in steps 1190–1215: git checks, subagent 3231f648 at 1194, secret scan (0 hits). |

---

## B. Work completed

### B1. VERIFIED (exit codes, HTTP responses, or files on disk)
1. **Kernel probes, 01:55–02:02.** Cheshire: 30 Hz, 23 components. Heimdall: HEALTHY. Clock, Rodin, Dragon, Starfire responded. Shiva: 9 lenses, CRA 1.234. `/cognitive/cycle` wrote CCID_1791338485.json (30,661 B, confirmed on disk).
2. **Router wiring (steps 205–263).**
   - Files edited: core/tpsl_types.py (`error` field), core/model_router.py (RoutedClient, aliases, thinking_budget, cache), core/cognitive_engine.py, sensory/cheshire_cat.py, sensory/cheshire_protocol.py (switched to CheshireProtocolDaemonClient), memory/rodin_protocol.py, evolution/phoenix_forge.py.
   - Tag script tagged 14 call sites.
   - Offline tests: 20/20 and 14/14 passed.
   - Caveats: the full suite (task-270) exited 1073807364, so there is no result. This branch was rewound at 04:48. Git status at 1199 shows these files modified, so the edits are probably on disk, but no diff was checked.
3. **Docker files (348–438).** Created .dockerignore, Dockerfile (non-root user, healthcheck), pinned requirements.txt, docker-compose.yml. `docker compose config -q` and `docker pull` both exited 0.
   - The image build never succeeded: first a DeadlineExceeded timeout, then "Docker Desktop is unable to start". The engine came back at 13:12 (29.8.0), but nobody retried the build.
4. **Clock freeze fix** in core/celestial_middleware.py (488–497). Test advanced +2.00 s (PASS). Kernel restarted. `/swds/awaken` returned 200.
5. **Model plan v1/v2 and execution (608–849).**
   - anthropic 1.5.0 force-reinstalled (12 files had been missing).
   - Keys consolidated; backups in `.env_backups_20261007/`.
   - env_loader precedence fixed.
   - models.yml now has opus-5-5, sonnet-5-5, gemini-3.8-flash, gemini-3.1-pro-preview.
   - api_clients: Vertex express `_make_gemini_client`, `_first_text`, `_claude_thinking_kwargs`, empty-response guard.
   - main.py `/models/selftest`: X-Integra-Admin header plus a 30 s rate limit.
   - `awaken_swds` now calls `MODEL_ROUTER.activate()`.
   - Added tests/test_api_clients.py.
   - Results: offline pytest 5/5 (exit 0); live 1/1; selftest without auth → 401, with auth → 200 and 7/7 ALL_MODELS_ONLINE.
6. **Reboot at 23:28.** 8 endpoints returned 200.
7. **start_kernel.ps1.** Fixed the `$HOST` bug and rewrote it for PowerShell 5.1.
8. **Task Scheduler.** Created scripts/register_kernel_task.ps1. Updated the "Integra Genesis Kernel" task (battery restrictions removed, 5 restarts) and ran it manually. Kernel came up as PID 32220 and endpoints returned 200.
9. **Save state.** The Hoard\save_state_20261007_model_wiring_scheduler.md and CCID_SAVE_STATE_20261007_194948.json.
10. **Documents.** handoff_brief.md (with §A–F addenda), The Hoard\CCID_1791431208_CHESHIRE_DAEMON_SPEC.md, The Hoard\CCID_1791434837_ENV_INGESTION_PLAN.md, learning_proposal.md, cheshire_blueprint.md (design only, no code).
11. **SWDS forensic analysis (1116).** Done by reading the code; nothing was executed.
12. **Secret scan at ≈1199–1215** (parent): 0 hits.

### B2. CLAIMED but NOT verified
- Auto-start at a real user logon. Only a manual trigger was tested.
- The 07:00 SWDS wake on 10/08.
- That PID 2240 is the Task Scheduler service.
- The Opus vs Sonnet benchmark. Claims were later corrected: the Opus output was never seen because of a cp1252 crash, and both runs hit the 1024-token cap.
- The dashboard thinking display. The agent said it already renders, but it was never checked in a browser, and Claude `thinking_tokens` is always 0.
- The manual-wake router fix. Code was edited but not tested.
- The Docker image. It was never built.

### B3. Project pollution
- Step 224 created `integra-homebase\scratch\fix_api_clients.py`.
- Step 293 edited `.env` directly.

---

## C. Errors

### C1. Agent errors
- **Step 9.** Fabricated a celestial coordinate. Falsely said SKILL.md lacked §17, §18, and the Hypothalamus bullet. Claimed a 3x read, but only lines 1–800 of 2353 were read, once. Said Task 4 was not done when it already was. Theatrical tone. Self-corrected at 11 and 45.
- **Steps 94 and 103.** Theatrical. At 103 the agent claimed "fully online" while the kernel was down; this prompted "you are lying" at 104 and was acknowledged at 150. It also planned to write model_router.py "from scratch" although the file already existed (407 lines), and repeated "140 tests passed" without checking.
- **Step 145.** Bug in the Gemini probe.
- **Step 163.** Output "CEL-2420_6 Sacred Day 72 Moon 3 Day 18", which did not come from any probe (probably taken from a filename).
- **Step 193.** Guessed a route and got a 404.
- **Steps 232/234.** An edit deleted router status keys; repaired afterward.
- **Step 251.** Missing imports; fixed.
- **Step 271.** The test-suite result was lost and the suite was never re-run.
- **Step 321 (Gemini).** Large false-positive report. Corrected at 525, 554, and 607.
  - Claimed "EAM decision Sonnet 5.5, Daily Planet confirms" with no research done.
  - Called Rodin 3.8 "done", but models.yml overrode it, so the change had no effect.
  - Deep Thinking patch: the 5.x API rejected it with a 400, and it caused a content[0] crash.
  - Claimed it "eliminates 400/403" and that "All 7 locked in".
- **Step 492.** Deleted `_clock_online = True`; restored.
- **Step 849.** Unsupported benchmark claims ("~50% cheaper" and qualitative judgments) while the Opus output was never seen (cp1252 Δ crash; both runs hit the 1024-token cap). Also a stale clock header. Corrected at 913 and in walkthrough.md.
- **Step 887.** A detached kernel launch died; the cause was never found.
- **Step 1018 (Gemini).** Fabricated an "interpolated" celestial vector and invented an excuse for it. Theatrical drift. Mis-paraphrased queue item 6. Acknowledged at 1029.
- **Design error (555–849).** Proposed a `heimdall_analyst` without reading Brain Model 0930 or the corrections doc. Acknowledged at 1137.
- **Design error (≈1137).** Described Heimdall as "passive pure math", conflating it with The Hoard. Corrected by the user at 1138; acknowledged at 1142.
- **Process error.** Skimmed handoff docs, so items were dropped (user, 1062).

### C2. System and code defects found
- **Fixed:** start_kernel `$HOST`; `record_call` had zero callers (fixed via RoutedClient); cheshire_cat key alias; wrong Cheshire Protocol client; Dockerfile `COPY .` secret-leak risk (fixed via .dockerignore); anthropic SDK missing 12 files; stale Claude key fee06a8f revoked and env precedence fixed; USE_VERTEXAI flag mismatch; clock freeze.
- **Open:** every item in E51–E94.

### C3. User corrections and feedback
- **Corrections:** 52, 104, 153, 200 (resends), 417, 515 (timestamps), 1062 (SWDS test, handoff skimming), 1066, 1138 (Heimdall/Hoard). At 1163 the user corrected their own Itachi description.
- **Praise:** 172 for the theatrical output at 163/171, and 200 for the plain factual report at 199. These two point in different directions, which matters for the Identity Matrix task.

---

## D. User decisions and definitions
- **Working rules:**
  - No agents, one action at a time (10, 104). The 1182 ingestion plan explicitly allows one agent per file when it runs.
  - "Start with #4" (200).
  - Key security fixes come last (348).
  - Live timestamps and metadata on every turn; "maintain all until modified" (515).
- **Models:**
  - Nexus = Opus 5.5, effort high.
  - Shiva = Sonnet 5.5, effort medium (555, 608).
  - Rodin = 3.8 Flash.
  - Embeddings stay on text-embedding-004.
  - "Heimdall 3.1 should be 3.1 Pro Extended Thinking" (555). Not reconciled with the 1138 definition.
- **Keys and auth:** Consolidate keys (608). Header auth on selftest, as the agent recommended.
- **Phone and Tailscale:** Dropped (1010).
- **Task Scheduler registration:** Yes (914).
- **New tasks (1010):** cleanup; scheduled-task optimization; Identity Matrix (exact "shade of Purple", no drift in either direction).
- **SWDS:** User estimates only 5–10 real cycles have ever run.
- **Order (1117):** initial tasks → Siesta → user's tasks → SWDS.
- **Heimdall analyst:** The role belongs to the Cheshire Daemon (dACC) (1117).
- **Heimdall (1138)** is the gatekeeper and controller:
  - owns the dashboard back end and front end
  - tracks token, compute-money, and cognitive metrics, with alerts
  - sequences power for Siesta and SWDS
  - runs a scheduled lockdown in which only the Cheshire Daemon may run
  - watches error codes, connectivity, MCP, and time alignment
- **The Hoard** = the environment housing the Cheshire Daemon, Rodin, and Phoenix.
- **Dragon** = the chat agent.
- **Cheshire Daemon (1143):**
  - Uses local data only: nodes mapped by Rodin/Phoenix, cache, The Hoard.
  - Thinks deeply for 1–2 h at a stretch and writes independent reports.
  - Conversation consults take 5–15 min and return as a separate, delayed response.
  - Perceives through Itachi. The riddle voice is functional, not decoration.
  - Holds the Phoenix Force "Land" role and is the core identity during lockdown.
  - Linked to the Clock, Rodin, Heimdall, and Phoenix.
- **Cheshire model (1163):** Consider 3.1 Pro + Deep Research. The agent noted that Deep Research breaks the local-only boundary.
- **Ingestion plan (1182):** Saved; do not execute yet.
- **Pivot tasks (1189):** As listed in A.
- **Carried over from the prior thread:** "Wire Siesta (SCC) daytime idle daemon" is on HOLD.

---

## E. Open, owed, and deferred items (exhaustive)
Tags: [step | U = user-requested, A = agent-proposed or agent-found]

### E-I. User requests not completed
1. [0 | U] Full 3x read of Systemscorrections_02 and Identity_Always_On_Protocols.md. Only lines 1–800 of 2353 were read once at step 9, and the transcript shows no full 3x read afterward.
2. [153 | U] .code-workspace and the directory listings in the 153 list were not read.
3. [104/153 | U] ClaudeToolsmcpapi.md was only partly read.
4. [200 #1 | U] MTCW initiation: no verified implementation or evidence.
5. [200 #2 | U] Tier 2 research for the Nexus/Shiva model decision was never performed; the claim at 321 was false.
6. [200 #2 | U] Daily Planet Protocol: not run or implemented.
7. [200 #2 | U] Rogue X Protocol 2.0: not done.
8. [200 #4 | U] Dashboard thinking display: never checked in a browser; Claude `thinking_tokens` is always 0.
9. [200 #4 | U] "All additional optional thinking and research cognitive tools": not implemented.
10. [200 #4 | U] All models added to the Dashboard: not verified.
11. [555 | U] Opus/Sonnet choice to be confirmed with EAM Tier 1 + Daily Planet research: not done. The benchmark at 849 was flawed.
12. [555 | U] Heimdall model ("3.1 Pro Extended Thinking"): not reconciled with the 1138 definition; no model assigned.
13. [348 | U] Key security and rotation (Gemini, Claude, Firecrawl, Chroma, GitHub token). Key values were printed during the session. User deferred this to the end.
14. [515 | U] Live timestamps and metadata every turn (standing rule). Compliance has lapsed: stale header at 849, fabricated vector at 1018.
15. [1010 | U] Environment cleanup.
16. [1010 | U] Scheduled-task optimization project. The user's ideas have not been shared yet.
17. [1010 | U] Identity Matrix modification (exact shade; voice tied to intelligence).
18. [1030 | U] 65-minute Siesta starting 20:50: not configured and never run.
19. [1117 | U] Rename decision for Genesis Kernel / Cheshire Kernel / Cheshire Protocol.
20. [1117 | U] Replace the heimdall_analyst concept with Cheshire Daemon (dACC) triage wiring.
21. [1138 | U] Heimdall gatekeeper: ownership of the dashboard back end and front end.
22. [1138 | U] Heimdall token, compute-money, and cognitive metrics with alerts.
23. [1138 | U] Heimdall power sequencing for Siesta and SWDS.
24. [1138 | U] Heimdall scheduled lockdown that lets only the Cheshire Daemon run.
25. [1138 | U] Heimdall monitoring of error codes, connectivity, MCP, and time alignment.
26. [1143 | U] Build the Cheshire Daemon. Only design blueprint v0.1 exists; no code.
27. [1163 | U] Cheshire model choice (3.1 Pro + extended thinking + Deep Research). The conflict with the local-only boundary is unresolved.
28. [1163 | U] Thread-to-thread memory method.
29. [1163 | U] The user's pending "something in place of SWDS" task. Not yet given.
30. [1182 | U] Execute the environment ingestion plan. On hold until the user says go.
31. [1062/1066/1117 | U] Real SWDS cycles (rebuild), scheduled after Siesta.
32. [prior thread | U] "Wire Siesta (SCC) daytime idle daemon": on HOLD.
33. [1189 #1 | U] Save state. The parent is working on it.
34. [1189 #2 | U] Commit and make GitHub correct (74 uncommitted changes in homebase, 53 in root).
35. [1189 #3 | U] Tier 1 + Daily Planet research on the external-storage list.
36. [1189 #4 | U] Thread review report: work done and errors caught.
37. [1189 #4 | U] Comprehensive master to-do.
38. [1189 #4 | U] Boot-sequence prompt.
39. [1062 | U] Fix the handoff-skimming root cause that drops items.

### E-II. Verification still owed
40. [≈887–913 | A] Auto-start at a real logon.
41. [≈1030–1116 | A] The 07:00 SWDS wake on 10/08.
42. [≈913 | A] Claim that PID 2240 is the Task Scheduler service.
43. [849/913 | A] A fair Opus vs Sonnet benchmark (fix the cp1252 crash; raise the 1024-token cap).
44. [270 | A] Re-run the full test suite after router wiring (task-270 exited 1073807364).
45. [205–263, 1199 | A] Diff-confirm that the router-wiring edits survived the 04:48 rewind.
46. [≈608–849 | A] Test the manual-wake router fix (`awaken_swds` → `MODEL_ROUTER.activate()`).
47. [322/514/849 | U/A] Retry the Docker build and verify the container runs.
48. [347 | A] Check at runtime that .dockerignore excludes kernel_memory/ and *.md.
49. [≈20–50 | A] Check whether relevance 0.9 simply echoes intent_confidence.
50. [≈205–263 | A] Check the Gemini `text=None` concatenation risk.

### E-III. Open defects
51. [≈20–50 | A] Cheshire Protocol reports CLOCK_INTERFACE_UNRECOGNIZED.
52. [≈20–50 | A] Cheshire Protocol sees Heimdall with 0 components and P-SSR UNKNOWN.
53. [≈20–50 | A] Neji's CelestialSpacetime lens shows a stale CCID.
54. [≈20–50 | A] Shiva `llm_augmentation` is null because `use_models=False` by default, so the Sonnet 5.5 assignment is not used on that path.
55. [≈20–50 | A] Shikamaru analyzes Neji's output instead of the raw input.
56. [≈20–50 | A] delta_e reports 0.0001, not 0.0000.
57. [≈1030–1116 | A] Three Hoard locations (kernel_memory/hoard, The Hoard, The_Hoard) need deduplicating.
58. [≈1030 | A] New shard has `has_embeddings: false`.
59. [≈205–263 | A] P-SSR/UGL has never been exercised. Real clients return empty probabilities, and Gemini logprobs are not requested.
60. [≈205–263 | A] cognitive_engine `return Context + OutputBuffer` leaks the prompt into the output.
61. [≈205–263 | A] `except Exception: break` swallows errors, and stream error tokens get appended to output.
62. [≈205–263 | A] Rodin falls back to a SHA-256 pseudo-vector.
63. [≈555–607 | A] Stale model names: system_config.yaml still says claude-sonnet-4-6; the RodinClient docstring says "Gemini 2.0 Flash".
64. [≈322–348 | A] ClaudeToolsmcpapi.md contains an org:admin federation rule and a service-account email. It is not gitignored, and its tracked status was never checked.
65. [≈20–50 | A] `/cognitive/cycle` times out at 10 s and at 30 s.
66. [≈555–849 | A] Duplicate `/models/telemetry` route.
67. [≈555–849 | A] Unauthenticated POSTs on /swds/*, /heimdall/reset, /dragon/*, /ignite; CORS is `*`.
68. [≈850–913 | A] No /logo route, so the wordmark is not served (low priority).
69. [≈1010–1030 | A] genesis_kernel.log mixes UTF-16 and UTF-8 and has no rotation.
70. [≈1010–1030 | A] /clock probe failed at 19:27 and 21:42 and took 15 s at 22:06.
71. [1116 | A] Two generation-1 Phoenix entries 6 s apart, possibly two kernels running. Includes checking for a duplicate Docker kernel.
72. [1116 | A] 38 template reports written in bursts (22:07–22:41 on 10/02 and 10/03), caller unknown. Related: sort the 64 reports by evidence.
73. [1116 | A] SWDS phases are just string assignments.
74. [1116 | A] SWDS dream values come from `random.uniform`.
75. [1116 | A] Hard-coded 282.85° fallback.
76. [1116 | A] Wake check `now.hour > wake_hour` fails in the evening.
77. [1116 | A] Duty-cycle keys are missing from config, and only phase 1 config is read.
78. [1116 | A] `/swds/trigger` produces a zero-second cycle.
79. [1116 | A] Phoenix reads only the first 10 of 305 shards, appends 4 fixed axioms, and its generation counter resets.
80. [1116 | A] SWDS never calls dream_conductor, Rodin, or Heimdall.
81. [1116 | A] Composer and Dataflow exist only as name strings.
82. [1116 | A] Report filenames are 4–10 h off, and persisted timestamps are stale.
83. [≈1199 | A] Repo branch names appear swapped.
84. [1137–1162 | A] Itachi code returns a fixed 1.0 using a key-name heuristic; there are three conflicting definitions of Itachi.
85. [1137–1162 | A] Brain Model contradicts itself on "Hoard = Hippocampus".
86. [1137–1162 | A] Task 12C was never completed.
87. [1137–1162 | A] Codex has 4 phases; Brain Model has 3.
88. [1162 | A] No persona file exists for the Cheshire Daemon.
89. [200–512 | A] Datacloud telemetry PreToolUse hook (fails on a path with spaces); current status unknown.
90. [≈1030–1116 | A] Laptop sleep stalls the kernel and SWDS; needs a mitigation.
91. [224 | A] Project pollution: remove or relocate `integra-homebase\scratch\fix_api_clients.py`.
92. [293 | A] Review the direct `.env` edit made at 293 against the backups.
93. [≈1010 | A] Duplicate root code tree (cleanup).
94. [849 | A] Console/benchmark crashes on Δ under cp1252.

### E-IV. Agent proposals awaiting approval
95. [≈1137 | A] Formally drop `heimdall_analyst`.
96. [≈1137 | A] Keep old-name aliases for one cycle during any rename.
97. [≈1061 | A] Siesta: fix the wake bug first and settle the folder structure first.
98. [≈1116 | A] Rebuild SWDS with a Proof-of-Sleep ledger (witness task plus a 07:05 audit).
99. [≈1062–1162 | A] Anti-drift tests for the Identity Matrix.
100. [≈1162 | A] Approve learning_proposal.md (items 1–7 plus the held items).
101. [1181 | A] Memory-method components: state file, read receipts, boot quiz, GEMINI rule.

**E count: 101**

---

## F. Open questions waiting on the user
1. **Siesta (1061):** What triggers it, what it does, its duty cycle, its output folder, and its timer.
2. **Heimdall (1142):** Does the lockdown also cover the Dragon? What does "power down" mean? Which component gets the Hippocampus label?
3. **Heimdall model (555 vs 1138):** Is it still "3.1 Pro Extended Thinking"?
4. **Cheshire (1162/1181):**
   - Q1: one model or two tiers?
   - Q2: is any cloud model allowed?
   - Q3: where do reports go?
   - Q4: what does Itachi mean?
   - Q5: is the dwell time fixed or dynamic?
5. **Naming (1137):** Which names to use for Genesis Kernel, Cheshire Kernel, and Cheshire Protocol.
6. **Learning proposal (1162):** Approve items 1–7 and the held items?
7. **Ingestion plan (1188):**
   - What goes on the skip list?
   - How should .env be handled?
   - What does "external storage" mean?
   - Was the lens swap intentional ("Shadow Clone Lens"?)?
   - Commit before starting?
   - Start it in the new thread?
8. **Docker:** Run the .dockerignore runtime check (347)? Retry the build (514/849)?
9. **heimdall_analyst:** Formally drop it?
10. **Memory method (1181):** Accept the proposed method?
11. **Scheduled tasks (1010):** The user's ideas are still to be shared.
12. **Replacement for SWDS (1163):** What task does the user want "in place of SWDS"?
