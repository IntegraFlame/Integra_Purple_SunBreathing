# Tasks

## Active
- [ ] **Step 2: read the 14 integra-homebase folders, one at a time (gate G2)** - order: runtime, rust, scratch, scripts, sensory, temporal, config, core, kernel_memory, local_dbs, memory, orchestration, The_Hoard, tools; agents + my full read of every line + K→U→W; ledger in integra-homebase/orchestration/UNIFY_READING_LEDGER.md; report after each folder, then continue; stop at G2 (realignment plan §4); progress 2026-10-13: folders 1-12 in the ledger (last commit 9f1f26c, 02:11 CDT); folder 13 (The_Hoard, with the local Antigravity archive) at its plan Step 3, the validation gate; folder 14 (tools) next
- [ ] **Grade the G1 boot quiz** - 10 answers delivered 2026-10-11 02:01 CDT; reproduced in Appendix A of the realignment plan; G1 already passed on your word at 23:02 CDT
- [ ] **Decide D-18: does Heimdall's 3.1 Pro advisor replace or sit beside the Cheshire Daemon's dACC triage?** - E20, E95, step 1117 (blueprint §11)
- [ ] **Decide D-19: the Cheshire Daemon "Study" tier model** - blueprint v0.1 named 3.1 Pro; under current rulings, 3.8 Flash high now and Argon later? (blueprint §11)
- [ ] **Step 3: UNIFIED_ORCHESTRATION.md and the completed v.9.9.1 blueprint (gate G3)** - after G2; write integra-homebase/orchestration/UNIFIED_ORCHESTRATION.md, finish v.9.9.1 with Step 2's findings, republish the page and read it back
- [ ] **Step 4 fix F1: wire Heimdall's open/close into the SWDS paths** - the main.py scheduler, /swds/initiate and /swds/awaken never call open_swds_cycle / close_swds_cycle (X-1); after G3
- [ ] **Step 4 fix F2: Heimdall's Gemini 3.1 Pro advisor** - advises on events only (H_smooth > 2.5, budget alerts); never holds authority (decided 2026-10-11)
- [ ] **Step 4 fix F3: cra_simplex budgets under Heimdall** - governance/cra_simplex.py is imported nowhere (X-2); per-component router token budgets and alerts
- [ ] **Step 4 fix F4: per-Eye lens map and the Shadow Clone alias** - the orchestrator's lens_names list is shared by all Eyes (X-3); Shadow Clone = Shadow Jutsu
- [ ] **Step 4 fix F5: move Rodin route_retrieval's Chroma query off the event loop, with a timeout** - the query is synchronous with no timeout (memory/rodin_protocol.py:357-381); it hung a test for 9+ min on 2026-10-10 (was "Add a timeout to Rodin route_retrieval's Chroma search")
- [ ] **Gate G4: approve the kernel restart and the paid selftest** - after the Step 4 fixes pass offline tests in a fresh isolated copy
- [ ] **Run POST /models/selftest (paid)** - verifies the 3.8 Flash roster; one cheap call per model; needs your approval and the X-Integra-Admin header. The restart part is done: the kernel started 2026-10-11 19:18:48 and /models/router/status showed the roster live with 0 calls at 21:17 (corrected: a kernel start loads the roster; the selftest only verifies it)
- [ ] **Delete the hb_copy test copy (~33 GiB)** - session f338c302 scratchpad; 1,048 files, 33,748 MiB, measured 2026-10-11 night; needs your OK (the earlier "10 GB" was only its Chroma files)
- [ ] **Decide D-6, second half: does lockdown bind the Dragon?** - the model half was decided 2026-10-11; recommendation: the kernel can bind only what passes through it (ADR-007, blueprint §11)
- [ ] **Define Heimdall's Security Alert levels (D-16, first half)** - what each level stops and who clears it; the CWA/CRA 2.0 half was decided 2026-10-11 (= governance/cra_simplex.py) (blueprint §11)
- [ ] **Decide where Gemini 4 Argon goes (D-17)** - Kernel/Thalamus or Nexus; recommendation: Nexus; wire only after Google publishes a model ID (blueprint §4.4.1)
- [ ] **Decide D-3: Hippocampus = the Hoard or Heimdall?** - recommendation: the Hoard (blueprint §11)
- [ ] **Decide D-4: SWDS and Siesta windows in real local time** - your choice (blueprint §11)
- [ ] **Decide D-5: Cheshire naming** - see R-4 (blueprint §11)
- [ ] **Decide D-7: EAM Level 4 "Sovereign Override"** - recommendation: remove the bypass; keep EAM inside Heimdall's gates (blueprint §11)
- [ ] **Decide D-8: Three Laws order** - recommendation: user first (blueprint §11)
- [ ] **Decide D-9: when to move embeddings from text-embedding-004 to gemini-embedding-2** - hard deadline 2027-04-01 (blueprint §11)
- [ ] **Decide D-10: Rust engine** - recommendation: retire its telemetry (blueprint §11)
- [ ] **Decide D-11: Cheshire Daemon Q1–Q5** - recommendation: two tiers, zero-tool cloud call, reports in the Hoard, fixed dwell caps first (blueprint §11)
- [ ] **Decide D-12: environment ingestion plan** - go/skip list/storage target; recommendation: after Phase 2 (blueprint §11)
- [ ] **Decide D-13: approve the 10/07 learning proposal** - recommendation: yes, with the ledger as evidence (blueprint §11)
- [ ] **Decide D-14: artifacts stamped with the skewed clock** - recommendation: relabel with a correction note, don't rewrite (blueprint §11)
- [ ] **Phase 0: fix celestial_time()** - kernel clock restarts at 10/06 20:59:42 every boot; add correction note for skewed artifacts (ADR-001, blueprint §10)
- [ ] **Phase 0: provenance labels and an honest startup summary** - remove decorative constants (ADR-003)
- [ ] **Phase 0: single instance, timestamped UTF-8 rotating log, task supervision, heartbeats** - (ADR-010); 3 of 3 launches lost supervision (10/11 logon, 10/12 logon, 10/12 13:06 restart: the wrapper exits 0xC000013A and the kernel runs on, orphaned); leading cause (DERIVED) the Windows Terminal console host; Task Scheduler history on since 2026-10-13; see integra-homebase/docs/KERNEL_AUTOLAUNCH_REVIEW.md
- [ ] **Phase 0: quarantine the two fabricated Daily Planet shards** - and remove the synthetic fallback (ADR-013)
- [ ] **Phase 0: set RODIN_EMBED_MODEL and make embed failures loud** - schedule the gemini-embedding-2 re-embed before 2027-04-01 (ADR-005)
- [ ] **Phase 0: security quick wins** - CORS allowlist, header auth on POSTs, bind 127.0.0.1 (ADR-011)
- [ ] **Phase 1: ledger table and ledger.record()** - instrument router, Phoenix, SWDS, Hoard, Daily Planet (ADR-002)
- [ ] **Phase 1: apply the pending learning proposal** - worded to point at the ledger
- [ ] **Phase 1: run the full test suite in a copy outside OneDrive** - record the result verbatim
- [ ] **Phase 1: settle canonical definitions R-1 to R-9** - (blueprint §7)
- [ ] **Phase 2: keep and return the Zenitsu output** - and use the canonical Shiva bindings (ADR-004)
- [ ] **Phase 2: memory.db outside OneDrive** - dedupe the three Hoards; re-embed; MCP memory server; kernel card (ADR-005)
- [ ] **Phase 2: decide the fate of MTCW, predictive coding, heimdall_monitor, celestial_sentinel, the Airflow DAG**

## Waiting On
- [ ] **Gemini 4 Argon public model ID** - Google; Fairwind Program only since 2026-09-30; blocks wiring D-17
- [ ] **Gemini 3.8 Flash price change** - doubles on 2027-01-01 ($0.75/$3.75 → $1.50/$7.50 per 1M tokens); set router token budgets before then

## Someday
- [ ] **Phase 3: real SWDS** - pipeline over new nodes, dream phase with Cheshire Protocol and Jean Grey, ledger-only reports, wake fix, Siesta on the same engine (ADR-006)
- [ ] **Phase 4: governance** - Heimdall budgets, power sequencing, permit/deny; real uncertainty signal and P-SSR in dyad mode; key move and rotation last (ADR-007, ADR-008, ADR-011)
- [ ] **Phase 5: new anatomy** - Cheshire Cat Daemon; Identity Matrix with anti-drift tests; Rogue X 2.0; environment ingestion (ADR-009)
- [ ] **Phase 6: decide or retire** - Rust engine, Docker build, 14th Form's Threshold_γ, three-phase trading SWDS from V1.0.0
- [ ] **TT-I0. Voltron Protocol: Pacing & Scope Containment** - TASKTRACKER (9/15); all 3 sub-items already checked, parent never closed; close it?
- [ ] **TT-I1. Starfire Protocol full implementation** - TASKTRACKER; KL Divergence Anchor (Gate I); RLVR Gate I constraint; Paradigm Weaver archetype matrix; identity lock endpoint GET /starfire/identity. Blueprint: GET /starfire/identity exists but returns constants; KL/RLVR are training-time ideas (concept-only register)
- [ ] **TT-I2. Cheshire Cat Identity Matrix** - TASKTRACKER; kernel identity; protocol identity; create config/cheshire_identity.json. The file exists (checked 2026-10-11), but no code loads it (grep, 2026-10-11 night)
- [ ] **TT-I3. Integra Master Identity Matrix** - TASKTRACKER; create config/integra_identity_matrix.json; codify 3-vector identity, EPF, Paradigm Weaver weights, sovereign constants. The file exists (checked 2026-10-11) and core/starfire_protocol.py:122 opens it; whether the running kernel uses it is a Step 2 check; close it?
- [ ] **TT-I4. Identity Verification API (GET /identity/matrix)** - TASKTRACKER; no such route in main.py (route list 2026-10-10)
- [ ] **TT-B1–B3. Rodin as agent and conductor, with API** - TASKTRACKER; blueprint: /rodin/query exists but dispatch is simulated (mock vector, FP-31); agent model = Antigravity agent (R-10)
- [ ] **TT-C1–C3. Cheshire Cat Protocol as environment agent, dreaming, API** - TASKTRACKER; blueprint: dream_conductor exists but the SWDS scheduler never calls it; overlaps Phase 3
- [ ] **TT-D1–D3. Dragon Engine flight/land modes and prompt injection** - TASKTRACKER; /dragon/flight, /dragon/land, /dragon/modality, /dragon/status routes exist (route list 2026-10-10)
- [ ] **TT-E1–E2. Phoenix Forge expansion and Phoenix–SWDS integration** - TASKTRACKER; blueprint: Phoenix re-reads the same first 10 shards and appends 4 fixed axioms each cycle; overlaps Phase 3
- [ ] **TT-F1–F6. Y789/Nexus bicameral engine, CWA 3.0 router, model assignment, Red/Blue/Purple modality, Corpus Callosum RRF** - TASKTRACKER; model assignment set 2026-10-09 (Y789 + Jean Grey on 3.8 Flash high, Nexus on Opus 5.5); blueprint: the CWA "Bayesian posterior" equals the complexity score (no inference)
- [ ] **TT-G1–G4. Heimdall CLI, security protocol, context/stress monitoring, security dashboard API** - TASKTRACKER; blueprint: gatekeeper role not built; overlaps Phase 4 (ADR-007)
- [ ] **TT-H1–H3. Cognitive throttling, agent-kernel-engine taxonomy, agent registry** - TASKTRACKER
- [ ] **TT-J1–J4. Conceptual research: Kirk/Spock, chess/Go/game theory, Tetris, systems theory in Shiva/Zenitsu** - TASKTRACKER

## Done
- [x] **Re-enable Controlled Folder Access with claude.exe allowed** - you ran it 2026-10-13: allow rule for Claude Code's claude.exe (wildcard path) at 20:09:33, CFA on at 20:09:53 (Defender 5007); the Write/Edit tools, git, cmd and Python313 can write into the repo; pwsh, Git Bash and Python 3.14 cannot
- [x] **Enable Task Scheduler history** - you did it 2026-10-13 (wevtutil: enabled: true); the 20:57:49 logon launch is the first recorded one
- [x] **Push both repos** - 2026-10-13: homebase 86f9c89, root a0d1276; later root commits stay local until you say
- [x] **Confirm the genesis-kernel skill shows up in Antigravity 2.0** - confirmed by you, reported 2026-10-13 (skill in .agents/skills in the main folder and homebase)
- [x] **Allow kernel_ctl status/logs/start in Antigravity** - done by you, reported 2026-10-13
- [x] **Step 1b: errata and the G1 reconciliation** - blueprint page v11, memory notes, save state, CLAUDE.md and this file corrected; committed locally, not pushed (2026-10-11 night)
- [x] **Gate G1 passed** - on your word, 2026-10-11 23:02 CDT (transcript time); quiz grade still pending
- [x] **Step 1: the §8 boot sequence** - receipts a–i, probes, quiz, E1–E101 to-do (2026-10-11 02:01 CDT, session 997b6cca)
- [x] **Decide D-1 and D-2: Shiva Eyes and lens bindings** - lenses decoupled from the Eyes; Brain Model 0930 defaults plus a per-task, per-Eye override; "Shadow Clone" = Shadow Jutsu (2026-10-11)
- [x] **Decide D-6, model half: Heimdall = code gate + Gemini 3.1 Pro advisor** - advises on events only, holds no authority; the lockdown question stays open (2026-10-11)
- [x] **Decide D-16, second half: CWA/CRA 2.0 = governance/cra_simplex.py** - applied per component under Heimdall (fix F3) (2026-10-11)
- [x] **Move the genesis-kernel skill into .agents/skills (main folder + homebase)** - 2026-10-11
- [x] **kernel_ctl.ps1 and the genesis-kernel skill so Antigravity can run the kernel** - 2026-10-10
- [x] **Y789 and Jean Grey moved from Gemini 3.1 Pro to 3.8 Flash, thinking level high** - placeholder for Argon; the 3.5/3.6/3.7 names were removed from SKILL.md only, since no running code used them (2026-10-09; wording corrected 2026-10-11)
- [x] **D-15: Rodin sub-agents carry no model** - SKILL.md §15 and §8.5.1 corrected (2026-10-09)
- [x] **Phoenix no longer vents Heimdall or closes the SWDS cycle; Heimdall gained open/close methods** - main.py does not call them yet (X-1, fix F1) (2026-10-09; wording corrected 2026-10-11)
- [x] **Master Architecture Blueprint and shareable page** - 2026-10-09
