"""
INTEGRA O/S: FRIDAY FORTRESS - AUTOPHAGIC HARVEST
Module: fortress/autophagic_harvest.py
Protocol: Protocol B (Annual Late December Rebalancing)
"""

import json
from typing import Dict, Any

class AutophagicHarvestProtocol:
    """
    Protocol B: The Cannibal Rebalancing Mechanic.
    Executed annually in late December:
    - 50% ABBV liquidation (ABBV is 20% of Reactor -> 10% total Reactor equity)
    - 25% JNJ liquidation (JNJ is 10% of Reactor -> 2.5% total Reactor equity)
    Total harvested capital is flushed directly into SGOV (The Bank).
    """
    def __init__(self, state_file_path: str = "fortress/portfolio_state.json"):
        self.state_path = state_file_path

    def execute_december_harvest(self) -> Dict[str, Any]:
        try:
            with open(self.state_path, "r") as f:
                data = json.load(f)
        except Exception:
            data = {"current_state": {"reactor": {"equity_usd": 5000.0}, "bank": {"equity_usd": 20000.0}}}

        reactor_equity = data["current_state"]["reactor"]["equity_usd"]
        
        abbv_harvest = reactor_equity * 0.20 * 0.50
        jnj_harvest = reactor_equity * 0.10 * 0.25
        total_harvested = abbv_harvest + jnj_harvest

        data["current_state"]["reactor"]["equity_usd"] = round(reactor_equity - total_harvested, 2)
        data["current_state"]["bank"]["equity_usd"] = round(data["current_state"]["bank"]["equity_usd"] + total_harvested, 2)

        try:
            with open(self.state_path, "w") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

        return {
            "abbv_harvested_usd": round(abbv_harvest, 2),
            "jnj_harvested_usd": round(jnj_harvest, 2),
            "total_flushed_to_bank_usd": round(total_harvested, 2),
            "post_harvest_bank_usd": data["current_state"]["bank"]["equity_usd"]
        }
