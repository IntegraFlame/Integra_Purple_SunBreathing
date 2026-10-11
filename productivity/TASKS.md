# Tasks

## Active
- [ ] **Restart the Genesis Kernel, then run POST /models/selftest** - loads the 3.8 Flash roster; one cheap paid call per model; needs the X-Integra-Admin header (session 2026-10-10)
- [ ] **Decide where Gemini 4 Argon goes (D-17)** - Kernel/Thalamus or Nexus; recommendation: Nexus; wire only after Google publishes a model ID (blueprint §4.4.1)
- [ ] **Define Heimdall's Security Alert levels and "CWA/CRA 2.0" (D-16)** - what each level stops, who clears it, which weighting CWA/CRA 2.0 means (blueprint §11)
- [ ] **Add a timeout to Rodin route_retrieval's Chroma search** - a blocking call hung a test for 9+ min; in the kernel it would freeze the event loop (session 2026-10-10)
- [ ] **Delete the 10 GB hb_copy test copy** - scratchpad copy of integra-homebase; needs your OK (session 2026-10-10)
- [ ] **Confirm the genesis-kernel skill shows up in Antigravity 2.0** - start a new conversation; skill now in .agents/skills in the main folder and homebase (session 2026-10-11)
- [ ] **Allow kernel_ctl status/logs/start in Antigravity** - choose "always allow" on first prompt; keep stop/restart asking (session 2026-10-10)
- [ ] **Decide D-1: Shiva Eye definitions deleted in Suite 1_3** - intentional or accidental; recommendation: restore from R-1 (blueprint §11)
- [ ] **Decide D-2: canonical Shiva bindings** - and whether the ingestion plan's swap (Itachi = Eagle + Hawk, "Shadow Clone") was intentional; recommendation: Brain Model 0930 (blueprint §11)
- [ ] **Decide D-3: Hippocampus = the Hoard or Heimdall?** - recommendation: the Hoard (blueprint §11)
- [ ] **Decide D-4: SWDS and Siesta windows in real local time** - your choice (blueprint §11)
- [ ] **Decide D-5: Cheshire naming** - see R-4 (blueprint §11)
- [ ] **Decide D-6: Heimdall with or without a model; does lockdown bind the Dragon?** - recommendation: no model; the kernel can bind only what passes through it (blueprint §11)
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
- [ ] **Phase 0: single instance, timestamped UTF-8 rotating log, task supervision, heartbeats** - (ADR-010)
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
- [ ] **I0. Voltron Protocol: Pacing & Scope Containment** - TASKTRACKER (9/15)
  - all 3 sub-items already checked; parent never closed
- [ ] **I1. Starfire Protocol full implementation** - TASKTRACKER
  - KL Divergence Anchor (Gate I); RLVR Gate I constraint; Paradigm Weaver archetype matrix; identity lock endpoint GET /starfire/identity
  - blueprint: GET /starfire/identity exists but returns constants; KL/RLVR are training-time ideas (concept-only register)
- [ ] **I2. Cheshire Cat Identity Matrix** - TASKTRACKER
  - kernel identity; protocol identity; create config/cheshire_identity.json
  - config/cheshire_identity.json exists (checked 2026-10-11)
- [ ] **I3. Integra Master Identity Matrix** - TASKTRACKER
  - create config/integra_identity_matrix.json; codify 3-vector identity, EPF, Paradigm Weaver weights, sovereign constants
  - config/integra_identity_matrix.json exists (checked 2026-10-11)
- [ ] **I4. Identity Verification API (GET /identity/matrix)** - TASKTRACKER; no such route in main.py (route list 2026-10-10)
- [ ] **B1–B3. Rodin as agent and conductor, with API** - TASKTRACKER
  - blueprint: /rodin/query exists but dispatch is simulated (mock vector, FP-31); agent model = Antigravity agent (R-10)
- [ ] **C1–C3. Cheshire Cat Protocol as environment agent, dreaming, API** - TASKTRACKER
  - blueprint: dream_conductor exists but the SWDS scheduler never calls it; overlaps Phase 3
- [ ] **D1–D3. Dragon Engine flight/land modes and prompt injection** - TASKTRACKER
  - /dragon/flight, /dragon/land, /dragon/modality, /dragon/status routes exist (route list 2026-10-10)
- [ ] **E1–E2. Phoenix Forge expansion and Phoenix–SWDS integration** - TASKTRACKER
  - blueprint: Phoenix re-reads the same first 10 shards and appends 4 fixed axioms each cycle; overlaps Phase 3
- [ ] **F1–F6. Y789/Nexus bicameral engine, CWA 3.0 router, model assignment, Red/Blue/Purple modality, Corpus Callosum RRF** - TASKTRACKER
  - model assignment set 2026-10-09 (Y789 + Jean Grey on 3.8 Flash high, Nexus on Opus 5.5)
  - blueprint: the CWA "Bayesian posterior" equals the complexity score (no inference)
- [ ] **G1–G4. Heimdall CLI, security protocol, context/stress monitoring, security dashboard API** - TASKTRACKER
  - blueprint: gatekeeper role not built; overlaps Phase 4 (ADR-007)
- [ ] **H1–H3. Cognitive throttling, agent-kernel-engine taxonomy, agent registry** - TASKTRACKER
- [ ] **J1–J4. Conceptual research: Kirk/Spock, chess/Go/game theory, Tetris, systems theory in Shiva/Zenitsu** - TASKTRACKER

## Done
- [x] ~~Move the genesis-kernel skill into .agents/skills (main folder + homebase)~~ (2026-10-11)
- [x] ~~kernel_ctl.ps1 and the genesis-kernel skill so Antigravity can run the kernel~~ (2026-10-10)
- [x] ~~Remove Gemini 3.5/3.6/3.7; Y789 and Jean Grey on 3.8 Flash high thinking~~ (2026-10-09)
- [x] ~~D-15: Rodin sub-agents carry no model; SKILL.md §15 and §8.5.1 corrected~~ (2026-10-09)
- [x] ~~Heimdall opens and closes the SWDS cycle; Phoenix no longer vents Heimdall~~ (2026-10-09)
- [x] ~~Master Architecture Blueprint and shareable page~~ (2026-10-09)
