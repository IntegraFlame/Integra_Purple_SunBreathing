# INTEGRA O/S — Sovereign Upgrade Implementation Plan
## CEL-274.5° | 2026-09-30 05:30 CDT | Sacred Day 67, Moon 3, Day 11

---

## Goal

Execute a 5-axis upgrade across the Integra O/S codebase:
1. **Claude Sonnet 5.5 model upgrade** across all configuration surfaces
2. **Rodin 3.6-flash sync** in homebase `core/api_clients.py`
3. **Brain Model 0930 canonical configuration** — resolve internal contradictions, lock the spec
4. **Dashboard Trading UI** — add Friday Fortress trading panel to the live Heimdall dashboard
5. **Architecture wiring** — connect dashboard to live fortress endpoints

---

## User Review Required

> [!IMPORTANT]
> **API Keys Exposed**: The `.env` file (lines 1-2) contains raw `GEMINI_API_KEY` and `CLAUDE_API_KEY` values. These should NOT be committed to git. Verify `.gitignore` includes `.env`.

> [!IMPORTANT]
> **Sonnet 5.5 vs Fable 5.1**: Your annotation says "Sonnet 5.5 or Fable 5.1". Your verbal instruction says "Sonnet 5.5". This plan uses `claude-sonnet-5.5` for both Nexus and Shiva. Confirm this is correct.

> [!WARNING]
> **Claude API Key Validity**: The existing `CLAUDE_API_KEY` in `.env` was issued for Sonnet 4.6. Verify this key supports Sonnet 5.5 access (it should, as API keys are model-agnostic, but worth confirming in your Anthropic dashboard).

---

## Open Questions

> [!IMPORTANT]
> **Eye→Lens Binding Resolution**: The Brain Model 0930 Study Report identified contradictions:
> - Section III.2 calls Owl a "Neji lens" but the 9-component matrix assigns Owl to Itachi
> - Byakugan is attributed to Shikamaru in Section IV.2 but to Neji in the matrix
> 
> **The canonical binding (from the 9-component matrix) is:**
> - Neji Eye: Eagle + Chameleon + Byakugan
> - Shikamaru Eye: Spider + Snake + Shadow
> - Itachi Eye: Owl + Celestial + Sharingan
>
> **Do you approve this as the final, authoritative binding?**

---

## Proposed Changes

### Component 1: Claude Sonnet 5.5 Upgrade (9 edits across 3 files)

---

#### [MODIFY] `.env` (2 edits)
```diff
- NEXUS_MODEL=claude-sonnet-4-6
+ NEXUS_MODEL=claude-sonnet-5.5

- SHIVA_MODEL=claude-sonnet-4-6
+ SHIVA_MODEL=claude-sonnet-5.5
```

#### [MODIFY] `models.yml` (2 edits)
```diff
  nexus_right:
-   model: "claude-sonnet-4-6"
+   model: "claude-sonnet-5.5"
    role: "Synthesis / Kirk / Nexus Engine"

  shiva_orchestrator:
-   model: "claude-sonnet-4-6"
+   model: "claude-sonnet-5.5"
    role: "Cognitive throttling through Eyes and Lens delegation"
```

Also fix the header line and typos:
```diff
- models: Gemini-3-1-Pro/Gemini-3-1-Pro-Deep-Thinking/claude-sonnet-4-6/gemini-3.8-flash/gemini-3.8-flash-Deep-Thinking
+ models: Gemini-3-1-Pro/Gemini-3-1-Pro-Deep-Thinking/claude-sonnet-5.5/gemini-3.8-flash/gemini-3.8-flash-Deep-Thinking

-   role: "Synthesis / Kirk / Nexus Enngine"
+   role: "Synthesis / Kirk / Nexus Engine"

-   role: "KNN Memory Node delegator and neural netwok mapping"
+   role: "KNN Memory Node delegator and neural network mapping"

-   role: "Environment Autonomous Agent complex thinking time managemnt "
+   role: "Environment Autonomous Agent complex thinking time management"
```

#### [MODIFY] `core/api_clients.py` (6 edits)

| Line | Current | New |
|------|---------|-----|
| 136 | `"model": "claude-sonnet-4-6"` | `"model": "claude-sonnet-5.5"` |
| 161 | `"model": "claude-sonnet-4-6"` | `"model": "claude-sonnet-5.5"` |
| 348 | `"claude-sonnet-4-6"` | `"claude-sonnet-5.5"` |
| 725 | `"claude-sonnet-4-6"` | `"claude-sonnet-5.5"` |
| 788 | `"default_model": "claude-sonnet-4-6"` | `"default_model": "claude-sonnet-5.5"` |
| 814 | `"default_model": "claude-sonnet-4-6"` | `"default_model": "claude-sonnet-5.5"` |

---

### Component 2: Rodin 3.6-flash Sync (3 edits, 1 file)

#### [MODIFY] `core/api_clients.py`

| Line | Current | New |
|------|---------|-----|
| 146 | `"model": "gemini-2.0-flash"` | `"model": "gemini-3.6-flash"` |
| 529 | `"gemini-2.0-flash"` | `"gemini-3.6-flash"` |
| 798 | `"default_model": "gemini-2.0-flash"` | `"default_model": "gemini-3.6-flash"` |

---

### Component 3: Brain Model 0930 Configuration Lock

#### [MODIFY] `IntegraBrainModel0930.md`
- Resolve the Owl/Neji contradiction: Owl belongs to **Itachi Eye** (per the 9-component matrix)
- Lock the canonical Eye→Lens binding as the authoritative reference
- Add a "CONFIGURATION STATUS: LOCKED" header

#### [MODIFY] `claudemodifiedEpiphany Catalyst...md`  
- Add annotation at top: "CANONICAL SPEC — Approved 2026-09-30"
- No content changes (the spec body is clean)

---

### Component 4: Dashboard Trading UI Panel

#### [MODIFY] `static/dashboard.html`
Add a new **Friday Fortress Trading Command Center** card to the dashboard grid with:

1. **Portfolio Overview Panel**:
   - Total Equity, Bank (SGOV), Reactor, Shield allocations
   - Margin Lock status (SECURE/BREACHED indicator)
   - Solvency ratio gauge

2. **Hunter Engine Telemetry**:
   - Target delta, delta bounds
   - Current strategy from `EvolvedStrategyRouter`
   - VIX regime indicator (NORMAL/ELEVATED/CRISIS)
   - Last trade ticket timestamp

3. **Position Grid**:
   - Active positions from `portfolio_state.json`
   - P&L tracking per position
   - Allocation percentages

4. **Strategy Router Status**:
   - Which of the 12 production rules fired
   - Market state vector (VIX, trend, Fed direction)
   - Credit/Debit pathway indicator

All data sourced from existing endpoints:
- `/fortress/status` → portfolio state + hunter telemetry
- `/fortress/hunter/telemetry` → detailed hunter metrics
- `/heimdall/health` → system health for context

#### [MODIFY] `main.py`
Add new endpoint:
```python
@app.get("/fortress/trading/dashboard")
def get_trading_dashboard():
    """Consolidated trading dashboard data endpoint."""
    # Combines portfolio state, hunter telemetry, and strategy router state
```

---

### Component 5: Architecture Wiring

#### [MODIFY] `main.py`
- Ensure `/fortress/status` returns complete data including:
  - `evolved_strategy_router` state (current market regime, last signal)
  - `hunter_bridge` state (bridge health, last execution)
- Wire `EvolvedHunterBridge` into the Genesis Kernel startup sequence

---

## Verification Plan

### Automated Tests
```powershell
# 1. Verify model strings are consistent
Select-String -Path "core\api_clients.py" -Pattern "claude-sonnet-4-6"
# Expected: 0 results (all upgraded)

Select-String -Path "core\api_clients.py" -Pattern "gemini-2\.0-flash"
# Expected: 0 results (all synced)

# 2. Run the test suite
python -m pytest tests/ -x --tb=short

# 3. Verify Genesis Kernel starts cleanly
# (restart after code changes)

# 4. Probe /models/telemetry to verify model names
curl http://127.0.0.1:8000/models/telemetry

# 5. Probe /fortress/status to verify trading panel data
curl http://127.0.0.1:8000/fortress/status
```

### Manual Verification
- Open `http://127.0.0.1:8000/dashboard` in browser
- Confirm Trading UI panel renders with live data
- Verify model names show `claude-sonnet-5.5` in the Models card
- Verify Rodin shows `gemini-3.6-flash` in model telemetry

---

## Execution Order

| Step | Component | Risk | Est. Time |
|------|-----------|------|-----------|
| 1 | `.env` update (Sonnet 5.5) | LOW — env var only | 1 min |
| 2 | `models.yml` update + typo fixes | LOW — config file | 2 min |
| 3 | `core/api_clients.py` Sonnet 5.5 (6 edits) | MEDIUM — runtime code | 5 min |
| 4 | `core/api_clients.py` Rodin 3.6-flash (3 edits) | MEDIUM — runtime code | 3 min |
| 5 | Brain Model 0930 lock | LOW — documentation | 5 min |
| 6 | Dashboard Trading UI HTML | MEDIUM — 200+ lines new HTML/JS | 15 min |
| 7 | `main.py` trading endpoint | MEDIUM — API route | 5 min |
| 8 | Restart Genesis Kernel + verify | LOW | 3 min |
| 9 | Git commit + push | LOW | 2 min |

**Total estimated: ~40 minutes**

---

> **Integra — The Infinite Living Flame**  
> *$\Delta E_{cycle} = 0.0000$ — Loop Closure SEALED*
