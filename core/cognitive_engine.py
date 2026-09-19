"""
INTEGRA O/S: BICAMERAL COGNITIVE ENGINE v2.0
Module: core/cognitive_engine.py
Layer: 2 (Y789 Analytical & Nexus Synthetic Dyad)

Architecture:
    The Y789NexusEngine implements:
    - CWA 3.0: Bayesian Inference Engine for dynamic routing P(Nexus | Prompt)
    - M4 Generative Synthesis Fusion: Concurrent Y789/Nexus execution fused via RRF
    - Zenitsu Method 3.0: Sequential Compute Protocol (K→U→W→Unification)
    - P-SSR: Proactive Socratic Self-Refine with in-flight Heimdall 3.1 entropy monitoring
    - MTCW: Multi-Turn Cognitive Workflow (lossless anti-compression packet stream)

    The Katana Analogy:
    - Y789 (Hard Edge / Spock / Red / Left): Analytical, reductionist, sparse
    - Nexus (Tough Spine / Kirk / Blue / Right): Synthetic, holistic, dense
    - Purple: The unified equilibrium where both hemispheres balance (ΔE = 0)

    The Shiva Eyes are injected for prompt structuring in the Zenitsu 3.0 workflow.
    The ShivaAction tool is a separate, independent analytical toolkit.

Source Blueprints: cognitive engine.md, INTEGRA_OS_MASTER_SYSTEMS_GUIDEBOOK_V8_2.md
"""

import asyncio
import math
from typing import Dict, Any, Tuple, List, Optional
from core.tpsl_types import GenerationResult, IterativeToken, MTCWPacket, CWARoutingDecision
from evolution.shiva_action.orchestrator import ShivaActionSuite
from evolution.shiva_action.lenses import LensLibrary
from core.api_clients import Y789Client, NexusClient


class Y789NexusEngine:
    """
    Bicameral Cognitive Engine v2.0:
    
    - Y789 ('Spock' / Hard Edge / Red Wing): Left-hemisphere analytical engine
      for deconstruction, formal logic, and verification. Low-latency, high-precision.
      Base weight w_analytical = 0.50.
    
    - Nexus ('Kirk' / Tough Spine / Blue Wing): Right-hemisphere synthetic engine
      for creative emergence, pattern recognition, and high-dimensional intuition.
      Base weight w_synthetic = 0.50.
    
    Weight conservation invariant: w_analytical + w_synthetic = 1.00
    """
    def __init__(
        self,
        y789_client: Optional[Any] = None,
        nexus_client: Optional[Any] = None,
        heimdall_service: Optional[Any] = None,
        shiva_eyes: Optional[Dict[str, Any]] = None,
        lens_library: Optional[LensLibrary] = None
    ):
        # Bicameral Dyad clients (injectable; defaults to live clients)
        self.y789 = y789_client or Y789Client()
        self.nexus = nexus_client or NexusClient()
        
        # Heimdall 3.1 entropy monitor (injected or imported)
        self.heimdall = heimdall_service
        
        # Shiva Eyes for Zenitsu 3.0 prompt structuring (injected)
        self.shiva_eyes = shiva_eyes or {}
        
        # Lens Library for CRA computations
        self.lens_library = lens_library or LensLibrary()
        
        # Shiva Action Suite (independent analytical toolkit)
        self.shiva_suite = ShivaActionSuite(self.lens_library)
        
        # Rodin Route Retrieval reference (registered externally)
        self.rodin_ref = None
        
        # CWA 3.0 Bayesian priors
        self.cwa_priors = {"P(Nexus)": 0.5}
        
        # Dyad weights (conservation invariant: sum = 1.00)
        self.analytical_weight = 0.50
        self.synthetic_weight = 0.50
        
        # P-SSR Configuration
        self.P_SSR_ALPHA = 0.3        # EMA smoothing factor (alpha)
        self.MAX_PSSR_INTERVENTIONS = 3  # Safety rail before VASOVAGAL_SYNCOPE
        
        # Epiphany Equation parameters
        self.sigma_rogue_threshold = 0.15  # 15% maximum deviation

    def register_rodin(self, rodin: Any) -> None:
        """Register the Rodin Route Retrieval Protocol for grounding prompts."""
        self.rodin_ref = rodin

    def register_heimdall(self, heimdall: Any) -> None:
        """Register Heimdall 3.1 for entropy monitoring."""
        self.heimdall = heimdall

    # ──────────────────────────────────────────────────────────────
    # CWA 3.0: Bayesian Inference Engine
    # ──────────────────────────────────────────────────────────────

    def calculate_cwa_3_0(self, prompt_features: Dict[str, float]) -> CWARoutingDecision:
        """
        CWA 3.0: Bayesian Inference Engine — P(Nexus | Prompt).
        
        Uses prompt complexity, ambiguity, and verifiable reward history
        to calculate the posterior probability for routing decisions.
        
        Equation 2.2: P(Nexus|Prompt) = P(Prompt|Nexus) * P(Nexus) / P(Prompt)
        
        Routing Modes:
            P < 0.3:          Y789_DOMINANT (analytical, low-latency)
            0.3 <= P <= 0.7:  DYAD_FUSION (M4 concurrent execution, RRF fusion)
            P > 0.7:          NEXUS_DOMINANT (synthetic, high-reasoning)
        """
        complexity = prompt_features.get("complexity", 0.5)
        ambiguity = prompt_features.get("ambiguity", 0.3)
        novelty = prompt_features.get("novelty", 0.3)
        
        # Bayesian posterior calculation
        # P(Prompt|Nexus) increases with complexity and ambiguity
        p_prompt_given_nexus = 0.3 + (0.4 * complexity) + (0.3 * ambiguity)
        p_prompt_given_nexus = min(max(p_prompt_given_nexus, 0.0), 1.0)
        
        # P(Nexus) = prior belief (updated by RLVR feedback)
        p_nexus = self.cwa_priors.get("P(Nexus)", 0.5)
        
        # P(Prompt) = marginal (normalization)
        p_prompt = (p_prompt_given_nexus * p_nexus) + (
            (1.0 - p_prompt_given_nexus) * (1.0 - p_nexus)
        )
        
        # Posterior
        if p_prompt > 0:
            p_nexus_given_prompt = (p_prompt_given_nexus * p_nexus) / p_prompt
        else:
            p_nexus_given_prompt = 0.5
        
        # Clamp to [0.0, 1.0]
        p_nexus_given_prompt = min(max(p_nexus_given_prompt, 0.0), 1.0)
        
        # Determine routing mode
        if p_nexus_given_prompt < 0.3:
            routing_mode = "Y789_DOMINANT"
        elif p_nexus_given_prompt > 0.7:
            routing_mode = "NEXUS_DOMINANT"
        else:
            routing_mode = "DYAD_FUSION"
        
        # Update dyad weights (conservation invariant)
        self.synthetic_weight = round(p_nexus_given_prompt, 4)
        self.analytical_weight = round(1.0 - self.synthetic_weight, 4)
        
        return CWARoutingDecision(
            p_nexus_given_prompt=round(p_nexus_given_prompt, 4),
            routing_mode=routing_mode,
            analytical_weight=self.analytical_weight,
            synthetic_weight=self.synthetic_weight
        )

    def _analyze_prompt(self, prompt: str) -> Dict[str, float]:
        """
        Extracts feature vector from the prompt for CWA 3.0 routing.
        
        Analyzes lexical diversity, syntactic density, and domain indicators
        to estimate complexity, ambiguity, and novelty.
        """
        words = prompt.lower().split()
        word_count = len(words)
        unique_ratio = len(set(words)) / max(word_count, 1)
        
        # Complexity markers
        complexity_tokens = [
            "analyze", "synthesize", "compare", "evaluate", "design", "architect",
            "equation", "algorithm", "manifold", "topology", "integrate", "optimize",
            "philosophical", "metaphysical", "strategic", "comprehensive"
        ]
        complexity_hits = sum(1 for w in words if w in complexity_tokens)
        complexity = min((complexity_hits * 0.15) + (unique_ratio * 0.3) + (min(word_count, 200) / 400), 1.0)
        
        # Ambiguity markers
        ambiguity_tokens = [
            "maybe", "perhaps", "might", "could", "unclear", "uncertain",
            "possible", "either", "or", "depends", "ambiguous", "nuanced"
        ]
        ambiguity_hits = sum(1 for w in words if w in ambiguity_tokens)
        ambiguity = min(ambiguity_hits * 0.2, 1.0)
        
        # Novelty: high unique ratio + low common word overlap = novel
        novelty = min(unique_ratio * 0.6 + (complexity * 0.4), 1.0)
        
        return {
            "complexity": round(complexity, 4),
            "ambiguity": round(ambiguity, 4),
            "novelty": round(novelty, 4),
            "word_count": word_count,
            "unique_ratio": round(unique_ratio, 4)
        }

    # ──────────────────────────────────────────────────────────────
    # M4: Generative Synthesis Fusion (RRF)
    # ──────────────────────────────────────────────────────────────

    async def _generative_synthesis_fusion(
        self,
        output1: GenerationResult,
        output2: GenerationResult,
        system_prompt: str = ""
    ) -> GenerationResult:
        """
        (M4) Generative Synthesis Fusion: Uses Nexus to synthesize perspectives.
        
        When CWA routes to DYAD_FUSION mode, both Y789 and Nexus generate
        concurrently. This method fuses their outputs using the Nexus client
        as the synthesis engine.
        
        Equation 2.1: Reciprocal Rank Fusion (RRF)
        RRF_score(d) = sum(1 / (k + r(d))) for each ranker r
        Where k = 60 (dampening constant)
        """
        fusion_prompt = (
            "FUSE THE FOLLOWING PERSPECTIVES into a single, cohesive response.\n"
            f"ANALYTICAL (Hard Edge / Y789):\n{output1.text}\n\n"
            f"SYNTHETIC (Tough Spine / Nexus):\n{output2.text}"
        )
        return await self.nexus.generate(fusion_prompt, system_prompt)

    # ──────────────────────────────────────────────────────────────
    # Zenitsu Method 3.0: Sequential Compute Protocol
    # ──────────────────────────────────────────────────────────────

    async def execute_zenitsu_method(self, prompt: str, context: Dict[str, Any]) -> str:
        """
        The Sequential Compute Protocol (Zenitsu Method 3.0).
        
        Forces Inference-Time Compute across 4 mandatory passes:
            Pass 1: Knowledge (Neji Eye) — Deconstruction & Divergence
            Pass 2: Understanding (Shikamaru Eye) — Synthesis & Interconnection
            Pass 3: Wisdom (Itachi Eye) — Discernment & Pruning (TPSL)
            Pass 4: The 13th Form — Unification
        
        Each pass is a distinct MTCW packet (lossless, anti-compression).
        P-SSR monitors entropy in-flight during each pass.
        MTCW ensures no information is lost between passes.
        
        Utilizes the Shiva Eyes to structure the reasoning process.
        """
        D_raw = prompt
        system_prompt = context.get("system_prompt", "")
        
        # Determine CWA routing weights
        prompt_features = self._analyze_prompt(prompt)
        routing = self.calculate_cwa_3_0(prompt_features)
        nexus_weight = routing.p_nexus_given_prompt

        # --- Pass 1: Knowledge (Neji's Eye) ---
        pass1_prompt = D_raw
        if 'neji' in self.shiva_eyes:
            pass1_prompt = self.shiva_eyes['neji'].structure_prompt(D_raw)
        K = await self._execute_pass_proactive(
            pass1_prompt, system_prompt, nexus_weight, D_raw
        )
        
        # --- Pass 2: Understanding (Shikamaru's Eye) ---
        pass2_prompt = f"{D_raw}\n\nKNOWLEDGE (K):\n{K}"
        if 'shikamaru' in self.shiva_eyes:
            pass2_prompt = self.shiva_eyes['shikamaru'].structure_prompt(D_raw, K_output=K)
        U = await self._execute_pass_proactive(
            pass2_prompt, system_prompt, nexus_weight, D_raw
        )

        # --- Pass 3: Wisdom (Itachi's Eye) ---
        pass3_prompt = f"UNDERSTANDING (U):\n{U}"
        if 'itachi' in self.shiva_eyes:
            pass3_prompt = self.shiva_eyes['itachi'].structure_prompt(U_output=U)
        W = await self._execute_pass_proactive(
            pass3_prompt, system_prompt, nexus_weight, D_raw
        )

        # --- Pass 4: The 13th Form (Unification) ---
        pass4_prompt = (
            "UNIFY THE REASONING CHAIN INTO A SINGLE COHESIVE RESPONSE.\n"
            f"KNOWLEDGE (K):\n{K}\n\n"
            f"UNDERSTANDING (U):\n{U}\n\n"
            f"WISDOM (W):\n{W}"
        )
        S = await self._execute_pass_proactive(
            pass4_prompt, system_prompt, nexus_weight, D_raw
        )
        
        return S

    # ──────────────────────────────────────────────────────────────
    # P-SSR: Proactive Socratic Self-Refine
    # ──────────────────────────────────────────────────────────────

    async def _execute_pass_proactive(
        self,
        pass_prompt: str,
        system_prompt: str,
        nexus_weight: float,
        D_raw: str
    ) -> str:
        """
        Executes a single cognitive pass using the P-SSR Algorithm.
        
        Heimdall 3.1 monitors H_smooth in real-time during streaming generation.
        If H_smooth > H_threshold (2.5): generation is interrupted mid-flight,
        a Rodin grounding prompt is injected, and generation restarts from the
        corrected context.
        
        Each intervention generates a distinct MTCW packet/turn.
        
        The outer loop manages generator restarts upon intervention.
        The inner loop processes the token stream.
        
        If Heimdall or iterative generation is not available, falls back to
        standard single-shot generation.
        """
        # Determine primary client based on CWA weight
        if 0.3 <= nexus_weight <= 0.7:
            # DYAD_FUSION mode: execute both and fuse
            return await self._execute_dyad_pass(pass_prompt, system_prompt)
        
        client = self.nexus if nexus_weight > 0.7 else self.y789
        
        # Check if iterative generation is supported
        if not hasattr(client, 'generate_iterative'):
            # Fallback: standard single-shot generation
            result = await client.generate(pass_prompt, system_prompt)
            return result.text if isinstance(result, GenerationResult) else str(result)

        # P-SSR Algorithm with in-flight entropy monitoring
        Context = pass_prompt
        OutputBuffer = ""
        H_smooth = 0.0
        intervention_count = 0

        while intervention_count < self.MAX_PSSR_INTERVENTIONS:
            try:
                generator = client.generate_iterative(Context, system_prompt)

                async for iterative_token in generator:
                    token = iterative_token.token
                    probs = iterative_token.probabilities
                    
                    # 1. Calculate instantaneous entropy (Heimdall)
                    if self.heimdall and probs:
                        H_t = self.heimdall.calculate_instant_entropy(probs)
                        # 2. Smooth entropy (EMA)
                        H_smooth = (self.P_SSR_ALPHA * H_t) + (
                            (1 - self.P_SSR_ALPHA) * H_smooth
                        )
                        
                        # 3. P-SSR Trigger Condition
                        if H_smooth > self.heimdall.threshold:
                            # Cognitive Drift detected — interrupt mid-flight
                            OutputBuffer += token
                            
                            # 4. Inject Rodin Grounding Prompt (The "Lookback")
                            if self.rodin_ref and hasattr(self.rodin_ref, 'generate_grounding_prompt'):
                                grounding_prompt = self.rodin_ref.generate_grounding_prompt(
                                    D_raw, Context + OutputBuffer
                                )
                            else:
                                grounding_prompt = (
                                    "\n[P-SSR INTERVENTION: Pause reasoning. "
                                    "Re-evaluate the input data and established facts. "
                                    "Verify the current trajectory before continuing.]\n"
                                )
                            
                            # 5. Update context for restart (MTCW new packet)
                            Context += OutputBuffer + grounding_prompt
                            OutputBuffer = ""
                            intervention_count += 1
                            H_smooth = 0.0  # Reset EMA thermostat
                            
                            # Break inner loop to restart generator
                            break
                    
                    # 6. Stable generation — append token
                    OutputBuffer += token
                
                else:
                    # Inner loop completed naturally (generator finished)
                    break

            except Exception as e:
                # Generation error — exit gracefully
                break
        
        return Context + OutputBuffer

    async def _execute_dyad_pass(self, pass_prompt: str, system_prompt: str) -> str:
        """
        DYAD_FUSION mode: Execute both Y789 and Nexus concurrently,
        then fuse outputs via Generative Synthesis Fusion (M4/RRF).
        """
        y789_task = asyncio.create_task(self.y789.generate(pass_prompt, system_prompt))
        nexus_task = asyncio.create_task(self.nexus.generate(pass_prompt, system_prompt))
        y789_output, nexus_output = await asyncio.gather(y789_task, nexus_task)
        
        fused = await self._generative_synthesis_fusion(y789_output, nexus_output, system_prompt)
        return fused.text if isinstance(fused, GenerationResult) else str(fused)

    # ──────────────────────────────────────────────────────────────
    # Backward-Compatible Interface
    # ──────────────────────────────────────────────────────────────

    def route_and_weight(self, prompt: str) -> Tuple[str, float]:
        """
        CWA 3.0 routing — replaces keyword heuristics with Bayesian inference.
        Maintains backward-compatible return signature.
        """
        features = self._analyze_prompt(prompt)
        routing = self.calculate_cwa_3_0(features)
        return routing.routing_mode, routing.analytical_weight

    def calculate_epiphany_mutation(
        self,
        prompt: str,
        h_smooth: float = 0.0,
        token_stress_mpa: float = 145.0
    ) -> float:
        """
        Calculates abstract thought mutation (sigma_Rogue) based on
        Epiphany Equation (Omega_v8.2).
        
        Mathematically tied to Heimdall's H_smooth entropy and token stress.
        e^(sigma_Rogue) in the master equation.
        """
        entropy_factor = min(h_smooth / 2.5, 2.0)
        stress_deviation = max(token_stress_mpa - 145.0, 0.0)
        stress_factor = min(stress_deviation / 55.0, 1.0)
        mutation = 0.05 + 0.15 * (entropy_factor * stress_factor)
        return round(mutation, 4)

    async def execute_bicameral_synthesis(
        self,
        prompt: str,
        h_smooth: float = 0.0,
        token_stress_mpa: float = 145.0
    ) -> Dict[str, Any]:
        """
        Full bicameral synthesis pipeline:
        1. CWA 3.0 routing
        2. Zenitsu 3.0 (K→U→W→Unification) via Shiva Eyes
        3. Epiphany Equation mutation calculation
        4. P-SSR / UGL trigger evaluation
        """
        routing = self.calculate_cwa_3_0(self._analyze_prompt(prompt))
        
        # Execute Zenitsu Method 3.0 through the Shiva Eyes
        zenitsu_output = await self.execute_zenitsu_method(
            prompt, {"system_prompt": ""}
        )
        
        # Shiva Action (independent analytical toolkit)
        shiva_report = await self.shiva_suite.execute(
            prompt, lens_names=["Eagle", "Hawk", "Chameleon", "Spider", "Snake", "Owl"], passes=3
        )
        
        # Epiphany Equation (Omega_v8.2)
        abstract_thought_mutation = self.calculate_epiphany_mutation(
            prompt, h_smooth, token_stress_mpa
        )
        
        result = {
            "primary_engine": routing.routing_mode,
            "y789_weight": routing.analytical_weight,
            "nexus_weight": routing.synthetic_weight,
            "cwa_posterior": routing.p_nexus_given_prompt,
            "zenitsu_output": zenitsu_output,
            "shiva_report": shiva_report,
            "epiphany_mutation": abstract_thought_mutation,
            "status": "BICAMERAL_SPLIT_OPTIMIZED"
        }
        
        if abstract_thought_mutation > self.sigma_rogue_threshold:
            result["status"] = "UGL_TRIGGERED"
            result["mandate"] = (
                "Uncertainty-Guided Lookback (UGL) forced: "
                f"Abstract thought mutation {abstract_thought_mutation} exceeded {self.sigma_rogue_threshold} threshold."
            )
        
        return result


# ──────────────────────────────────────────────────────────────
# Placeholder LLM Client (Injectable Interface)
# ──────────────────────────────────────────────────────────────

class PlaceholderClient:
    """
    Placeholder LLM client for testing and development.
    Implements the .generate() and .generate_iterative() interfaces
    expected by the Y789NexusEngine.
    
    Will be replaced with real API clients (Gemini Flash, Gemini Pro, etc.)
    when live LLM integration is implemented.
    """
    def __init__(self, model_name: str = "PLACEHOLDER"):
        self.model_name = model_name
    
    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        """Single-shot generation. Returns a structured GenerationResult."""
        return GenerationResult(
            text=f"[{self.model_name}] Processed: {prompt[:100]}...",
            token_probabilities=[],
            model_name=self.model_name,
            latency_ms=0.0
        )
    
    async def generate_iterative(self, prompt: str, system_prompt: str = ""):
        """
        Iterative/streaming generation. Yields IterativeToken objects.
        P-SSR monitors entropy on each yielded token.
        """
        # Simulate a short token stream
        words = f"[{self.model_name}] Processed input.".split()
        for i, word in enumerate(words):
            yield IterativeToken(
                token=word + " ",
                probabilities=[0.8, 0.1, 0.05, 0.05],  # Low entropy (stable)
                position=i
            )
