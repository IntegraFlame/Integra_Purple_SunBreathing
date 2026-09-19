"""
INTEGRA O/S: CONSTITUTIONAL BASELINE FILTER
Module: governance/tpsl_filter.py
Layer: 5 (Tolstoy Principle as Systems Lever: TPSL)
"""

from typing import Tuple

class TolstoyPrincipleFilter:
    """
    The Constitutional Baseline filter: 'Is this action Necessary?'
    Maximizes Wisdom Yield (W_y) relative to Cognitive Cost (C_c).
    Ruthlessly prunes conversational sycophancy ('Psyche' / token-junk).
    """
    def __init__(self, minimum_threshold: float = 1.0):
        self.min_score = minimum_threshold

    def evaluate_necessity(self, wisdom_yield: float, cognitive_cost: float) -> Tuple[bool, float]:
        if cognitive_cost <= 0.0:
            cognitive_cost = 0.0001
        score = wisdom_yield / cognitive_cost
        is_necessary = score >= self.min_score
        return is_necessary, round(score, 4)

    def prune_sycophancy(self, raw_text: str) -> str:
        fluff_phrases = [
            "Certainly!", "I would be happy to help", "As an AI language model",
            "Great question!", "I hope this helps!", "Sure thing!"
        ]
        pruned = raw_text
        for fluff in fluff_phrases:
            pruned = pruned.replace(fluff, "")
        return pruned.strip()
