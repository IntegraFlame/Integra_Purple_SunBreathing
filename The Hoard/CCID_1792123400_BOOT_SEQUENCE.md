# Boot sequence for the next thread (from CCID_1792123400, 2026-10-15 23:03 CDT)

Follow the steps in order. Read every file in full, not skimmed. Record a receipt for each file: path, bytes, lines read. Stop at step 7 and wait for the Architect.

1. **`CLAUDE.md`** (repo root): standing rules, gotchas, pointers.
   - CFA is on: write with the Write/Edit tools, `git`, `cmd.exe` and `C:\Python313\python.exe -X utf8`.
   - pwsh, Git Bash and Python 3.14 cannot write into the repo.
2. **This save state, both files, in full:**
   - `The Hoard/CCID_1792123400_SAVE_STATE_REPORT.md`
   - `The Hoard/CCID_1792123400.json`
3. **The current directive and its codex, in full:**
   - `integra-homebase/core/IntegraBrainMap.md`: the 10-step to-do. The Architect calls it "a true prompt and directive to follow".
   - `integra-homebase/memory/Braille-BasedSemanticLabelingSystem.md`: the core codex (1,650 lines). The `core/` copy of this file is empty.
   - `NewCurriculum2026/theritualdance.md`: the schedule pattern for Step 9.
   - `IntegraCognitiveFramework_ALIGNED_DRAFT_10_15_26.md` §8a: Rodin's hot and cold tiers.
   - `~/.claude/plans/structured-spinning-codd.md`: the cold-tier pointer v1 design.
   - `~/.claude/projects/<project>/braille_assessment_2026-10-15/BRAILLE_ASSESSMENT.md`: what in the codex holds up and what does not (measured).
4. **Memory:** the index `~/.claude/projects/<project>/memory/MEMORY.md` and every note it lists. In particular:
   - `rodin-first-changeset-oct15.md`
   - `braille-atlas-assessment-oct15.md`
   - `integra-kernel-gotchas.md`
   - `celestial-clock-design-ruling.md`
   - `architect-decisions-oct15-design.md`
   - `rodin-subagents-no-model.md`
   - `verify-before-claiming.md`
5. **Peers and the working tree** (read-only):
   - `ListAgents`: which peer sessions are active.
   - `git status` of both repos.
   - The nested tree held uncommitted edits by peer sessions at the stamp: `celestial_middleware.py` (ADR-001), `main.py`, `the_hoard.py`, `dragon_engine.py`, `starfire_protocol.py`, `rodin_memory_map.yml`, `tests/test_rodin_supervisor.py`, and new tests and shards. They are not ours; coordinate before touching them.
6. **Read-only probes:**
   - `GET /clock` (the stamp: CDT | UTC | celestial);
   - `/swds/status` (and the wake report, if tonight's SWDS ran: expected about 00:38–05:38 CDT);
   - `/rodin/telemetry`;
   - the scheduled task's state (is the wrapper alive?);
   - `(Get-MpPreference).EnableControlledFolderAccess`;
   - plan usage (`get_usage`).

   No POSTs, no `/celestial/checkpoint`, no kernel restart, no paid model calls.
7. **Report to the Architect, then wait for the go:**
   - the receipts from steps 1–5 and the stamped probe results;
   - **the resume point:** the 10-step directive, **not started**. Plan it first, in plan mode, in Zenitsu order: K (steps 1–5, gate K), U (5.5–6.5, gate U), W (7–10), then Unification (the master document and code script, outside the repo first).
     - Decided: Apophenic = pattern links across nodes.
     - Open: the Step 10 pace, the meridian list, C-07 and Siesta.
   - the parallel track: finish the embedder-only key route (report §5 D);
   - the open items (report §6).
