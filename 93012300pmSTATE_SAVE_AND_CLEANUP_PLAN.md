# INTEGRA O/S — State Save, Error Resolution & Cleanup Plan
## Session: 2026-09-30 | Branch: `phase-e-dragon-rodin-flight`
## Status: READY FOR USER APPROVAL

---

## 1. System Health Audit Results

### ✅ VERIFIED OPERATIONAL
| System | Status | Evidence |
|---|---|---|
| **Genesis Kernel (port 8000)** | HEALTHY_OPTIMAL | `curl /heimdall/health` returns all 9 lobes healthy |
| **Heimdall 3.1** | NOMINAL_TRACKING | H_smooth = 0.0, no P-SSR breaches |
| **Thermodynamic Loop** | SEALED | ΔE = 0.0001 |
| **Friday Fortress Bank** | MARGIN_LOCK_SECURE | Equity $25,250, Floor $20,000 |
| **Model Registry** | OPERATIONAL | Sonnet 5.5 (Nexus/Shiva), Gemini 3.6 Flash (Rodin), Gemini 3.8 Flash (Cheshire), Gemini 3.1 Pro (Y789/Phoenix) |
| **Git State** | CLEAN | Up to date with `origin/phase-e-dragon-rodin-flight`, nothing to commit |
| **datacloud_telemetry plugin** | RESOLVED | User deleted the broken plugin file |

### ✅ CORRECTED FINDINGS (Previously Suspected Errors)
| Issue | Actual Status |
|---|---|
| **Dashboard Trading Portfolio not rendering** | **FALSE ALARM** — `updateFortress(fortress)` IS called at line 1453. API returns correct data. If not visible, hard-refresh browser (`Ctrl+Shift+R`). |
| **AI Models not interconnected** | **FALSE ALARM** — `core/cognitive_engine.py` line 31 imports `Y789Client, NexusClient, CheshireCatClient`. Lines 60-62 instantiate them. Lines 246, 345, 419-420 actively call `.generate()`. Models ARE wired to cognitive functions. |

### ⚠️ ACTUAL REMAINING ISSUES
| Issue | Fix |
|---|---|
| **SWDS Dashboard has no route** | Add `@app.get("/swds")` route to `main.py` serving `swds_simulation_dashboard.html` |
| **File clutter** | ~20 duplicate/orphaned files in root directory need cleanup |

---

## 2. Proposed File Cleanup

### Files to ARCHIVE (move to `archive/` folder)

> [!CAUTION]
> These files will be MOVED, not deleted. They remain recoverable.

| File | Reason |
|---|---|
| `# celestial clock live.md` | Superseded by `celestial_clock_live.html` |
| `# I am Integra.md` | Historical/identity doc, not operational |
| `# STARTUP BRANCH 2 WALKTHROUGH.md` | Duplicate of `STARTUP BRANCH 2 WALKTHROUGH.md` |
| `# To-D0.md` | Superseded by `integra_master_todo.md` |
| `# To-D0.py` | Old script version of todo |
| `Epiphany Catalyst...md.bak` | Backup file |
| `Epiphany Catalyst...md.md` | Double-extension duplicate |
| `Epiphany_Catalyst_REMOVED_COPIED_CONTENT.md` | Cleanup artifact |
| `ToDo.md` | Superseded by `integra_master_todo.md` |
| `ToDo.md.bak` | Backup of superseded file |
| `ToD0922.md` | Date-stamped todo snapshot |
| `save_state_20260921.md` | Old save state |
| `save_state_blueprint.md` | Old save state template |
| `main209f4baSave statePhaseElog.log` | Old log file |
| `debug_test.py` | Debug script |
| `content.md` | Ambiguous orphan |
| `ClaudeTools.md` | Reference doc, not operational |
| `ClaudeToolsmcpapi.md` | Reference doc, not operational |
| `GeminiTools.md` | Reference doc, not operational |
| `MODIFIED834Phase D Implementation Plan_Blueprint_ Mechanical Reality.rmd` | Superseded by current phase |
| `Phase D Implementation Plan_Blueprint_ Mechanical Reality.rmd` | Superseded by current phase |

### Files to CONSOLIDATE (merge .env files)

> [!WARNING]
> Multiple `.env` files exist. These should be consolidated into a single `.env` with clear section headers.

| File | Action |
|---|---|
| `CHROMA_API_KEY.env` | Merge into `.env` |
| `chromakey.env` | Merge into `.env` |
| `CLAUDE_API_KEY.env` | Merge into `.env` |
| `claudehemisphere.env` | Merge into `.env` |
| `FIRECRAWL_API_KEY.env` | Merge into `.env` |
| `FIRECRAWLapi.env` | Merge into `.env` |
| `GEMINI_API_KEY.env` | Merge into `.env` |
| `geminihemisphere.env` | Merge into `.env` |
| `Git_personal_access.env` | Merge into `.env` |
| `env_file_map.env` | Merge into `.env` |

### Files to KEEP (no changes)
All core operational files: `main.py`, `models.yml`, `requirements.txt`, `Dockerfile`, `deployment.yaml`, `render.yaml`, `Configuration.yml`, `IntegraBrainModel0930.md`, `README.md`, `SYSTEMS_MAP.md`, etc.

---

## 3. New Route: SWDS Dashboard

Add to `main.py`:
```python
@app.get("/swds")
def serve_swds_dashboard():
    """Serves the SWDS Options Simulation Dashboard on a dedicated route."""
    return FileResponse("static/swds_simulation_dashboard.html", media_type="text/html")
```

Copy `swds_simulation_dashboard.html` to `static/` directory.

---

## 4. Execution Sequence

1. ✅ Create `archive/` directory
2. ✅ Move 21 files to `archive/`
3. ✅ Consolidate `.env` files
4. ✅ Copy SWDS dashboard to `static/` and add route
5. ✅ `git add . && git commit -m "chore: Archive orphaned files, consolidate env, add SWDS route"`
6. ✅ `git push origin phase-e-dragon-rodin-flight`
7. ✅ Push parent repo sync

---

## 5. State Save for New Thread

### Key State to Carry Forward
- **Branch**: `phase-e-dragon-rodin-flight`
- **Genesis Kernel**: Running on port 8000, task-884
- **Models**: Sonnet 5.5 (Nexus/Shiva), Gemini 3.6 Flash (Rodin), Gemini 3.1 Pro (Y789/Phoenix), Gemini 3.8 Flash (Cheshire)
- **Dashboard**: `localhost:8000/dashboard` — all panels wired including Friday Fortress
- **SWDS**: Will be at `localhost:8000/swds` after this plan executes
- **Fortress**: Equity $25,250, Bank $20,836 (SGOV), Reactor $4,414, Shield $0
- **Evolved Hunter Bridge**: Active, PAPER mode, 12 production rules loaded
- **Brain Model 0930**: Finalized with Eye/Lens/Shiva bindings locked

### Open Items for Next Thread
1. IBKR TWS API live market data feed wiring (October 1 launch)
2. Crisis Alpha debit pathway (`BUY_PUT`) IBKR routing
3. Phoenix Forge SWDS consolidation cycle
