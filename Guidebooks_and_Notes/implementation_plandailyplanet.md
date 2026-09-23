# Integra O/S Implementation Plan: Daily Planet Protocol, OmegaMetric & Neurobiological Upgrades

## Background & Context

The previous implementation plan (**Rogue X Protocol 2.0 & SQL Trigger Repair**) has been **100% completed, verified, and passes all 116 tests with zero regressions**. 

Following our exhaustive multi-pass forensic audits of [`Geminiconversationdata.md`](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/Guidebooks_and_Notes/Geminiconversationdata.md), [`Integra Forensic Investigation Worker.md`](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/Guidebooks_and_Notes/Integra%20Forensic%20Investigation%20Worker.md), and [`INTEGRA_OS_EXHAUSTIVE_MASTER_V9.md`](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/The%20Hoard/INTEGRA_OS_EXHAUSTIVE_MASTER_V9.md), all 5 prior architectural fixes (P1–P5) are active in code. The 11-file `env_loader.py` mapping is formalized as canonical.

We now transition to the **next operational phase**:
1. **Daily Planet Protocol (`tools/daily_planet.py`):** Lossless multi-modal external intelligence engine aligned with the Firecrawl API.
2. **OmegaMetric ($\Omega$) & CircuitBreaker:** Mathematical thermodynamic boundary enforcement ($\Omega = (\text{Agency}/\text{Entropy}) \times \text{celestial\_scalar}$) wired into Heimdall 3.1 and Dragon Engine.
3. **GAP-1 & GAP-2 Resolution:** Upgrading 14th Form MRL Respiration from mock hashing to true Matryoshka embeddings, and upgrading Corpus Callosum to true Asymmetric Predictive Coding (descending priors vs. ascending errors).
4. **V9 Missing Protocols (Tier 1-3, Mad Hatter, Rebuttal):** Full schema mapping and behavioral implementation for omitted Master V9 cognitive structures.

---

## Proposed Changes

### Phase 1: Daily Planet Protocol & Firecrawl Engine

#### [NEW] [daily_planet.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/tools/daily_planet.py)
Build the sovereign intelligence engine implementing the 6-stage lifecycle:
- **Pydantic Data Models:** `SourceProvenance`, `ContradictionVector`, `MetacognitiveBinding`, `DailyPlanetReport`.
- **`DailyPlanetProtocol` Core:**
  - Ingestion via Firecrawl REST (`POST /v2/search`, `POST /v2/scrape`, `GET /v2/search/research/papers`).
  - Analysis via Shiva Action Suite: Neji Eye (Chameleon Lens) for provenance; Shikamaru Eye (Spider + Snake) for contradiction mapping; Itachi Eye (Owl + Eagle, CRA=1.20) for synthesis.
  - Persistence: Commits output directly as a schemed `HoardNode` v2.0 with coarse 64d and fine 768d embeddings.

#### [MODIFY] Subsystem Wiring
- **alexandria_protocol.py:** Wire `execute_loop_2_learning()` to dispatch `DailyPlanetProtocol.execute_daily_planet_brief()`.
- **shiva_toolkit.py:** Connect the `"daily_planet"` CRA catalog entry.
- **rogue_x.py:** Connect `target_type="live_data"` directly to ingest `DailyPlanetReport` payloads.

---

### Phase 2: OmegaMetric ($\Omega$) & CircuitBreaker

#### [MODIFY] [heimdall.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/sensory/heimdall.py)
- Implement `calculate_omega_metric()`: $\Omega = \left(\frac{\text{Agency}}{\text{Entropy} + \epsilon}\right) \times \text{celestial\_scalar}$
- Implement the **4-Step Emergency CircuitBreaker**: Throttle $\to$ Veto $\to$ Isolate $\to$ UGL_Reset.

#### [MODIFY] [dragon_engine.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/core/dragon_engine.py)
- Wire `Heimdall31.circuit_breaker` into `process_intention()` to trigger hard cognitive halts if $\Omega < \Omega_{\text{floor}}$.

---

### Phase 3: Neurobiological Bridge Upgrades (GAP-1 & GAP-2)

#### [MODIFY] [phoenix_forge.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/evolution/phoenix_forge.py)
- Replace mock `hashlib.sha256` in `_generate_placeholder_embedding` with true Matryoshka sub-vector alignment.

#### [MODIFY] [corpus_callosum.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/core/corpus_callosum.py)
- Upgrade from static bidirectional passing to **Asymmetric Predictive Coding** (Descending feedback vs. Ascending feedforward).

---

### Phase 4: Missing V9 Protocols Integration

Based on the newly generated **Mapping Manifesto**, the following architectural gaps will be closed:

#### [MODIFY] [tpsl_types.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/core/tpsl_types.py)
- Migrate current `@dataclass` definitions to strictly validated `pydantic.BaseModel` implementations for database and ChromaDB serialization.
- Implement the three missing V9 schemas: `ResearchTierRoute`, `MadHatterMutationEvent`, and `RebuttalStressTest`.

#### [MODIFY] [cwa_router.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/core/cwa_router.py)
- **Fix Tier Routing:** `evaluate_task` currently only implements Tier 1 and Tier 3. TIER_2 (Standard Report) logic will be explicitly implemented, utilizing the new `ResearchTierRoute` schema to govern token allocations and API execution paths.

#### [MODIFY] [phoenix_forge.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/evolution/phoenix_forge.py) & [rogue_x.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/evolution/rogue_x.py)
- **Mad Hatter Autonomous Bridge:** The V9 document dictates Mad Hatter runs autonomously on "Orphaned Insight Nodes". Currently, `rogue_x.py` runs it synchronously. We will build an asynchronous bridge allowing the `phoenix_forge.py` SWDS daemon to pull orphaned vectors from ChromaDB and feed them into `rogue_x.py` using the `MadHatterMutationEvent` schema.

#### [MODIFY] [shiva_toolkit.py](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/tools/shiva_toolkit.py)
- **Rebuttal Protocol Execution:** Implement the missing executable logic for the rebuttal protocol. This requires piping `target_hypothesis` outputs from the `Y789NexusEngine` into a new generation call using Shiva's "Hawk Lens" to isolate logical fault lines (`adversarial_vectors`), followed by an M4 Generative Fusion call to produce the `zenkai_boost_output`.

---

## Verification Plan

### Automated Tests
1. **Daily Planet Tests:** (`tests/test_daily_planet_lifecycle.py`)
2. **OmegaMetric & CircuitBreaker Tests:** (`tests/test_omega_circuit_breaker.py`)
3. **Missing Protocols Tests:**
   Create [`tests/test_v9_protocols.py`](file:///c:/Users/Javon%20Jenkins/OneDrive/Desktop/Integra_Purple_SunBreathing/integra-homebase/tests/test_v9_protocols.py):
   - Verify `cwa_router.py` correctly routes all 3 tiers (Tier 1, Tier 2, Tier 3).
   - Verify Mad Hatter SWDS bridge correctly triggers on orphaned vectors.
   - Verify Rebuttal Protocol produces valid `RebuttalStressTest` structures.
4. **Full Regression Suite:**
   Run all 116+ core tests to ensure 0 regressions.
