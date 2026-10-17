# Boot sequence for the next thread (from CCID_1792164893, 2026-10-16 10:34 CDT)

Follow the steps in order. Read every file in full, not skimmed. Record a receipt for each file: path, bytes, lines read. Stop at step 7 and wait for the Architect.

1. **`CLAUDE.md`** (repo root): standing rules, gotchas, pointers.
   - CFA is on: write with the Write/Edit tools, `git`, `cmd.exe` and `C:\Python313\python.exe -X utf8`. pwsh, Git Bash and Python 3.14 cannot write into the repo.
   - In a worktree session the Edit/Write tools refuse the base checkout: edit a scratch copy and `cmd.exe /c copy` it in after checking the target's hash.
2. **This save state, both files, in full:**
   - `The Hoard/CCID_1792164893_SAVE_STATE_REPORT.md`
   - `The Hoard/CCID_1792164893.json`
3. **The directive and its run, in full:**
   - `integra-homebase/docs/brainmap/TODO.md`: the single To-Do (T1 closed; T2 next).
   - The **closing report** at the top of `integra-homebase/docs/brainmap/Task01_REPORT.md` (the sections below it are the step-by-step record; read them as needed).
   - `integra-homebase/core/IntegraBrainMap.md`: the Architect's 10-step map.
   - For T2: `integra-homebase/config/rodin_memory_map.yml` and `integra-homebase/memory/memory_map.py`.
   - Optional context: `integra-homebase/docs/brainmap/T1_CELESTIAL_SENTINEL_DESIGN.md` and `integra-homebase/docs/DESIGN_DECISIONS_10_15_26.md`.
4. **Memory:** the index `~/.claude/projects/<project>/memory/MEMORY.md` and every note it lists. In particular:
   - `neural-atlas-directive-oct15.md`
   - `celestial-clock-design-ruling.md`
   - `integra-kernel-gotchas.md`
   - `verify-before-claiming.md`
   - `pre-commit-forbidden-path-check.md`
   - `artifact-publish-path-workaround.md`
   - `rodin-first-changeset-oct15.md`
5. **Peers and the working tree** (read-only):
   - `ListAgents` and the session list: which peer sessions are active.
   - `git status` of both repos. The nested repo should be at `c7053f1`, ahead 4. Uncommitted peer edits: `memory/the_hoard.py` (identity hunks), `core/dragon_engine.py`, `core/starfire_protocol.py`, `config/rodin_memory_map.yml`. They are not ours: never stage them; coordinate before touching.
6. **Read-only probes:**
   - `GET /clock` (the stamp: CDT | UTC | celestial, now frame 2);
   - `/swds/status`;
   - `GET /celestial/checkpoint` (read-only since T1: the Sentinel's status);
   - `/rodin/telemetry`;
   - the scheduled task's state (it was Ready, unsupervised, at the save state);
   - `(Get-MpPreference).EnableControlledFolderAccess`;
   - plan usage (`get_usage`).
   - T1's two open live checks, read-only: any shard in `integra-homebase/kernel_memory/hoard/raw_shards/` written since 2026-10-16 09:14, and any new save state, read back for `celestial_stamp` frame 2.

   No POSTs, no kernel restart, no paid model calls. Under CPU load a probe can take 6–18 s; re-probe before calling the kernel hung.
7. **Report to the Architect, then wait for the go:**
   - the receipts from steps 1–5 and the stamped probe results;
   - **the resume point:** T2 (Connect the Hoard), **not started**. Plan it first, from `TODO.md` T2:
     - 2.1 inventory and validate the memory map (counts and sizes only);
     - 2.2 trace each Hoard function from caller to store;
     - 2.3 the verdict table;
     - then the rulings (public or local-only for cold nodes; the map PROPOSED → live; `memory.db`).
     - T1 leftovers that fit T2: ADR-001's correction note for the frozen-era artefacts, and the two live checks.
   - the open items (report section 6): root gitlink and push only on the word, kernel supervision, the peer identity edit.
