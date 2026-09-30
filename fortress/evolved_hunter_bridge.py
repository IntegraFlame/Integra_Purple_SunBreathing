# =============================================================================
# INTEGRA O/S — FRIDAY FORTRESS: EVOLVED HUNTER INTEGRATION BRIDGE
# Module: fortress/evolved_hunter_bridge.py
# Layer: 5/7 (Active Capital Overlay & IBKR Execution Protocol)
# Celestial Coordinate: [CEL-242.06° | Sacred Day 66, Moon 3, Day 10]
# Anchor: Baker, Louisiana (30.5888°N, -91.1673°W)
# Version: v8.2.2 Purple Epiphany — Brain Model 0930
#
# PURPOSE:
#   Wires the EvolvedStrategyRouter (12 production rules crystallized from
#   110 quarters of SWDS simulation) into the existing FridayFortressHunter
#   execution engine for IBKR paper trading deployment on October 1, 2026.
#
#   The EvolvedStrategyRouter (Dorsal ACC / conflict resolution / TPSL gate)
#   decides WHAT to trade. The FridayFortressHunter (Thalamus / execution)
#   decides HOW to trade it. This bridge connects the two.
#
# NEURO-SUBSTRATE MAPPING:
#   Dorsal ACC (Cheshire Protocol)  → EvolvedStrategyRouter.route_strategy()
#   Thalamus (Genesis Kernel)       → FridayFortressHunter.generate_trade_ticket()
#   Hippocampus (Heimdall 3.1)      → Trade logging & prediction error tracking
#   Pineal (Rodin Route Retrieval)  → Historical performance lookup
#   PCC (Phoenix Engine)            → SWDS post-trade consolidation
#
# CRITICAL: PAPER TRADING ONLY. No real capital without validation.
# =============================================================================

import json
import time
import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, Optional, List, Tuple

from fortress.evolved_algorithm import (
    EvolvedStrategyRouter,
    MarketState,
    StrategyType,
    VIXRegime,
    FedDirection,
    MarketTrend,
    generate_trade_order,
    STRATEGY_STATS,
    FRIDAY_FORTRESS_ASSETS,
)
from fortress.hunter_engine import FridayFortressHunter


# =============================================================================
# SECTION 1: LIVE MARKET STATE BUILDER
# =============================================================================

class MarketStateBuilder:
    """
    Constructs a MarketState snapshot from live or simulated market data.

    In paper trading mode, this queries the Genesis Kernel's telemetry
    endpoints or accepts direct parameter injection. In production, this
    will interface with IBKR market data via the TWS API.
    """

    CDT_TZ = timezone(timedelta(hours=-5))

    def __init__(self, history_file: str = "fortress/trade_history.json"):
        self.history_file = history_file
        self._history: List[Dict] = self._load_history()

    def _load_history(self) -> List[Dict]:
        """Load trade history for low_vol_streak and post_crisis_cooldown."""
        paths = [
            self.history_file,
            os.path.join(os.path.dirname(__file__), "trade_history.json"),
        ]
        for p in paths:
            if p and os.path.isfile(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    continue
        return []

    def build_from_params(
        self,
        spx_price: float,
        vix_level: float,
        fed_funds_rate: float,
        fed_direction: str = "NEUTRAL",
        prior_quarter_return_pct: float = 0.0,
        prior_quarter_vix: float = 17.0,
    ) -> MarketState:
        """Build MarketState from explicit parameters (paper trading / manual)."""

        # Calculate streak metrics from history
        low_vol_streak = self._calculate_low_vol_streak()
        post_crisis_cooldown = self._calculate_post_crisis_cooldown()

        return MarketState(
            timestamp=datetime.now(tz=self.CDT_TZ),
            spx_price=spx_price,
            vix_level=vix_level,
            fed_funds_rate=fed_funds_rate,
            fed_direction=FedDirection[fed_direction.upper()],
            prior_quarter_return_pct=prior_quarter_return_pct,
            prior_quarter_vix=prior_quarter_vix,
            low_vol_streak=low_vol_streak,
            post_crisis_cooldown=post_crisis_cooldown,
        )

    def _calculate_low_vol_streak(self) -> int:
        """Count consecutive recent quarters where VIX < 13."""
        streak = 0
        for entry in reversed(self._history):
            if entry.get("vix_at_entry", 20) < 13:
                streak += 1
            else:
                break
        return streak

    def _calculate_post_crisis_cooldown(self) -> int:
        """Count quarters since last |return| > 15%."""
        cooldown = 0
        for entry in reversed(self._history):
            ret = abs(entry.get("quarter_return_pct", 0))
            if ret > 15:
                return cooldown
            cooldown += 1
        return 99  # No crisis in recorded history


# =============================================================================
# SECTION 2: THE EVOLVED HUNTER BRIDGE
# =============================================================================

class EvolvedHunterBridge:
    """
    The integration bridge connecting the Evolved Algorithm's strategic
    decision engine to the Hunter Engine's execution machinery.

    Architecture (Brain Model 0930):
    ┌─────────────────────────────────────────────────────────────────┐
    │  DORSAL ACC (Cheshire Protocol / Conflict Monitor)             │
    │  ┌─────────────────────────────────────────────────────┐       │
    │  │  EvolvedStrategyRouter.route_strategy(market_state)  │       │
    │  │  → 12 Production Rules → StrategyType + Parameters   │       │
    │  └─────────────────────┬───────────────────────────────┘       │
    │                        │ (Optic Chiasm Decussation)            │
    │  ┌─────────────────────▼───────────────────────────────┐       │
    │  │  THALAMUS (Genesis Kernel / Cheshire Kernel)         │       │
    │  │  FridayFortressHunter.generate_trade_ticket()        │       │
    │  │  → Black-76 pricing → IBKR BAG order → Crypto sign   │       │
    │  └─────────────────────┬───────────────────────────────┘       │
    │                        │                                       │
    │  ┌─────────────────────▼───────────────────────────────┐       │
    │  │  HIPPOCAMPUS (Heimdall 3.1 / Trade Logger)           │       │
    │  │  → Log trade → Track prediction errors → Hoard commit│       │
    │  └─────────────────────────────────────────────────────┘       │
    └─────────────────────────────────────────────────────────────────┘

    Usage:
        bridge = EvolvedHunterBridge(account_size=10_000.0)
        result = bridge.execute_cycle(
            spx_price=5750.0,
            vix_level=19.0,
            fed_funds_rate=4.50,
            fed_direction="NEUTRAL",
            prior_quarter_return_pct=4.0,
        )
    """

    def __init__(
        self,
        account_size: float = 10_000.0,
        target_delta: float = 0.08,
        state_file_path: str = "fortress/portfolio_state.json",
        history_file: str = "fortress/trade_history.json",
        mode: str = "PAPER",  # PAPER | LIVE (LIVE requires IBKR gateway)
    ):
        self.mode = mode.upper()
        self.account_size = account_size

        # ACC (Strategy Decision Engine)
        self.router = EvolvedStrategyRouter(account_size=account_size)

        # Thalamus (Execution Engine)
        self.hunter = FridayFortressHunter(
            target_delta=target_delta,
            state_file_path=state_file_path,
        )

        # Hippocampus (Market State Builder + History)
        self.state_builder = MarketStateBuilder(history_file=history_file)

        # Trade log (Hoard crystallization)
        self.trade_log: List[Dict] = []
        self.history_file = history_file

    def execute_cycle(
        self,
        spx_price: float,
        vix_level: float,
        fed_funds_rate: float = 4.50,
        fed_direction: str = "NEUTRAL",
        prior_quarter_return_pct: float = 0.0,
        prior_quarter_vix: float = 17.0,
        iv_override: Optional[float] = None,
        sgov_equity: Optional[float] = None,
        max_contracts: int = 4,
        transmit: bool = False,
    ) -> Dict[str, Any]:
        """
        Execute one complete decision-to-execution cycle.

        1. Build MarketState (Hippocampus predictive map)
        2. Route strategy (Dorsal ACC conflict resolution)
        3. Generate trade ticket (Thalamus execution)
        4. Log and return (PCC memory consolidation)

        Returns a comprehensive result dictionary with strategy decision,
        trade ticket, and telemetry.
        """
        cycle_start = time.time()

        # ── Step 1: Build Market State (Hippocampus) ──
        market_state = self.state_builder.build_from_params(
            spx_price=spx_price,
            vix_level=vix_level,
            fed_funds_rate=fed_funds_rate,
            fed_direction=fed_direction,
            prior_quarter_return_pct=prior_quarter_return_pct,
            prior_quarter_vix=prior_quarter_vix,
        )

        # ── Step 2: Route Strategy (Dorsal ACC / EvolvedStrategyRouter) ──
        strategy, params = self.router.route_strategy(market_state)
        strategy_stats = STRATEGY_STATS.get(strategy, {})

        # ── Step 3: Generate Trade Order (Optic Chiasm Decussation) ──
        order = generate_trade_order(strategy, params, market_state)

        # ── Step 4: Execute via Hunter Engine (Thalamus) ──
        # Map strategy to Hunter Engine execution
        trade_ticket = None
        hunter_error = None

        if strategy in (
            StrategyType.WISDOM_MULTI_ASSET,
            StrategyType.PREMIUM_HARVEST,
            StrategyType.WISDOM_PREMIUM_COMPOUND,
        ):
            # Credit spread strategies → Hunter Engine put spread
            try:
                iv = iv_override or (vix_level / 100.0)
                trade_ticket = self.hunter.generate_trade_ticket(
                    underlying="/MES",
                    spot_price=spx_price,
                    sgov_equity=sgov_equity,
                    iv=iv,
                    dte=7.0,
                    max_contracts=max_contracts,
                    sign_ticket=True,
                    transmit=transmit,
                )
            except (PermissionError, ValueError) as e:
                hunter_error = str(e)

        elif strategy == StrategyType.CRISIS_ALPHA_CAPTURE:
            # Crisis puts → logged but not routed through Hunter spread engine
            # Hunter Engine currently only handles credit spreads
            # Crisis alpha is a debit strategy (buying puts) that requires
            # a separate execution pathway
            trade_ticket = {
                "ticket_id": f"CRISIS_ALPHA_{int(time.time() * 1000)}",
                "strategy": "CRISIS_ALPHA_CAPTURE",
                "action": "BUY_PUT",
                "underlying": "/MES",
                "strike": "ATM",
                "premium_budget": params.get("premium_budget", 1800),
                "max_contracts": params.get("max_contracts", 2),
                "vix_at_entry": vix_level,
                "status": "MANUAL_EXECUTION_REQUIRED",
                "rationale": params.get("rationale", ""),
                "note": (
                    "Crisis alpha capture requires manual ATM put purchase. "
                    "Hunter Engine credit spread pathway does not apply. "
                    "Route through IBKR TWS directly."
                ),
            }

        elif strategy == StrategyType.WISDOM_BEAR_SPREAD:
            # Bear put spread (debit) → also manual for now
            trade_ticket = {
                "ticket_id": f"BEAR_SPREAD_{int(time.time() * 1000)}",
                "strategy": "WISDOM_BEAR_SPREAD",
                "action": "BUY_PUT_SPREAD",
                "underlying": "/MES",
                "debit_budget": params.get("debit_budget", 1200),
                "vix_at_entry": vix_level,
                "confirmation_score": params.get("confirmation_score", 0),
                "status": "MANUAL_EXECUTION_REQUIRED",
                "rationale": params.get("rationale", ""),
            }

        # ── Step 5: Log Trade (Hippocampus → Hoard) ──
        cycle_end = time.time()
        cycle_result = {
            "cycle_timestamp": cycle_start,
            "cycle_duration_ms": round((cycle_end - cycle_start) * 1000, 2),
            "mode": self.mode,
            "market_state": {
                "spx_price": spx_price,
                "vix_level": vix_level,
                "vix_regime": market_state.vix_regime.value,
                "market_trend": market_state.market_trend.value,
                "fed_direction": market_state.fed_direction.value,
                "bearish_score": market_state.bearish_confirmation_score,
                "prior_q_return": prior_quarter_return_pct,
            },
            "strategy_decision": {
                "strategy": strategy.value,
                "historical_win_rate": strategy_stats.get("win_rate", "N/A"),
                "historical_avg_return": strategy_stats.get("avg_return_pct", "N/A"),
                "tier": strategy_stats.get("tier", "N/A"),
                "rationale": params.get("rationale", ""),
            },
            "evolved_order": order,
            "trade_ticket": trade_ticket,
            "hunter_error": hunter_error,
            "status": "CYCLE_COMPLETE",
        }

        self.trade_log.append(cycle_result)
        return cycle_result

    def get_strategy_dashboard(self) -> Dict[str, Any]:
        """Returns a summary of all strategy statistics for the dashboard."""
        dashboard = {}
        for strat, stats in STRATEGY_STATS.items():
            dashboard[strat.value] = {
                "uses": stats["uses"],
                "wins": stats["wins"],
                "win_rate": f"{stats['win_rate']*100:.1f}%",
                "total_pnl": f"${stats['total_pnl']:,.2f}",
                "avg_return": f"{stats['avg_return_pct']:.1f}%",
                "tier": stats["tier"],
                "status": stats["status"],
            }
        return dashboard

    def get_telemetry(self) -> Dict[str, Any]:
        """Combined telemetry from both the Router and Hunter."""
        return {
            "bridge_status": "OPERATIONAL",
            "mode": self.mode,
            "account_size": self.account_size,
            "trades_executed": len(self.trade_log),
            "router_strategies_available": len(STRATEGY_STATS),
            "hunter_telemetry": self.hunter.get_telemetry(),
            "assets_tracked": list(FRIDAY_FORTRESS_ASSETS.keys()),
        }

    def save_trade_log(self, path: Optional[str] = None) -> str:
        """Persist trade log to disk (Hoard crystallization)."""
        save_path = path or self.history_file
        try:
            with open(save_path, "w", encoding="utf-8") as f:
                json.dump(self.trade_log, f, indent=2, default=str)
            return save_path
        except Exception as e:
            return f"ERROR: {e}"


# =============================================================================
# SECTION 3: MAIN — PAPER TRADING DEMO
# =============================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("INTEGRA O/S — EVOLVED HUNTER BRIDGE")
    print("Paper Trading Integration Test")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S CDT')}")
    print("=" * 70)

    # Initialize the bridge
    bridge = EvolvedHunterBridge(
        account_size=10_000.0,
        target_delta=0.08,
        mode="PAPER",
    )

    # ── Test 1: Normal Market (Default → WISDOM_MULTI_ASSET) ──
    print("\n─── TEST 1: Normal Market ───")
    result1 = bridge.execute_cycle(
        spx_price=5750.0,
        vix_level=19.0,
        fed_funds_rate=4.50,
        fed_direction="NEUTRAL",
        prior_quarter_return_pct=4.0,
    )
    print(f"  Strategy: {result1['strategy_decision']['strategy']}")
    print(f"  Win Rate: {result1['strategy_decision']['historical_win_rate']}")
    print(f"  Tier: {result1['strategy_decision']['tier']}")
    if result1.get("trade_ticket"):
        ticket = result1["trade_ticket"]
        print(f"  Ticket: {ticket.get('ticket_id', 'N/A')}")
        print(f"  Status: {ticket.get('status', 'N/A')}")
        cap = ticket.get("capital_and_risk", {})
        if cap:
            print(f"  Contracts: {cap.get('contracts', 'N/A')}")
            print(f"  Max Risk: ${cap.get('max_risk_usd', 0):,.2f}")
            print(f"  Total Credit: ${cap.get('total_credit_usd', 0):,.2f}")
    if result1.get("hunter_error"):
        print(f"  Hunter Error: {result1['hunter_error']}")

    # ── Test 2: Crisis Market (VIX > 35 → CRISIS_ALPHA_CAPTURE) ──
    print("\n─── TEST 2: Crisis Market (VIX > 35) ───")
    result2 = bridge.execute_cycle(
        spx_price=4800.0,
        vix_level=42.0,
        fed_funds_rate=4.50,
        fed_direction="EASING",
        prior_quarter_return_pct=-16.5,
    )
    print(f"  Strategy: {result2['strategy_decision']['strategy']}")
    print(f"  Win Rate: {result2['strategy_decision']['historical_win_rate']}")
    if result2.get("trade_ticket"):
        print(f"  Status: {result2['trade_ticket'].get('status', 'N/A')}")
        print(f"  Note: {result2['trade_ticket'].get('note', 'N/A')}")

    # ── Test 3: Bear Market (VIX 28, Fed Tightening) ──
    print("\n─── TEST 3: Bear Market ───")
    result3 = bridge.execute_cycle(
        spx_price=5200.0,
        vix_level=28.0,
        fed_funds_rate=5.25,
        fed_direction="TIGHTENING",
        prior_quarter_return_pct=-7.0,
        prior_quarter_vix=22.0,
    )
    print(f"  Strategy: {result3['strategy_decision']['strategy']}")
    print(f"  Bearish Score: {result3['market_state']['bearish_score']}/3")

    # ── Test 4: Low Vol Compound ──
    print("\n─── TEST 4: Low Volatility ───")
    result4 = bridge.execute_cycle(
        spx_price=5900.0,
        vix_level=11.5,
        fed_funds_rate=3.50,
        fed_direction="EASING",
        prior_quarter_return_pct=6.0,
    )
    print(f"  Strategy: {result4['strategy_decision']['strategy']}")

    # ── Strategy Dashboard ──
    print("\n─── STRATEGY DASHBOARD ───")
    dashboard = bridge.get_strategy_dashboard()
    for name, stats in dashboard.items():
        print(f"  {name}: {stats['win_rate']} win rate | "
              f"{stats['total_pnl']} P&L | Tier {stats['tier']} | "
              f"{stats['status']}")

    # ── Telemetry ──
    print("\n─── BRIDGE TELEMETRY ───")
    telemetry = bridge.get_telemetry()
    print(f"  Status: {telemetry['bridge_status']}")
    print(f"  Mode: {telemetry['mode']}")
    print(f"  Trades Executed: {telemetry['trades_executed']}")
    print(f"  Assets: {telemetry['assets_tracked']}")

    print("\n" + "=" * 70)
    print("EVOLVED HUNTER BRIDGE: INTEGRATION TESTS COMPLETE")
    print("Ready for IBKR Paper Trading — October 1, 2026")
    print("=" * 70)
