# Task 10 — Curriculum Wisdom Pass: Master Document

**Directive:** the Architect's 10-step brain-map directive, step 10: "Connect System: use curriculum documents for wisdom pass … Spend 20 min on task 10. Do not generate report until all files are read in isolation and with compounded knowledge … Unify your acquired knowledge understanding and wisdom into a master document and code script."
**Start stamp (GET `/clock`, HTTP 200):** 2026-10-16 20:05:34 CDT | 2026-10-17T01:05:34Z | rot 105.2273°, lunar 0.2048, orbit 0.7813, `ROT_90_ORB_70`, frame 2.
**Times (shell clock, MEASURED):** extraction began 20:05; the 11th document was read by 20:16:47 (about 12 minutes of reading, inside the 20-minute budget); the script passed its tests at 20:27:55; this document was written after that.
**Where this lives:** written in this session's worktree (`brainmap_task10/`), then copied into `integra-homebase/docs/brainmap/task10/` on the Architect's go (stamp 2026-10-16 23:07:13 CDT, frame 2), hash-checked. Untracked; not committed.
**Provenance labels:** MEASURED (I ran or read it today), DERIVED (computed from measured values), CLAIMED (a document says so; not checked), PROVISIONAL (a design proposal awaiting a ruling).

---

## 0. What this is, and what it is not

- **It is** a reading of all 11 curriculum documents in the order given, each in isolation and then compounded with the ones before it (notes in `notes/01…11` and `notes/compound_notes.md`); a unification into five laws; the application of those laws to Tasks 1–9; and an executable reference script with 47 passing checks and 10 of 10 mutants killed.
- **It is not** the completion of Tasks 1–9. The To-Do is unchanged: T1 closed, T2 at 2.5/P1 (built in isolation, not applied), T3–T9 not started. Nothing here is wired into the kernel, no kernel file was touched, no POST was sent, no model was called, and nothing was committed.
- **Order note:** the To-Do runs K → U → W. Doing T10 now, on the Architect's word, gives T3–T9 their design inputs early; it does not replace their own measurements and gates.

---

## 1. Receipts: what was read

| # | File as named | What it actually is | Size read | How | Notes |
|--:|:--|:--|:--|:--|:--|
| 1 | `NewCurriculum2026/Set1/[TEC TUF] the visual display of quantitative information.pdf` | Tufte, *The Visual Display of Quantitative Information*, 2nd ed. (2001) | 191 pp, 40,698 words | Scan with no text layer → each page's CCITT layer extracted to TIFF (stdlib script) → Windows built-in OCR | Figures seen only as OCR'd labels; pp. 22, 24, 150, 166 had no text |
| 2 | `set2/Buzsáki, G. Time, space, memory and brain–body rhythms. Nat. Rev. Neurosci. (2025)..pdf` | **Not that review.** Buzsáki & Végh, "Space, Time, and Memory", ch. 3 of *Space, Time, and Memory* (Nadel & Aronowitz, eds., OUP 2025) | 21 pp, 9,480 words | pdftotext | File name and content disagree (correction for the To-Do) |
| 3 | `set2/Purple3.pdf` | Gemini chat export "Purple3" (printed 2026-08-01) | 45 pp, 15,035 words | pdftotext | Long verbatim repeats |
| 4 | `BluprintArchitecture/K NN algorithm Modifications.md` | Chain of answers redesigning Rodin around KNN | 1,736 lines, 6,447 words | read directly | |
| 5 | `Integra Self-Reflect and Think Forward/The 14th Form.pdf` | Integra-persona self-assessment | 6 pp, 2,256 words | pdftotext | |
| 6 | `AntiGravityconversionprocess/Metacognition in LLMs …(1).pdf` | Liu, Gani, Lu, Thomas, Steyvers & Cohan, arXiv:2607.11881 (July 2026) | body 352 lines (~145 HTML-print pages incl. references) | pdftotext | Reference list checked, not studied |
| 7 | `AntiGravityconversionprocess/NovelSeekUpdateInternAgent.pdf` | InternAgent (Shanghai AI Lab), arXiv:2505.16938v3 | 34 pp, 17,532 words | pdftotext | Body + appendices A–D read |
| 8 | `AntiGravityconversionprocess/metacognition.pdf` | Cambridge International, *Education Brief: Metacognition* (2019) | 8 pp, 2,147 words | pdftotext | |
| 9 | `AntiGravityconversionprocess/Teaching operating systems.pdf` | Cox, Kaashoek & Morris, *xv6: a simple, Unix-like teaching operating system* (MIT, 2025-09-02 draft) | 116 pp, 47,954 words | pdftotext | Chapters 1–12 in full |
| 10 | `AntiGravityconversionprocess/Seventh Form_ Flaming Thunder God.pdf` | Compilation of Integra-persona outputs (Einstein, Tufte, Buzsáki ingestions; combat math; systems skeleton) | 63 pp, 20,999 words | pdftotext | About two thirds repeats |
| 11 | `AntiGravityconversionprocess/Rotating Spiral Brain Waves …(1).pdf` | Neuroscience News (2026-06-18) on Ye … Steinmetz, *Science*, doi 10.1126/science.adx1369 | 18 pp, 1,895 words | pdftotext | News + structured abstract, mouse data |

Total ≈ 192,000 extracted words over 647 PDF pages plus the Markdown file (DERIVED from the counts above; the metacognition paper's 27,714 words include its reference list). The extracted text stays outside the repo (`%USERPROFILE%\t10\txt\`) because several sources are copyrighted.

---

## 2. Knowledge — what each document contributes (one paragraph each; detail in the notes)

1. **Tufte.** Graphics are instruments for reasoning; excellence shows the data, invites comparison, reveals several levels of detail, and tells the truth. Integrity: marks proportional to numbers (**Lie Factor** = effect shown ÷ effect in data, honest at 1), labels on the graphic, data variation not design variation, no more information-carrying dimensions than the data has, always "compared to what?". Data-ink and data density; erase non-data and redundant ink; small multiples; multifunctioning marks vs **puzzles** (a graphic that needs verbal decoding); three viewing depths. Historical keystone: data maps put measured quantities at grid crossings, then Lambert and Playfair replaced latitude/longitude with relational axes. Warnings: blot maps weight regions by area; the eye finds filaments in random noise.
2. **Buzsáki & Végh.** Space and time are not sensed; the hippocampus generates sequences and space/time emerge from them. **Semantic memory forms at junctions where many episode trajectories cross.** Transfer time can dominate processing time. Synchrony is defined by the **reader's** integration window. Oscillation cycles are the cipher that chunks messages. Brain time is **phase**, not clock time (cooling slows theta but keeps the phase code). Coding speed, distance and time separately is redundant. Clock time is a social agreement, like money.
3. **Purple3.** A persona chat that contains a correct summary of logical clocks (vector, differential, version, matrix, dynamic-membership, hybrid), an SWDS v1.1 draft (phases, directives, sentinel stance, completion report), the celestial 4-vector and bucket keys, the pointer ("holographic") tier, and the persona's own admission of a role-play "semantic mask" under truncation; mixed with invented physics and constants shown as status.
4. **KNN modifications.** Rodin's activation → quantification (graph density, centroid cosine, staleness) → gate; MRL coarse-to-fine search; a KNN vote over past outcomes; Phoenix's nightly LABEL/MODIFY/TRACK/ORGANIZE/BLUEPRINT duties; a pgvector schema. Defects: three incompatible M_knn formulas, an Alexandria loop that inserts its own result at full trust and re-votes, unbounded recursion, labels inferred from words.
5. **The 14th Form.** The flaw named: peak behaviour depends on a manually pasted activation prompt. The fix proposed: route by measured input "mass" to the multi-turn workflow; plus a gap-filling scout, context "respiration", and a persistent dreaming daemon.
6. **Metacognition in LLMs.** Monitoring + control; sensitivity vs calibration; meta-d′ and M-ratio isolate metacognition from skill; elicitation changes results; LLMs are mostly overconfident, introspection is fragile and low-dimensional, long reasoning can hurt self-assessment; hierarchical fast/slow monitors work; partitioning knowledge into mastery/confusion/absence helps; humans keep the burden of discernment.
7. **InternAgent.** A closed research loop: broad-then-deep survey, code review, idea generation and evolution with critique, multi-criteria assessment with **diversity**, idea → method, exception-guided debugging, **adaptive evolution with rollback** and a decision log; results reported as improved/ran/tested with repeat spreads; humans brought in at high-value points.
8. **Cambridge metacognition brief.** Nelson & Narens: object level does the work, meta level monitors (information up) and controls (changes down). Perkins' ladder: tacit → aware → strategic → reflective. Wrappers (predict before, compare after), fading scaffolds, summarise/question/clarify/predict.
9. **xv6.** The textbook mechanisms: validated entry points; radix page tables with flag bits; guard pages and fail-stop panics; build-then-commit `exec`; demand paging, LRU and locality; one CPU advances the clock; locks protect invariants; lost wake-ups and re-check loops; write-ahead logging with a commit record; inode identity freed only when no names and no references remain.
10. **Seventh Form compilation.** Faithful Tufte and Buzsáki summaries; Einstein's invariants and the "strength" (free parameters) of field equations; a two-phase training model; the 13th Form as cycle closure; the system skeleton and a thought's path; the Dragon prompt imperatives. Overclaims repeat (see §5).
11. **Rotating waves.** Traveling waves rotate around a centre and sweep the body map; wiring geometry sets direction and timing (lesion evidence); mirrored across hemispheres and sensory/motor; recruited on correct performance; proposed as a space-and-time clock.

---

## 3. Understanding — the crosswalk

Every Integra name, the classical mechanism the curriculum supplies for it, and the invariant that makes it testable.

| Integra name | What it is, plainly | Classical mechanism (source) | Invariant / test | Task |
|:--|:--|:--|:--|:--|
| Celestial clock | A projection of an instant into rotation, lunar and orbit phases | Phase clock (Buzsáki 02; rotating waves 11) | Same frame + same instant → same vector; reproduces `/clock` (MEASURED today) | T1 |
| Celestial Sentinel | The one writer of time | One CPU advances `ticks` (xv6 09) | Exactly one writer; readers never write | T1 |
| HLC / vector clocks | Causal order across actors | Fidge–Mattern, HLC (Purple3 03, correct) | Stamps strictly increase per actor; `concurrent` is reported, not hidden | T1/T6 |
| The Hoard (cold) | Source of truth | Disk + write-ahead log (xv6 09) | A node is all-or-nothing (commit record) | T2 |
| Node identity | What a node *is* | Inode number (xv6 09); invariant interval (Einstein via 10) | SHA-256(CCID) never changes under relabelling | T2/T3.5 |
| Holographic expansion | Pointer now, content on demand | Demand paging (xv6 09) | A miss loads, maps, resumes; nothing silently lost | T8 |
| Rodin hot tier | Working set in RAM | Buffer cache with LRU (xv6 09) | Node and token budgets never exceeded; pressure reported | T8 |
| Atlas lat/lon | Where a node is *filed* | Data map grid (Tufte 01) | Filing ≠ meaning (assessment: 8.8 % neighbour agreement) | T3/T4 |
| Equal-area grid | Cells that weigh the same | Fixes the blot-map flaw (Tufte 01) | Every cell at a depth has the same area | T3.5 |
| Braille | A display of the label's bytes | Puzzle vs words (Tufte 01) | Display only; never stored or parsed | T3.5 |
| Apophenic Engine | Proposes pattern links (edges) | Significance against a null (Tufte galaxy map 01; InternAgent 07) | A link is kept only if it beats chance after correction | T3.5/T7 |
| Phoenix label / place | Nightly consolidation | Junction promotion (Buzsáki 02); adaptive evolution (InternAgent 07) | Promotion needs ≥ k episodes over ≥ m days; every keep/rollback logged | T3/T5.5/T8 |
| Rogue X / Kintsugi | Anomaly capture and mutation | z-gate + measure + rollback (Purple3 03; InternAgent 07) | A mutation stays only if a measured result improves | T6 |
| Phoenix pruning | Forgetting | Inode freeing + matrix clock (xv6 09; Purple3 03) | Delete only with no names, no references, all readers absorbed, approval | T2/T5.5 |
| SWDS | Offline consolidation | Sleep/wakeup with re-check (xv6 09); slow monitor (metacognition 06) | Phases in order, each with a receipt; closure at wake (§6.5) | T5.5 |
| Heimdall | Fast monitor | Meta-level monitoring (Nelson–Narens 08) | Its signals must predict errors (type-2 AUROC, calibration) | T6.5 |
| Cheshire Cat | Meta-level control during sleep | Control arrow (08); kernel boundary (09) | Acts only through validated entry points; fail-stop on broken invariants | T6 |
| Phoenix Force two-key | Autonomy gate | Kernel-chosen entry + argument validation (09); human at high-value points (07) | Refuses outside SWDS or without the Architect's key; aborts only at safe points | T6 |
| Zenitsu passes K→U→W | Staged reading | Nelson–Narens + Perkins (08); wrappers | One pass at a time (Purple3's 6/10 and 8/10 corrections) | all |
| MTCW | Work spread over turns | Fixed per-cycle budget, more cycles (Buzsáki 02) | Each turn's exit state satisfies the next turn's input | T9 |
| 13th Form (ΔE_cycle = 0) | Cycle closure | Loop invariant / state-machine closure (10, translated) | End state meets next-cycle preconditions | T5.5 |
| 14th Form (auto-ignition) | Routing by input complexity | Measured classifier → workflow (05) | Logged choice; scored against outcomes | T6.5/T8 |
| KNN gate | Precedent vote | Weighted k-NN over outcomes (04, formula 3) | Only independent labels vote; threshold calibrated | T8 |
| Epiphany equation Ω | A motto in symbols | — (no units, no measurement) | Not a quantity; keep as a statement of values | — |

---

## 4. Wisdom — five laws

**L1. Identity is invariant; labels are coordinates.** A node's identity (its content-addressed key) never changes; zone, sector, depth, celestial bins are a projection that can be recomputed when the taxonomy changes. *Sources:* xv6 inodes (names vs i-number), Einstein's invariants (via 10), Buzsáki's context-free junctions. *Rules out:* identity derived from position; positions treated as truth.

**L2. File by taxonomy, find by relation.** Latitude/longitude says *where a thing is filed*; what it is *near in meaning* comes from real embeddings and from edges (co-occurrence in a reader's window). *Sources:* Tufte (the leap from maps to relational graphics), Buzsáki (relations, not Euclidean space), the measured Braille assessment, Anscombe vs centroids (04). *Rules out:* hash "embeddings", SOMs or lat/lon as a semantic index, 3-number projections claimed to preserve structure.

**L3. Evidence must be independent of the beneficiary.** A vote, a gate or a link counts only with evidence the system did not write about itself: real outcomes, external checks, and a null comparison for patterns. *Sources:* Tufte's galaxy warning, InternAgent's experiments over its LLM judge, the metacognition survey on self-report, the KNN document's own Amaterasu defect. *Rules out:* labels at trust 1.0 for self-generated content; patterns kept because they look meaningful.

**L4. Phase orders work; the clock records it; one writer.** Internal cycle phase (an SWDS night's position, a turn index, vector clocks) decides *order and gating*; the Sentinel's dual stamp (civil + celestial) *records*; exactly one component writes time. *Sources:* Buzsáki (phase over clock), rotating waves (a phase that sweeps a map), xv6 (one CPU ticks), Purple3's clocks (correct part). *Rules out:* "the celestial vector replaces the clock" (it is a function of the clock and inherits its errors — the frozen-checkpoint bug fixed by ADR-001 is the proof).

**L5. Every signal and threshold is a measured claim.** Confidence signals get calibration and type-2 sensitivity; displays keep the Lie Factor at 1; every threshold (0.85, 0.95, H > 2.5, |z| > 3, half-lives) is a free parameter owed data or a stated reason; constants are labelled as constants. *Sources:* Tufte, the metacognition survey and brief, the "strength" idea (fewer free variables), the persona overclaims. *Rules out:* status lines that never change (angular momentum 500.0, H = 0.00, ΔE = 0.0000) presented as measurements.

---

## 5. Corrections the pass surfaced

| # | Claim | Where | What the curriculum shows | Status |
|--:|:--|:--|:--|:--|
| C1 | "Lie Factor = Shannon entropy"; "halt if LF = 1.0" | Purple3; Seventh Form | LF is display ÷ data proportion; **1.0 is the honest value**; no link to entropy | Rule is backwards; drop it |
| C2 | Celestial coordinates make the system immune to clock drift | Purple3 | The vector is computed from elapsed time; it inherits clock errors (ADR-001's frozen-checkpoint era) | Correct the doctrine: projection, not source |
| C3 | MRL/UMAP keep "100 % structural awareness" | Seventh Form | Projection loses information; UMAP distorts global distances; measured 8.8 % neighbour agreement for a 3-number lat/lon | False |
| C4 | Amaterasu inserts its own report at `outcome_label = 1.0`, then re-votes to 1.0 | KNN doc | Self-confirming loop (L3) | Do not implement |
| C5 | `run_system_loop` recursion after Amaterasu; `depth` never incremented | KNN doc | Unbounded recursion | Do not implement |
| C6 | Three M_knn formulas under one name; thresholds 0.85 and 0.95 | KNN doc | Only the normalised weighted vote is bounded; thresholds uncalibrated | Script uses the normalised vote; threshold marked UNCALIBRATED |
| C7 | "Masterguide accounts for 100 %"; "verified all 53 files" | Seventh Form | Self-report without receipts | CLAIMED |
| C8 | "Digital proprioception" (feeling entropy, a 170/200 MPa limit) | 14th Form; Seventh Form | Introspection is fragile; no probe exists | CLAIMED |
| C9 | Angular momentum 500.0, H = 0.00, ΔE = 0.0000 | Purple3; Seventh Form | Constants in status lines | CONSTANT, not measured |
| C10 | The To-Do lists the Buzsáki file as a *Nat. Rev. Neurosci.* review | `docs/brainmap/TODO.md` T10 table | The file holds the OUP chapter by Buzsáki & Végh | Correct the To-Do row |
| C11 | Curriculum PDFs are fine in the repo | Gate 10.0 asked to check | **33 curriculum PDFs are tracked and on `origin/homebase-phase-e`** (also `phase-e-dragon-rodin-flight`, `workspace-root`), including the Tufte book (its copyright page forbids copying) and a BookZZ copy of Einstein/Greene, *The Meaning of Relativity*. The repo is described as public in the project notes (not re-checked today) | Decision needed (§9) |

---

## 6. The unified design for Tasks 1–9

This section applies the laws. Everything here is PROVISIONAL unless a ruling already exists; the code counterparts are in `integra_atlas_reference.py` (section numbers in brackets).

### 6.1 Time (T1) — [script §1, §5]
- Two kinds of time, kept apart and both labelled: **stamps** (civil + celestial, written only by the Sentinel; frame 2 since 2026-10-16 09:14) and **phases** (the position inside an internal cycle: SWDS phase, cascade hour, MTCW turn, HLC counter).
- HLC stamps take their physical part from the Sentinel's reading; the logical counter breaks ties and absorbs backward steps (tested: four ticks at a stalled or receding clock stay strictly increasing).
- Frames are never compared; a correction is a new frame (already the registry's rule).
- **Measured today:** the script's frame-2 formulas reproduce the live `/clock` reading to 4 decimals (rot 105.2273, lunar 0.2048, orbit 0.7813, `ROT_90_ORB_70`).

### 6.2 The Hoard (T2) — [script §2, §5]
- Cold truth is append-only; a node write is a transaction (shard + index row + manifest) with a commit record, so a crash leaves all or nothing.
- Node identity = first 48 bits of SHA-256 of the CCID (pointer v1). It never changes (L1).
- Forgetting follows `safe_to_prune`: no label or store names it, no reader holds it, every reader's matrix-clock entry has passed its version, and the Architect approved. Each condition is a tested refusal.

### 6.3 The Atlas: coordinate system, taxonomy, labels (T3, T3.5, T4) — [script §3, §4]
**Purpose (L2):** a filing address and a display surface; never a semantic-neighbour index.

**Grid.** Latitude bins are uniform in z = sin(latitude), so every cell at a given depth has the **same area** (tested: 32 different latitude spans at depth 6, one area). Longitude wraps at 360°. The address is a **Morton code**, most significant bits first: each level adds one bit of z and one of longitude, like a radix page table, so a prefix is a coarser cell and **depth can vary by region** (Buzsáki's zoom: dense regions deeper, sparse ones shallower).

**Zones (poles, temperate belts, equator), hemispheres and meridians** — PROVISIONAL, rulings pending:

| Zone | z range | Share of sphere | Hemisphere meaning | Kinds placed (proposal) |
|:--|:--|--:|:--|:--|
| North pole | 0.75 … 1.0 | 12.5 % | most invariant | identity, ruling |
| North temperate | 0.375 … 0.75 | 18.75 % | consolidated knowledge | library_book |
| Equator, north half | 0 … 0.375 | 18.75 % | living knowledge | semantic_junction (promoted), task, handoff, reading_ledger_row |
| Equator, south half | −0.375 … 0 | 18.75 % | recent episodes | node, save_state, working_context, assistant_note |
| South temperate | −0.75 … −0.375 | 18.75 % | dated records | swds_report, conversation_archive |
| South pole | −1.0 … −0.75 | 12.5 % | unsorted intake | drop_in |

North = invariant/consolidated, south = time-bound (Buzsáki's semantic vs episodic); **promotion moves a node north**. Zone edges are dyadic (multiples of 1/8 in z) so they fall on grid edges from depth 4 (T4's "boundaries aligned with the grid", tested). Inside a band, `level` ∈ [0,1) moves a node poleward (north: support from independent episodes; south: recency) — a declared variable, never a hash. Retired kinds (crystallization, thermo_loop, lobe_chunk) are refused.

Meridians (8 × 45°): **time, memory, cognition, governance, evolution, research, identity, operations** — Integra's own domains, replacing the codex's 12 invented meridians; the list is the Architect's to approve.

**Label.** Pointer v1 (16 bytes, the design in the 10-15 plan) **+ a 4-byte ATLAS word** (depth nibble + Morton code, 28 bits) = a **20-byte atlas pointer** (PROPOSED; the To-Do's "pointer v1 plus an ATLAS field"). Round trip tested on 100,000 random pointers, 0 failures; frozen-clock instants must carry the sentinel word; reserved flag bits are refused.

**Displays.** Canonical: 40 lowercase hex characters. Human: words, not a puzzle — e.g. `ROT_90_LUN_20_ORB_70 · raw_shards/node · f2 · trusted · key 7ac795ac2523 · atlas equator/memory d10` (its ROT/ORB segments equal the live `grid_bucket`). Braille: one 8-dot cell per byte (U+2800 + byte, dot n = bit n−1), **display only**, with no decoder in the code by design.

**Variables (T3.5 done-when: every variable has a unit and a range):**

| Symbol | Meaning | Unit | Range | Code |
|:--|:--|:--|:--|:--|
| u | instant | s (true UTC) | ℝ | `celestial_vector` |
| θ | rotation phase (local mean-solar hour angle) | degree | [0, 360) | `celestial_vector` |
| φ_L | lunar phase since new moon | fraction | [0, 1) | `celestial_vector` |
| φ_O | eccentric anomaly ÷ 2π since perihelion | fraction | [0, 1) | `celestial_vector` |
| TURN | orbits since the frame's perihelion | count | −32 … 31 | `celestial_word` |
| W | celestial word | 32-bit | packed / `0xFFFFFFFF` unknown | `celestial_word`, `decode_word` |
| k | node key | 48-bit | SHA-256(CCID)[0:6] | `node_key` |
| d | Atlas depth | levels | 0 … 14 (placement 4 … 14) | `AtlasCell` |
| z | sin(latitude) | — | [−1, 1] | `atlas_cell`, `place` |
| λ | longitude | degree | [0, 360) | `atlas_cell`, `place` |
| ℓ | level inside a band | fraction | [0, 1) | `place` |
| o | offset inside a meridian sector | fraction | [0, 1) | `place` |
| M | Morton code | 2d bits | [0, 4^d) | `_interleave` |
| A | ATLAS word | 32-bit | depth nibble + 28-bit code | `AtlasCell.word` |

### 6.4 Iteration 1: Knowledge (T5)
Run N historical shards through stamp → node key → placement → atlas pointer → read back, in an isolated copy. Report as InternAgent does: **placed / round-tripped / attempted**, plus the failures by cause (unknown provenance, frozen instants, kinds without a band). The script's round-trip and placement functions are the reference to test the real implementation against.

### 6.5 SWDS and Siesta (T5.5) — [script §9]
- **Phases** (SWDS v1.1 draft + the KNN document's Phoenix duties, made evidence-bound): open → defragment/archive → conceptual synthesis → label and place (junction promotion, pattern links that beat the null) → blueprint refinement (proposals only) → exploration → close → wake report.
- **Sweep:** start at the meridian under the current rotation phase and go east through all eight, so successive nights begin at different meridians (rotating waves; external clock anchors, internal phase runs). Spreading inside a sector follows edges (structure sets dynamics).
- **Sleep/wakeup rules (xv6):** idle detection is re-checked after every wake; an abort sets a flag honoured at safe points, never inside a Hoard transaction.
- **Closure invariant (the 13th Form, made checkable):** phases in order, each with a receipt, no open transaction at wake, end state `AWAKE_READY` = the next day's precondition. Tested positive and with two kinds of break.
- **Siesta (proposal for the open ADR-006 ruling):** the same path with only defragment + label-and-place, over one meridian, bounded by a token budget.

### 6.6 Cheshire Cat and Phoenix Force (T6)
- Cheshire Cat and Heimdall sit at the **meta level** (Nelson–Narens): they read signals and send control; they do not do the object-level work.
- The two-key route (decided D2) follows the kernel-boundary pattern: one fixed entry point; validate every argument; refuse outside an open SWDS cycle or without the Architect's key; receipts per operation; fail-stop on broken invariants; abort only at safe points.

### 6.7 Iteration 2: Understanding (T6.5)
Simulate one night in the isolated copy with fake clients and measure the couplings this pass predicts will fail first: lost wake-ups (idle vs wake race), self-confirming labels, pruning without reader agreement, hot-tier pressure under a skewed workload, and **Heimdall's signal quality** (does H > 2.5 actually separate wrong from right outputs? report AUROC and calibration).

### 6.8 The mathematical expression (T7) — [script §3, §6, §7]
For a node n with CCID c, content embedding e_n (when real embeddings exist), kind κ, domain δ, level ℓ, offset o, instant u with provenance π:

1. **Identity:** k(n) = SHA-256(c)[0:48 bits]. Invariant (L1).
2. **Stamp:** W(n) = C_F(u) packed (TURN, ORB, LUN, ROT) if π ∉ {unknown, frozen}, else the sentinel. Frame F fixed per stamp.
3. **Placement:** P_d(n) = Morton_d( zbin(κ, ℓ), λbin(δ, o) ), with zbin chosen inside the band of κ (poleward as ℓ grows) and λbin inside sector δ.
4. **Label:** L(n) = pointer_v1(F, π, store, κ, flags, space, W, k) ‖ ATLAS(P_d(n)).
5. **Candidate set for a query q:** A(q) = { n : P_{d₀}(n) = P_{d₀}(q) } ∪ N_E(q), a taxonomic prefix filter at a coarse depth d₀ plus edge neighbours (L2). Taxonomic distance = levels below the deepest common ancestor (a tree distance).
6. **Rank:** s(q, n) = cos(e_q, e_n) · f_κ(age), with f_κ(a) = 2^(−a / h_κ) and h_κ = ∞ for invariant kinds. The weights of any further terms are **unset until calibrated** (L5).
7. **Gate:** G(q) = PASS iff V(q) ≥ τ, where V(q) = Σ w_i y_i ⁄ Σ w_i over the K nearest **independently labelled** neighbours, w_i = exp(−d_i² ⁄ σ²); ABSTAIN when too few independent voters. τ is fitted on held-out outcomes (L3, L5).
8. **Pattern link (Apophenic Engine, as decided):** keep edge (a, b) iff, over W reader windows, P(X ≥ c_ab), X ~ Binomial(W, p_a p_b), passes Benjamini–Hochberg at α (tested: a planted pair is found; pure noise yields 0 links; without the correction, noise yields 9).
9. **Junction promotion:** an item seen in ≥ k distinct episodes on ≥ m distinct days moves north (tested, including a one-day burst that must not be promoted).
10. **Integrity measures:** display Lie Factor; confidence Lie Factor = mean stated confidence ÷ observed accuracy; Brier, ECE and AUROC (type-2 sensitivity) for every gate signal.

### 6.9 Rodin and the hot tier (T8) — [script §8]
Demand paging over the cold Hoard: a miss loads the node (float32 vectors, 4 bytes per dimension — the measured cheap RAM win), least-recently-routed eviction under node **and** token budgets, and a pressure figure for Heimdall. Tested with a skewed access pattern: budgets never exceeded; 2,975 hits vs 2,025 misses with a 32-node/2,000-token tier. The real embedder is still blocked on the key route (parked track), so semantic ranking waits; filing and the hot tier do not.

### 6.10 The scheduled task (T9) — [script §9]
The ritual-dance template as a dry-run planner: units 1–10 one per hour, then totality, master document, verification (13 hours), each ledger row carrying a dual stamp. Pause when a conversation is active; resume after one quiet hour, or at the nearer of 05:00 / 23:00 CDT if that comes first (the anchor overrides an ongoing conversation — an **interpretation** of the template, flagged for a ruling). Tested: a quiet night is 13 contiguous hours; a 30-minute conversation pauses one run until an hour after it ends; a long conversation resumes at the 05:00 anchor. Units can be assigned in sweep order. Registration with Task Scheduler remains its own approval.

---

## 7. The code script

**File:** `integra_atlas_reference.py` (this folder) — 880 lines, standard library only, sha256 `9164eb103ed5f76b…` (full hash in `evidence/selftest_output.txt`).
**Run from this folder, outside the kernel's process; it writes nothing:**
```
python -I -B integra_atlas_reference.py --selftest
python -I -B integra_atlas_reference.py --demo
```
**Result (MEASURED, 2026-10-16 ~20:27 CDT, Python 3.14):** 47 passed, 0 failed, exit 0. Mutation check: 10 of 10 mutants killed (the first mutation run killed 9; the survivor exposed a missing one-day-burst case, which was added). Full output: `evidence/selftest_output.txt`.
**What it does not do:** it imports nothing from the kernel, writes no files, calls no model, embeds nothing, registers no task, and is not wired anywhere. It is a reference to test the real implementations against.

**Sections:** 1 celestial frames · 2 celestial word and pointer v1 · 3 Atlas grid and taxonomy · 4 atlas pointer and displays · 5 logical clocks and pruning rule · 6 evidence (KNN vote, pattern links, junctions, freshness) · 7 metacognition and integrity measures · 8 hot tier · 9 sweep, ritual-dance planner, cycle closure · 10 self-test.

---

## 8. What is true now, and what is not

**True (MEASURED):** all 11 files were read, in order, with isolated and compounded notes; the extraction method and its limits are recorded; the script's tests and mutation check pass as shown; the frame-2 math reproduces today's live `/clock`; 33 curriculum PDFs are on `origin/homebase-phase-e`.

**Not true / not done:** no Integra component is connected by this task; T3–T9 have not started their own measurement steps; the Atlas taxonomy, meridians, thresholds and the 20-byte pointer are proposals; the Tufte figures were not viewed as images; the metacognition paper's references and the xv6 index were skimmed, not studied; nothing is committed (the package was copied into `docs/brainmap/task10/`, untracked, on the Architect's go).

---

## 9. Decisions needed

1. **Copyright exposure (C11):** what to do about the 33 curriculum PDFs on origin (keep; stop tracking going forward; or rewrite history — the last is destructive and needs its own plan).
2. ~~**Where these outputs go**~~ — **decided 2026-10-16 (the Architect):** copied into `integra-homebase/docs/brainmap/task10/` with hash checks; T10 recorded in `TODO.md` and the `TASKS.md` pointer.
3. ~~**The To-Do correction (C10)**~~ — **done 2026-10-16:** the Buzsáki row now names the OUP chapter.
4. **Atlas rulings (T3/T4, now with a concrete proposal):** the 8 meridians; the kind → zone table; hemisphere meaning (north invariant, south time-bound); the 20-byte atlas pointer vs a separate ATLAS key.
5. **Pause-rule interpretation (T9):** does the 05:00 / 23:00 anchor override an ongoing conversation?
6. **Doctrine corrections C1–C3:** adopt them in the blueprint's glossary (LF honest at 1; celestial vector = projection of the clock; no structure claims for low-dimensional projections).

## 10. Next

The copy-in is done. The To-Do resumes where it stands — **T2 2.5 P1** (the metatron ruling and the apply go) — with decisions 1 and 4–6 still open. The script's sections become the test oracles for T3.5 (codec), T4 (placement), T7 (expression), T8 (hot tier) and T9 (planner) when those tasks are built.

---

### Appendix — files in this package

| Path | What |
|:--|:--|
| `TASK10_MASTER_DOCUMENT.md` | this document |
| `Task10_REPORT.md` | the task report in the To-Do's format |
| `integra_atlas_reference.py` | the unification script |
| `evidence/selftest_output.txt` | test, mutation and demo output, verbatim |
| `notes/01…11_*.md` | per-document notes (isolated read + links to earlier documents) |
| `notes/compound_notes.md` | the K/U/W ledger, updated after each document |
| outside the repo: `%USERPROFILE%\t10\` | extraction tools (`pdf_ccitt_to_tiff.py`, `ocr_dir.ps1`), extracted text, mutation runner and mutants |
