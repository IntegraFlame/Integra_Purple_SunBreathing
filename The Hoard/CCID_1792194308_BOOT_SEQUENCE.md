# Boot sequence for the next thread (from CCID_1792194308, 2026-10-16 18:45 CDT)

Follow the steps in order. Read every file in full, not skimmed, and record a receipt for each: path, bytes, lines read. Stop at step 7 and wait for the Architect.

1. **`CLAUDE.md`** (repo root): the standing rules, gotchas and pointers.
   - CFA is on, so write with the Write/Edit tools, `git`, `cmd.exe` and `C:\Python313\python.exe -X utf8`.
   - In a worktree session, the Edit/Write tools refuse the base checkout. Edit a scratch copy, check the target's hash, then `cmd.exe /c copy` it in.
2. **This save state**, both files: `The Hoard/CCID_1792194308_SAVE_STATE_REPORT.md` and `The Hoard/CCID_1792194308.json`.
3. **The directive and its run:**
   - `integra-homebase/docs/brainmap/TODO.md`, the single To-Do (T1 closed; T2 at step 2.5).
   - `integra-homebase/docs/brainmap/T2_5_PLAN.md`, the 2.5 plan; P1 is next.
   - `integra-homebase/docs/brainmap/Task02_VERIFICATION_REPORT.md`, with its rulings section R1–R8.
   - `integra-homebase/core/IntegraBrainMap.md`, the Architect's 10-step map.
   - For P1:
     - `integra-homebase/config/rodin_memory_map.yml`: the working tree carries the peer's identity edit, so also read HEAD's version with `git show HEAD:config/rodin_memory_map.yml`;
     - `integra-homebase/memory/memory_map.py` and `tests/test_memory_map_audit.py`, as committed in `e519534`.
4. **Memory:** the index `~/.claude/projects/<project>/memory/MEMORY.md` and every note it lists, especially:
   - `neural-atlas-directive-oct15.md`;
   - `verify-before-claiming.md`;
   - `pre-commit-forbidden-path-check.md`;
   - `integra-kernel-gotchas.md`;
   - `celestial-clock-design-ruling.md`.
5. **Peers and the working tree** (read-only):
   - list the sessions; the T2 boot session is suspended and gets no messages;
   - `git status` of both repos: the nested repo should be at `e519534`, ahead 5. The uncommitted peer edits are not ours: never stage them.
6. **Read-only probes:**
   - `GET /clock` (the stamp, frame 2);
   - `/swds/status`;
   - `GET /celestial/checkpoint` (read-only);
   - `/rodin/telemetry`;
   - the scheduled task's state (Running at the save state, since the 18:07 restart);
   - `(Get-MpPreference).EnableControlledFolderAccess`;
   - plan usage.

   No POST, no kernel restart, no paid call.
7. **Report to the Architect, then wait for the go:**
   - the receipts and the stamped probes;
   - **the resume point:** T2 step 2.5, **P1**. First ask the one remaining ruling, the five gap fixes (save-state report section 5 B). Then, on the go, build in a fresh isolated copy: the HEAD map, the fixes, the three dead kinds retired, the 8 locations declared, the writer text, `shares_path_with`.
   - **the open items:** the root gitlink and push only on the Architect's word; kernel supervision; the peer identity edit; reading the Braille codex and HTML in full at T3's start.
