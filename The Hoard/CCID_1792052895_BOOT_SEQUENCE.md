# Boot sequence for the next thread (from CCID_1792052895, 2026-10-15 03:28 CDT)

Follow the steps in order. Read every file in full, not skimmed. Record a receipt for each: path, bytes, lines read. Stop at step 7 and wait for the Architect.

1. **`CLAUDE.md`** (repo root): standing rules, gotchas (CFA: write with the Write/Edit tools and `C:\Python313\python.exe -X utf8`; pwsh, Git Bash and Python 3.14 cannot write), pointers.
2. **The save state, both files, in full:**
   - `The Hoard/CCID_1792052895_SAVE_STATE_REPORT.md`
   - `The Hoard/CCID_1792052895.json`
3. **The plan file** `~/.claude/plans/1-productivity-start-text-integra-kind-cocke.md`: the section **"Plan (2026-10-13 midday): folder 13 — read what carries meaning, account for every byte"**, including **"Additions from the Architect's notes"**. It governs folder 13. The original four-step plan is `~/.claude/plans/extract-the-design-system-curried-dragon.md` (background).
4. **Memory:** the index `~/.claude/projects/C--Users-<user>-OneDrive-Desktop-Integra-Purple-SunBreathing/memory/MEMORY.md` and every note it lists, especially `folder13-archive-method.md`, `verify-before-claiming.md`, `zenitsu-sun-breathing-ruling.md`, `integra-model-roster-argon.md` and `integra-naming-oct14.md`.
5. **Local, git-ignored resume detail** (never copy its content into the public repo):
   - `The Hoard/antigravity_conversations/_summaries/RESUME_HERE.md`. Its first section is the reading-cycle loop and the progress log through cycle 22; read the whole file.
   - `_summaries/guide.md`: the compounding guide (primer plus 22 cycle sections). The readers get it through their briefs; read it so you know what they know.
   - `_summaries/cycles_v4/cycle_22.md`: the latest cycle synthesis (its "Contradictions and questions to watch" feed the next cycles).
   - `_summaries/cycles_v4/agents.tsv` and `cycles.tsv`: the last rows only (agent ids, verify results).
6. **Read-only probes:**
   - `GET /clock` (the stamp: CDT | UTC | celestial), `/heimdall/health` (once), `/swds/status`, `/cheshire/status`;
   - the scheduled task's state and its Task Scheduler history (is the wrapper alive?);
   - `(Get-MpPreference).EnableControlledFolderAccess` and new Defender 1123 events;
   - plan usage (`get_usage`).

   No POSTs, no `/celestial/checkpoint`, no kernel restart, no paid model calls.
7. **Report to the Architect, then wait for the go:**
   - the receipts from steps 1–5 and the stamped probe results;
   - **the resume point: Step 2, folder 13, plan Step 4, cycle 23 (units U089–U092).** The briefs are not written yet. On the go, run the loop exactly as RESUME_HERE describes it:
     1. usage check (5-hour window above ~80–85%: wait for the reset; weekly above ~85%: stop and ask);
     2. from `_summaries/tools`: `C:\Python313\python.exe -X utf8 cycle_tool.py briefs U089 U090 U091 U092`;
     3. launch 4 general-purpose agents in the background, each with: "Read and follow exactly the brief at <...>\cycles_v4\briefs\U0xx_brief.md . It is self-contained."; log ids in `agents.tsv` with times from `/clock` only;
     4. when all 4 finish: `partial_redact.py`, then `cycle_tool.py verify 23 U089 U090 U091 U092`, then `report_scan.py U089 U090 U091 U092` and `extra_scan.py <the 4 reports>`;
     5. `cycle_tool.py synth 23 U089 U090 U091 U092`, launch the synthesizer on `briefs/cycle_23_synth_brief.md`;
     6. spot-check with `guide_check.py 23` and `extra_scan.py` on `cycle_23.md` and `guide.md`; write the progress lines in RESUME_HERE; next cycle.
   - the open items for the Architect (report section 6).
