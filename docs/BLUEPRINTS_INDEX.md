# Blueprint index (consolidation map)

Measured on disk 2026-10-12, about 15:12-15:20 CDT (session c88f5000), after the 10/12 corrections and the page republish. Stamp for this pass: 2026-10-12 15:10:34 CDT | 2026-10-12T20:10:34Z | rot 91.4767°, lunar 0.6585, orbit 0.2175, ROT_90_ORB_20 (`GET /clock`, HTTP 200).

- **Hashes.** `sha16` is the first 16 hex digits of SHA-256 over the bytes on disk. The working tree uses CRLF line endings (system gitconfig `core.autocrlf=true`), so a fresh checkout elsewhere may hash differently. Compare files on the same machine.
- **Paths.** Paths starting `integra-homebase/` are in the homebase repo; every other path is in the root repo.
- **Tracking.** Every file listed here is tracked in git, except the one in section 5.
- **Nothing was moved, renamed or deleted.** Tests and scripts depend on some of these paths (section 6).

## 1. The rule

There is **one canonical blueprint**. Edit only that file. The two "v.9.9.1…" export files are exact copies of it, re-copied after every republish of the page (procedure in section 7).

## 2. Canonical blueprint and exact copies

| Path | Bytes | sha16 | Role |
|:--|--:|:--|:--|
| `integra-homebase/docs/MASTER_ARCHITECTURE_BLUEPRINT.md` | 188,333 | `cbcebbf137168db1` | **Canonical**, v.9.9.1 with the 2026-10-12 corrections (Appendix B, item 11). Page: https://claude.ai/artifact/CSEgvRaUnBzC5VdyRep98i, version 13 (`1791835991-322b`). |
| `integra-homebase/docs/v.9.9.1Integra Master Architecture Blueprint.md` | 188,333 | `cbcebbf137168db1` | **Exact copy.** The export name is kept. Refreshed 2026-10-12 15:12; it held the 10/09 v.9.9 text (`11e7bab245c89c1f`) until then. |
| `v.9.9.1Integra Master Architecture Blueprint.md` | 188,333 | `cbcebbf137168db1` | **Exact copy**, same history as the row above. |

Relative links inside the blueprint resolve only from `integra-homebase/docs/`. In the root copy, the two links to `RODIN_SUBAGENT_MODEL_RESEARCH.md` do not resolve; that is expected for a byte-identical copy.

The 10/11 attempt to refresh the two copies failed. The cause was Windows Defender Controlled Folder Access (events 1123), not OneDrive; see the canonical, "Other changes → Page exports".

## 3. Misnamed file

| Path | Bytes | sha16 | Role |
|:--|--:|:--|:--|
| `integra-homebase/Guidebooks_and_Notes/v.9.9.1Integra Master Architecture Blueprint.md` | 461,842 | `09e41432b6e21ba0` | **Not a blueprint.** It is byte-identical to `integra-homebase/docs/OCT9Suite1_2T.md`, the Suite 1_2T conversation transcript. It is left unchanged; renaming it is the Architect's call. |

## 4. Historical design documents

These are sources, not the current state of the system. For the current state, see the canonical. Most of them exist twice, once in the root repo and once in `integra-homebase`.

| Document | Copies (path, bytes, sha16) | What it is (first lines read 2026-10-12) |
|:--|:--|:--|
| Phase D Implementation Plan | `Phase D Implementation Plan_Blueprint_ Mechanical Reality.rmd`, `MODIFIED834Phase D Implementation Plan_Blueprint_ Mechanical Reality.rmd`, and the same two names under `integra-homebase/`. 4 copies, all 102,239 bytes, `473d4a164e3844b9`. | "Phase D Implementation Plan: Blueprint → Mechanical Reality", Integra O/S v8.2.2 → v8.2.4 Purple Epiphany. 1,438 lines. The "MODIFIED834" copies are byte-identical to the originals. |
| Comprehensive Systems Guidebook v8.2 | `Guidebooks_and_Notes/DPathForward192026/BlueuprintmasterdesignArchitecture.md` and the `integra-homebase/` copy. 1,036,036 bytes, `17394e2d0ecacebc`. | "Comprehensive Systems Guidebook (v8.2, The Purple Epiphany Build)", dated August 13, 2026. 14,887 lines. |
| CODE "Packet 2" blueprint architecture | Under `CODE/` and `integra-homebase/CODE/`, the files `Markdowncopy1Packet 2  Matrix map_systems workflow_fulcrum fragility_bluprintarchitecture.md` (25,620 bytes, `c7126a691644c202`), `TXTcopy1…txt` (24,345, `bd9d21e2ff3a0127`) and `PDFcop1…pdf` (216,630, `387f127f4940688f`). 6 files, 3 formats × 2. | A "Packet 2" system log: Phase 4, the 13th Form final synthesis. 157 lines (`.md`). |
| System Blueprint Creation (PDF) | `AntiGravityconversionprocess/Integra OS System Blueprint Creation.pdf` and the `integra-homebase/` copy. 1,190,470 bytes, `ddfc680f4a94ea15`. | A PDF, not read in this pass (to be read in Step 2 or Step 3). |
| Cheshire Cat Daemon blueprint v0.1 | `The Hoard/thread_f2e7cc92_handoff/cheshire_blueprint.md`, root only. 10,214 bytes, `a5fe190ac7107a9f`. | "Cheshire Cat Daemon: Blueprint v0.1 (design only, no code written)", stamped 2026-10-07 23:05:08 CDT. Boot file (e). |
| Save-state blueprint, text A | `AntiGravityconversionprocess/save_state_blueprint.md` and `Automatedactionsv2/save_state_blueprint.md`, in both repos. 4 copies, 6,405 bytes, `af58e8c494e83394`. | "Integra O/S Save State Blueprint & Analytical Report", session `4e32d431…`. 91 lines. |
| Save-state blueprint, text A′ | `The Hoard/save_state_blueprint.md` in both repos. 2 copies, 6,420 bytes, `e236a4c664ce0d10`. | Text A plus several added blank lines, minus one trailing space. No other change (diff checked). |
| Save-state blueprint, text B | `save_state_blueprint.md` at the top of both repos. 2 copies, 7,126 bytes, `463e56ba6152957e`. | The same report for session `882ff934…`. 102 lines. **A test reads the `integra-homebase` copy** (section 6). |
| `BluprintArchitecture/` source library | `BluprintArchitecture/` and `integra-homebase/BluprintArchitecture/`. 80 files each, 19,276,725 bytes each. The trees are identical: tree hash `3db930595c3e20f9`, computed over the relative paths and per-file SHA-256. | A source library rather than a blueprint: guidebooks v8.2, the Identity Matrix, the Dragon Prompt, the Cheshire Cat Personality Matrix, MCP/API notes and others. The knowledge ingester reads it as the "architecture" lobe. |

## 5. Name match, unrelated

| Path | Bytes | sha16 | Role |
|:--|--:|:--|:--|
| `integra-homebase/Antigravity IDE/User/globalStorage/googlecloudtools.datacloud/remote-kernel/Lib/site-packages/pygments/lexers/blueprint.py` | 6,191 | `756f8be5b148896c` | The Pygments lexer for the "Blueprint" UI language, from a vendored site-packages. Not tracked: `Antigravity IDE/` is in `integra-homebase/.gitignore` (L74). |

## 6. Path dependencies (change these before moving or renaming anything)

| Code | Depends on |
|:--|:--|
| `integra-homebase/tests/test_systems_audit_and_protocols.py:373` | `integra-homebase/save_state_blueprint.md` (text B) |
| `integra-homebase/scripts/ingest_knowledge.py:10, 49` | `BluprintArchitecture` as the "architecture" lobe |
| `integra-homebase/scripts/inspect_hygiene.py:9` | `ROOT_DIR / "BluprintArchitecture"` |
| `integra-homebase/tests/test_knowledge_ingestion.py:109, 114` | the `LOBE_CONFIG["BluprintArchitecture"]` key |
| Hoard shards in `integra-homebase/kernel_memory/hoard/raw_shards/` | These are data, not code. Many shards quote `save_state_blueprint` text. `CCID_1791704093.json:37` names the canonical's path and the page URL. |

## 7. Update procedure (after every change to the canonical)

1. Edit only `integra-homebase/docs/MASTER_ARCHITECTURE_BLUEPRINT.md`.
2. Rebuild the page with the builder:
   - run `md2html_blueprint.py` with `blueprint_template.html` from a session scratchpad;
   - normalize the output to LF;
   - read the live page first;
   - publish to the same URL;
   - read it back.
3. Copy the canonical's bytes over both export copies (section 2) and check the SHA-256.
   - While Controlled Folder Access is on, use the Edit/Write tools, `git`, or `C:\Python313\python.exe` (allowed apps).
   - Do not use `pwsh`, Git-bash `cp`, or `C:\Python314\python.exe` (blocked).
4. Update the hashes and the page version in section 2 of this file.

## 8. Open consolidation decisions (for the Architect, Step 3 or later)

- **Duplicate copies.** Root and `integra-homebase` hold duplicate copies of almost every file in section 4: 9/28 and 9/29 copies of the same bytes. Removing one side changes the paths in section 6, so it is not done here.
- **The misnamed Guidebooks file** (section 3): rename it, or leave it.
- **What merges into the canonical.** Which of the historical documents in section 4 should be merged into the canonical as source material is decided in Step 3 (the unified document), after gate G2.
