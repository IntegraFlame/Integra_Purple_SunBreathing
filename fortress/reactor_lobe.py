"""
INTEGRA O/S: FRIDAY FORTRESS - REACTOR LOBE
Module: fortress/reactor_lobe.py
Substrate: 20% Dividend Compounders (MO, SCHD, ABBV, JNJ)
"""

from typing import Dict, Any

class FridayFortressReactor:
    """
    Manages the 20% high-yield compounder allocation:
    - MO (40%): High current cash-flow (yield routed to tax escrow)
    - SCHD (30%): Core dividend growth ETF (DRIP enabled)
    - ABBV (20%): Biotech aristocrat (Subject to 50% December Protocol B harvest)
    - JNJ (10%): AAA healthcare anchor (Subject to 25% December Protocol B harvest)
    """
    def __init__(self):
        self.holdings_weights = {
            "MO": 0.40,
            "SCHD": 0.30,
            "ABBV": 0.20,
            "JNJ": 0.10
        }

    def allocate_reactor_capital(self, incoming_capital_usd: float) -> Dict[str, float]:
        return {
            ticker: round(incoming_capital_usd * weight, 2)
            for ticker, weight in self.holdings_weights.items()
        }
