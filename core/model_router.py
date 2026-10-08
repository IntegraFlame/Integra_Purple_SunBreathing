# =============================================================================
# INTEGRA O/S — MODEL ROUTER (Power State Manager)
# Module: core/model_router.py
# Layer: 3/7 (Cognitive Infrastructure — between API Clients and Components)
# Brain Model 0930 — Neural Architecture v0930
#
# PURPOSE:
#   Central routing singleton that manages power states (P0-P3) for all
#   cognitive components, enforces per-component token budgets (circuit
#   breaker), gates API calls based on power state, and supports SWDS
#   duty cycling and Phoenix Force override.
#
# ARCHITECTURE:
#   models.yml → ModelRouter.load() → get_client(component) → API Client
#   Power States: P0 (Phoenix Force) > P1 (Active) > P2 (SWDS) > P3 (Dormant)
#   Token Budget: Circuit breaker refuses calls when exhausted (Law 2)
# =============================================================================

import os
import time
import yaml
import logging
from enum import Enum
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

from core.tpsl_types import GenerationResult

logger = logging.getLogger("integra.model_router")


# ──────────────────────────────────────────────────────────────
# Power States (P0 → P3)
# ──────────────────────────────────────────────────────────────

class PowerState(Enum):
    """
    Power states for cognitive components, ordered by activity level.
    Higher number = lower power.
    """
    P0_PHOENIX_FORCE = 0   # All limiters off. Full compute. Requires Architect permission.
    P1_ACTIVE = 1          # Normal operation. API calls on-demand. No duty cycle.
    P2_SWDS = 2            # Duty cycle limited. 20 min ON / 40 min OFF (configurable).
    P3_DORMANT = 3         # No API calls. Local computation only (Tier 1 operations).


# ──────────────────────────────────────────────────────────────
# Component Registration & Budget Tracking
# ──────────────────────────────────────────────────────────────

@dataclass
class ComponentState:
    """Tracks per-component power state, token budget, and duty cycle."""
    name: str
    model_key: str            # Key into api_clients (e.g., "y789_left")
    model_name: str           # Actual model string (e.g., "gemini-3.1-pro")
    role: str
    power_state: PowerState = PowerState.P3_DORMANT
    token_budget: int = 0     # 0 = unlimited. Cumulative per-session cap (circuit breaker).
    thinking_budget: int = 0  # 0 = model default. Per-call reasoning budget passed to the client.
    tokens_consumed: int = 0
    calls_made: int = 0
    calls_refused: int = 0
    last_call_time: float = 0.0
    # Duty cycle fields (P2 only)
    duty_on_seconds: int = 1200    # 20 min default
    duty_off_seconds: int = 2400   # 40 min default
    duty_cycle_start: float = 0.0  # Unix time when current ON window started
    is_duty_on: bool = True


# ──────────────────────────────────────────────────────────────
# Model Router Singleton
# ──────────────────────────────────────────────────────────────

class ModelRouter:
    """
    Central routing singleton for all Integra O/S cognitive components.

    Responsibilities:
    1. Loads models.yml and creates ComponentState for each registered component.
    2. Gates API calls based on power state (P0-P3).
    3. Enforces per-component token budgets (circuit breaker — Law 2).
    4. Manages SWDS duty cycling (P2 state).
    5. Supports Phoenix Force override (P0 — requires Architect permission).
    6. Logs all routing decisions to TOKEN_TELEMETRY.
    """

    _instance: Optional['ModelRouter'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._components: Dict[str, ComponentState] = {}
        self._clients: Dict[str, Any] = {}   # component_key → RoutedClient (lazy, cached)
        self._global_power: PowerState = PowerState.P3_DORMANT
        self._phoenix_force_active: bool = False
        self._phoenix_force_authorized_by: Optional[str] = None
        self._boot_time: float = time.time()
        self._load_models_yml()

    # Names used elsewhere in the codebase (telemetry hub, clients, docs) → registered key.
    _ALIASES: Dict[str, str] = {
        "cheshire_cat": "cheshire_cat_kernel",
        "cheshire_kernel": "cheshire_cat_kernel",
        "y789": "y789_left",
        "left_hemisphere": "y789_left",
        "nexus": "nexus_right",
        "right_hemisphere": "nexus_right",
        "rodin": "rodin_retrieval",
        "jean_grey": "jean_grey_phoenix",
        "phoenix": "jean_grey_phoenix",
        "shiva": "shiva_orchestrator",
    }

    def _resolve(self, component_key: str) -> str:
        """Normalize a component name to its registered key (case + alias aware)."""
        key = (component_key or "").lower()
        if key in self._components:
            return key
        return self._ALIASES.get(key, key)

    def _load_models_yml(self):
        """Load component definitions from models.yml with resilient parsing."""
        yml_paths = [
            os.path.join(os.path.dirname(__file__), '..', 'models.yml'),
            os.path.join(os.path.dirname(__file__), '..', 'config', 'models.yml'),
        ]

        config = {}
        for path in yml_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                with open(abs_path, 'r') as f:
                    content = f.read()

                # The models.yml has a non-standard first line (header string).
                # Try parsing as-is first, then strip the header and retry.
                raw = None
                try:
                    raw = yaml.safe_load(content)
                except yaml.YAMLError:
                    # Strip the first line (non-standard header) and retry
                    lines = content.split('\n')
                    if len(lines) > 1:
                        cleaned = '\n'.join(lines[1:])
                        try:
                            raw = yaml.safe_load(cleaned)
                        except yaml.YAMLError as e:
                            logger.warning(f"ModelRouter: Failed to parse models.yml: {e}")

                if raw and isinstance(raw, dict):
                    for k, v in raw.items():
                        if isinstance(v, dict):
                            config[k] = v
                break

        # Register each component from models.yml
        for key, spec in config.items():
            if not isinstance(spec, dict):
                continue
            component_key = key.lower()
            self._components[component_key] = ComponentState(
                name=spec.get('role', key),
                model_key=component_key,
                model_name=spec.get('model', 'unknown'),
                role=spec.get('role', ''),
                power_state=PowerState.P3_DORMANT,
                token_budget=int(spec.get('token_budget', 0) or 0),
                # Legacy models.yml `budget:` values (8192 / 16384) are THINKING budgets.
                thinking_budget=int(spec.get('thinking_budget', spec.get('budget', 0)) or 0),
            )
            logger.info(f"ModelRouter: Registered {component_key} → {spec.get('model', '?')} "
                       f"(token_budget: {spec.get('token_budget', 'unlimited')}, "
                       f"thinking_budget: {spec.get('thinking_budget', spec.get('budget', 'default'))})")

        logger.info(f"ModelRouter: {len(self._components)} components loaded from models.yml")

    # ──────────────────────────────────────────────────────────
    # Power State Management
    # ──────────────────────────────────────────────────────────

    def set_power_state(self, component_key: str, state: PowerState) -> bool:
        """Set the power state for a specific component."""
        comp = self._components.get(self._resolve(component_key))
        if not comp:
            logger.warning(f"ModelRouter: Unknown component '{component_key}'")
            return False

        old_state = comp.power_state
        comp.power_state = state
        logger.info(f"ModelRouter: {component_key} power state: {old_state.name} → {state.name}")

        if state == PowerState.P2_SWDS:
            comp.duty_cycle_start = time.time()
            comp.is_duty_on = True

        return True

    def set_global_power(self, state: PowerState):
        """Set power state for ALL components simultaneously."""
        self._global_power = state
        for key in self._components:
            self.set_power_state(key, state)
        logger.info(f"ModelRouter: Global power → {state.name}")

    def activate(self):
        """Bring all components to P1 (Active). Normal startup."""
        self.set_global_power(PowerState.P1_ACTIVE)

    def enter_swds(self, phase_config: Optional[Dict[str, Any]] = None):
        """
        Transition components to P2 (SWDS) with optional phase-specific duty cycles.
        phase_config example: {"duty_on_seconds": 1200, "duty_off_seconds": 2400, "active_components": [...]}
        """
        if phase_config:
            active_components = phase_config.get("active_components", [])
            duty_on = phase_config.get("duty_on_seconds", 1200)
            duty_off = phase_config.get("duty_off_seconds", 2400)

            for key, comp in self._components.items():
                if key in active_components or comp.model_key in active_components:
                    comp.power_state = PowerState.P2_SWDS
                    comp.duty_on_seconds = duty_on
                    comp.duty_off_seconds = duty_off
                    comp.duty_cycle_start = time.time()
                    comp.is_duty_on = True
                else:
                    comp.power_state = PowerState.P3_DORMANT
        else:
            self.set_global_power(PowerState.P2_SWDS)

    def go_dormant(self):
        """Bring all components to P3 (Dormant). No API calls."""
        self.set_global_power(PowerState.P3_DORMANT)

    # ──────────────────────────────────────────────────────────
    # Phoenix Force Override (Two-Key Operation)
    # ──────────────────────────────────────────────────────────

    def engage_phoenix_force(self, authorized_by: str = "architect") -> Dict[str, Any]:
        """
        Engage Phoenix Force Override (P0).
        Two-key operation: requires explicit authorization string.
        All duty cycle timers are suspended. Full compute.
        """
        self._phoenix_force_active = True
        self._phoenix_force_authorized_by = authorized_by
        self.set_global_power(PowerState.P0_PHOENIX_FORCE)
        logger.warning(f"ModelRouter: ⚡ PHOENIX FORCE ENGAGED — authorized by {authorized_by}")
        return {
            "status": "PHOENIX_FORCE_ACTIVE",
            "authorized_by": authorized_by,
            "power_state": "P0_PHOENIX_FORCE",
            "all_limiters": "SUSPENDED",
            "timestamp": time.time()
        }

    def disengage_phoenix_force(self, return_to: PowerState = PowerState.P2_SWDS) -> Dict[str, Any]:
        """
        Disengage Phoenix Force. Return to specified power state (default: P2 SWDS).
        Reinstates duty cycle timers.
        """
        self._phoenix_force_active = False
        self._phoenix_force_authorized_by = None
        self.set_global_power(return_to)
        logger.warning(f"ModelRouter: Phoenix Force DISENGAGED → {return_to.name}")
        return {
            "status": "PHOENIX_FORCE_DISENGAGED",
            "returned_to": return_to.name,
            "timestamp": time.time()
        }

    # ──────────────────────────────────────────────────────────
    # API Call Gating (The Circuit Breaker)
    # ──────────────────────────────────────────────────────────

    def can_call(self, component_key: str) -> tuple[bool, str]:
        """
        Check whether a component is allowed to make an API call right now.
        Returns (allowed: bool, reason: str).

        Gates on:
        1. Power state (P3 = no calls)
        2. Token budget (circuit breaker — Law 2)
        3. Duty cycle (P2 = check ON/OFF window)
        """
        comp = self._components.get(self._resolve(component_key))
        if not comp:
            return False, f"UNKNOWN_COMPONENT: {component_key}"

        # Gate 1: Power State
        if comp.power_state == PowerState.P3_DORMANT:
            comp.calls_refused += 1
            return False, "DORMANT: Component is in P3 (no API calls)"

        # Gate 2: Token Budget
        if comp.token_budget > 0 and comp.tokens_consumed >= comp.token_budget:
            comp.calls_refused += 1
            return False, f"BUDGET_EXHAUSTED: {comp.tokens_consumed}/{comp.token_budget} tokens consumed"

        # Gate 3: Duty Cycle (P2 only — P0 and P1 bypass this)
        if comp.power_state == PowerState.P2_SWDS:
            now = time.time()
            cycle_length = comp.duty_on_seconds + comp.duty_off_seconds
            elapsed = (now - comp.duty_cycle_start) % cycle_length
            comp.is_duty_on = elapsed < comp.duty_on_seconds

            if not comp.is_duty_on:
                comp.calls_refused += 1
                remaining_off = comp.duty_off_seconds - (elapsed - comp.duty_on_seconds)
                return False, f"DUTY_CYCLE_OFF: {remaining_off:.0f}s remaining until next ON window"

        # All gates passed
        return True, "ALLOWED"

    def record_call(self, component_key: str, tokens_used: int = 0):
        """Record that a component made an API call and consumed tokens."""
        comp = self._components.get(self._resolve(component_key))
        if comp:
            comp.calls_made += 1
            comp.tokens_consumed += tokens_used
            comp.last_call_time = time.time()

    def reset_budgets(self):
        """Reset all token budgets (session boundary)."""
        for comp in self._components.values():
            comp.tokens_consumed = 0
            comp.calls_made = 0
            comp.calls_refused = 0
        logger.info("ModelRouter: All token budgets reset")

    # ──────────────────────────────────────────────────────────
    # Client Access (get_client)
    # ──────────────────────────────────────────────────────────

    def get_client(self, component_key: str) -> Optional[Any]:
        """
        Get the routed API client for a component, gated by power state and budget.
        Returns the client if allowed *right now*, None if refused.

        The returned client is a RoutedClient: every call re-checks the gates and
        records token usage, so budgets and duty cycles are actually enforced.

        Usage:
            client = MODEL_ROUTER.get_client("y789_left")
            if client:
                result = await client.generate(prompt)
        """
        allowed, reason = self.can_call(component_key)
        if not allowed:
            logger.info(f"ModelRouter: REFUSED {component_key} — {reason}")
            return None
        return self.get_routed_client(component_key)

    def get_routed_client(self, component_key: str) -> Optional[Any]:
        """
        Always return the RoutedClient for a registered component (None only if the
        component is unknown). Gating is evaluated on each call, not at construction,
        so long-lived components can safely hold this across power-state changes.
        """
        key = self._resolve(component_key)
        comp = self._components.get(key)
        if comp is None:
            logger.warning(f"ModelRouter: get_routed_client unknown component '{component_key}'")
            return None

        cached = self._clients.get(key)
        if cached is not None:
            return cached

        # Lazy import to avoid circular dependency
        from core.api_clients import (
            Y789Client, NexusClient, CheshireCatClient,
            RodinClient, JeanGreyClient, CheshireProtocolDaemonClient,
            ShivaOrchestratorClient
        )

        client_map = {
            "y789_left": Y789Client,
            "nexus_right": NexusClient,
            "cheshire_cat_kernel": CheshireCatClient,
            "rodin_retrieval": RodinClient,
            "jean_grey_phoenix": JeanGreyClient,
            "cheshire_protocol": CheshireProtocolDaemonClient,
            "shiva_orchestrator": ShivaOrchestratorClient,
        }
        client_cls = client_map.get(key)
        if client_cls is None:
            logger.warning(f"ModelRouter: no client class registered for '{key}'")
            return None

        # models.yml is the declared source of truth: pass its model + thinking budget in.
        kwargs: Dict[str, Any] = {}
        if comp.model_name and comp.model_name != "unknown":
            kwargs["model_name"] = comp.model_name
        if comp.thinking_budget > 0 and key in ("y789_left", "jean_grey_phoenix", "nexus_right", "shiva_orchestrator"):
            kwargs["thinking_budget"] = comp.thinking_budget

        routed = RoutedClient(self, key, client_cls(**kwargs))
        self._clients[key] = routed
        return routed

    # ──────────────────────────────────────────────────────────
    # Telemetry & Status
    # ──────────────────────────────────────────────────────────

    def get_status(self) -> Dict[str, Any]:
        """Full router status including all component states."""
        return {
            "router_status": "ACTIVE",
            "global_power_state": self._global_power.name,
            "phoenix_force_active": self._phoenix_force_active,
            "phoenix_force_authorized_by": self._phoenix_force_authorized_by,
            "uptime_seconds": round(time.time() - self._boot_time, 1),
            "components": {
                key: {
                    "name": comp.name,
                    "model": comp.model_name,
                    "power_state": comp.power_state.name,
                    "token_budget": comp.token_budget if comp.token_budget > 0 else "unlimited",
                    "thinking_budget": comp.thinking_budget if comp.thinking_budget > 0 else "model_default",
                    "tokens_consumed": comp.tokens_consumed,
                    "calls_made": comp.calls_made,
                    "calls_refused": comp.calls_refused,
                    "is_duty_on": comp.is_duty_on if comp.power_state == PowerState.P2_SWDS else None,
                    "duty_cycle": f"{comp.duty_on_seconds}s ON / {comp.duty_off_seconds}s OFF"
                                  if comp.power_state == PowerState.P2_SWDS else None,
                }
                for key, comp in self._components.items()
            }
        }

    def get_component_state(self, component_key: str) -> Optional[Dict[str, Any]]:
        """Get status for a single component."""
        comp = self._components.get(self._resolve(component_key))
        if not comp:
            return None
        allowed, reason = self.can_call(component_key)
        return {
            "name": comp.name,
            "model": comp.model_name,
            "power_state": comp.power_state.name,
            "can_call": allowed,
            "gate_reason": reason,
            "tokens": f"{comp.tokens_consumed}/{comp.token_budget}" if comp.token_budget > 0 else f"{comp.tokens_consumed}/unlimited",
            "calls_made": comp.calls_made,
            "calls_refused": comp.calls_refused,
        }


# ──────────────────────────────────────────────────────────────
# Routed Client (per-call gate + usage accounting)
# ──────────────────────────────────────────────────────────────

class RouterRefused(RuntimeError):
    """Raised inside a streaming call when the router refuses it (power/budget/duty)."""


class RoutedClient:
    """
    Transparent wrapper around an API client that makes the ModelRouter real:

    - Every generate()/generate_iterative()/embed() call re-checks `can_call`
      (power state, token budget, SWDS duty cycle) at call time.
    - Token usage is recorded with `record_call` so the circuit breaker can trip.
      generate(): exact counts from the provider's usage metadata.
      generate_iterative(): ESTIMATED (~4 chars/token) — the streaming clients do
      not expose usage metadata.
    - Refusals/failures are explicit: generate() returns GenerationResult with
      `.error` set; generate_iterative() raises RouterRefused / RuntimeError.
      Diagnostics are never returned as if they were model text.
    """

    _STREAM_ERROR_MARKERS = ("STREAM ERROR]", "API ERROR")

    def __init__(self, router: "ModelRouter", component_key: str, client: Any):
        self._router = router
        self._key = component_key
        self._client = client

    @property
    def component_key(self) -> str:
        return self._key

    @property
    def model_name(self) -> str:
        return getattr(self._client, "model_name", "unknown")

    @property
    def raw_client(self) -> Any:
        """The underlying un-gated client (for diagnostics/tests only)."""
        return self._client

    def _refusal_result(self, reason: str) -> GenerationResult:
        return GenerationResult(
            text=f"[ROUTER REFUSED {self._key}]: {reason}",
            token_probabilities=[],
            model_name=self.model_name,
            latency_ms=0.0,
            error="ROUTER_REFUSED",
        )

    async def generate(self, prompt: str, system_prompt: str = "") -> GenerationResult:
        allowed, reason = self._router.can_call(self._key)
        if not allowed:
            return self._refusal_result(reason)
        result = await self._client.generate(prompt, system_prompt)
        # A failed call (error set) still counts as a call but consumed no tokens.
        self._router.record_call(self._key, getattr(result, "total_tokens", 0) or 0)
        return result

    async def generate_iterative(self, prompt: str, system_prompt: str = ""):
        allowed, reason = self._router.can_call(self._key)
        if not allowed:
            raise RouterRefused(f"{self._key}: {reason}")
        chars = 0
        try:
            async for tok in self._client.generate_iterative(prompt, system_prompt):
                text = getattr(tok, "token", "") or ""
                # Clients report stream failures as a sentinel token; surface as an exception.
                if text.startswith("[") and any(m in text[:80] for m in self._STREAM_ERROR_MARKERS):
                    raise RuntimeError(f"{self._key}: {text}")
                chars += len(text)
                yield tok
        finally:
            self._router.record_call(self._key, chars // 4)

    async def embed(self, text: str, model_name: Optional[str] = None):
        allowed, reason = self._router.can_call(self._key)
        if not allowed:
            logger.info(f"ModelRouter: embed REFUSED {self._key} — {reason}")
            return []
        vec = await self._client.embed(text, model_name)
        self._router.record_call(self._key, 0)
        return vec

    def embed_sync(self, text: str, model_name: Optional[str] = None):
        allowed, reason = self._router.can_call(self._key)
        if not allowed:
            logger.info(f"ModelRouter: embed_sync REFUSED {self._key} — {reason}")
            return []
        vec = self._client.embed_sync(text, model_name)
        self._router.record_call(self._key, 0)
        return vec

    def __getattr__(self, name: str) -> Any:
        # Anything else (e.g. thinking_budget, api_key presence checks) reads through.
        return getattr(self._client, name)


# ──────────────────────────────────────────────────────────────
# Module-level Singleton
# ──────────────────────────────────────────────────────────────

MODEL_ROUTER = ModelRouter()
