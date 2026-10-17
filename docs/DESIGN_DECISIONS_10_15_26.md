# Design: the Architect's 2026-10-15 decisions

Status: **design only. No code, model, task or kernel was changed.** Code moves in Step 4, after gate G3; renames wait for G3 as well. Written 2026-10-15 (CDT) in Claude Code session 3d3aedaa, from the Architect's answers to the twelve questions of the Step 5 synthesis. The archive evidence behind the Zenitsu requirements is local and git-ignored (`The Hoard/antigravity_conversations/_summaries/step56/`); nothing from it is quoted here.

Labels: **DECIDED** = the Architect's own words; **ASSUMED** = my reading, needs a yes; **OPEN** = nobody has decided; **MEASURED** = read in the current code on 2026-10-15 (`file:line`); **DERIVED** = follows from measured code.

## 1. Decisions recorded

| # | Decision (DECIDED) | Touches |
|:--|:--|:--|
| D1 | The `~/.gemini` governance files are rewritten to the current rulings (not retired); the home locality and the Sovereign Override are removed. The Three Laws move into the Guiding Principles. Their order waits for historical documents the Architect will find. | Q8, Q9 |
| D2 | Phoenix Force is Jean Grey's "Operation Phoenix Force" run, executed by the Phoenix **during an SWDS cycle**. While Phoenix flies on predetermined prompt operations, Cheshire Cat performs Phoenix's tasks. When Phoenix ends, each returns to its own function. The second authentication exists only inside an SWDS cycle and **is the Architect's own prompt** requesting the autonomous action. | Q10 |
| D3 | "Shesha" stays retired (it was a typo). Cheshire Cat keeps its name; the former Cheshire Kernel is "The Flame". | Q11 |
| D4 | The Genesis Kernel (which boots the always-on actions) is consolidated and merged with the Dragon functions. The merged component may keep "Genesis Kernel" or be called "Dragon driver" or "Dragon engine". | rename ruling |
| D5 | The celestial time function gets a **Celestial Sentinel** (the file already begun) as its runtime owner. | Q12 |
| D6 | Zenitsu pass 4 is **Unification**. Neji's pass runs on Y789 (Opus); Shikamaru's on Nexus (Argus, Flash as fallback). **Itachi links Celestial Time, Heimdall, Cheshire and Rodin.** | Q1, Q2 |
| D7 | Budgets are ignored in this design. | Q4 |
| D8 | Gate III (Alexandria fallback): the Architect will find a historical document and wants a reminder. | Q5 |
| D9 | Tier 1 = Deep Synthesis (0.9/0.9), Tier 2 = Standard (0.6/0.5), Tier 3 = Fact-Check (0.2/0.1). | Q6 |
| D10 | Callers (Q7): Sun Breathing is Zenitsu's home; the Dragon P-SSR recovery path, Research Tier 1 and the Architect's own invocation may request it; Rogue X and Phoenix go through Sun Breathing; Heimdall gates all. | Q7 |

## 2. Assumptions to confirm and open items

- **A1 (DECIDED 2026-10-15: "A1 is correct").** Heimdall performs the Phoenix/Cheshire handover. The blueprint agrees (ADR-006 action 2, R-5). Heimdall alone opens and closes SWDS and no other component moves thalamic state (ruling of 2026-10-09). D2 does not say who triggers the swap.
- **A2 (DECIDED 2026-10-15: "A2 correct").** "Ignore budgets" (D7) removes per-pass caps from the Zenitsu contract. It does not lift the standing rules: no paid call, restart or deletion without the Architect's approval, and no test against the live repo. In D2 the Architect's prompt is that approval for the run.
- **A3 (OPEN).** No model is assigned to Itachi's pass or to Unification. Suggestion: Itachi's pass is mostly linking, so it runs on whichever hemisphere the CWA weight selects; Unification on Nexus, as the existing fusion step does (`core/cognitive_engine.py:252`).
- **A4 (ASSUMED; supported by the blueprint, see 2b).** With D5, `GET /celestial/checkpoint` becomes read-only and only the Sentinel writes the checkpoint.
- **A5 (OPEN).** The merged Genesis/Dragon component's name (D4).
- **A6 (OPEN).** The Three Laws' order (D1, awaiting documents); the name of the chaos engine that the old guidebook calls "Cheshire Cat" (it collides with D3); Gate III (D8); the models for Itachi and Unification (A3).

## 2b. Cross-check against the Master Architecture Blueprint v.9.9.1

The Architect pointed out on 2026-10-15 that many answers already sit in [MASTER_ARCHITECTURE_BLUEPRINT.md](MASTER_ARCHITECTURE_BLUEPRINT.md). Read for this check: section 1, the v.9.9.1 update, 4.4.1, 4.5, 5.0-5.4, 5.6-5.9, section 7 (R-1 to R-10), ADR-001, 005, 006, 007, 009, 010, 011, and sections 10 and 11. Line numbers are the blueprint's.

| Topic | What the blueprint says | Effect on this design |
|:--|:--|:--|
| Pass names and Itachi (Q1) | L513: the cognition path runs "Neji → Shikamaru → Itachi → Unification". R-1 (L897): Itachi = Wisdom / temporal bridge between Rodin and Heimdall. R-2 (L907): Itachi tests each understanding against time and intent; "drop TPSL pruning from Itachi; TPSL is a governance gate, not an Eye". | Pass 4 = Unification agrees. The Itachi row in 4.4 no longer returns a TPSL verdict. D6 adds Cheshire to Itachi's links. R-2 is still a proposal awaiting sign-off. |
| Models (Q2) | 4.4.1 holds the 2026-10-09 roster. R-1 seats Neji on the Left (Y789) and Shikamaru on the Right (Nexus). | The 10-15 roster supersedes 4.4.1 (Step 3 updates it). Itachi's and Unification's models are set nowhere (A3). |
| Lens map (Q3) | Decision 2 (L84) and R-1: Brain Model 0930 defaults, lenses decoupled, per-task override. | Answered. |
| Budgets (Q4) | ADR-007 duty 1: per-component budgets through the router, alerts at 80 %, hard stop at 100 % (Proposed). | D7 keeps budgets out of the Zenitsu contract; ADR-007 stays the home of budgets. |
| Gate III (Q5) | FP-31 and 5.3.2: fixed mock vector, always HALT into Alexandria; the fix is a real query embedding and model-free swarm roles. | Whether Zenitsu pass 3 keeps the Alexandria route is not answered; it waits for the Architect's document (D8). |
| Tiers (Q6) | L507: T1 0.9/0.9, T2 0.6/0.5, T3 0.2/0.1. | Agrees with D9. The "inverse numbering" in the Step 5 synthesis was a misreading of the ruling's listing order. |
| Governance files (Q8) | D-7: remove the Sovereign Override. D-15 done. Finding 12: the 10/07 learning proposal was never applied. | Consistent with D1. |
| Three Laws (Q9) | R-8 (L937) and D-8: the user first, the user's code and data second, the system's continuity third; the V1.0.0 order "should not survive into any constitution". | The proposal exists. The Architect will bring historical documents before signing off (D1). |
| Phoenix Force (Q10) | FP-26 (L855) and 5.2.5: "two-key" is a label. ADR-011 action 1 (L1447): the header **and** a second factor. ADR-009 (L1355): the Daemon acts as the Land crew during Phoenix Force. ADR-006 action 2 (L1240): Heimdall opens and closes every cycle; Phoenix never moves thalamic state. 5.6.1: the Jean Grey smelt is reachable only through `_kintsugi_ref`, which is never assigned. | D2 is the blueprint's design with the second factor defined as the Architect's prompt, scoped to SWDS. It supports A1. |
| Chaos engine (Q11) | R-4: one entity named Cheshire with two modes. 5.4.2: `dream_conductor` lives in the Protocol. | DERIVED: the old guidebook's REM chaos engine is the Cheshire Cat's dream conductor, so it needs no separate name. Needs a yes. |
| Clock and checkpoint (Q12) | Finding 1, 5.7.2 and ADR-001 (Proposed): `celestial_time()` returns `time.time()`; the checkpoint becomes a record on a timer, never the time source. | Supports A4. |
| Celestial Sentinel (D5) | 5.7.3 (L758): "UNNECESSARY REMOVE ... Retired, as intended." | D5 reverses that. Blueprint 5.7.3 and E81 change in Step 3. |
| Voltron | 5.8 (L767): an agent rule (pacing, scope containment); Antigravity `max_turns` and `timeout_mins` can enforce it. | No kernel-side form exists (section 10). |
| Rodin and memory | 5.3.2 and FP-31; ADR-005: `memory.db`, `gemini-embedding-2` at 768-d, loud failures, and an MCP memory server (`get_kernel_card`, `write_handoff`) so new threads do not start blind. | Section 10. |

## 3. Current state (MEASURED)

| Area | What the code does today |
|:--|:--|
| Who owns Phoenix | `CheshireCatKernel` builds `PhoenixForge()` (`sensory/cheshire_cat.py:62`); `swds_scheduler` calls `cheshire_cat.phoenix.execute_swds` (`main.py:1106-1191`). Phoenix does not call Heimdall (2026-10-09 rework); Heimdall's `open_swds_cycle` / `close_swds_cycle` are not called by `main.py` (X-1). |
| Phoenix Force (P0) | `POST /models/router/phoenix-force` (`main.py:1220-1234`) calls `MODEL_ROUTER.engage_phoenix_force(authorized_by=...)` (`core/model_router.py:250-266`). The field defaults to `"architect"`, there is no header check and no check that SWDS is open. The "two-key" is a string. P0 suspends all limiters. |
| Jean Grey | `JeanGreyClient` (`core/api_clients.py:783`; gemini-3.8-flash, high). Its only caller is `analyze_kintsugi_sandbox` (`evolution/phoenix_forge.py:323-354`). There is no "Operation Phoenix Force" function, no prompt-operation list. |
| Dragon | `DragonDriver` (`core/dragon_driver.py`, Layer-0 identity text) and `DragonEngine` (`core/dragon_engine.py`, state and modality). The kernel builds it with Heimdall only (`main.py:188`), so no Cognitive Engine is injected. `/ignite` calls the synchronous `process_intention` (`main.py:636-637`); `process_intention_async`, the path that reaches Zenitsu (`dragon_engine.py:236`), has no caller in `main.py`. |
| Genesis boot | `main.py` is the host: `lifespan` (L71) starts `swds_scheduler` (L103), the Cheshire loop (L134) and the Kintsugi hypervisor (L150); components are registered with Heimdall by name (L206). The scheduled task's wrapper is lost on every launch (ADR-010). |
| Celestial Sentinel | `temporal/celestial_sentinel.py` is 15 lines of constants (`verify_sentinel` returns True flags). Only a test imports it. `sensory/cheshire_protocol.py:44` says its kinematics were absorbed from it. |
| Clock runtime | `celestial_time()` is a frozen 10-06 checkpoint plus uptime (`core/celestial_middleware.py:300-331`, ADR-001). `GET /celestial/checkpoint` (`main.py:1360-1371`) awaits `get_celestial_timestamp()`, which saves the checkpoint file every time the clock is online (`celestial_middleware.py:243-251`): the read route writes. Automatic stamping is not wired (gap a). |
| Zenitsu | `execute_zenitsu_method` (`core/cognitive_engine.py:258-317`); `execute_bicameral_synthesis` always calls it (L480), so every `/cognitive/cycle`, rebuttal and Tier-1 dispatch pays for four passes. |

## 4. High-level design

### 4.1 Phoenix Force run (D2)

```
Architect prompt        Heimdall (delegator)        Cheshire Cat           Phoenix + Jean Grey
 (authenticated)              |                          |                        |
 POST /swds/phoenix-force --->| 1 SWDS open? admin header? prompt present?        |
                              | 2 write authorization record to the ledger         |
                              |-- 3 handover(land) ----->| takes Phoenix's land   |
                              |                          | tasks (consolidation)  |
                              |-- 4 start(flight, ops) ------------------------->| runs the predetermined
                              |                          |                        | prompt operations via
                              |<-------- 5 receipt per operation ----------------| Jean Grey
                              |-- 6 end(flight) --------------------------------->| back to its function
                              |-- 7 release(land) ------>| back to its function    |
 <---- run receipt -----------| 8 disengage P0, ledger the run                      |
```

Abort at any step if the SWDS window closes (wake time), a receipt is missing for too long, or Phoenix errors: Heimdall performs 6, 7 and 8, and the run is ledgered as ABORTED (never COMPLETE).

### 4.2 Genesis and Dragon merged (D4)

```
                    +-----------------  DRAGON (name open)  ------------------+
 Windows task  --->  | boot       : ordered start of the always-on actions       |
 (supervised)        |              (lifespan today), single instance, log       |
                     | driver     : Layer-0 identity text (dragon_driver.py)     |
                     | state      : STANDBY / ACTIVE, Flight / Land modality     |
                     |              (dragon_engine.py)                           |
                     | request    : the on-demand door to Zenitsu via Sun        |
                     |              Breathing, gated by Heimdall                 |
                     +-----------------------------------------------------------+
 FastAPI routes stay in main.py (or move to routers); no new port.
```

### 4.3 Celestial Sentinel (D5)

```
 celestial_clock.py (math, kept as the ruling says)
        ^                                  stamp(kind) --> Hoard, SWDS, CCID, ledger
        |                                  checkpoint()  (only writer, atomic)
   Sentinel  ---- status() ------------>   GET /celestial/checkpoint (read-only)
        |
        +--> Itachi's link report (D6): Celestial Time ~ Heimdall ~ Cheshire ~ Rodin
```

### 4.4 Zenitsu 3.0 contract with the decisions applied

| Pass | Eye | Model | Input | Output |
|:--|:--|:--|:--|:--|
| 1 K | Neji | Y789, claude-opus-5-5 (D6) | request payload | boundaries and constants, no inference |
| 2 U | Shikamaru | Nexus, gemini-4-argus, fallback gemini-3.8-flash (D6) | payload + K | relational map |
| 3 W | Itachi | OPEN (A3) | U + the link inputs below | link report: intent, invariants over time, risk (blueprint R-2; TPSL stays a Heimdall gate, not an Eye) |
| 4 | Unification | OPEN (A3); suggestion Nexus | K, U, W | the result; status COMPLETE / PARTIAL / ERROR, never a fixed label |

Itachi's link inputs (D6): the Sentinel's stamp and ephemeris (Celestial Time); Heimdall's health, H_smooth and gate verdict; Cheshire's state, queue and triage; Rodin's retrieval summary. Itachi reads them and reports; it does not change them.

## 5. Deep dive

### 5.1 Phoenix Force run

- **Authorization record (D2).** The Architect's prompt arrives over an authenticated route (the existing `X-Integra-Admin` header mechanism, `main.py:479-495`) and is stored as the record: operation id, time from `/clock`, a hash and length of the prompt, the SWDS cycle id, the operations requested. It is valid only for the SWDS cycle that is open when it arrives and expires when Heimdall closes the cycle. Outside SWDS the route refuses; this replaces the current unauthenticated, state-blind P0 route (`main.py:1220-1234`) and removes the `"architect"` default.
- **Predetermined prompt operations.** A versioned list (proposed file: `config/phoenix_force_operations.yaml`), each entry with an id, a prompt template, the inputs it may read, where its output goes, and whether it may write to the Hoard. The list is part of the repo and reviewed; the Architect's prompt picks from it or names the whole set. Its contents are OPEN.
- **Handover.** Heimdall sends two instructions, `handover(land)` to Cheshire Cat and `start(flight)` to Phoenix, and records both. Cheshire Cat runs only the tasks `execute_swds` performs today (consolidation, pruning, dreaming) while Phoenix is away. Phoenix never moves thalamic state itself (ruling of 2026-10-09).
- **P0.** Limiters are suspended only between steps 4 and 6, then the router returns to P2 (the existing `disengage_phoenix_force`).
- **Receipts.** One per operation with its start and end time, model, token counts as the client reports them, and its status. A run with a missing receipt is PARTIAL.
- **Tests.** Offline, in an isolated copy, with a fake Jean Grey client: the refusal outside SWDS, the refusal without the header, the handover order, the abort at wake time, the return of both roles on error.

### 5.2 Genesis and Dragon

Today the Dragon pieces are small and the host is `main.py` (about 1,400 lines). The merge is a consolidation of responsibilities, not a rewrite:
1. Move the ordered start of the always-on actions out of `lifespan` into one boot function owned by the Dragon component, keeping the same order and the single-instance guard.
2. Inject what `DragonEngine` needs (Heimdall, the Cognitive Engine, the Shiva suite) so `process_intention_async` is reachable (today it is not, `main.py:188`).
3. Keep the routes where they are; do not add a port.
4. Rename last (G3 ruling). Naming options and their cost are in section 7.

### 5.3 Celestial Sentinel

Responsibilities: (a) stamp, one function every writer calls, replacing `datetime.now()`, `time.time()` and the frozen `celestial_time()`; (b) write the checkpoint, atomically, versioned, at an interval, as a continuity record and not as the time source; (c) serve a read-only status; (d) feed Itachi's link report. It keeps `temporal/celestial_clock.py` as the math, as the ruling says, and states both readings of "uncoupled from NTP": no network fetch, and not independent of the OS clock. Open clock items stay open: the epoch label (D-20) and the year constant. The 15-line stub is replaced, not extended; its True flags are removed (ADR-003). A port is not needed: it runs in the kernel process.

### 5.4 Zenitsu

On top of the contract in 4.4: invoked on demand only (D10); the per-cycle call and the "mandatory" wording are removed; lenses are a parameter with the Brain Model 0930 defaults and a per-Eye override; model ids come from `models.yml` and are validated at load; one MTCW packet per pass with a real losslessness check; result status computed from the run; client errors surface as errors; no success line without a check; provenance labels on outputs. Budgets: none specified (D7). Tests are written from the contract, run offline in an isolated copy, with fake clients. The Gate III route to Alexandria stays out until D8's document is read.

### 5.5 Governance files and Guiding Principles

Steps, in order: diff today's `~/.gemini` files (SKILL.md changed on 2026-10-09, after the v9 capture used by the synthesis) against the sixteen conflicts; rewrite them to the current rulings; remove the home locality and the Sovereign Override; move the Three Laws to the Guiding Principles with the order the Architect's documents give; keep the old text in the archive only. The genesis-kernel skill's line that treats `/celestial/checkpoint` as a free read is corrected once A4 is confirmed.

## 6. Scale and reliability

One machine, one user, one kernel process; load is not the constraint, correctness and supervision are.
- **Single instance and supervision (ADR-010).** The merged boot must run as one supervised process; today the wrapper dies on every launch and the kernel runs orphaned.
- **Failure of the run in 5.1.** Heimdall owns the abort path; both roles return even if Phoenix dies.
- **Observability.** Every run, authorization and handover is a ledger record (ADR-002). Health endpoints report the Sentinel's last stamp and checkpoint age.
- **Data.** The checkpoint file is written by one writer only; the Hoard writes of a flight run happen only for operations that allow them.

## 7. Trade-offs

| Choice | Option A | Option B | Recommendation |
|:--|:--|:--|:--|
| Who runs the handover | Heimdall (matches the authority ruling; more code in Heimdall) | Phoenix itself (simpler; breaks the ruling) | A (A1) |
| Authorization | The Architect's prompt as an authenticated record (D2) | Header only, as the selftest does | A; it is what D2 asks for |
| Dragon merge depth | Rename only | Consolidate responsibilities (5.2) | Consolidate; rename last |
| Merged name | Keep "Genesis Kernel" (the scheduled task, `kernel_ctl.ps1`, the skill and CLAUDE.md keep working) | "Dragon engine" (the engine already exists and holds the state machine) or "Dragon driver" (the Layer-0 identity text) | Architect's choice; "Dragon engine" is the least surprising for the code |
| Sentinel process | In the kernel process (no new port) | A separate server (needs its own port by ruling) | In-process |
| Itachi model | Follow the CWA weight | Pin to Y789 | Follow the weight until the Architect assigns one |

## 8. Work breakdown (Step 4, after G3) and what I would revisit

1. Sentinel: stamp API, atomic checkpoint, read-only route, tests; remove the stub's True flags.
2. Phoenix Force route and record, the operation list, the Heimdall handover, tests.
3. Dragon boot consolidation and dependency injection; routes unchanged.
4. Zenitsu contract: separate the call from `execute_bicameral_synthesis`, move it behind Sun Breathing.
5. Governance rewrite and Guiding Principles (documents, no kernel restart).
6. Renames last; a kernel restart for any of this needs the Architect's approval.

Revisit when: the Architect's documents for Gate III and the Three Laws arrive; Itachi's and Unification's models are chosen; Argus gets a public id; the first Phoenix Force run has produced receipts to read.

## 9. Reminders owed to the Architect

1. Find the historical document for Gate III (the Alexandria fallback in pass 3).
2. Find the historical documents for the Three Laws' order.

## 10. The always-on set: what "on" means, today, and the first steps

The Architect's list (2026-10-15): Genesis kernel, The Flame kernel, Dragon Engine (always-on actions), Dragon Prompt, Starfire Protocol, Rodin, Voltron Protocol. The server process is up. The blueprint's own test is that a component does its job, not that it exists (Pattern C, section 3.4).

| Component | "On" means (checkable) | Today, MEASURED 2026-10-15 15:49-15:54 CDT | Work item |
|:--|:--|:--|:--|
| Genesis kernel | One instance, supervised by its task (task Running, wrapper alive), timestamped log, loops with heartbeats | Up 42 h 50 m on 127.0.0.1:8000. Task Ready / 0xC000013A; the wrapper is gone and python 10636 runs orphaned. The log has no per-line timestamps. | ADR-010 items 1-4; the supervision fix |
| The Flame kernel | The 30 Hz loop ticks with a heartbeat and handles event content | `/cheshire/status`: OPERATIONAL, 30.0 Hz, queue 0, 23 components. The loop runs but drains events without reading them (blueprint 5.4.1). | Give it real work, or call it a heartbeat |
| Dragon Engine | ACTIVE_WAKING_STATE after boot, reachable from the request path | `/dragon/status`: STANDBY. `POST /dragon/flight` would set it ACTIVE (`main.py:686-699`) and reset the SWDS idle timer, but no code path depends on the state, and the engine is built with Heimdall only (`main.py:188`). | D4; do not flip the label alone (Pattern A) |
| Dragon Prompt | Passed as the system prompt of kernel model calls | A 681-character text held by the engine. The router shows 0 calls and 0 tokens for all seven components since boot, so no call has carried it. | ADR-004 with D4 |
| Starfire | Scores real outputs against the identity vector | `/starfire/identity`: ANCHORED, KL 0.0, computed between the anchor and itself (blueprint 5.1). | Identity Matrix task, after ADR-004 |
| Rodin | A real query vector, real embeddings, loud failures, model-free swarm roles, and a RAM working-memory tier (the Architect's four roles) | `/rodin/telemetry` says ONLINE, a constant. The supervisor queries a fixed `[0.1] * 768` (`orchestration/rodin_supervisor.py:88`). Embeddings are hashes. No RAM tier. | ADR-005 |
| Voltron | Pacing and scope limits that are enforced | A rule in agent files (blueprint 5.8). No kernel-side form, no route. | Define it: router duty cycle and call caps, Heimdall gates, and `max_turns` / `timeout_mins` for agents |

### First steps, in dependency order

Stack detected (`requirements.txt` and the venv): FastAPI 0.141.1, Starlette 1.6.0, uvicorn 0.52.4, anyio 4.15.1, pydantic 2.13.5, google-genai 2.25.0, anthropic 1.5.0, chromadb 1.5.9, httpx 0.28.1, Python 3.13.7.

1. **Architect prerequisite: a standard Gemini API key and the no-Vertex switch** (already an open item). Without them Rodin's embed calls can fail, and the failure is silent.
2. **Rodin embeddings (Step 4).** Official sources, fetched 2026-10-15:
   - The Gemini API [embeddings page](https://ai.google.dev/gemini-api/docs/embeddings) (last updated 2026-10-09): `gemini-embedding-2` is the latest stable model; "Flexible, supports: 128 - 3072, Recommended: 768, 1536, 3072"; "Gemini Embedding 2 also auto-normalizes truncated dimensions"; "You cannot use the `task_type` field for the `gemini-embedding-2` model" (put the task in the text prefix); "The embedding spaces between `gemini-embedding-001` and `gemini-embedding-2` are incompatible". Call shape: `client.models.embed_content(model="gemini-embedding-2", contents=..., config=types.EmbedContentConfig(output_dimensionality=768))`; the default is 3072.
   - The [deprecations page](https://ai.google.dev/gemini-api/docs/deprecations) (last updated 2026-10-12): `text-embedding-004` shut down 2026-01-14 (replacement `gemini-embedding-2`); `gemini-embedding-2` released 2026-04-22, no shutdown announced.
   - Consequences: (a) `core/api_clients.py:702` still defaults to `text-embedding-004`. The blueprint records it as served on the Agent Platform until 2027-04-01, but with Vertex off it fails and Rodin falls back to hash vectors silently (`memory/rodin_protocol.py:343-351`), so `RODIN_EMBED_MODEL=gemini-embedding-2` must change together with the key switch. (b) The call must pass `output_dimensionality=768`. (c) The 64-d coarse tier is below the documented minimum of 128: use a 128-d tier, or test the 64-d truncation (UNVERIFIED that it holds recall). (d) Re-embed everything; the current vectors are hashes anyway.
3. **Loud failures and the real query vector** at `orchestration/rodin_supervisor.py:88`; then ADR-005's `memory.db` and MCP memory server, so a new thread starts from `get_kernel_card` and ends with `write_handoff`. This is the blueprint's cure for threads that lose their place.
4. **Boot hygiene (ADR-010).** The Python [asyncio docs](https://docs.python.org/3.13/library/asyncio-task.html) say: "Save a reference to the result of this function, to avoid a task disappearing mid-execution. The event loop only keeps weak references to tasks." `main.py:103, 134, 150` create tasks without stored references. The FastAPI [lifespan page](https://fastapi.tiangolo.com/advanced/events/) recommends `lifespan` and says that with it "startup and shutdown event handlers will no longer be called"; it does not cover background tasks started at startup, so that part rests on the asyncio docs alone.
5. **Supervision.** The leading cause is DERIVED (Windows Terminal as the default console host); changing that default is the Architect's system setting, or Step 4 adds a headless wrapper.
6. **Dragon Prompt, Starfire and Voltron** come after 2-4, because each needs model output kept (ADR-004) before it can be measured.

Not done without approval: a kernel restart, `POST /dragon/flight`, a paid embedding probe.
