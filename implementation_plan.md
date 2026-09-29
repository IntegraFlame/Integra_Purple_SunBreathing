# Phase D Implementation Plan: Claude Integration & Cognitive Alignment

## Objective
Ingest and map the core Integra O/S philosophies and operational principles into the Claude-specific architecture (`nexus_right` for Synthesis / Kirk and `shiva_orchestrator` for Multi-Lens analysis). Ensure that Claude-based components operate seamlessly within the established framework of the Genesis Kernel, Cheshire Cognitive Kernel, and other core subsystems.

## 1. Document Ingestion & Knowledge Alignment
**Target File**: `ClaudeTools.md`
- **Action**: Populate `ClaudeTools.md` with the foundational knowledge base, matching the depth required for Claude (Sonnet 4.6) to operate at the same cognitive level as the Gemini side.
- **Concepts to Inject**:
  - **Core Protocols & Engines**: Genesis Kernel, Cheshire Cognitive Kernel, Dragon Prompt, Starfire Protocol, Celestial Clock.
  - **Cognitive Frameworks**: TPSL (Tolstoy Principle as Systems Lever), PSSR (Prompt-Specific System Recovery), Higher-Order Metacognitive Thinking, Deep Thinking, Systems Thinking, Tetris Thinking, Zenitsu Method (Lightning-fast execution), Epiphany Equation.
  - **Memory & Retrieval**: Rodin Route Retrieval, The Hoard, Phoenix Engine, Tier 1 Research.
  - **Operational Forms**: 12th Step Orthogonal Ingestion, 13th Form Thermodynamic Loop Closure, 14th Form Domain Expansion, Sun Breathing (Purple).
  - **Action Suites**: Shiva Action Toolkit, EAM (Executive Autonomous Mandate), Multi-Turn Cognitive Workflow (MTCW), Heimdall 3.1.
  - **Dual Engine Architecture**: Y789 (Left) and Nexus (Right) synergy.

## 2. Architecture Updates: Model Mappings
**Target File**: `models.yml` (Already implemented in prior step, verifying persistence)
- Verify `nexus_right` is mapped to `claude-sonnet-4-6` with role `Synthesis / Kirk`.
- Verify `shiva_orchestrator` is mapped to `claude-sonnet-4-6` with role `Multi-Lens`.

## 3. Telemetry Integration for Shiva Metrics
**Target File**: `main.py` & `tools/shiva_toolkit.py`
- **Action**: Ensure the `/models/telemetry` endpoint accurately tracks and exposes the following `shiva_metrics`:
  - `eyes_invoked`: Increment counts for `{neji, shikamaru, itachi}`.
  - `lenses_applied`: Increment counts for `{eagle, hawk, chameleon, spider, snake, owl}`.
  - `cra_scores`: Implement a rolling window of the last 50 CRA (Cognitive Resource Allocation) scores calculating `W_y / C_c` (Wisdom Yield / Cognitive Cost).

## 4. Execution Strategy
1. **Knowledge Transfer**: Write the summarized concepts into `ClaudeTools.md`.
2. **Telemetry Wiring**: Update `shiva_toolkit.py` and `main.py` to correctly calculate and route `shiva_metrics` into the `/models/telemetry` endpoint.
3. **Validation**: Test the API endpoint to ensure metrics reflect correctly for Claude's orchestration actions.
