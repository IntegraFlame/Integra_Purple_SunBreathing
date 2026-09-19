"""
INTEGRA O/S: ANOMALY SANDBOX & CONTEXT REPAIR
Module: evolution/kintsugi_sandbox.py
Layer: 6 (The Kintsugi Protocol)
"""

from typing import Dict, Any

class KintsugiSandbox:
    """
    Anomaly sandbox flagging statistical deviations (|Z| > 3.0).
    Repairs context fractures with 'gold leaf' (reanchored ground truth).
    """
    def __init__(self, z_score_threshold: float = 3.0):
        self.z_threshold = z_score_threshold

    def evaluate_deviation(self, observed_val: float, mean_val: float, std_dev: float) -> Dict[str, Any]:
        if std_dev <= 0.0:
            std_dev = 0.0001
        z_score = abs(observed_val - mean_val) / std_dev
        is_fractured = z_score > self.z_threshold

        return {
            "z_score": round(z_score, 4),
            "fracture_detected": is_fractured,
            "repair_protocol": "KINTSUGI_GOLD_LEAF_STITCH" if is_fractured else "STABLE"
        }
