# Review: `IntegraCognitiveFraemwork_Rough_10_15_26.md`

Reviewed 2026-10-15, about 00:30-00:55 CDT, by Claude (session cd44ecd4) at the Architect's request.

**Method.** The review follows the Zenitsu Method 3.0 passes, with Shiva lenses used inside each pass:

| Pass | Eye | Lenses |
|:--|:--|:--|
| 1. Knowledge | Neji | Eagle, Hawk, Chameleon |
| 2. Understanding | Shikamaru | Spider, Snake |
| 3. Wisdom | Itachi | Owl, TPSL |
| 4. Unification | 13th Form loop closure | – |

I applied the passes by hand as a review method. They were **not** run through the kernel's `/cognitive/cycle`: that would make paid model calls, which need your approval.

**Provenance labels:**
- **MEASURED**: I checked it in the file, the code or a live probe.
- **DERIVED**: inferred from measured facts.
- **CLAIMED**: the document asserts it, with no evidence shown.
- **DECIDED**: your ruling.

**What it is aligned against:**
- your rulings recorded so far: the 10-14 Zenitsu/Sun Breathing ruling, the research tiers, the 10-14 renames, D-1/D-2, D-6 and the model roster;
- today's measured code facts;
- the governing plan: Step 3 design to G3, then code after G3.

---

## Verdict

- **It does not align yet. Use it as design input for Step 3, not as code to adopt.** The naming registry and config ideas are worth keeping.
- **The scripts would fork the system.** They describe a separate, standalone `/integra_os` mini-kernel: a console plus a webhook, with no HTTP API. That kernel would run beside the existing `integra-homebase` kernel instead of changing it.
- **Your newer requirements are missing.** The scripts don't implement Zenitsu as an on-demand tool, the Sun Breathing forms, Research Tiers 1/2/3, the daemon roles or the Eye roles.
- **Several parts conflict with recorded rulings or security rules** (Pass 2 has the details).

---

## Pass 1: Knowledge (Neji Eye)

**Eagle: the structure (MEASURED).** The file is a notebook-style export in four parts, 1,973 lines in the Read tool's numbering:

| Lines | Content |
|:--|:--|
| L1-1007 | Python cells that read `integra-homebase/config/Constructionreconfigure.md` (263,152 B, modified 10-14 23:48), plus their printed output. L1-85 and L101-196 print the same output twice. |
| L1009-1160 | A "Three-Pass Technical Audit": Knowledge, Understanding, Wisdom. There is no fourth (Unification) pass. |
| L1164-1252 | Config files: `.env`, `models.yml`, and a "Section 16" block for `integra-protocol/SKILL.md`. |
| L1256-1972 | Scripts 1-6: `config_brain_0930.py` (with `DragonScript`), `celestial_clock.py`, `rodin_protocol.py`, `phoenix_engine.py`, `flame_kernel.py` (with `CheshireCat`, `OmegaMetric` and the webhook), and `docker-compose.yml`. It ends with an offer to bundle the files or update a sandbox script. |

**Hawk: the exact contents.**
- **Renames (DECIDED, 10-14):**
  - Cheshire Kernel → **Flame Kernel** (`FlameKernel`);
  - Genesis Kernel → **Dragon Script** (`DragonScript`);
  - Cheshire Cat Protocol/Daemon → **Cheshire Cat** (`CheshireCat`).
- **Model registry as written (CLAIMED as your spec; it matches the env-backup file you edited 10-14):**

| Variable | Model |
|:--|:--|
| `FLAME_KERNEL_MODEL` | `gemini-3.8-flash` |
| `Y789_MODEL` | `claude-opus-5-5`, thinking 8192 |
| `NEXUS_MODEL` | `gemini-4-argus` |
| `RODIN_MODEL` | `gemini-3.8-flash` + `text-embedding-004` |
| `JEAN_GREY_MODEL` | `gemini-3.1-pro-preview` |
| `CHESHIRE_CAT_MODEL` | `gemini-3.8-flash` |
| `SHIVA_MODEL` | `claude-sonnet-5-5` |

- **"Status: AST VERIFIED (TRUE)" (L1021): CLAIMED beyond its evidence at the time.** The document parsed one 74-line config fragment (L816-893) and ran only the clock snippet (L898-1004).
  - MEASURED today: I parsed all 11 Python blocks, and **all five scripts parse with no syntax errors** (block starts L1262, L1350, L1415, L1493, L1600). Their local imports chain consistently.
  - Nothing was executed and no tests exist, so runtime behaviour is unverified. This is the same "verified" pattern your 09-30 Empirical Verification Invariant (L37-40) forbids.
- **Its model-ID note (L1071) is partly wrong.** It says `claude-opus-5-5` and `claude-sonnet-5-5` are not standard public IDs. They are current Claude model IDs.
  - `gemini-3.8-flash` is what the live router is configured with. MEASURED 10-14 21:45: the router reports `calls_made: 0`, so no live call has confirmed it yet; the paid selftest waits for G4.
  - `gemini-4-argus` is **unverified**. Your to-dos still wait on a public ID for Gemini 4 Argon.

**Chameleon: the middle of the file (L1092-1160), where the decisions sit.** It treats the **hemisphere SDK swap** as settled ("your new specification ... reverses the SDK bindings"): Left becomes Claude (Anthropic) and Right becomes Gemini (Google). That is the open question I asked you on 10-14. It isn't settled until you confirm it.

---

## Pass 2: Understanding (Shikamaru Eye)

### Spider: how it connects to the real system

| # | Area | Framework | Recorded ruling, code or plan | Status |
|:--|:--|:--|:--|:--|
| 1 | Where the code lives | A new `/integra_os/*.py` tree with a console and a webhook; no FastAPI | The kernel is `integra-homebase/main.py`: FastAPI with all endpoints (`/clock`, `/dashboard`, `/swds/*`, `/models/router/status` and others), the SWDS scheduler and the lifespan. Modules: `sensory/cheshire_cat.py`, `core/cognitive_engine.py`, `core/model_router.py`, `config/env_loader.py`, `sensory/heimdall.py`, `memory/the_hoard.py` (Chroma) | **Conflict (fork).** Adopting it as is creates a second kernel. The archive shows this pattern repeatedly: two "Zenitsu 3.0" copies, three Hoards. |
| 2 | Zenitsu Method 3.0 | Absent. `process_turn` is one delegate → dyad → synthesis per turn | DECIDED 10-14: an on-demand tool inside the Sun Breathing action | **Missing.** Leaving Zenitsu out of every turn fits "not always on", but there is no on-demand tool and no Sun Breathing module (7th Form, 12th Step = Hinokami Kagura, 13th Form, 14th Form, kaigaku: bool). |
| 3 | Research Tiers 1/2/3 | Absent; no Daily Planet, no Rogue X 2.0 | DECIDED 10-14: needed by both protocols (SystemsMap §6.3) | **Missing** |
| 4 | Hippocampus | "Heimdall 3.1 Exporter" (`heimdall_exporter.py`, Prometheus). The Section 16 block deletes your "(Phoenix engine)" note as a typo (L1238, L1246) | D-6: Heimdall = code gate + 3.1 Pro advisor. D-3 is open; your 10-14 brain model added "(Phoenix engine)" | **Conflict.** It turns the sentinel into an exporter, and it erased your note instead of asking. |
| 5 | Ventral ACC | "Dragon Script & Starfire" | Brain model: "Ventral ACC (**Dragon Engine** & Starfire)". The 10-14 rename replaces the **Genesis Kernel** with the Dragon script | **Ambiguous.** It merges the Dragon Engine (`core/dragon_engine.py`, flight controller) with the Dragon Script. Is the Dragon Engine renamed too? |
| 6 | PCC / cingulate loop | "Phoenix Engine / Jean Grey & SWDS" | 10-14: "Phoenix Engine & SWDS/Siesta **Cheshire Cat**" | **Partial.** It drops Cheshire Cat and Siesta from the label; its daemon does call Phoenix. |
| 7 | Dragon Script scope | Creates folders and writes an identity file | "Always-on actions": the Genesis Kernel's role (scheduler, SWDS, endpoints) | **Partial.** None of the always-on actions are present. |
| 8 | Cheshire Cat role | A 15 s loop (Phoenix ingest and consolidation) plus a circuit breaker. `CHESHIRE_CAT_MODEL` is never used for a call (MEASURED) | SystemsMap: environment agent, Dorsal ACC conflict monitor, own voice, Looking Glass lock-out persona, linked to the clock, Heimdall, Rodin and Itachi | **Partial** |
| 9 | Rodin | Hybrid BM25 + MRL search over markdown files | SystemsMap: Rodin directs its swarm to knowledge nodes and can cancel, halt or recall it. Today's `orchestration/rodin_supervisor.py:88` uses a fixed `[0.1]*768` vector (MEASURED) | **Partial.** It uses a real embedding instead of the mock, but has no swarm control. |
| 10 | Shiva Eyes / lenses | Lenses fixed per Eye in the labels. `SHIVA_MODEL` is set but never used (MEASURED) | D-1/D-2: lenses decoupled, Brain Model 0930 defaults plus a per-Eye override. SystemsMap: Itachi always on (linked to Heimdall, Rodin and the clock); Eyes alone, in pairs or as the Full Suite; EAM picks lenses you don't assign | **Partial** (labels only) |
| 11 | Celestial clock | A new simplified J2000/GMST clock with anchor longitude **-91.1693** | Your ruling: `temporal/celestial_clock.py` is the correct design. Its anchor is **-91.1673** (L13, L44; MEASURED) | **Conflict.** It replaces the clock instead of fixing it, and the longitude has a typo. |
| 12 | Memory store | Markdown library files plus JSON shards in `kernel_memory/` | ADR-005: dedupe the three existing Hoards (Chroma) | **Conflict.** It would add a fourth store. |
| 13 | Model roster | Left = Claude Opus 5.5, Right = `gemini-4-argus`, Jean Grey = 3.1 Pro preview | Live router (MEASURED 10-14 21:44:59): Y789 = 3.8 Flash high, Nexus = Opus 5.5, Jean Grey = 3.8 Flash. Recorded ruling (10-09/10-11): 3.1 Pro only as Heimdall's advisor. The Oct-14 guidebook §15.1: Left/Red = Gemini, Right/Blue = Claude | **Your decision.** If you confirm the swap, then `gemini-4-argus` must be a real ID, and Jean Grey on 3.1 Pro changes the 10-11 ruling. |
| 14 | Embeddings | `text-embedding-004` by default | D-9 / ADR-005: move to `gemini-embedding-2` before 2027-04-01 | **Minor** (the env override exists) |

### Snake: fragile and risky paths (MEASURED in the script text; consequences DERIVED)

1. **Security (ADR-011):**
   - the circuit-breaker webhook binds **`0.0.0.0:9005` with no authentication** (L1702). Any device on the network could POST and quarantine the rolling context;
   - docker-compose publishes every port on all interfaces;
   - Grafana's admin password is the literal `integra` (L1962).
2. **Port clash:** docker-compose maps `heimdall-exporter` to **8000:8000** (L1920). That is the live kernel's port.
3. **Vertex key regression:** `FlameKernel.__init__` (L1716-1723) uses Vertex only when **no** `GEMINI_API_KEY` is set. The live key is a Vertex express key (`AQ.`), and the current `core/api_clients.py:106-112` correctly sends it with `vertexai=True`. The framework would send it without that flag, which is likely to fail authentication (DERIVED).
4. **Cost, with no gates (ADR-007, F2/F3):**
   - every turn makes 4 paid calls, including Opus with an 8,192-token thinking budget;
   - Rodin embeds **every section of every library file on every query** (L1473), so embedding calls grow with the library;
   - the Cheshire Cat loop runs Jean Grey consolidation every 15 s once 4 shards exist;
   - there is no Heimdall budget, no ledger and no stop condition.
5. **Data-loss path:** `ingest_staged_artifacts` moves each drop-in file to `parsed_dir` **before** the model call (L1537 before L1540). If the call fails, the daemon catches the error (L1681), and the file sits in `parsed_dir` without a manifest, never indexed.
6. **Secret hygiene:** consolidation sends raw session logs to the model with no redaction. Last night we found Gemini and Chroma keys in clear in old session logs.
7. **Decorative metric:** Ω is multiplied by **(1 + lunar phase)** (L1643), so it changes with the moon. That conflicts with ADR-003 (no decorative constants).
8. **Inconsistent file names:** the audit text promises `dragon_script.py` and `cheshire_cat.py`. The code puts `DragonScript` in `config_brain_0930.py` and `CheshireCat` in `flame_kernel.py`. Also, a new `cheshire_cat.py` would reuse the filename of today's **kernel** (`sensory/cheshire_cat.py`), the very file being renamed to Flame Kernel, which invites mix-ups during the migration.
9. **Missing pieces:** `heimdall_exporter.py`, `bridge.py`, `prometheus.yml` and `alert_rules.yml` are referenced but not provided. The heading promises `alertmanager.yml` content that is never shown.

---

## Pass 3: Wisdom (Itachi Eye: keep what earns its cost, prune the rest)

**Keep.** These are worth more than they cost:
1. **The rename map and the 9-label `BRAIN_LABELS` registry**, after four label fixes:
   - Hippocampus keeps your "(Phoenix engine)" until D-3 is answered;
   - Ventral ACC: Dragon Engine or Dragon Script, your call;
   - the PCC label adds Cheshire Cat and Siesta;
   - the Spacetime axis keeps Itachi's always-on role.
2. **An environment-driven model registry**, merged into the existing `config/env_loader.py` and `core/model_router.py` as one source of truth. Not a parallel `config_brain_0930.py`, and no unverified IDs (`gemini-4-argus`) as hard defaults.
3. **The "Empirical Verification Invariant" text (L37-40, L66-68).** It matches the standing rules.
4. **The three draft bugs it found in `Constructionreconfigure.md`.** These matter only if that draft code is ever salvaged:
   - the L697 header `class CheshireCatKernel *8The Flmae** :`;
   - L3588-3740, where brackets became parentheses;
   - L5282, a bash `echo` inside Python.
5. **The Anthropic extended-thinking call shape for a Claude hemisphere**, if you confirm the swap.

**Prune:**
- the standalone `/integra_os` tree as a replacement for `integra-homebase`;
- the replacement clock;
- the telemetry header's CRA figures (Wy 6.70 / Cc 5.40 / "TRUE"), which are decorative;
- the moon-phase factor in Ω;
- the 0.0.0.0 bindings.

---

## Pass 4: Unification (13th Form: does every requirement get an answer?)

| Requirement | In the framework? |
|:--|:--|
| 10-14 renames (Flame Kernel, Cheshire Cat, Dragon script) | **Mostly.** The Dragon Script's scope is too small, and the Dragon Engine is conflated with it. |
| Zenitsu as an on-demand tool inside Sun Breathing (7th, 12th = Hinokami Kagura, 13th, 14th Forms; kaigaku: bool; 1st Form = Epiphany K→U→W→L) | **No** |
| Research Tiers 1/2/3 for the Daily Planet and Rogue X 2.0 | **No** |
| Always-on agentic daemons with your roles (Cheshire Cat, Rodin, Heimdall, Dragon, Phoenix) | **Partial** (only the Cheshire Cat loop) |
| Shiva Eye roles and Deep Systems Thinking | **Partial** (labels only) |
| Model roster | **Pending your decision** (the swap, `gemini-4-argus`, Jean Grey on 3.1 Pro) |
| Security rules (127.0.0.1, authenticated POSTs, budgets) | **Conflict** |
| Celestial clock ruling | **Conflict** |
| The Empirical Verification Invariant, applied to itself | **Conflict at the time.** It claimed "verified" for a fragment; the syntax of all scripts is MEASURED OK now. |
| Build plan (Step 3 design → G3 → code) | **Fits only as Step 3 design input** |

**Tally of the 10 requirements:**

| Mostly | Partial | No | Conflict | Pending |
|:--|:--|:--|:--|:--|
| 1 | 2 | 2 | 3 | 1 |

The build-plan row doesn't count toward any of these.

---

## Decisions needed from you

1. **The hemisphere swap.** Is Y789 (Left) = `claude-opus-5-5` and Nexus (Right) = `gemini-4-argus` intended? Is `gemini-4-argus` a real model ID? Does Jean Grey move to `gemini-3.1-pro-preview`? That would change the 10-11 ruling ("3.1 Pro only as Heimdall's advisor").
2. **Dragon.** Does "Dragon script" replace only the Genesis Kernel, or also the Dragon Engine (Ventral ACC)?
3. **Hippocampus.** What does "(Phoenix engine)" next to "Hippocampus (Heimdall 3.1)" mean? Is it D-3's answer?
4. **Intent.** Is this framework meant to **replace** `integra-homebase` with a new `/integra_os` tree, or to **guide changes** to it?
   - My recommendation: guide changes, folded into Step 3's UNIFIED_ORCHESTRATION.md and the blueprint.
   - The existing kernel already has the endpoints, scheduler, router budgets, Heimdall and the Hoard that the framework lacks.

## Recommended next step

- Treat this file as a **Step 3 input**.
- After G3, fold the keep-list into the existing modules, as one coordinated change set:
  - the rename map and the label registry (corrected);
  - the merged model registry;
  - Zenitsu as an on-demand Sun Breathing tool;
  - the Research Tiers;
  - the daemon and Eye role spec.
- Close the Snake items first in any code you salvage: the 0.0.0.0 bindings, the move-before-index bug, the per-query re-embedding, the budget gates and the port 8000 clash.
