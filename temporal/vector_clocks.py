"""
INTEGRA O/S: MICRO-CAUSALITY ENGINE
Module: temporal/vector_clocks.py
Layer: 7 (Hybrid Logical Clocks & Fidge-Mattern Supremum)
"""

import time
from typing import List, Tuple

class HybridLogicalClock:
    """
    Enforces the Causal Invariant across asynchronous agent swarms:
    V_i[j] <- max(V_i[j], V_msg[j])
    Invariant: I(V_exit > V_input). The exit vector must strictly dominate.
    """
    def __init__(self, node_id: int, total_nodes: int = 4):
        self.node_id = node_id
        self.logical_vector = [0] * total_nodes
        self.physical_utc_max = time.time()

    def send_event(self) -> Tuple[float, List[int]]:
        self.logical_vector[self.node_id] += 1
        self.physical_utc_max = max(self.physical_utc_max, time.time())
        return self.physical_utc_max, list(self.logical_vector)

    def receive_event(self, msg_utc: float, msg_vector: List[int]) -> bool:
        self.physical_utc_max = max(self.physical_utc_max, msg_utc, time.time())
        
        is_strictly_greater = False
        for i in range(len(self.logical_vector)):
            if msg_vector[i] > self.logical_vector[i]:
                is_strictly_greater = True
            self.logical_vector[i] = max(self.logical_vector[i], msg_vector[i])

        self.logical_vector[self.node_id] += 1
        return is_strictly_greater
