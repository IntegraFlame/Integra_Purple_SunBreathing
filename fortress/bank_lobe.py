"""
INTEGRA O/S: FRIDAY FORTRESS - BANK LOBE
Module: fortress/bank_lobe.py
Substrate: 75% SGOV & $20,000 Margin Lock Floor
"""

import json
from typing import Dict, Any

class FridayFortressBank:
    """
    Enforces the $20,000 margin floor and routes yields into risk-free treasury collateral.
    SGOV is credited at 99% margin utility for writing index options.
    """
    def __init__(self, state_file_path: str = "fortress/portfolio_state.json"):
        self.state_path = state_file_path
        self.MARGIN_LOCK_FLOOR = 20000.0

    def verify_solvency(self, bank_equity: float) -> bool:
        return bank_equity >= self.MARGIN_LOCK_FLOOR

    def calculate_margin_buying_power(self, sgov_equity: float) -> float:
        if not self.verify_solvency(sgov_equity):
            raise PermissionError("MARGIN LOCK BREACHED: Hunter options writing suspended.")
        return sgov_equity * 0.99

    def process_weekly_inflow(self, hunter_extraction_usd: float) -> float:
        try:
            with open(self.state_path, "r") as f:
                data = json.load(f)
        except Exception:
            data = {"current_state": {"bank": {"equity_usd": 20000.0}, "reactor": {"equity_usd": 0.0}, "shield": {"equity_usd": 0.0}}}

        bank_equity = data["current_state"]["bank"]["equity_usd"]
        
        # If Bank is below target floor, shunt 100% of inflow to SGOV
        if bank_equity < self.MARGIN_LOCK_FLOOR:
            deficit = self.MARGIN_LOCK_FLOOR - bank_equity
            allocation_to_bank = min(hunter_extraction_usd, deficit)
            data["current_state"]["bank"]["equity_usd"] += allocation_to_bank
            hunter_extraction_usd -= allocation_to_bank

        # Rebalance surplus across Reactor (80%) and Shield (20%)
        if hunter_extraction_usd > 0:
            reactor_cut = hunter_extraction_usd * 0.80
            shield_cut = hunter_extraction_usd * 0.20
            data["current_state"]["reactor"]["equity_usd"] += reactor_cut
            data["current_state"]["shield"]["equity_usd"] += shield_cut

        total = (data["current_state"]["bank"]["equity_usd"] +
                 data["current_state"]["reactor"]["equity_usd"] +
                 data["current_state"]["shield"]["equity_usd"])
        data["current_state"]["total_equity_usd"] = round(total, 2)

        with open(self.state_path, "w") as f:
            json.dump(data, f, indent=2)

        return data["current_state"]["total_equity_usd"]
