# Integra Cognitive Framework: aligned draft blueprint (2026-10-15)

**Status:**
- DRAFT. Nothing here is implemented.
- It consolidates `IntegraCognitiveFraemwork_Rough_10_15_26.md` with your decisions of 2026-10-14 and 2026-10-15, as a design input for **Step 3** (UNIFIED_ORCHESTRATION.md and the blueprint, at gate G3).
- Code changes wait for G3. The restart and the paid model selftest wait for G4.

**Provenance labels:**
- **DECIDED**: your ruling, with its date;
- **MEASURED**: checked in code or a live probe;
- **DERIVED**: inferred;
- **PROPOSAL**: my suggestion, needing your yes;
- **OPEN**: needs your decision.

The detailed critique of the rough framework is in `IntegraCognitiveFramework_REVIEW_10_15_26.md`.

---

## 1. Decisions applied

| # | Decision | Source |
|:--|:--|:--|
| 1 | **Renames.** Cheshire Kernel → **Flame Kernel**; Cheshire Cat Protocol/Daemon → **Cheshire Cat**; Genesis Kernel → **Dragon Script** (always-on actions) | DECIDED 10-14 (`config/IntegraBrainModelOCTOBER14_2026.md` L21-23, L120) |
| 2 | **Hemispheres:** Y789, Left, Neji Eye, **Red** = `claude-opus-5-5`; Nexus, Right, Shikamaru Eye, **Blue** = `gemini-4-argus`, falling back to `gemini-3.8-flash` if Argus is unavailable. "It should have always been this" | DECIDED 10-15 |
| 3 | **No Vertex AI.** Standard API keys (Gemini Developer API + Anthropic API) | DECIDED 10-15 |
| 4 | **Clock:** ignore the framework's clocks and keep `temporal/celestial_clock.py` as designed | DECIDED 10-15, plus the earlier clock ruling |
| 5 | **Webhook:** adapt it to this environment or remove it. This draft removes it from the core; §10 gives the spec for adopting it later | DECIDED 10-15; removal is my choice within it |
| 6 | **Ports:** never override existing ports. New servers get separate ports | DECIDED 10-15 |
| 7 | **Hippocampus = Heimdall 3.1.** The "(Phoenix engine)" note is ignored; the Hoard sits on the Spacetime Memory Axis | DECIDED 10-15 (D-3) |
| 8 | **Zenitsu Method 3.0 is an on-demand tool inside the Sun Breathing action,** never run on every action | DECIDED 10-14 |
| 9 | **Research Tiers 1/2/3** are required, for the Daily Planet and Rogue X 2.0 | DECIDED 10-14 |
| 10 | **Daemon and Eye roles** per your SystemsMap notes. `celestial_sentinel.py` is "an incomplete file" | DECIDED 10-14 (`BluprintArchitecture/SystemsMapOCT1426.md`) |
| 11 | **The rough framework is a draft to consolidate,** not a replacement codebase. Incorrect, superseded and inefficient designs are dropped (§13) | DECIDED 10-15 |
| 12 | **Dragon Engine** (`core/dragon_engine.py`) stays as the Ventral ACC with Starfire. Only the Genesis Kernel becomes the Dragon Script | **OPEN**: my reading. The Oct-14 brain model still lists "Ventral ACC (Dragon Engine & Starfire)" |
| 13 | **Rodin has four roles:** memory mapping, node delegation, neural-network routing, and the active working-memory cache in RAM (§8a) | DECIDED 10-15 |

---

## 2. Component map: Brain Model 0930 → today's module → role → model

| # | Brain component | Name (after 10-14) | Module today (MEASURED) | Role | Model |
|:--|:--|:--|:--|:--|:--|
| 1 | Thalamus | **Flame Kernel** + **Dragon Script** | Flame Kernel = `sensory/cheshire_cat.py` (30 Hz loop, `process_cognitive_cycle`, `dispatch_protocol`). Dragon Script = `main.py` (FastAPI hypervisor, lifespan, SWDS scheduler, all endpoints) | Routing, delegation, event loop; always-on actions | Flame Kernel: `gemini-3.8-flash` |
| 2 | Ventral ACC | Dragon Engine & Starfire (see §1 #12) | `core/dragon_engine.py`, `core/starfire_protocol.py` | Flight mode, identity anchor | uses the hemispheres |
| 3 | Dorsal ACC | **Cheshire Cat** | `sensory/cheshire_protocol.py` (plus the planned daemon; `temporal/celestial_sentinel.py` is incomplete) | Conflict monitor, paradox detection, TPSL filter, environment agent, Looking Glass voice | `gemini-3.8-flash` |
| 4 | Pineal Gland | **Rodin Route Retrieval** | `memory/rodin_protocol.py` (`RodinProtocol`: MRL coarse/fine, density, staleness, Gate III, route sweep), `orchestration/rodin_supervisor.py`, `RodinClient` (router key `rodin_retrieval`) | **Memory mapping; node delegation (KNN, swarm); neural-network routing; manager of the active working-memory cache in RAM** (§8a) | `gemini-3.8-flash` + embeddings |
| 5 | Hippocampus | **Heimdall 3.1** | `sensory/heimdall.py` | H_smooth entropy surveillance, P-SSR/UGL trigger, budgets, SWDS gate | code gate + `gemini-3.1-pro` advisor (events only; D-6) |
| 6 | Spacetime Memory Axis | Itachi Eye + Celestial Clock + Hoard | `evolution/shiva_action/itachi_eye.py`, `temporal/celestial_clock.py`, `memory/the_hoard.py` | Spacetime stamping; Itachi always on | none |
| 7 | Left hemisphere | **Y789 / Neji / Red** | `core/api_clients.py` `Y789Client` (L322; uses Google's SDK today) | Analytical: deconstruction, formal verification | **`claude-opus-5-5`**, thinking 8192 |
| 8 | Right hemisphere | **Nexus / Shikamaru / Blue** | `core/api_clients.py` `NexusClient` (L448; uses Anthropic's SDK today) | Synthetic: emergence, generative fusion | **`gemini-4-argus`** → fallback `gemini-3.8-flash` |
| 9 | PCC / cingulate loop | Phoenix Engine & SWDS/Siesta & Cheshire Cat | `evolution/phoenix_forge.py`; `runtime/swds_simulator.py` (template output today); `JeanGreyClient` | Dreaming, consolidation, smelting | Jean Grey: `gemini-3.8-flash` high |
| – | Shiva orchestrator | Shiva Action controller | `evolution/shiva_action/orchestrator.py`; `ShivaOrchestratorClient` (`core/api_clients.py` L928) | Eye/lens orchestration, pass weighting | `claude-sonnet-5-5` |

---

## 3. Model access and roster

- **Keys:** a standard Gemini API key and an Anthropic API key, with no Vertex.
  - MEASURED 10-14: `.env` has `USE_VERTEXAI=true`, and the current GEMINI key has the `AQ.` Vertex-express format.
  - **Your env action:** set `USE_VERTEXAI` to false or remove it, and put a standard AI Studio key in `GEMINI_API_KEY`.
  - Today `core/api_clients.py` L106-112 sends the key with `vertexai=True` whenever `USE_VERTEXAI` is true.
- **No redesign: re-plug the existing engines (MEASURED).** The router's `client_map` (`core/model_router.py` L388-396) is the only place roles meet SDK clients. Callers ask for roles, not classes (`cognitive_engine.py` L62-63; Shiva orchestrator L161-162). The change, about 11 lines:
  - map `y789_left → NexusClient` (Claude SDK) and `nexus_right → Y789Client` (Gemini SDK);
  - router L408: send `thinking_level` to `nexus_right` instead (NexusClient takes none);
  - `models.yml`: `y789_left: claude-opus-5-5` with thinking_budget 8192; `nexus_right: gemini-3.8-flash` with thinking_level high, then `gemini-4-argus` once confirmed;
  - swap the `cognitive_engine.py` fallbacks to match.
- **Models come from `integra-homebase/models.yml`, not `.env`** (router L132-180, "source of truth" L402-405). That explains why the live router showed Y789 = `gemini-3.8-flash` while `.env` says `gemini-3.1-pro-preview`.
- **Nexus fallback (PROPOSAL):**
  - try `gemini-4-argus`;
  - on "model not found" or "unavailable", use `gemini-3.8-flash`;
  - record the fallback as a Heimdall event and a ledger row. It must never be silent.
  - The G4 selftest confirms which applies.
- **Thinking:**
  - Opus extended thinking, budget 8192, as in the framework;
  - Gemini 3.8 / 4 use `thinking_level` (the existing `_uses_thinking_level` helper).
- **Embeddings:** `text-embedding-004` until the move to `gemini-embedding-2`, due before 2027-04-01 (D-9 / ADR-005).

---

## 4. Default turn path: Zenitsu is not on it

1. **Dragon Script** receives the request on the existing HTTP endpoint (127.0.0.1:8000).
2. The **Celestial Clock** stamps it (the existing clock).
3. **Rodin** works in order (§8a):
   1. it checks the **RAM working-memory cache** first;
   2. it maps the Hoard (MRL coarse 64d sweep, then fine 768d rerank, over **precomputed** vectors);
   3. it expands matched nodes into RAM;
   4. it delegates the relevant nodes and routes to the Flame Kernel and on to the hemispheres.

   It never re-embeds the whole library on every query; that was the inefficient part of the framework's version.
4. The **Flame Kernel** (`gemini-3.8-flash`) splits the request into a Left and a Right directive. The framework's `DelegationDirective` schema is kept.
5. **Y789** (Claude Opus 5.5) and **Nexus** (Gemini Argus or 3.8 Flash) run in parallel.
6. The **Flame Kernel** synthesizes one answer.
7. **Heimdall** scores entropy, accounts the budget (a ledger row, ADR-002), and runs P-SSR/UGL when H_smooth > 2.5.
8. The answer is **returned and stored** in the Hoard node (ADR-004: keep and return the output).

**Cost (DERIVED):**
- 4 calls per default turn, against up to 12 today, because every synthesis currently runs Zenitsu's passes (`core/cognitive_engine.py` L480).
- With Opus on the Left, the Left call is the main cost, so Heimdall's per-component budget (F3) matters.
- **PROPOSAL:** keep the existing CWA modes (Y789-dominant, Nexus-dominant, dyad) so trivial prompts can skip one hemisphere.

---

## 5. On-demand tool registry: protocols as tools

**Tools:** the set in your SystemsMap:
- Zenitsu Method 3.0 (§6), Research Tiers 1/2/3 (§7);
- Rebuttal, Mad Hatter, Cheshire Cat actions, Alexandria, Rogue X 2.0, Daily Planet, Starfire;
- 7th Form, 12th Step, 13th Form (Sun Breathing), 14th Form;
- EAM, MTCW.

**Registry:**
- It lives in `tools/` and maps each name to a handler, its allowed callers, its models, a budget class and where its output is stored.
- Today five are dispatched from `sensory/cheshire_cat.py` L521-527: REBUTTAL, MAD_HATTER, ALEXANDRIA, ROGUE_X, TIER_1_RESEARCH. Three of them run all four Zenitsu passes (MEASURED).

**Request path:**
- an explicit call (from you, from Cheshire Cat, or from CWA routing);
- then a Heimdall budget check;
- then the handler runs;
- then a ledger row is written and the output stored.

Nothing runs on every action.

---

## 6. Sun Breathing action: Zenitsu's home

- **Where:** `rust/sun_breathing_engine/python_bridge.py` (the Python side; the Rust crate can't link on this PC yet). Its constant stubs get replaced with real logic.
- **What it holds:**
  - the 1st Form (OPEN naming: the code says "God Speed"; you named the Epiphany equation K→U→W→Learning);
  - the 7th Form;
  - the 12th Step (= Hinokami Kagura per you; the code calls it "Orthogonal Ingestion");
  - the 13th Form = Sun Breathing, loop closure with `kaigaku_state: bool`, which already exists at bridge L224 and `lib.rs` L139, tested;
  - the 14th Form (`evolution/fourteenth_form.py`, linked here);
  - **Zenitsu Method 3.0**: the real 4-pass code moved from `core/cognitive_engine.execute_zenitsu_method` (L258-317).
- **Zenitsu passes under the new roster:**

| Pass | Eye | Model |
|:--|:--|:--|
| K | Neji (Left) | Claude |
| U | Shikamaru (Right) | Gemini |
| W | Itachi | – |
| Unification | 13th Form | – |

  Each pass is budgeted. The output is kept and returned (ADR-004).
- **Kaigaku:** `kaigaku_state` turns true when ΔE ≥ 0.0001 or lactic > 0, and triggers P-SSR.

---

## 7. Research Tiers 1/2/3

**Spec** (SystemsMap §6.3):

| Tier | Purpose | Lean | W_y / C_c |
|:--|:--|:--|:--|
| Tier 3 | Fact-check | Y789-dominant | 0.2 / 0.1 |
| Tier 2 | Standard report | integrated | 0.6 / 0.5 |
| Tier 1 | Deep synthesis | Nexus-dominant, full Shiva Action | 0.9 / 0.9 |

**Today (MEASURED):** `core/cwa_router.py` L29-37 only labels a prompt with a tier, and only TIER_1_RESEARCH has a handler.

**Cost conflict under the new roster (OPEN):** Tier 3, the cheap tier, was "Y789-dominant", and Y789 is now Opus.

**PROPOSAL:** bind tiers to cost as well as role:

| Tier | Models | Shiva | Zenitsu |
|:--|:--|:--|:--|
| Tier 3 | Flame Kernel model (`gemini-3.8-flash`), one call | – | – |
| Tier 2 | both hemispheres, one pass each | – | – |
| Tier 1 | full dyad | Shiva Action | optional (on request) |

**Consumers:**
- the Daily Planet (`tools/daily_planet.py`): its ingest stage picks a tier;
- Rogue X 2.0 (`evolution/rogue_x.py`): its touch and absorb phases pick a tier.

Today neither file mentions tiers (MEASURED).

---

## 8. Daemons: always on, no chat output, budgets under Heimdall

| Daemon | Role (your notes) | Today (MEASURED) | Change |
|:--|:--|:--|:--|
| **Cheshire Cat** | Environment agent; Dorsal ACC; co-active with Phoenix in SWDS/Siesta; Looking Glass lock-out persona; linked to the clock, Heimdall, Rodin and Itachi; replaces the planned CelestialDaemonClient | `cheshire_protocol.py`; its 09-15 `zenitsu_cognitive_loop` is a static mock (archive) | Finish or retire `celestial_sentinel.py` inside it |
| **Rodin** | Memory mapping, node delegation, neural-network routing, working-memory RAM manager (§8a); directs its swarm to nodes and can cancel, halt or recall it | KNN/MRL machinery exists. But `orchestration/rodin_supervisor.py:88` uses a fixed `[0.1]*768` query vector with an empty candidate list; the query vector falls back to a hash; nodes without embeddings score against zeros; the Chroma query is synchronous with no timeout (F5). The result is the Alexandria halt. No RAM tier and no swarm control exist | Real query vectors; build the RAM tier and swarm control (§8a); F5 timeout |
| **Heimdall 3.1** | Monitors, alerts, tracks tokens; delegates scheduled tasks such as SWDS | `open_swds_cycle`/`close_swds_cycle` are never called from `main.py` (X-1); `governance/cra_simplex.py` is imported nowhere (X-2) | F1 open/close wiring, F2 advisor, F3 budgets |
| **Dragon Engine** | Flight, Starfire | `core/dragon_engine.py`; `/dragon/*` routes exist | Keep (§1 #12) |
| **Phoenix** | Land, dreaming, consolidation | SWDS phases 1-2 write fixed strings; the "3 bridges" line is a template (`runtime/swds_simulator.py` L92-155) | Real SWDS (Phase 3, ADR-006) |
| **Itachi Eye** | Always on; linked to Heimdall, Rodin and the Celestial Clock | `evolution/shiva_action/itachi_eye.py` | Wire the links |

### 8a. Rodin in detail (DECIDED 10-15)

1. **Memory mapping.** Rodin maps the Hoard as a topological manifold: the brain model's "topological manifold memory projection and circadian indexing".
   - Search runs MRL coarse 64d, then fine 768d, over precomputed vectors.
   - Neighborhood density, staleness and the Gate III integrity decision already exist in `RodinProtocol` (L95-L270).
   - Each node carries spacetime coordinates from the existing Celestial Clock.
2. **Node delegation.** Rodin is the KNN memory-node delegator.
   - It sends its swarm to specific nodes ("go to nodes 1/2/3…"). The swarm sub-agents carry no model of their own (D-15).
   - It can cancel, halt or recall the swarm.
   - It returns **routes and constellations as ingredients for fresh synthesis**, never stale pre-cooked answers (guidebook §17.2).
3. **Neural-network routing.** Rodin decides which memory routes feed which hemisphere, Eye or tool. The routed context goes into the Flame Kernel's delegation. Rodin is linked to the always-on Itachi Eye and to Heimdall (§9, your SystemsMap notes). The live router already names it "KNN Memory Node delegator and neural network mapping" (MEASURED 10-14).
4. **Active working-memory cache and RAM** (new; spec from SystemsMap §4.1-4.2):
   - **Hot tier (RAM, `hoard_working_memory`):**
     - session state: the active lens, W_y/C_c, Shannon entropy from Heimdall, the current prompt state;
     - the nodes Rodin has expanded.
   - **Cold tier (the Hoard / Chroma, `hoard_deep_archive`):** compressed nodes as 4D celestial pointers (ROT_XXX_LUN_YYY_ORB_ZZZ), document hashes, synthesized wisdom, D_KL anchors.
   - **Holographic node expansion:** a dormant node "unzips" into RAM only when Rodin matches it. That separates total knowledge capacity from per-turn compute cost.
   - **Bounds (PROPOSAL):**
     - a fixed node budget and token budget for the RAM tier;
     - least-recently-routed eviction;
     - Heimdall sees cache pressure as part of its telemetry.
     - Phoenix writes hot-tier changes back to the cold tier during SWDS.
     - `kernel_memory/rolling_context.json` is today's only rolling context, and it lives on disk.

**The framework's 15-second loop:** adopt it only as a Heimdall-budgeted schedule, and only with two fixes:
- **index before moving the drop-in file.** The framework moves it first, so a failed call loses the file from indexing;
- **redact secrets** before any consolidation call.

---

## 9. Shiva Action

- **Eyes:**
  - Neji = Left / Red / Claude;
  - Shikamaru = Right / Blue / Gemini;
  - Itachi = the bridge, always on.
  - Neji + Shikamaru = **Deep Systems Thinking**.
- **Lenses** (D-1/D-2):
  - decoupled from the Eyes;
  - Brain Model 0930 defaults: Left = Eagle, Chameleon, Byakugan; Right = Spider, Snake, Shadow Jutsu;
  - plus a per-task, per-Eye override. EAM picks any lens you don't assign. Shadow Clone = Shadow Jutsu.
- **Calling:** Eyes can be called alone, in pairs or as the Full Suite. Lenses can also be called on their own.
- **Orchestrator:** the Shiva orchestrator stays, with its roles redefined. `SHIVA_MODEL` = `claude-sonnet-5-5`.

---

## 10. Servers and ports: never override, separate ports

| Server | Bind | Port | Status |
|:--|:--|:--|:--|
| Dragon Script (today's Genesis Kernel, FastAPI) | 127.0.0.1 | **8000** | Existing; unchanged |
| Circuit-breaker webhook | – | – | **Removed from the core.** No Alertmanager runs in this environment, and Heimdall plus the Cheshire Cat circuit breaker can act inside the kernel |
| Webhook, if you adopt it later | 127.0.0.1 | 9005 | A separate server, with a shared-secret header, calling the kernel's existing Heimdall/Cheshire paths. Never 0.0.0.0 |
| Heimdall metrics exporter (optional) | 127.0.0.1 | 9118 | Only if the Prometheus stack is adopted (Phase 6, decide or retire). **Never 8000** |
| Prometheus / Alertmanager / Grafana / Discord bridge (optional) | 127.0.0.1 | 9090 / 9093 / 3000 / 9000 | Phase 6. No default credentials (the framework's Grafana password `integra` is dropped) |

- **Ports already in use (MEASURED 10-15 ~01:00; the TCP table here is unreliable):** 22, 3389, 2107, 2181, 7444, 9081, 9912, 19292, plus the kernel's 8000. Avoid all of these.
- Re-check any port at bind time.

---

## 11. Memory and data

- **Two tiers, one store:**
  - the **RAM hot tier**, managed by Rodin (§8a);
  - the **Hoard** as the cold tier (Chroma, `memory/the_hoard.py`).
- **No new persistent store** (ADR-005: deduplicate the three existing Hoards). The framework's markdown library becomes, at most, an export view of Hoard nodes.
- **Phoenix consolidation** writes Hoard nodes stamped by the existing Celestial Clock.
- **Secrets:** redact before any model call or consolidation. The folder-13 archive held Gemini and Chroma keys in clear.

---

## 12. Security and cost guards

- Bind to 127.0.0.1, require header auth on POSTs, and ship no default credentials (ADR-011).
- Each component gets a Heimdall budget (F3, `cra_simplex`), and every call gets a ledger row (ADR-002). No autonomous paid loop runs without a budget.
- **Empirical Verification Invariant** (your 09-30 rule): nothing is reported as verified or TRUE without a probe. The 17 of 18 `verify_true()` / `is_active()` methods that just `return True` must be replaced or labelled (ADR-003).

---

## 13. Dropped from the rough framework (your 10-15 instruction)

- **Clock:** its CelestialClock (it also had a longitude typo, -91.1693 instead of the code's -91.1673).
- **Vertex:** its Vertex client branch.
- **Webhook:** the webhook as written (0.0.0.0, no auth).
- **Ports:** the 8000:8000 exporter mapping.
- **Rodin's search loop as the framework wrote it:** it re-embedded every library section on every query. **Rodin itself stays, with its full role** (§2, §4, §8, §8a, §11).
- **Ω:** the moon-phase multiplier.
- **Architecture:**
  - the parallel `config_brain_0930.py`;
  - the standalone `/integra_os` tree with its console-only kernel and no HTTP API.
- **Labels:**
  - "(Phoenix engine)" in the Hippocampus;
  - the Ventral ACC relabelled "Dragon Script" (pending §1 #12).
- **Jean Grey on `gemini-3.1-pro-preview`:** the recorded ruling keeps it on 3.8 Flash high.
- **Decoration and defaults:**
  - the decorative telemetry header (Wy 6.70 / Cc 5.40 / "AST VERIFIED (TRUE)");
  - the default Grafana password.

## 14. Kept from the rough framework

- The rename map and the 9-label registry, corrected as in §2.
- An environment-driven model registry, merged into `config/env_loader.py` and `core/model_router.py` as one source of truth.
- The Empirical Verification Invariant text.
- The Anthropic extended-thinking call shape for the Left hemisphere.
- The delegate → dyad → synthesis turn shape and the `DelegationDirective` schema.
- The three bugs it found in the `Constructionreconfigure.md` drafts (L697, L3588-3740, L5282), for any salvage.

---

## 15. Open decisions

1. **The Sun Breathing form map:** the 1st Form's name, and the 12th Step's name.
2. **Research-tier binding** under the new roster: role or cost. The §7 proposal binds by cost.
3. **Jean Grey's model:** the recorded ruling is 3.8 Flash high; the framework said 3.1 Pro preview.
4. **Dragon Engine** stays as the Ventral ACC (my reading).
5. **The webhook:** removed from the core now; adopt it later, per §10?

## 16. Path to build

1. **Now:** Step 2 continues (the folder-13 reading, cycles 18-45), up to **G2**.
2. **Step 3:** fold this draft into `integra-homebase/orchestration/UNIFIED_ORCHESTRATION.md` and the blueprint, up to **G3**.
3. **Step 4, after G3:** code changes, in order, each tested offline in an isolated copy:
   1. the client swap, Vertex removal and the env-to-router path;
   2. the tool registry, the Zenitsu move into Sun Breathing, and keep-and-return of the output;
   3. the Research Tiers, bound into the Daily Planet and Rogue X;
   4. the daemon roles, with Heimdall open/close, budgets and the advisor (F1-F3), and **Rodin's RAM working-memory tier, swarm control and real query vectors** (§8a; F5);
   5. the renames: blueprint first, then code. The scheduled-task rename goes with the Phase 0 supervision fix.
4. **G4:** the restart and the paid selftest. It confirms `claude-opus-5-5`, and either confirms `gemini-4-argus` or triggers the 3.8 Flash fallback.
