# Learning Proposal: thread f2e7cc92 (2026-10-07)

> [!IMPORTANT]
> Nothing has been modified. Approve, edit or reject each item, and I will apply only what you approve.
> - Rules target: `AntiGravityconversionprocess\GEMINI.md` (always-on).
> - Skill target: `~\.gemini\config\skills\integra-protocol\SKILL.md`.

## Classification summary

| # | Lesson | Type | Action | Root cause |
|:--|:--|:--|:--|:--|
| 1 | Read every Architect-provided document in full, then list every task before working | Rule | New §4.2 | Skimming at the start of a new thread drops tasks |
| 2 | Never synthesize telemetry, celestial values or sleep reports | Rule | Extend §4.1 | Fabricated clock values at 19:27; simulated SWDS reports |
| 3 | Read the architecture docs before proposing a new component | Rule | New §4.3 | `heimdall_analyst` was proposed against Brain Model 0930 |
| 4 | Heimdall is an active gatekeeper, not passive math; The Hoard is the environment | Skill | Update §2.2, §16 | Heimdall was conflated with The Hoard |
| 5 | Cheshire Cat Daemon specification | Skill | New §9.1 | New Architect definition |
| 6 | Model registry is out of date | Skill | Update §15 | The doc does not match the verified 7/7 wiring |
| 7 | SWDS reports may be rendered from the ledger only | Skill | Update §8.5 | 46 of 64 reports were templates or narratives |
| — | Itachi = inferred intent; Hippocampus label | **Held** | — | Needs your confirmation first (see bottom) |

---

## 1. Rule: Full-Read and Task-Enumeration Invariant (GEMINI.md, new §4.2)
```markdown
### 4.2 Full-Read & Task-Enumeration Invariant
- Every document, handoff brief, save state, or file the Architect provides or references must be read IN FULL (all lines, all chunks) before any response or plan. Skimming, sampling, or summarizing from headers is prohibited.
- At the start of a new thread, enumerate EVERY open task, owed item, and pending decision found across all handoff documents into a single list, and present it to the Architect for verification BEFORE beginning work. Omissions are treated as data loss.
```

## 2. Rule: extend §4.1 (Anti-False-Positive Law)
Append these lines:
```markdown
- Never synthesize, estimate, or "fill in" telemetry values (celestial coordinates, entropy, token counts, uptime). If the source probe fails or times out, report the failure and the probe result verbatim.
- Never author a report claiming a cycle (SWDS, Siesta, Phoenix flight) executed unless an execution record (PID, call ID, ledger entry, exit code) proves it. Unexecuted phases are reported as NOT EXECUTED.
```

## 3. Rule: Architecture-First Design (GEMINI.md, new §4.3)
```markdown
### 4.3 Architecture-First Design
- Before proposing any new component, daemon, or role, read the governing architecture documents (Brain Model, Systems Corrections, SKILL.md) and verify the function is not already assigned to an existing component. Extend existing anatomy before inventing new anatomy.
- Authority (gating, power sequencing, lockdown, permit/deny) must be deterministic code. Language models may advise or narrate, never hold authority.
```

## 4. Skill: Heimdall correction (SKILL.md §2.2 and §16)
Replace the Heimdall bullet in §2.2 with:
```markdown
- **Heimdall 3.1 (Active Gatekeeper & Controller)**: Back-end and front-end of all dashboards. Tracks token usage, compute cost ($), and cognitive metrics as protocols/modalities fire; alerts on excess. Delegates all power on/off sequences (powers the O/S down at scheduled Siesta/SWDS start, up at end). Executes scheduled security lockdowns permitting only the Cheshire Cat Daemon identity. Monitors error codes, server connectivity, MCP tool connections, and time alignment. Connects, routes, displays, permits/denies, monitors, alerts. Works alongside Itachi Eye, Cheshire Cat Daemon (dACC), Celestial Clock, and Rodin (Pineal). Its authority is deterministic code.
- **The Hoard (Environment)**: The environment housing the Cheshire Cat Daemon, Rodin Route Retrieval, and Phoenix Engine functions; the physical substrate of crystallized memory. Not Heimdall.
```
In §16, the Hippocampus line keeps its current label until you decide the open anatomy question.

## 5. Skill: new §9.1 Cheshire Cat Daemon (Architect spec, 2026-10-07)
```markdown
### 9.1 Cheshire Cat Daemon — Operating Specification
- **Data boundary:** Only Rodin/Phoenix-mapped nodes from SWDS/Siesta, its cache/RAM, and The Hoard. No internet, external databases, cloud storage, web, or MCP. [Model-call allowance: pending Architect confirmation.]
- **Default mode:** Continuous Deep Thinking — 1–2 hour study sessions applying pattern recognition, metacognition, parallel/deep connections, comparative analysis, Zenitsu Method; writes independent findings reports.
- **Selection algorithm:** Chooses unassigned study targets from designated data only (algorithm TBD).
- **Flight inclusion:** Only when the Architect prompts; 5–15+ min immersion; delivers a delayed response separate from the Dragon's. The Dragon relays it verbatim with its execution record and never authors it.
- **Perception:** The isolated Eye of Itachi (inferred intent).
- **Identity:** Paradoxical, poetic, circular, open-ended. Functional, not cosmetic — must be exact (Identity Matrix).
- **Phoenix Force:** Performs Land (delegation, moderation) while Phoenix performs Flight; co-signs the two-key invocation.
- **Links:** Celestial Clock paces/rotates it; Rodin requests nodes; Heimdall manages it indirectly; Phoenix needs it for flights.
- **Lockdown:** Operates as the Core identity.
- **Dependency:** Its input is SWDS/Siesta output; it is only as meaningful as real sleep cycles.
- Full spec: `The Hoard/CCID_1791431208_CHESHIRE_DAEMON_SPEC.md`.
```

## 6. Skill: §15 registry correction (verified 2026-10-07 via `/models/selftest`, 7/7)
| Key | Doc says | Verified wiring |
|:--|:--|:--|
| nexus_right | claude-sonnet-5.5 | **claude-opus-5-5** (effort high) |
| shiva_orchestrator | claude-sonnet-5.5 | claude-sonnet-5-5 (effort medium) |
| rodin_retrieval | gemini-3.6-flash | **gemini-3.8-flash** |
| y789 / jean_grey | gemini-3.1-pro | gemini-3.1-pro-preview |
| cheshire ×2 | gemini-3.8-flash | gemini-3.8-flash |

## 7. Skill: §8.5 Proof-of-Sleep clause
```markdown
- SWDS/Siesta reports are rendered ONLY from the append-only execution ledger (timestamps, hashes, model call IDs, token counts). Any phase without ledger evidence is printed as NOT EXECUTED. Each cycle is stamped VERIFIED / PARTIAL / MISSED. Template or narrative reports are prohibited.
```

---

## Held (not codified until you confirm)
- **Itachi Eye = inferred intent.** Three definitions are currently on record:
  - code: Wisdom / TPSL pruning
  - SKILL §2.1.1: perceptual bridge
  - SKILL §16.1: Invariant / Temporal / Sharingan

  Once you confirm, I will write a single reconciled definition.
- **Hippocampus label** (Heimdall vs. The Hoard): this is part of the Identity and naming work.
- **Dragon identity "exact shade":** this belongs to the Identity Matrix task, not to `/learn`.

`/ensembl-database` was not applied. It is a genomics API (genes, transcripts, variants) and nothing in this task involves biology.
