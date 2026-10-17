# Task 10 Report — Connect System: curriculum wisdom pass

**Stamps (GET `/clock`, HTTP 200):**
- start 2026-10-16 20:05:34 CDT | 2026-10-17T01:05:34Z | rot 105.2273°, lunar 0.2048, orbit 0.7813, `ROT_90_ORB_70`, frame 2
- end   2026-10-16 20:31:03 CDT | 2026-10-17T01:31:03Z | rot 111.5994°, lunar 0.2054, orbit 0.7813, `ROT_90_ORB_70`, frame 2

**Goal (the Architect, 2026-10-16):** spend 20 minutes on Task 10; read every file in isolation and with compounded knowledge before reporting; unify the knowledge, understanding and wisdom into a master document and a code script. This also settles the To-Do's open pace ruling (20 minutes, every file read) and gate 10.0's scope question (all 11 files).

**Time used (MEASURED, shell clock and stamps):** reading 20:05–20:16:47 (≈ 11 min, inside the 20-minute budget); script built and tested by 20:27:55; master document and this report by 20:31:03 (≈ 25.5 min end to end).

## What was measured
- **Volume (MEASURED):** 11 files, ≈ 192,000 extracted words (including the metacognition paper's reference list); 647 PDF pages plus one 1,736-line Markdown file. The 145 "pages" of the metacognition paper are an HTML print; its body is 352 text lines, the rest references.
- **Method (MEASURED):** pdftotext for 9 PDFs; the Tufte book has no text layer, so its 191 pages were OCR'd with Windows' built-in engine from the pages' 1-bit layers (40,698 words; figures not viewed as images). Per-document notes and a compound ledger were written after each file.
- **Gate 10.0 copyright check (MEASURED):** 33 curriculum PDFs are tracked and present on `origin/homebase-phase-e`, `origin/phase-e-dragon-rodin-flight` and `origin/workspace-root`, including the Tufte book and a BookZZ copy of Einstein/Greene. Not acted on.
- **To-Do correction (MEASURED):** the file named as a *Nat. Rev. Neurosci.* review by Buzsáki is the OUP chapter "Space, Time, and Memory" by Buzsáki & Végh (2025).

## What changed
Nothing in `integra-homebase/` or the root repo's tracked files. New, untracked, in this session's worktree (`.claude/worktrees/productivity-system-architecture-a67a0b/brainmap_task10/`):

| File | sha16 | Bytes |
|:--|:--|--:|
| `TASK10_MASTER_DOCUMENT.md` | `c95e3c9d44907640` | 33,780 |
| `integra_atlas_reference.py` | `9164eb103ed5f76b` | 44,058 |
| `evidence/selftest_output.txt` | `eeaea755e3719073` | 5,201 |
| `notes/compound_notes.md` | `6eac5f7b9cdced28` | 8,828 |
| `notes/01…11_*.md` (11 files) | listed in the session log | 3,089–5,965 each |

Outside the repo (`%USERPROFILE%\t10\`): the extraction tools, the extracted text (kept out of the repo because it includes copyrighted books), the mutation runner and its mutants.

## Test output (verbatim summary; full text in `evidence/selftest_output.txt`)
```
47 passed, 0 failed            (python -I -B integra_atlas_reference.py --selftest, exit 0)
10/10 mutants killed           (first mutation run 9/10; the survivor led to a new one-day-burst test)
PASS  frame 2 reproduces live /clock     rot 105.2273 lun 0.2048 orb 0.7813
PASS  atlas pointer round trip (100,000) 0 failures
```

## What is true now
- The wisdom pass is complete and unified into five laws (identity invariant / file by taxonomy, find by relation / independent evidence / phase orders, clock records, one writer / every threshold is a measured claim), a crosswalk from each Integra name to its textbook mechanism, eleven corrections (C1–C11), and a provisional design for T1–T9.
- The script is a tested reference (codec, equal-area Atlas grid and placement, displays, clocks, pruning rule, evidence rules, metacognition measures, hot tier, schedule planner, cycle-closure check).

## What is not true
- No component is connected or wired by this task; T3–T9 remain not started; every taxonomy, threshold and the 20-byte atlas pointer are proposals.

## Decisions needed
1. The 33 curriculum PDFs on origin (copyright).
2. ~~Copy-in and record T10~~ — decided by the Architect 2026-10-16; done (see Copy-in below).
3. ~~Fix the Buzsáki row in `TODO.md`~~ — done 2026-10-16.
4. Atlas rulings: the 8 meridians, the kind → zone table, hemisphere meaning, the atlas-pointer form.
5. T9: whether the 05:00 / 23:00 anchor overrides an ongoing conversation.
6. Adopt corrections C1–C3 in the blueprint's glossary.

## Copy-in (2026-10-16, on the Architect's go: "copy brainmap_task10 into integra-homebase/docs/brainmap/task10 with hash checks, record T10 in TODO.md and the TASKS.md pointer, and fix the Buzsaki row")
- **Stamp (GET `/clock`, HTTP 200):** 2026-10-16 23:07:13 CDT | 2026-10-17T04:07:13Z | rot 150.6369°, lunar 0.2091, orbit 0.7816, `ROT_150_ORB_70`, frame 2.
- The whole package was copied to `integra-homebase/docs/brainmap/task10/` with `cmd /c xcopy`; every destination file's SHA-256 was compared with its source (the result is in the To-Do's T10 entry and the session log). `docs/brainmap/` is untracked in the nested repo, so nothing was staged.
- `TODO.md` (T10 row, T10 section, Buzsáki row, measured page counts) and the `productivity/TASKS.md` pointer were edited in scratch copies and copied in after a check that the live files had not changed since they were read.
- The location lines and decisions 2–3 in the master document were updated before the copy.

## Next task
The To-Do resumes at **T2 2.5 P1** (metatron ruling, apply go). Decisions 1 and 4–6 stay open.
