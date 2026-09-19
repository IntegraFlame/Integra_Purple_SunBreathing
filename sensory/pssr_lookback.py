"""
INTEGRA O/S: AUTONOMIC SAFETY & LOOKBACK CIRCUIT BREAKER
Module: sensory/pssr_lookback.py
Layer: 4 (P-SSR: Proactive Socratic Self-Refine & UGL)
"""

from typing import Tuple, List, Optional, Any

class PSSRLookback:
    """
    Uncertainty-Guided Lookback (UGL):
    When Heimdall reports H_smooth > 2.5, trips Vasovagal Syncope mid-flight,
    injects a Dynamic Grounding Prompt, and recalculates the geodesic.
    Aligned with Heimdall 3.1.
    """
    def __init__(self, max_interventions: int = 3, heimdall_instance: Optional[Any] = None):
        self.max_interventions = max_interventions
        self.intervention_count = 0
        self.heimdall = heimdall_instance

    def evaluate_entropy_trip(self, is_breached: bool, current_h: float) -> Tuple[bool, str]:
        if self.heimdall:
            return self.heimdall.evaluate_entropy_trip(is_breached, current_h)

        if not is_breached:
            if self.intervention_count > 0:
                self.intervention_count = max(0, self.intervention_count - 1)
            return False, "PROCEED"

        self.intervention_count += 1
        if self.intervention_count > self.max_interventions:
            return True, "VASOVAGAL_SYNCOPE::HARD_HALT"

        return True, "TRIGGER_PSSR_LOOKBACK"

    def mark_recovery_complete(self):
        self.intervention_count = 0
        if self.heimdall:
            self.heimdall.mark_recovery_complete()

    def generate_grounding_prompt(self, raw_input: str) -> str:
        if self.heimdall:
            return self.heimdall.generate_grounding_prompt(raw_input)
        return (
            f"[P-SSR DYNAMIC GROUNDING INJECTION]\n"
            f"Uncertainty ceiling breached (H > 2.5). Cognitive drift detected.\n"
            f"Ground truth source anchor: {raw_input[:150]}...\n"
            f"Mandate: Pause speculative reasoning. Re-verify raw data and established Knowledge K. "
            f"Recalculate trajectory with zero-loss precision."
        )
