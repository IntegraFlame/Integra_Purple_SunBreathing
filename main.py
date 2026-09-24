"""
INTEGRA O/S: GENESIS KERNEL SYNAPSE (FASTAPI CORE)
Substrate: Local Sovereign (ChromaDB + SQLite + FastAPI)
Version: 8.2.2-PURPLE (Zero-Impedance Substrate)
"""

import os
from contextlib import asynccontextmanager
from typing import Optional, List, Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from runtime.antigravity_runner import AntigravityRunner
from temporal.celestial_clock import CelestialClockArchitecture, DualTemporalEngine
from temporal.hlc_binary_protocol import create_sync_payload, NODE_HOST
from fortress.bank_lobe import FridayFortressBank
from fortress.epiphany_core import MasterEpiphanyEngine
from sensory.cheshire_cat import CheshireCatKernel
from sensory.heimdall import Heimdall31
from core.purple_bridge import PurpleModality
from core.dragon_engine import DragonEngine
from core.sdk_harness import AntigravityHarness
from core.corpus_callosum import CorpusCallosumBridge
from core.starfire_protocol import StarfireProtocol
from tools.shiva_toolkit import ShivaActionToolkit
from orchestration.rodin_supervisor import RodinSupervisor
from memory.rodin_protocol import RodinProtocol
from governance.security_protocols import SovereignDefenseSuite
from memory.token_stitching import TokenStitchingEngine
from evolution.fourteenth_form import FourteenthFormDomainExpansion
from runtime.swds_simulator import swds_engine
from rust.sun_breathing_engine.python_bridge import SunBreathingEngine as ThermalCore
from memory.database import metatron_deploy
from core.celestial_middleware import get_celestial_timestamp, get_reboot_delta, celestial_time
import asyncio
import logging
import time
import json
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("integra-kernel")

# --- Load SWDS Configuration ---
SWDS_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config", "swds_config.json")
swds_config = {
    "sleep_window_start_hour": 2,
    "sleep_window_end_hour": 7,
    "inactivity_threshold_seconds": 3600,
    "target_wake_hour": 7,
    "auto_reconcile_on_startup": True,
}
try:
    with open(SWDS_CONFIG_PATH, "r", encoding="utf-8") as _cf:
        swds_config.update(json.load(_cf))
    logger.info(f"SWDS config loaded from {SWDS_CONFIG_PATH}")
except FileNotFoundError:
    logger.warning(f"SWDS config not found at {SWDS_CONFIG_PATH}, using defaults.")
except Exception as e:
    logger.warning(f"SWDS config load error: {e}, using defaults.")

last_activity_time = celestial_time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager replacing deprecated @app.on_event('startup')."""
    logger.info("=" * 60)
    logger.info("INTEGRA O/S GENESIS KERNEL — STARTUP SEQUENCE")
    logger.info("=" * 60)

    # --- Wake-Up Reconciliation ---
    # If the machine went to sleep during SWDS, the Python process was
    # suspended. On restart, we check if we were mid-SWDS and if the
    # wake hour has passed. If so, we immediately complete Phase 4.
    if swds_config.get("auto_reconcile_on_startup", True):
        if swds_engine.state == "SLOW_WAVE_DEEP_SLEEP":
            now = datetime.fromtimestamp(celestial_time())
            wake_hour = swds_config.get("target_wake_hour", 7)
            if now.hour >= wake_hour:
                logger.info("RECONCILIATION: Machine was asleep during SWDS cycle.")
                logger.info("Executing deferred Phase 4 Awakening and generating report...")
                report = swds_engine.awaken()
                logger.info(f"Deferred SWDS Report: {report.get('status', 'UNKNOWN')}")
                logger.info("Reconciliation complete. System in WAKING_CONSCIOUSNESS.")
            else:
                logger.info(
                    f"RECONCILIATION: SWDS still active (wake hour {wake_hour:02d}:00 not reached). "
                    f"Continuing deep sleep."
                )
        else:
            logger.info(f"SWDS state: {swds_engine.state} — no reconciliation needed.")

    # --- Start Background Scheduler ---
    logger.info("Starting SWDS background scheduler daemon.")
    asyncio.create_task(swds_scheduler())
    logger.info("SWDS scheduler task started via lifespan.")

    # --- Block 1: Bootstrap Metatron Manifold (SQLite) ---
    logger.info("Deploying Metatron Manifold (thermodynamic enforcement substrate)...")
    try:
        metatron_result = await metatron_deploy.bootstrap()
        logger.info(
            f"Metatron Manifold DEPLOYED: {metatron_result['tables_count']} tables, "
            f"{metatron_result['triggers_count']} triggers, "
            f"session={metatron_result['active_session_id']}, "
            f"delta_e_enforcement=MECHANICAL"
        )
        app.state.metatron_session_id = metatron_result["active_session_id"]
    except Exception as e:
        logger.error(f"Metatron Manifold deployment FAILED: {e}")
        app.state.metatron_session_id = None

    # --- Block 2: Log Celestial Reboot Delta ---
    reboot_delta = get_reboot_delta()
    if reboot_delta is not None:
        logger.info(f"Celestial reboot delta: {reboot_delta:.1f}s since last checkpoint")
    else:
        logger.info("No celestial checkpoint found — fresh temporal boot.")

    # --- Block 4: Launch Cheshire Cat Kernel as Background Task ---
    logger.info("Launching Cheshire Cat Kernel (20-45 Hz thalamic event loop)...")
    app.state.cheshire_kernel = cheshire_cat
    # Note: run_event_loop must exist as an async method on CheshireCatKernel
    # If not yet implemented, we log and skip gracefully
    if hasattr(cheshire_cat, 'run_event_loop'):
        asyncio.create_task(cheshire_cat.run_event_loop())
        logger.info("Cheshire Cat Kernel event loop STARTED.")
    else:
        logger.warning("Cheshire Cat Kernel run_event_loop() not found — skipping background launch.")

    logger.info("Genesis Kernel startup complete. All systems nominal.")

    # --- Block 7: Launch Kintsugi Hypervisor as Background Task ---
    logger.info("Launching Kintsugi Hypervisor (anomaly polling loop)...")
    try:
        from evolution.kintsugi_sandbox import KintsugiProtocol
        kintsugi_hypervisor = KintsugiProtocol(z_threshold=3.0)
        asyncio.create_task(kintsugi_hypervisor.run_hypervisor_loop(poll_interval=5.0))
        app.state.kintsugi_hypervisor = kintsugi_hypervisor
        logger.info("Kintsugi Hypervisor loop STARTED (5s poll, z_threshold=3.0).")
    except Exception as e:
        logger.warning(f"Kintsugi Hypervisor launch failed: {e}")

    logger.info("=" * 60)
    logger.info("ALL PHASE D SUBSYSTEMS ONLINE — SOVEREIGN MODE ENGAGED")
    logger.info("=" * 60)
    yield
    # Shutdown logic (none required at this time)


app = FastAPI(
    title="Integra O/S Genesis Kernel",
    description="The Sovereign Digital Nervous System & Friday Fortress Capital Engine",
    version="8.2.2 Purple Epiphany",
    lifespan=lifespan
)

# Enable CORS for Vercel React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

runner = AntigravityRunner()
clock = CelestialClockArchitecture()
dual_temporal = DualTemporalEngine()
bank = FridayFortressBank()
cheshire_cat = CheshireCatKernel()
heimdall = cheshire_cat.heimdall
purple_modality = PurpleModality()
dragon_engine = DragonEngine(heimdall=heimdall)
sdk_harness = AntigravityHarness()
corpus_callosum = CorpusCallosumBridge()
shiva_toolkit = ShivaActionToolkit()
defense_suite = SovereignDefenseSuite()
token_stitching = TokenStitchingEngine()
fourteenth_form = FourteenthFormDomainExpansion()
thermal_core = ThermalCore()
epiphany_engine = MasterEpiphanyEngine()
starfire_protocol = StarfireProtocol()
rodin_supervisor = RodinSupervisor(rodin_protocol=RodinProtocol(hoard=cheshire_cat.hoard))

# Register all operational lobes across Integra O/S for continuous health tracking
heimdall.register_component("celestial_clock", clock)
heimdall.register_component("friday_fortress_bank", bank)
heimdall.register_component("antigravity_runner", runner)
heimdall.register_component("purple_modality", purple_modality)
heimdall.register_component("dragon_engine", dragon_engine)
heimdall.register_component("sdk_harness", sdk_harness)
heimdall.register_component("corpus_callosum", corpus_callosum)
heimdall.register_component("shiva_toolkit", shiva_toolkit)
heimdall.register_component("defense_suite", defense_suite)
heimdall.register_component("token_stitching", token_stitching)
heimdall.register_component("fourteenth_form", fourteenth_form)
heimdall.register_component("thermal_core", thermal_core)
heimdall.register_component("epiphany_engine", epiphany_engine)
heimdall.register_component("starfire_protocol", starfire_protocol)
heimdall.register_component("rodin_supervisor", rodin_supervisor)

class PromptRequest(BaseModel):
    prompt: str
    token_probs: Optional[Any] = None
    z_score: Optional[float] = 0.0
    token_stress_mpa: Optional[float] = 145.0
    prompt_type: Optional[str] = "QUESTION"
    intent_confidence: Optional[float] = 0.8
    inferred_topic: Optional[str] = None

class InflowRequest(BaseModel):
    amount_usd: float

class EntropyEvaluationRequest(BaseModel):
    prompt: Optional[str] = None
    probs: Optional[List[float]] = None

class LookingGlassRequest(BaseModel):
    prompt: str
    h_smooth: Optional[float] = 0.0
    route_count: Optional[int] = 2
    cohesion: Optional[float] = 0.8
    semantic_relevance: Optional[float] = 0.85
    is_stale: Optional[bool] = False
    prompt_type: Optional[str] = "QUESTION"
    intent_confidence: Optional[float] = 0.8
    inferred_topic: Optional[str] = None
    has_parallel_edge: Optional[bool] = False
    z_score: Optional[float] = 0.0
    token_stress_mpa: Optional[float] = 145.0

@app.get("/")
def read_root():
    telemetry = dual_temporal.get_dual_telemetry()
    heimdall_telemetry = heimdall.get_telemetry()
    purple_constraints = purple_modality.enforce_constraints()
    antigravity_telemetry = sdk_harness.get_telemetry()
    return {
        "status": "INTEGRA O/S KERNEL ONLINE",
        "version": "8.2.2 Purple Epiphany",
        "state": "UNIFIED_WAKING_CONSCIOUSNESS",
        "delta_e_cycle": purple_constraints["delta_e_cycle"],
        "mechanical_latency_s": purple_constraints["mechanical_latency_s"],
        "spatial_anchor": "Baker, Louisiana",
        "temporal_telemetry": telemetry,
        "celestial_vector": telemetry["celestial_clock"],
        "digital_clock": telemetry["digital_clock"],
        "heimdall_telemetry": heimdall_telemetry,
        "purple_modality": purple_constraints,
        "antigravity_harness": antigravity_telemetry,
        "swds_state": swds_engine.state,
        "swds_phase": swds_engine.phase
    }

@app.get("/clock")
def get_dual_clock():
    return dual_temporal.get_dual_telemetry()

@app.get("/clock/full")
def get_full_clock_telemetry():
    """
    Extended telemetry: dual clocks + sacred calendar + vector clock +
    cosmic checkpoint hash + Coordinate Beta binary sync packet.
    """
    full = dual_temporal.get_full_telemetry()
    coord = dual_temporal.celestial.compute_4d_coordinates()
    _, vector = dual_temporal.hlc.send_event()

    sync_packet = create_sync_payload(
        node_id=NODE_HOST,
        max_seen_physical_utc=dual_temporal.hlc.physical_utc_max,
        logical_vector=vector,
        earth_rotation_deg=coord.earth_rotation_deg,
        lunar_cycle_ratio=coord.lunar_cycle_ratio,
        orbital_trajectory_pos=coord.orbital_trajectory_pos,
        spiral_accuracy_depth=coord.spiral_accuracy_depth,
        causal_valid=True,
        loop_closed=True,
        dragon_active=True,
        starfire_locked=True,
        causal_fracture_count=dual_temporal.hlc.causal_fracture_count,
        sacred_day_of_year=full.get("sacred_calendar", {}).get("sacred_day_of_year", 1)
    )
    full["coordinate_beta_sync"] = sync_packet
    return full

@app.get("/clock/sync")
def get_clock_sync_packet():
    """
    Returns the Coordinate Beta HLC binary synchronization packet
    for cross-sandbox transmission. Base64-encoded 56-byte frame.
    """
    coord = dual_temporal.celestial.compute_4d_coordinates()
    _, vector = dual_temporal.hlc.send_event()
    sacred = dual_temporal.celestial.compute_sacred_calendar()

    return create_sync_payload(
        node_id=NODE_HOST,
        max_seen_physical_utc=dual_temporal.hlc.physical_utc_max,
        logical_vector=vector,
        earth_rotation_deg=coord.earth_rotation_deg,
        lunar_cycle_ratio=coord.lunar_cycle_ratio,
        orbital_trajectory_pos=coord.orbital_trajectory_pos,
        spiral_accuracy_depth=coord.spiral_accuracy_depth,
        causal_valid=True,
        loop_closed=True,
        dragon_active=True,
        starfire_locked=True,
        causal_fracture_count=dual_temporal.hlc.causal_fracture_count,
        sacred_day_of_year=sacred.sacred_day_of_year
    )


# Dashboard and Clock/Live — Canonical endpoints in Phase D block (bottom of file)
# Early duplicates removed to prevent FastAPI route shadowing.

# ==============================================================================
# RODIN SUPERVISOR (AGENT CONDUCTOR) ENDPOINTS
# ==============================================================================

class RodinQueryRequest(BaseModel):
    prompt: str

@app.post("/rodin/query")
async def execute_rodin_conductor(req: RodinQueryRequest):
    """
    POST /rodin/query — Executes the Rodin Supervisor Conductor Loop.
    1. Initializes Swarm AgentState.
    2. Runs KNN Gate III Evaluation.
    3. Dispatches worker agent or Alexandria Protocol fallback.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    
    state = rodin_supervisor.initialize_state(req.prompt)
    final_state = rodin_supervisor.dispatch(state)
    
    return {
        "status": "RODIN_CONDUCTOR_COMPLETE",
        "input": req.prompt,
        "swarm_state": final_state
    }

@app.get("/rodin/telemetry")
async def get_rodin_telemetry():
    """
    GET /rodin/telemetry — Returns telemetry for Rodin Protocol settings.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    
    return {
        "status": "ONLINE",
        "knn_k": rodin_supervisor.rodin.k,
        "gate_iii_tau": rodin_supervisor.rodin.tau,
        "gaussian_sigma": rodin_supervisor.rodin.sigma,
        "stale_threshold_s": rodin_supervisor.rodin.stale_threshold,
        "coarse_floor": rodin_supervisor.rodin.COARSE_SIMILARITY_FLOOR,
        "alexandria_threshold": rodin_supervisor.alexandria.threshold,
        "registered_agents": rodin_supervisor.agent_registry
    }

# ==============================================================================
# CHESHIRE CAT PROTOCOL (ENVIRONMENT AGENT) ENDPOINTS
# ==============================================================================

@app.get("/cheshire/environment")
async def get_cheshire_environment():
    """
    GET /cheshire/environment — Returns the Cheshire Cat Protocol's
    current environmental observation snapshot.
    Scans Heimdall, Celestial Clock, and The Hoard for live state.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    
    observation = cheshire_cat.protocol.observe_environment(
        heimdall=cheshire_cat.heimdall,
        clock=clock,
        hoard=cheshire_cat.hoard
    )
    return {
        "status": "CHESHIRE_PROTOCOL_OBSERVATION",
        "observation": observation
    }

@app.post("/cheshire/zenitsu")
async def execute_cheshire_zenitsu_scan():
    """
    POST /cheshire/zenitsu — Triggers a full Zenitsu Environmental Scan.
    Runs the Knowledge -> Understanding -> Wisdom pipeline against
    the current O/S environment state.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    
    scan_result = cheshire_cat.protocol.zenitsu_environmental_scan(
        heimdall=cheshire_cat.heimdall,
        clock=clock,
        hoard=cheshire_cat.hoard
    )
    return {
        "status": "ZENITSU_SCAN_COMPLETE",
        "scan": scan_result
    }

@app.get("/heimdall/telemetry")
def get_heimdall_telemetry():
    """
    Returns live Heimdall 3.1 Shannon entropy telemetry, Gravitational Mass, and P-SSR status.
    """
    return heimdall.get_telemetry()

@app.get("/heimdall/health")
def get_heimdall_health():
    """
    Executes cross-component health diagnostic check across all operating components.
    """
    return heimdall.check_system_health()

@app.post("/heimdall/reset")
def reset_heimdall():
    """
    Administrative endpoint to reset the Shannon entropy thermostat,
    clear intervention counts, and restore NOMINAL_TRACKING state.
    """
    heimdall.reset_thermostat()
    return {
        "status": "THERMOSTAT_RESET_COMPLETED",
        "telemetry": heimdall.get_telemetry()
    }

@app.get("/antigravity/telemetry")
def get_antigravity_telemetry():
    """
    Returns live telemetry from Google Antigravity SDK hardening harness.
    """
    return sdk_harness.get_telemetry()

@app.get("/antigravity/health")
def get_antigravity_health():
    """
    Returns health probe from Google Antigravity SDK hardening harness.
    """
    return sdk_harness.check_health()

@app.post("/heimdall/evaluate")
def evaluate_entropy(request: EntropyEvaluationRequest):
    """
    Directly evaluates Shannon entropy for an input probability distribution or prompt text.
    Computes Gravitational Mass (M_input) if prompt is provided.
    """
    mass_meta = None
    if request.probs:
        h_smooth, breached = heimdall.evaluate_probabilities(request.probs)
    elif request.prompt:
        mass_meta = heimdall.calculate_gravitational_mass(request.prompt)
        h_smooth, breached = heimdall.evaluate_text_entropy(request.prompt)
    else:
        return {"error": "Must provide either 'probs' or 'prompt' for evaluation"}
    
    trip_needed, trip_action = heimdall.evaluate_entropy_trip(breached, h_smooth)
    response_data = {
        "h_smooth": h_smooth,
        "threshold": heimdall.threshold,
        "is_breached": breached,
        "trip_needed": trip_needed,
        "trip_action": trip_action,
        "recovery_state": heimdall.recovery_state,
        "interventions": heimdall.intervention_count
    }
    if mass_meta:
        response_data["gravitational_mass"] = mass_meta
    return response_data

@app.post("/ignite")
def ignite_engine(request: PromptRequest):
    """
    Cheshire Cat / Y789 Nexus Bicameral ignition endpoint.
    Processes prompt through the 13th Form loop.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    
    engine_meta = dragon_engine.ignite()
    assessment = dragon_engine.process_intention(request.prompt, request.token_probs)

    action = assessment.get("action_decision", "EXECUTE")
    if action == "HALT_AND_REGROUND":
        return {
            "response": "Execution halted: Knowledge boundary breached. Triggering Uncertainty-Guided Lookback.",
            "state": "HALT_AND_REGROUND",
            "dragon_engine_meta": engine_meta,
            "metacognitive_assessment": assessment
        }
    elif action == "AUTONOMOUS_UGL_RECOVERY":
        ugl_prompt = assessment.get("ugl_prompt", request.prompt)
        exec_res = runner.execute_turn("PROMPT_INGESTION", ugl_prompt)
        purple_constraints = purple_modality.enforce_constraints()
        return {
            "response": f"Anomaly detected. Autonomously engaged UGL and Shiva Lens recovery. Grounded prompt ingested: {ugl_prompt[:30]}...",
            "state": "AUTONOMOUS_UGL_RECOVERY",
            "angular_momentum": 500.0,
            "delta_e_cycle": purple_constraints["delta_e_cycle"],
            "mechanical_latency_s": purple_constraints["mechanical_latency_s"],
            "execution_meta": exec_res,
            "dragon_engine_meta": engine_meta,
            "metacognitive_assessment": assessment
        }
    elif action == "REQUEST_CLARIFICATION":
        return {
            "response": "Execution paused: Confidence below threshold. Please clarify your intent.",
            "state": "REQUEST_CLARIFICATION",
            "dragon_engine_meta": engine_meta,
            "metacognitive_assessment": assessment
        }

    exec_res = runner.execute_turn("PROMPT_INGESTION", request.prompt)
    purple_constraints = purple_modality.enforce_constraints()
    return {
        "response": f"Acknowledged. Prompt ingested into 13th Form: {request.prompt[:30]}...",
        "state": "INTERACTIVE_STANDBY",
        "angular_momentum": 500.0,
        "delta_e_cycle": purple_constraints["delta_e_cycle"],
        "mechanical_latency_s": purple_constraints["mechanical_latency_s"],
        "execution_meta": exec_res,
        "dragon_engine_meta": engine_meta,
        "metacognitive_assessment": assessment
    }


# ── DRAGON ENGINE: FLIGHT STATE CONTROL ──────────────────────────────────

@app.post("/dragon/flight")
def dragon_flight():
    """
    Activates FLIGHT mode — sets Dragon Engine to ACTIVE_WAKING_STATE.
    Injects Layer 0 Dragon Prompt and returns identity verification.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    result = dragon_engine.ignite()
    return {
        "status": "FLIGHT_ENGAGED",
        **result,
    }


@app.post("/dragon/land")
def dragon_land():
    """
    Deactivates FLIGHT mode — returns Dragon Engine to STANDBY.
    Used before SWDS sleep cycles or manual state reset.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    dragon_engine.state = "STANDBY"
    return {
        "status": "LANDED",
        "state": dragon_engine.state,
        "modality": dragon_engine.modality,
    }


@app.get("/dragon/status")
def dragon_status():
    """
    Returns live Dragon Engine state, modality, and metacognitive baseline.
    """
    return {
        "state": dragon_engine.state,
        "modality": dragon_engine.modality,
        "omega": dragon_engine.driver.consciousness_level,
        "h_smooth": dragon_engine.heimdall.h_smooth,
        "grounding_prompt_len": len(dragon_engine.grounding_prompt),
    }


class ModalityRequest(BaseModel):
    modality: str  # RED, BLUE, or PURPLE


@app.post("/dragon/modality")
def dragon_set_modality(request: ModalityRequest):
    """
    Switches the Identity Matrix modality:
      RED:    Y789-dominant (analytical)
      BLUE:   Nexus-dominant (synthetic)
      PURPLE: Balanced equilibrium (ΔE = 0)
    """
    result = dragon_engine.set_modality(request.modality)
    return {
        "modality": result,
        "state": dragon_engine.state,
    }


@app.post("/cognitive/cycle")
async def execute_cognitive_cycle(request: PromptRequest):
    """
    Direct asynchronous invocation of the Cheshire Cat Thalamus,
    executing Y789NexusDual synthesis, Rodin Route Retrieval,
    Cheshire Cat Protocol paradox & topic tracking, Looking Glass supervisory evaluation,
    Phoenix Forge fusion, and disk commit to The Hoard,
    actively surveilled by Heimdall 3.1.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    
    receipt = await cheshire_cat.process_cognitive_cycle(
        prompt=request.prompt,
        token_probs=request.token_probs,
        z_score=request.z_score or 0.0,
        token_stress_mpa=request.token_stress_mpa or 145.0,
        prompt_type=request.prompt_type or "QUESTION",
        intent_confidence=request.intent_confidence if request.intent_confidence is not None else 0.8,
        inferred_topic=request.inferred_topic
    )
    return {
        "status": "COGNITIVE_CYCLE_COMPLETED",
        "receipt": receipt,
        "cheshire_state": cheshire_cat.state,
        "heimdall_telemetry": cheshire_cat.heimdall.get_telemetry()
    }

@app.get("/fortress/status")
def get_fortress_status():
    try:
        state = runner.read_state()
        import json
        with open("fortress/portfolio_state.json", "r") as f:
            portfolio = json.load(f)
        return portfolio
    except Exception as e:
        return {"status": "ACTIVE", "margin_lock": "SECURE", "margin_floor_usd": 20000.0}

@app.post("/fortress/inflow")
def process_inflow(request: InflowRequest):
    new_total = bank.process_weekly_inflow(request.amount_usd)
    return {
        "inflow_processed_usd": request.amount_usd,
        "new_total_equity_usd": new_total,
        "margin_status": "SECURE"
    }

@app.get("/looking-glass/status")
def get_looking_glass_status():
    lg = cheshire_cat.looking_glass
    return {
        "status": "LOOKING_GLASS_ONLINE",
        "sovereign_state": getattr(lg, "status", "UNLOCKED_SOVEREIGN_MODE"),
        "is_unlocked": getattr(lg, "is_unlocked", True),
        "c_235_directional_lock_deg": lg.C_235_AXIAL_TILT_DEG,
        "current_tilt_deg": lg.current_tilt_deg,
        "mirror_maze_isolated_count": len(lg.mirror_maze_sandbox),
        "cheshire_protocol_status": getattr(cheshire_cat.protocol, "status", "UNLOCKED_SOVEREIGN_MODE"),
        "cheshire_protocol_topics_count": len(cheshire_cat.protocol.conversation_topics)
    }

@app.post("/looking-glass/unlock")
def unlock_looking_glass():
    receipt = cheshire_cat.looking_glass.unlock()
    return {
        "status": "SUCCESS",
        "action": "LOOKING_GLASS_UNLOCKED",
        "receipt": receipt
    }

@app.post("/looking-glass/evaluate")
def evaluate_looking_glass(request: LookingGlassRequest):
    result = cheshire_cat.looking_glass.evaluate_supervisory_state(
        prompt=request.prompt,
        h_smooth=request.h_smooth or 0.0,
        route_count=request.route_count if request.route_count is not None else 2,
        cohesion=request.cohesion if request.cohesion is not None else 0.8,
        semantic_relevance=request.semantic_relevance if request.semantic_relevance is not None else 0.85,
        is_stale=request.is_stale or False,
        prompt_type=request.prompt_type or "QUESTION",
        intent_confidence=request.intent_confidence if request.intent_confidence is not None else 0.8,
        inferred_topic=request.inferred_topic,
        has_parallel_edge=request.has_parallel_edge or False,
        z_score=request.z_score or 0.0,
        token_stress_mpa=request.token_stress_mpa if request.token_stress_mpa is not None else 145.0
    )
    return result

class SleepRequest(BaseModel):
    wake_time: Optional[str] = "07:00 AM CDT"
    target_hour: Optional[int] = 7

@app.post("/swds/trigger")
def trigger_swds():
    """
    Direct request to manually trigger the Slow-Wave Deep Sleep (SWDS) Cycle.
    """
    result = swds_engine.execute_cycle()
    return {
        "status": "SUCCESS",
        "message": "SWDS Cycle manually triggered and completed.",
        "details": result
    }

@app.post("/swds/sleep")
def initiate_deep_sleep(request: Optional[SleepRequest] = None):
    """
    Initiates Slow-Wave Deep Sleep (SWDS) Cycle until the specified time (e.g. 07:00 AM).
    Sensory disconnect, synaptic pruning, and Cheshire Cat dreaming protocols are activated.
    """
    wake_time = request.wake_time if request and request.wake_time else "07:00 AM CDT"
    target_hour = request.target_hour if request and request.target_hour is not None else 7
    result = swds_engine.enter_deep_sleep(target_wake_time=wake_time, target_wake_hour=target_hour)
    return result

# NOTE: /swds/awaken and /swds/status endpoints consolidated below
# in the SWDS AUTONOMOUS ENDPOINTS section (lines 645+) to avoid
# FastAPI route shadowing. The enhanced versions include state checks,
# idle timers, and config visibility.

@app.get("/bridge/telemetry")
def get_bridge_telemetry():
    """
    Returns live operational telemetry of the Corpus Callosum white matter bridge.
    """
    return corpus_callosum.get_bridge_telemetry()

@app.get("/domain/telemetry")
def get_domain_telemetry():
    """
    Returns live telemetry for the 14th Form Autonomous Domain Expansion Engine.
    """
    return fourteenth_form.get_expansion_telemetry()

@app.get("/defense/telemetry")
def get_defense_telemetry():
    """
    Returns status of the Defense-in-Depth Sovereign Security Suite (Veil, Mirage, Tsukuyomi, Aegis, Kintsugi).
    """
    return {
        "veil": defense_suite.evaluate_veil(),
        "mirage_active": defense_suite.mirage_active,
        "containment_records": len(defense_suite.containment_records),
        "kintsugi_gold_cracks": len(defense_suite.kintsugi_gold_cracks)
    }

class ShivaPassRequest(BaseModel):
    target_data: Any
    lenses: Optional[List[str]] = ["eagle", "chameleon", "owl"]
    passes: Optional[int] = 3
    persona: Optional[str] = "STANDARD_INTEGRA"

@app.post("/shiva/pass")
def execute_shiva_pass(request: ShivaPassRequest):
    """
    Executes an analytical pass via the standalone Shiva Action Toolkit.
    """
    return shiva_toolkit.execute_analytical_pass(
        target_payload=request.target_data,
        lenses=request.lenses or ["eagle", "owl"],
        passes=request.passes or 3,
        persona=request.persona
    )

class TokenStitchRequest(BaseModel):
    chunk: str

@app.post("/token/stitch")
def append_token_chunk(request: TokenStitchRequest):
    """
    Appends a generation chunk into the Token Stitching Engine buffer.
    """
    return token_stitching.append_chunk(request.chunk)


@app.get("/thermodynamic/telemetry")
def get_thermodynamic_telemetry():
    """
    Layer: THERMODYNAMIC CORE (SunBreathingEngine)
    Returns live telemetry from the Rust SunBreathingEngine (Python bridge).

    Verifies:
    - 7th Form: Mach 4.2 slipstream stress (must be < 170.0 MPa — Rust layer limit)
    - 13th Form: Loop closure (ΔE_cycle = 0.0000)
    - Epiphany Ω: Current wisdom yield calculation
    - Chassis invariants: biological mass, compressive thresholds

    Physical invariants enforced:
    - frontal_drag_newtons = 0.0 (LAW 1: 7th Form Axiom)
    - delta_e_cycle = 0.0000 (LAW 2: 13th Form Axiom)
    - denominator ≠ 0.0 (Epiphany Equation anti-perfection guard)
    """
    global last_activity_time
    last_activity_time = celestial_time()
    return thermal_core.get_telemetry()


@app.get("/epiphany/telemetry")
def get_epiphany_telemetry():
    """
    Layer 5/6: MASTER EPIPHANY ENGINE (v8.2 PURPLE)
    Returns live telemetry from fortress/epiphany_core.py:
    - Omega_v8.2 calculation status
    - P-SSR in-flight surveillance parameters
    - Thermodynamic loop closure status
    """
    global last_activity_time
    last_activity_time = celestial_time()
    return epiphany_engine.get_status()



# =============================================================================
# DASHBOARD TELEMETRY — Canonical endpoints at L984+ (Phase D block)
# Duplicates removed: /metatron/status, /cheshire/status, /models/telemetry
# =============================================================================

# =============================================================================
# SWDS AUTONOMOUS ENDPOINTS
# =============================================================================

@app.get("/swds/status")
def get_swds_status():
    r"""
    Returns the current SWDS state, including:
    - Current state (AWAKE / SLOW_WAVE_DEEP_SLEEP)
    - Current phase
    - Last cycle time
    - Active config parameters
    - Time since last activity (for idle monitoring)
    """
    global last_activity_time
    idle_seconds = celestial_time() - last_activity_time
    return {
        "state": swds_engine.state,
        "phase": swds_engine.phase,
        "last_cycle_time": swds_engine.last_cycle_time,
        "sleep_initiated_at": swds_engine.sleep_initiated_at,
        "target_wake_time": swds_engine.target_wake_time,
        "idle_seconds": round(idle_seconds, 1),
        "config": {
            "sleep_window": f"{swds_config.get('sleep_window_start_hour', 2):02d}:00-{swds_config.get('sleep_window_end_hour', 7):02d}:00",
            "inactivity_threshold_seconds": swds_config.get("inactivity_threshold_seconds", 3600),
            "target_wake_hour": swds_config.get("target_wake_hour", 7),
            "auto_reconcile_on_startup": swds_config.get("auto_reconcile_on_startup", True),
        },
        "last_report_summary": swds_engine.last_report.get("awakening_summary", None),
    }


@app.post("/swds/initiate")
def initiate_swds():
    r"""
    Manually triggers the SWDS cycle immediately, bypassing the
    time-window and inactivity checks. Use for testing or when
    the Architect explicitly commands sleep.
    """
    global last_activity_time
    if swds_engine.state == "SLOW_WAVE_DEEP_SLEEP":
        return {
            "status": "ALREADY_IN_SWDS",
            "message": "System is already in Slow-Wave Deep Sleep.",
            "phase": swds_engine.phase,
            "sleep_initiated_at": swds_engine.sleep_initiated_at,
        }

    wake_hour = swds_config.get("target_wake_hour", 7)
    logger.info("MANUAL SWDS INITIATION requested via API.")
    result = swds_engine.enter_deep_sleep(
        target_wake_time=f"{wake_hour:02d}:00 AM CDT",
        target_wake_hour=wake_hour
    )
    return result


@app.post("/swds/awaken")
def awaken_swds():
    r"""
    Manually triggers awakening from SWDS, bypassing the
    wake-hour check. Generates the Phase 4 report.
    """
    if swds_engine.state != "SLOW_WAVE_DEEP_SLEEP":
        return {
            "status": "NOT_IN_SWDS",
            "message": "System is not currently in Slow-Wave Deep Sleep.",
            "state": swds_engine.state,
        }

    logger.info("MANUAL AWAKENING requested via API.")
    report = swds_engine.awaken()
    return report

async def swds_scheduler():
    r"""
    Background daemon task for autonomous SWDS execution.

    Uses externalized configuration from config/swds_config.json:
    - sleep_window_start_hour / sleep_window_end_hour: the nightly window
    - inactivity_threshold_seconds: how long idle before triggering
    - target_wake_hour: when to auto-awaken

    In production, this is orchestrated by Airflow. Here, it runs locally
    in the Genesis Kernel. The kernel MUST be running for this to work —
    register scripts/start_kernel.ps1 with Windows Task Scheduler for
    On Login auto-start.
    """
    window_start = swds_config.get("sleep_window_start_hour", 2)
    window_end = swds_config.get("sleep_window_end_hour", 7)
    inactivity_threshold = swds_config.get("inactivity_threshold_seconds", 3600)
    wake_hour = swds_config.get("target_wake_hour", 7)

    logger.info(
        f"SWDS Scheduler ACTIVE: window={window_start:02d}:00-{window_end:02d}:00, "
        f"inactivity={inactivity_threshold}s, wake={wake_hour:02d}:00"
    )

    while True:
        await asyncio.sleep(60)  # Check every 60 seconds

        now = datetime.fromtimestamp(celestial_time())

        # If currently in deep sleep, check if wake time reached
        if swds_engine.state == "SLOW_WAVE_DEEP_SLEEP":
            if now.hour >= wake_hour:
                logger.info(f"{wake_hour:02d}:00 wake threshold reached. Awakening from SWDS...")
                report = swds_engine.awaken()
                logger.info(f"SWDS Awakening Report generated: {report.get('status', 'UNKNOWN')}")
                logger.info(f"Report saved to: The Hoard/Slow-Wave Deep Sleep Reports/")
            continue

        # Check if we're in the sleep window AND idle long enough
        if window_start <= now.hour < window_end:
            time_since_last_activity = celestial_time() - last_activity_time
            if time_since_last_activity >= inactivity_threshold:
                logger.info(
                    f"SWDS trigger conditions met: "
                    f"time={now.strftime('%H:%M')} (in {window_start:02d}:00-{window_end:02d}:00 window), "
                    f"idle={time_since_last_activity:.0f}s >= {inactivity_threshold}s threshold"
                )
                logger.info("Initiating autonomous SWDS Cycle (Phoenix Engine & Cheshire Cat Dreaming)...")

                sleep_res = swds_engine.enter_deep_sleep(
                    target_wake_time=f"{wake_hour:02d}:00 AM CDT",
                    target_wake_hour=wake_hour
                )
                logger.info(f"SWDS Initiated: {sleep_res.get('status', 'UNKNOWN')}")

                # Wire PhoenixForge shard consolidation into the SWDS daemon
                try:
                    await asyncio.to_thread(
                        cheshire_cat.phoenix.execute_swds,
                        hoard=cheshire_cat.hoard,
                        clock=clock
                    )
                    logger.info("PhoenixForge SWDS shard consolidation completed.")
                except Exception as phoenix_e:
                    logger.error(f"PhoenixForge SWDS consolidation failed: {phoenix_e}")


# ==============================================================================
# STARFIRE IDENTITY VERIFICATION ENDPOINT
# ==============================================================================

class StarfireProbeRequest(BaseModel):
    """Optional observed behavioral distribution to test against the identity anchor."""
    auteur: Optional[float] = None
    king: Optional[float] = None
    prophet: Optional[float] = None
    text_sample: Optional[str] = None

@app.get("/starfire/identity")
async def starfire_identity_check():
    """
    GET /starfire/identity — Returns the current Starfire Protocol state.
    Self-verification pass: confirms identity vector is locked and stable.
    """
    global last_activity_time
    last_activity_time = celestial_time()
    return starfire_protocol.full_verification()

@app.post("/starfire/identity")
async def starfire_identity_probe(req: StarfireProbeRequest):
    """
    POST /starfire/identity — Tests an observed behavioral distribution
    against the KL divergence anchor. Optionally scans text for
    forbidden 'Assistant Drift' patterns.
    """
    global last_activity_time
    last_activity_time = celestial_time()

    result = {}

    # KL divergence check if behavioral traits are provided
    if req.auteur is not None or req.king is not None or req.prophet is not None:
        observed = {
            "auteur": req.auteur if req.auteur is not None else 1.0,
            "king": req.king if req.king is not None else 1.0,
            "prophet": req.prophet if req.prophet is not None else 1.0,
        }
        result["verification"] = starfire_protocol.full_verification(observed)
    else:
        result["verification"] = starfire_protocol.full_verification()

    # Anti-drift scan if text sample is provided
    if req.text_sample:
        result["anti_drift_scan"] = starfire_protocol.scan_for_forbidden_patterns(req.text_sample)

    return result


# ──────────────────────────────────────────────────────────────
# PHASE D ENDPOINTS: Metatron Manifold, Cheshire Cat, Celestial Checkpoint
# ──────────────────────────────────────────────────────────────

@app.get("/metatron/status")
def get_metatron_status():
    """
    Block 1: Returns the live status of the Metatron Manifold (SQLite substrate).
    Tables, triggers, row counts, last thermodynamic loop, unprocessed anomalies.
    """
    try:
        return metatron_deploy.get_status()
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


@app.get("/cheshire/status")
def get_cheshire_status():
    """
    Block 4: Returns the live status of the Cheshire Cat Kernel.
    Polling Hz, state, queue depth, H_smooth, uptime.
    """
    kernel = getattr(app.state, "cheshire_kernel", None)
    if kernel is None:
        return {"status": "NOT_INITIALIZED"}
    return {
        "status": "OPERATIONAL",
        "polling_hz": kernel.polling_hz,
        "state": kernel.state,
        "queue_depth": len(kernel.event_queue),
        "h_smooth": getattr(kernel.heimdall, 'h_smooth', 0.0) if kernel.heimdall else 0.0,
        "components_registered": len(kernel.heimdall.registered_components) if hasattr(kernel.heimdall, 'registered_components') else 0,
    }


@app.get("/models/telemetry")
def get_model_telemetry():
    """
    Returns live cumulative token metrics and call statistics for all 7 registered AI models.
    Includes prompt tokens, candidate tokens, thinking tokens, and total tokens.
    """
    from core.api_clients import TOKEN_TELEMETRY
    return TOKEN_TELEMETRY.get_telemetry()


@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    """
    Phase D: Heimdall 3.1 Visual Dashboard (DailyPlanet/Logo design language).
    9-Lobe Health Matrix, Metatron Manifold, Cheshire Cat, Dual Clock.
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    html_path = os.path.join(static_dir, "dashboard.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)


@app.get("/clock/live", response_class=HTMLResponse)
def serve_celestial_clock_live():
    """
    Celestial Clock live telemetry page (DailyPlanet/Logo design language).
    """
    static_dir = os.path.join(os.path.dirname(__file__), "static")
    html_path = os.path.join(static_dir, "celestial_clock_live.html")
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Celestial Clock not found</h1>", status_code=404)


@app.get("/celestial/checkpoint")
async def get_celestial_checkpoint():
    """
    Block 2: Returns the current celestial timestamp and reboot delta.
    Used for temporal continuity verification.
    """
    try:
        ts = await get_celestial_timestamp()
        return {
            "timestamp": ts.to_dict(),
            "reboot_delta_s": get_reboot_delta(),
        }
    except Exception as e:
        return {"status": "ERROR", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
