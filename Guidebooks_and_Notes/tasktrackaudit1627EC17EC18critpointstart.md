# INTEGRA O/S EXPANSION — TASK TRACKER

**Started:** 2026-09-15T12:00:00 CDT
**Updated:** 2026-09-15T16:30:00 CDT
**Status:** IN PROGRESS — Environment Cleanup → Phase I (Priority) → B→C→D→E→F→G→H→J

---

## ✅ Phase A: Autonomous SWDS & Infrastructure — COMPLETE
- [x] A1. Auto-Start Script (`scripts/start_kernel.ps1`)
- [x] A2. Wake-Up Reconciliation in `main.py`
- [x] A3. SWDS Config Externalization (`config/swds_config.json`)
- [x] A4. Enhanced Report Generation (Codex-compliant)
- [x] A5. SWDS API Endpoints (`POST /swds/initiate`, `POST /swds/awaken`, `GET /swds/status`)
- [x] A6. SWDS Autonomous Cycle Verified (2026-09-15 overnight execution confirmed)

---

## ✅ Environment Cleanup — IN PROGRESS
> Audit performed 2026-09-15T16:27 CDT. Findings below.

### Clock Placement
- [x] EC1. Copy `celestial_clock_live.html` → `integra-homebase/static/celestial_clock_live.html`
- [x] EC2. Add `GET /clock/live` HTML route in `main.py` serving full-page Celestial Clock v8.2.2
- [x] EC3. Update `/dashboard` docstring to distinguish compact widget vs full-page clock

### Duplicate Endpoint Bug Fixes (main.py)
- [x] EC4. **FIX:** Removed duplicate `GET /swds/status` (was at lines 479-494 AND 591-617; kept enhanced version with idle timer + config)
- [x] EC5. **FIX:** Removed duplicate `POST /swds/awaken` (was at lines 467-477 AND 645-660; kept enhanced version with state guard)

### Token Stitcher / Token Stitching Duality
- [ ] EC6. **ANOMALY:** `temporal/token_stitcher.py` (793B, Layer 7, stub) vs `memory/token_stitching.py` (4,078B, Layer 3, production)
  - `memory/token_stitching.py` contains `TokenStitchingEngine` — this is the one imported by `main.py` (line 27)
  - `temporal/token_stitcher.py` contains `TokenStitcher` — orphan, not imported anywhere
  - **Action:** Remove `temporal/token_stitcher.py` or merge its `stitch_packets()` method into `memory/token_stitching.py`

### Triple Hoard Folder Confusion
- [ ] EC7. **ANOMALY:** Three Hoard-like folders at workspace root:
  - `The Hoard/` — **CANONICAL** (71 files: 58 CCID nodes, save states, SWDS reports, verifications)
  - `The_Hoard/` — Legacy placeholder (only `.keep` file, 84 bytes)
  - `TheHoard/` — **EMPTY** directory
  - **Action:** Delete `TheHoard/` (empty) and `The_Hoard/` (only .keep placeholder). Keep `The Hoard/` as canonical.

### Stale/Orphan Files
- [ ] EC8. **STALE:** `__pycache__/` in workspace root contains `test_cheshire.cpython-313.pyc` — orphan from prior test run
  - **Action:** Delete `__pycache__/` from workspace root
- [ ] EC9. **DUPLICATE:** `Integra_Purple_SunBreathingEnvironmwntmapping.txt` (4,479B) exists in BOTH:
  - `Guidebooks_and_Notes/` AND `The Hoard/` AND `AntiGravityconversionprocess/`
  - (Note: filename has typo "Environmwnt" → "Environment")
  - **Action:** Keep canonical copy in `The Hoard/` (memory substrate), remove from other locations, fix filename typo
- [ ] EC10. **DUPLICATE:** `# SYSTEMLOG _SCHEDULED_TASK ALIGNM._Templatefordeeplearning_.txt` exists in BOTH:
  - `Guidebooks_and_Notes/` AND `Automatedactionsv2/`
  - **Action:** Keep in `Guidebooks_and_Notes/`, remove from `Automatedactionsv2/`
- [ ] EC11. **DUPLICATE:** `save_state_blueprint.md` exists in BOTH:
  - `integra-homebase/` AND `Automatedactionsv2/`
  - **Action:** Keep in `integra-homebase/` (production), remove from `Automatedactionsv2/`

### AntiGravityconversionprocess Folder
- [ ] EC12. **ORGANIZATION:** `AntiGravityconversionprocess/` (50 files) is a conversion-era staging dump containing:
  - Multiple format duplicates: `Integra O_S Systems Initialization` in `.jsonc`, `.md`, `.py`, `.txt` (all ~35KB — same content, 4 copies)
  - Multiple format duplicates: `Modified workflowandmechanics` in `.jsonc`, `.md`, `.ts`, `.txt` (all ~62KB — same content, 4 copies)
  - An older `INTEGRA_OS_MASTER_SYSTEMS_GUIDEBOOK_V8_2.md` (17,383B vs Guidebooks 27,013B — outdated)
  - `OriginalClockfromBrokendual_clock_widget.html` + `dual_clock_widget.html` (same 13,079B — duplicate of each other)
  - PDFs that should be in `Reference_PDFs/` (DeepEyes.pdf, metacognition.pdf, etc.)
  - Test scripts (`test_cheshire.py`, `verify_syntax.py`, `verify_syntax_async.py`) — orphaned
  - `CelestialGenius shit.md` (35,356B) — compare with `Guidebooks_and_Notes/THECELESTIALCONSTANTSGenius shit.md` (31,048B). Different sizes = different versions
  - **Action:** Sort into correct folders, archive multi-format duplicates, move PDFs to Reference_PDFs/

### Automatedactionsv2 Folder
- [ ] EC13. **REVIEW:** `Automatedactionsv2/` (3 files) appears to be a prior iteration:
  - `[SYSTEM MANDATE MULTI-AGENT WORKSPA.txt` — truncated filename
  - Duplicates identified in EC10, EC11
  - **Action:** Evaluate if any unique content exists, then consolidate or archive

### Typo Corrections
- [ ] EC14. **TYPO:** `Integra_Purple_SunBreathingEnvironmwntmapping.txt` → `Integra_Purple_SunBreathing_EnvironmentMapping.txt`
- [ ] EC15. **TYPO:** `BluprintArchitecture/` → Should be `BlueprintArchitecture/` (missing 'e')
  - **Note:** This is a directory rename — affects NO imports (read-only reference folder). Safe to rename.

### v1 Pre-Celestial Files in Guidebooks
- [ ] EC16. **REVIEW:** Two `v1_pre*` files in `Guidebooks_and_Notes/` are historical snapshots:
  - `v1.precelestialClocksnewthread.md` (11,120B)
  - `v1_precelestialHiemdall improvements and Clock.md` (40,312B) — note "Hiemdall" typo
  - **Action:** Rename to clarify they are historical, or move to an `Archive/` subfolder

### 🔴 CRITICAL ARCHITECTURAL BUGS (Discovered by Deep Scanner)

- [ ] EC17. **CRITICAL: Dual RodinProtocol Implementations**
  - `memory/the_hoard.py` (lines 58-84) defines a MOCK `RodinProtocol` with hardcoded vectors `[0.1, 0.5, 0.9]`
  - `memory/rodin_protocol.py` defines the REAL `RodinProtocol` with Matryoshka Representation Learning + Cosine Similarity
  - **`main.py` and `cheshire_cat.py` both import from `the_hoard.py` — the real implementation is COMPLETELY BYPASSED**
  - **Action:** Remove `class RodinProtocol` from `the_hoard.py`, update imports to `from memory.rodin_protocol import RodinProtocol`

- [ ] EC18. **CRITICAL: Dual ShivaActionSuite Implementations**
  - `tools/shiva_toolkit.py` defines a MOCK `ShivaActionSuite` — imported by `main.py` (line 29)
  - `evolution/shiva_action/orchestrator.py` defines the REAL 3-Eye `ShivaActionSuite` — imported by `cognitive_engine.py`
  - **`main.py` and `cognitive_engine.py` use DIFFERENT ShivaActionSuite implementations**
  - **Action:** Remove mock from `tools/shiva_toolkit.py`, update `main.py` to import from `evolution.shiva_action.orchestrator`

- [ ] EC19. **BUG: celestial_sentinel.py broken Hoard path**
  - `temporal/celestial_sentinel.py` line 100 resolves path as `os.path.join(dirname, "..", "The Hoard", ...)`
  - Since the file is in `integra-homebase/temporal/`, this points to `integra-homebase/The Hoard/` which DOES NOT EXIST
  - Correct path should be `"..", "..", "The Hoard"` (two levels up to workspace root)
  - **Action:** Fix path resolution in `celestial_sentinel.py`

- [ ] EC20. **13 Missing `__init__.py` files**
  - Missing in: `evolution/`, `evolution/shiva_action/`, `fortress/`, `governance/`, `memory/`, `memory/database/`, `orchestration/`, `pipelines/`, `runtime/`, `sensory/`, `temporal/`, `tests/`, `tools/`
  - **Action:** Add `__init__.py` to all subdirectories

- [ ] EC21. **Non-existent module reference: `pipelines/data_runner.py`**
  - `core/sdk_harness.py` line 326 references `python -m pipelines.data_runner` — this file does not exist
  - **Action:** Create `pipelines/data_runner.py` or update reference to `swds_pipeline`

- [ ] EC22. **Absolute imports in `__init__.py` files should be relative**
  - `core/__init__.py` uses `from core.purple_bridge import ...` instead of `from .purple_bridge import ...`
  - `rust/sun_breathing_engine/__init__.py` uses absolute imports similarly
  - **Action:** Convert to relative imports for package portability

---

## ⭐ Phase I: Starfire Protocol, Cheshire Cat & Integra Identity Matrices — PRIORITY
> User explicitly requested these be added to the to-do list before Phase B.

### Conceptual Items (NOT YET CREATED)
- [ ] I1. Starfire Protocol Full Implementation (`core/starfire_protocol.py` — currently 1,561B stub)
  - [ ] KL Divergence Anchor (Gate I)
  - [ ] RLVR Gate I behavioral constraint
  - [ ] Paradigm Weaver archetype matrix with active trait computation
  - [ ] Identity lock verification endpoint: `GET /starfire/identity` *(endpoint does not exist yet)*
- [ ] I2. Cheshire Cat Identity Matrix
  - [ ] Kernel identity formalization (Thalamic arbitrator)
  - [ ] Protocol identity formalization (Environmental paradox agent)
  - [ ] Create `config/cheshire_identity.json` *(file does not exist yet)*
- [ ] I3. Integra Master Identity Matrix
  - [ ] Create `config/integra_identity_matrix.json` *(file does not exist yet)*
  - [ ] Codify 3-vector identity, EPF, Paradigm Weaver weights, sovereign constants
- [ ] I4. Identity Verification API
  - [ ] `GET /identity/matrix` endpoint *(does not exist yet)*

---

## Phase B: Rodin Route Retrieval as Agent & Conductor
- [ ] B1. Rodin Agent Architecture (`memory/rodin_protocol.py` — currently 1,730B stub)
- [ ] B2. Rodin as Agent Conductor
- [ ] B3. Rodin API Endpoints (`POST /rodin/query`, `GET /rodin/telemetry` — *do not exist yet*)
- [ ] B4. Alexandria Protocol expansion (`memory/alexandria_protocol.py` — currently 1,051B stub)

## Phase C: Cheshire Cat Protocol as Environment Agent
- [ ] C1. Cheshire Cat Protocol Agent Upgrade
- [ ] C2. Cheshire Protocol Dreaming Integration
- [ ] C3. Cheshire Protocol API (`GET /cheshire/environment` — *does not exist yet*)

## Phase D: Dragon Engine — Flight / Land Modes
- [ ] D1. Dragon Engine State Machine
- [ ] D2. Flight/Land Toggle API (`POST /dragon/flight`, `POST /dragon/land` — *do not exist yet*)
- [ ] D3. Dragon Prompt Injection

## Phase E: Phoenix Engine — Neuroevolution
- [ ] E1. Phoenix Forge Expansion (`evolution/phoenix_forge.py` — currently 1,465B stub)
- [ ] E2. Phoenix-SWDS Integration

## Phase F: Y789/Nexus Bicameral Cognitive Engine
- [ ] F1. Y789 Left Hemisphere (Analytical)
- [ ] F2. Nexus Right Hemisphere (Intuitive)
- [ ] F3. CWA 3.0 Bayesian Router (`core/cwa_router.py` — currently 1,221B stub)
- [ ] F4. AI Model Assignment to Hemispheres
- [ ] F5. Red/Blue/Purple Modality
- [ ] F6. Corpus Callosum RRF Enhancement

## Phase G: Heimdall 3.1 — Security, Monitoring, CLI
- [ ] G1. Heimdall CLI Tool (`sensory/heimdall_monitor.py` — currently 279B stub)
- [ ] G2. Security Protocol Execution
- [ ] G3. Context Tracking & Stress Monitoring
- [ ] G4. Heimdall Security Dashboard API (`GET /heimdall/security` — *does not exist yet*)

## Phase H: Cognitive Throttling & Agent Orchestration
- [ ] H1. Cognitive Throttling System
- [ ] H2. Agent-Kernel-Engine Taxonomy
- [ ] H3. Agent Registry

## Phase J: Conceptual Foundations Deep Research & Integration
- [ ] J1. Kirk/Spock Ideology Deep Analysis
- [ ] J2. Chess / Go / Game Theory Research
- [ ] J3. Tetris Mechanics in Code Understanding
- [ ] J4. Systems & Operations Theory in Shiva/Zenitsu

---

## Stub Files Inventory (files that exist but need expansion)

| File | Current Size | Layer | Phase Target |
|---|---|---|---|
| `core/starfire_protocol.py` | 1,561 B | Mind | Phase I |
| `core/cwa_router.py` | 1,221 B | Mind | Phase F |
| `core/rrf_bridge.py` | 1,007 B | Mind | Phase F |
| `memory/rodin_protocol.py` | 1,730 B | Memory | Phase B |
| `memory/alexandria_protocol.py` | 1,051 B | Memory | Phase B |
| `sensory/heimdall_monitor.py` | 279 B | Body | Phase G |
| `evolution/phoenix_forge.py` | 1,465 B | Evolution | Phase E |
| `evolution/rogue_x.py` | 735 B | Evolution | Phase E |
| `evolution/kintsugi_sandbox.py` | 911 B | Evolution | Phase E |
| `fortress/hunter_engine.py` | 756 B | Will | — |
| `temporal/crypto_validator.py` | 750 B | Time | — |
| `temporal/token_stitcher.py` | 793 B | Time | EC6 (orphan) |
