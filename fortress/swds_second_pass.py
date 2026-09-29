# =============================================================================
# INTEGRA O/S — SWDS SECOND PASS SIMULATION
# Applies the 12 Evolved Algorithm Rules to ALL 110 Quarters Retroactively
# Generated: 2026-09-29 03:35 AM CDT | Celestial: 200.72° Earth Rotation
# CCID: CCID_SWDS_SECOND_PASS_20260929
# =============================================================================
#
# PURPOSE: Test the "what if" scenario — if we had known the 12 production
# rules from 1999 Q1 (day 1), how would the algorithm have performed?
#
# This removes the learning curve and applies Wisdom-era logic to all 110
# quarters, giving us the TRUE theoretical ceiling for the algorithm.
# =============================================================================

import sys
import os
import json
import math
from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
from datetime import datetime

# Add parent path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the evolved algorithm and the simulation data
from evolved_algorithm import (
    EvolvedStrategyRouter, MarketState, VIXRegime,
    FedDirection, StrategyType, black_scholes_put,
    find_strike_for_delta, FRIDAY_FORTRESS_ASSETS
)

# =============================================================================
# HISTORICAL DATA (same as original simulation)
# =============================================================================

# S&P 500 quarterly close prices (end of each quarter)
SPX_QUARTERLY_CLOSE = {
    (1998, 4): 1229.23,
    (1999, 1): 1286.37, (1999, 2): 1372.71, (1999, 3): 1282.71, (1999, 4): 1469.25,
    (2000, 1): 1498.58, (2000, 2): 1454.60, (2000, 3): 1436.51, (2000, 4): 1320.28,
    (2001, 1): 1160.33, (2001, 2): 1224.38, (2001, 3): 1040.94, (2001, 4): 1148.08,
    (2002, 1): 1147.39, (2002, 2): 989.82,  (2002, 3): 815.28,  (2002, 4): 879.82,
    (2003, 1): 848.18,  (2003, 2): 974.50,  (2003, 3): 995.97,  (2003, 4): 1111.92,
    (2004, 1): 1126.21, (2004, 2): 1140.84, (2004, 3): 1114.58, (2004, 4): 1211.92,
    (2005, 1): 1180.59, (2005, 2): 1191.33, (2005, 3): 1228.81, (2005, 4): 1248.29,
    (2006, 1): 1294.87, (2006, 2): 1270.20, (2006, 3): 1335.85, (2006, 4): 1418.30,
    (2007, 1): 1420.86, (2007, 2): 1503.35, (2007, 3): 1526.75, (2007, 4): 1468.36,
    (2008, 1): 1322.70, (2008, 2): 1280.00, (2008, 3): 1166.36, (2008, 4): 903.25,
    (2009, 1): 797.87,  (2009, 2): 919.14,  (2009, 3): 1057.08, (2009, 4): 1115.10,
    (2010, 1): 1169.43, (2010, 2): 1030.71, (2010, 3): 1141.20, (2010, 4): 1257.64,
    (2011, 1): 1325.83, (2011, 2): 1320.64, (2011, 3): 1131.42, (2011, 4): 1257.60,
    (2012, 1): 1408.47, (2012, 2): 1362.16, (2012, 3): 1440.67, (2012, 4): 1426.19,
    (2013, 1): 1569.19, (2013, 2): 1606.28, (2013, 3): 1681.55, (2013, 4): 1848.36,
    (2014, 1): 1872.34, (2014, 2): 1960.23, (2014, 3): 1972.29, (2014, 4): 2058.90,
    (2015, 1): 2067.89, (2015, 2): 2063.11, (2015, 3): 1920.03, (2015, 4): 2043.94,
    (2016, 1): 2059.74, (2016, 2): 2098.86, (2016, 3): 2168.27, (2016, 4): 2238.83,
    (2017, 1): 2362.72, (2017, 2): 2423.41, (2017, 3): 2519.36, (2017, 4): 2673.61,
    (2018, 1): 2640.87, (2018, 2): 2718.37, (2018, 3): 2913.98, (2018, 4): 2506.85,
    (2019, 1): 2834.40, (2019, 2): 2941.76, (2019, 3): 2976.74, (2019, 4): 3230.78,
    (2020, 1): 2584.59, (2020, 2): 3100.29, (2020, 3): 3363.00, (2020, 4): 3756.07,
    (2021, 1): 3972.89, (2021, 2): 4297.50, (2021, 3): 4307.54, (2021, 4): 4766.18,
    (2022, 1): 4530.41, (2022, 2): 3785.38, (2022, 3): 3585.62, (2022, 4): 3839.50,
    (2023, 1): 4109.31, (2023, 2): 4450.38, (2023, 3): 4288.05, (2023, 4): 4769.83,
    (2024, 1): 5254.35, (2024, 2): 5460.48, (2024, 3): 5762.48, (2024, 4): 5881.63,
    (2025, 1): 5611.85, (2025, 2): 5525.21, (2025, 3): 5842.01,
    (2026, 1): 5680.00, (2026, 2): 5920.00, (2026, 3): 5750.00,
}

# VIX quarterly average levels
VIX_QUARTERLY = {
    (1999, 1): 26.5, (1999, 2): 24.0, (1999, 3): 23.5, (1999, 4): 24.0,
    (2000, 1): 23.5, (2000, 2): 22.0, (2000, 3): 20.5, (2000, 4): 27.0,
    (2001, 1): 32.5, (2001, 2): 26.0, (2001, 3): 35.0, (2001, 4): 30.0,
    (2002, 1): 22.0, (2002, 2): 26.0, (2002, 3): 38.0, (2002, 4): 32.0,
    (2003, 1): 30.0, (2003, 2): 20.0, (2003, 3): 19.0, (2003, 4): 16.0,
    (2004, 1): 16.5, (2004, 2): 17.0, (2004, 3): 15.5, (2004, 4): 13.5,
    (2005, 1): 13.0, (2005, 2): 12.5, (2005, 3): 12.0, (2005, 4): 12.5,
    (2006, 1): 12.0, (2006, 2): 14.5, (2006, 3): 12.5, (2006, 4): 11.0,
    (2007, 1): 13.0, (2007, 2): 15.5, (2007, 3): 22.0, (2007, 4): 24.0,
    (2008, 1): 28.0, (2008, 2): 22.0, (2008, 3): 32.0, (2008, 4): 56.0,
    (2009, 1): 45.0, (2009, 2): 30.0, (2009, 3): 24.0, (2009, 4): 22.0,
    (2010, 1): 18.0, (2010, 2): 28.0, (2010, 3): 24.0, (2010, 4): 18.0,
    (2011, 1): 17.5, (2011, 2): 16.5, (2011, 3): 36.0, (2011, 4): 28.0,
    (2012, 1): 17.0, (2012, 2): 21.0, (2012, 3): 14.5, (2012, 4): 16.0,
    (2013, 1): 13.5, (2013, 2): 15.0, (2013, 3): 14.0, (2013, 4): 13.0,
    (2014, 1): 14.0, (2014, 2): 11.5, (2014, 3): 14.0, (2014, 4): 16.0,
    (2015, 1): 15.5, (2015, 2): 13.5, (2015, 3): 25.0, (2015, 4): 16.5,
    (2016, 1): 20.0, (2016, 2): 15.0, (2016, 3): 12.0, (2016, 4): 13.5,
    (2017, 1): 11.5, (2017, 2): 10.5, (2017, 3): 10.0, (2017, 4): 9.5,
    (2018, 1): 17.0, (2018, 2): 13.0, (2018, 3): 12.5, (2018, 4): 25.0,
    (2019, 1): 16.0, (2019, 2): 15.0, (2019, 3): 17.0, (2019, 4): 13.5,
    (2020, 1): 57.0, (2020, 2): 30.0, (2020, 3): 26.0, (2020, 4): 22.0,
    (2021, 1): 20.0, (2021, 2): 17.0, (2021, 3): 21.0, (2021, 4): 19.0,
    (2022, 1): 24.0, (2022, 2): 28.0, (2022, 3): 27.0, (2022, 4): 22.0,
    (2023, 1): 19.0, (2023, 2): 14.0, (2023, 3): 17.0, (2023, 4): 13.5,
    (2024, 1): 13.0, (2024, 2): 12.5, (2024, 3): 16.0, (2024, 4): 15.0,
    (2025, 1): 22.0, (2025, 2): 18.0, (2025, 3): 20.0,
    (2026, 1): 18.0, (2026, 2): 16.0, (2026, 3): 19.0,
}

# Federal Reserve policy direction by year
FED_POLICY = {
    1999: FedDirection.TIGHTENING,   # Raising from 4.75% to 5.50%
    2000: FedDirection.TIGHTENING,   # Peaked at 6.50%
    2001: FedDirection.EASING,       # 11 cuts, 6.50% -> 1.75%
    2002: FedDirection.EASING,       # Cut to 1.25%
    2003: FedDirection.EASING,       # Cut to 1.00%
    2004: FedDirection.TIGHTENING,   # Began "measured" hikes
    2005: FedDirection.TIGHTENING,   # Continued hikes
    2006: FedDirection.TIGHTENING,   # Peaked at 5.25%
    2007: FedDirection.EASING,       # Cut from 5.25% in Sept
    2008: FedDirection.EASING,       # Emergency cuts to 0-0.25%
    2009: FedDirection.EASING,       # ZIRP + QE
    2010: FedDirection.EASING,       # QE2
    2011: FedDirection.EASING,       # Operation Twist
    2012: FedDirection.EASING,       # QE3
    2013: FedDirection.NEUTRAL,      # Taper talk
    2014: FedDirection.NEUTRAL,      # Taper completed
    2015: FedDirection.TIGHTENING,   # First hike in Dec
    2016: FedDirection.TIGHTENING,   # One hike in Dec
    2017: FedDirection.TIGHTENING,   # Three hikes
    2018: FedDirection.TIGHTENING,   # Four hikes + QT
    2019: FedDirection.EASING,       # Three cuts (insurance)
    2020: FedDirection.EASING,       # Emergency cut to 0-0.25%
    2021: FedDirection.EASING,       # Still at ZIRP
    2022: FedDirection.TIGHTENING,   # Fastest hikes since Volcker
    2023: FedDirection.TIGHTENING,   # Hikes to 5.25-5.50%
    2024: FedDirection.NEUTRAL,      # Holding / first cut in Sept
    2025: FedDirection.NEUTRAL,      # Paused
    2026: FedDirection.NEUTRAL,      # Holding
}

FED_RATES = {
    1999: 5.50, 2000: 6.50, 2001: 1.75, 2002: 1.25, 2003: 1.00,
    2004: 2.25, 2005: 4.25, 2006: 5.25, 2007: 4.25, 2008: 0.25,
    2009: 0.25, 2010: 0.25, 2011: 0.25, 2012: 0.25, 2013: 0.25,
    2014: 0.25, 2015: 0.50, 2016: 0.75, 2017: 1.50, 2018: 2.50,
    2019: 1.75, 2020: 0.25, 2021: 0.25, 2022: 4.50, 2023: 5.50,
    2024: 4.75, 2025: 4.50, 2026: 4.50,
}


# =============================================================================
# P&L SIMULATION (uses Black-Scholes from evolved_algorithm)
# =============================================================================

def simulate_quarter_pnl(
    strategy: StrategyType,
    params: Dict,
    state: MarketState,
    spx_start: float,
    spx_end: float,
) -> Tuple[float, str]:
    """
    Simulate the P&L for a single quarter given a strategy and market state.

    Returns (pnl_dollars, description_string).
    """
    account = 10_000.0
    quarterly_return_pct = (spx_end - spx_start) / spx_start
    vix = state.vix_level
    sigma = vix / 100.0
    T = 90 / 365.0
    r = state.fed_funds_rate / 100.0

    if strategy == StrategyType.CRISIS_ALPHA_CAPTURE:
        # Buy ATM puts on /MES
        risk_pct = 0.18
        premium = black_scholes_put(spx_start, spx_start, T, r, sigma)
        contracts_value = account * risk_pct
        if premium > 0:
            num_contracts = max(1, int(contracts_value / (premium * 5)))
        else:
            num_contracts = 1

        # Put payoff at expiry
        intrinsic = max(spx_start - spx_end, 0) * 5 * num_contracts
        cost = premium * 5 * num_contracts
        pnl = intrinsic - cost
        desc = f"CRISIS_ALPHA: Bought {num_contracts} ATM puts, premium={premium:.2f}, payoff={intrinsic:.2f}"
        return pnl, desc

    elif strategy == StrategyType.WISDOM_BEAR_SPREAD:
        # Bear put spread (debit)
        risk_pct = 0.12
        debit_budget = account * risk_pct
        short_strike = spx_start * 0.95  # 5% OTM
        long_strike = spx_start * 0.90   # 10% OTM
        spread_width = short_strike - long_strike

        short_premium = black_scholes_put(spx_start, short_strike, T, r, sigma)
        long_premium = black_scholes_put(spx_start, long_strike, T, r, sigma)
        net_debit = short_premium - long_premium
        if net_debit <= 0:
            net_debit = 0.50

        num_contracts = max(1, int(debit_budget / (net_debit * 5)))

        # At expiry
        short_payoff = max(short_strike - spx_end, 0)
        long_payoff = max(long_strike - spx_end, 0)
        spread_payoff = (short_payoff - long_payoff) * 5 * num_contracts
        cost = net_debit * 5 * num_contracts
        pnl = spread_payoff - cost
        desc = f"BEAR_SPREAD: {num_contracts}x, debit={net_debit:.2f}, payoff={spread_payoff:.2f}"
        return pnl, desc

    elif strategy == StrategyType.WISDOM_PREMIUM_COMPOUND:
        # Sell 8-delta put spread (credit) — enhanced sizing
        risk_pct = 0.15
        max_risk = account * risk_pct
        short_delta = 0.08
        spread_width = 50  # points

        short_strike = find_strike_for_delta(spx_start, short_delta, T, r, sigma, "put")
        long_strike = short_strike - spread_width

        short_premium = black_scholes_put(spx_start, short_strike, T, r, sigma)
        long_premium = black_scholes_put(spx_start, long_strike, T, r, sigma)
        credit = short_premium - long_premium
        if credit <= 0:
            credit = 0.15
        max_loss_per = (spread_width - credit) * 5
        num_contracts = max(1, int(max_risk / max(max_loss_per, 1)))

        # At expiry
        if spx_end >= short_strike:
            pnl = credit * 5 * num_contracts
        elif spx_end <= long_strike:
            pnl = -(spread_width - credit) * 5 * num_contracts
        else:
            loss = (short_strike - spx_end - credit)
            pnl = -loss * 5 * num_contracts
        desc = f"PREMIUM_COMPOUND: {num_contracts}x 8-delta spread, credit={credit:.2f}"
        return pnl, desc

    elif strategy == StrategyType.WISDOM_MULTI_ASSET:
        # Multi-component strategy
        total_pnl = 0.0
        details = []

        # Component 1: /MES put credit spread (40%)
        mes_risk = account * 0.40
        short_delta = 0.08
        spread_width = 50
        short_strike = find_strike_for_delta(spx_start, short_delta, T, r, sigma, "put")
        long_strike = short_strike - spread_width
        short_p = black_scholes_put(spx_start, short_strike, T, r, sigma)
        long_p = black_scholes_put(spx_start, long_strike, T, r, sigma)
        credit = short_p - long_p
        if credit <= 0:
            credit = 0.12
        max_loss_per = (spread_width - credit) * 5
        n_mes = max(1, int(mes_risk / max(max_loss_per, 1)))

        if spx_end >= short_strike:
            mes_pnl = credit * 5 * n_mes
        elif spx_end <= long_strike:
            mes_pnl = -(spread_width - credit) * 5 * n_mes
        else:
            loss = (short_strike - spx_end - credit)
            mes_pnl = -loss * 5 * n_mes
        total_pnl += mes_pnl
        details.append(f"/MES spread {n_mes}x: ${mes_pnl:.0f}")

        # Component 2: MO CSP (30%) — modeled as premium capture
        mo_alloc = account * 0.30
        # Simplified: MO moves ~60% of SPX with higher vol
        mo_return = quarterly_return_pct * 0.6
        # CSP delta = 0.20, so probability of profit ~80%
        csp_premium_pct = vix / 100 * 0.20 * (T ** 0.5) * 100  # rough premium
        if mo_return > -0.05:
            # Not assigned — keep premium
            mo_pnl = mo_alloc * csp_premium_pct / 100
        else:
            # Assigned — loss = (mo drop - premium)
            mo_pnl = mo_alloc * (mo_return + csp_premium_pct / 100)
        total_pnl += mo_pnl
        details.append(f"MO CSP: ${mo_pnl:.0f}")

        # Component 3: Dividend capture (20%)
        div_alloc = account * 0.20
        div_yield_q = 0.01  # ~4% annual / 4
        div_price_change = quarterly_return_pct * 0.5  # lower beta
        div_pnl = div_alloc * (div_yield_q + div_price_change)
        total_pnl += div_pnl
        details.append(f"Div: ${div_pnl:.0f}")

        # Component 4: SGOV (10%) — risk-free rate
        sgov_alloc = account * 0.10
        sgov_pnl = sgov_alloc * (r / 4)  # quarterly interest
        total_pnl += sgov_pnl
        details.append(f"SGOV: ${sgov_pnl:.0f}")

        desc = f"MULTI_ASSET: " + " | ".join(details)
        return total_pnl, desc

    else:
        # Fallback — should not reach here
        return 0.0, f"UNKNOWN strategy: {strategy.value}"


# =============================================================================
# MAIN SIMULATION: SECOND PASS
# =============================================================================

def run_second_pass():
    print("=" * 70)
    print("INTEGRA O/S -- SWDS SECOND PASS SIMULATION")
    print("Applying 12 Evolved Algorithm Rules to ALL 110 Quarters")
    print("=" * 70)

    router = EvolvedStrategyRouter(account_size=10_000.0)
    results = []

    # Track state for low-vol streak
    low_vol_streak = 0

    # Build quarter list
    quarters = []
    for year in range(1999, 2027):
        max_q = 3 if year == 2026 else 4
        for q in range(1, max_q + 1):
            if (year, q) in SPX_QUARTERLY_CLOSE:
                quarters.append((year, q))

    total_wins = 0
    total_losses = 0
    cumulative_pnl = 0.0
    best_quarter = None
    worst_quarter = None

    for i, (year, q) in enumerate(quarters):
        # Get market data
        vix = VIX_QUARTERLY.get((year, q), 18.0)
        spx_end = SPX_QUARTERLY_CLOSE[(year, q)]

        # Get prior quarter data
        prev_q = q - 1
        prev_y = year
        if prev_q == 0:
            prev_q = 4
            prev_y = year - 1
        spx_start = SPX_QUARTERLY_CLOSE.get((prev_y, prev_q), spx_end)
        prior_q_return = (spx_start - SPX_QUARTERLY_CLOSE.get(
            (prev_y - 1 if prev_q == 4 else prev_y, prev_q - 1 if prev_q > 1 else 4),
            spx_start
        )) / max(spx_start, 1) * 100

        # Get prior quarter VIX
        prior_vix = VIX_QUARTERLY.get((prev_y, prev_q), 18.0)

        # Track low-vol streak
        if vix < 13:
            low_vol_streak += 1
        else:
            low_vol_streak = 0

        # Build MarketState
        fed_dir = FED_POLICY.get(year, FedDirection.NEUTRAL)
        fed_rate = FED_RATES.get(year, 4.50)

        state = MarketState(
            timestamp=datetime(year, q * 3, 1),
            spx_price=spx_start,
            vix_level=vix,
            fed_funds_rate=fed_rate,
            fed_direction=fed_dir,
            prior_quarter_return_pct=prior_q_return,
            prior_quarter_vix=prior_vix,
            low_vol_streak=low_vol_streak,
        )

        # Route strategy using Evolved Algorithm
        strategy, params = router.route_strategy(state)

        # Simulate P&L
        pnl, desc = simulate_quarter_pnl(strategy, params, state, spx_start, spx_end)

        # Cap extreme values (realistic position sizing)
        pnl = max(pnl, -2000)  # Max loss cap at $2,000
        pnl = min(pnl, 3000)   # Max gain cap at $3,000

        cumulative_pnl += pnl
        is_win = pnl > 0

        if is_win:
            total_wins += 1
        else:
            total_losses += 1

        result = {
            "year": year,
            "quarter": q,
            "strategy": strategy.value,
            "vix": vix,
            "vix_regime": state.vix_regime.value,
            "spx_start": round(spx_start, 2),
            "spx_end": round(spx_end, 2),
            "spx_return_pct": round((spx_end - spx_start) / spx_start * 100, 2),
            "pnl": round(pnl, 2),
            "cumulative_pnl": round(cumulative_pnl, 2),
            "is_win": is_win,
            "description": desc,
        }
        results.append(result)

        if best_quarter is None or pnl > best_quarter["pnl"]:
            best_quarter = result
        if worst_quarter is None or pnl < worst_quarter["pnl"]:
            worst_quarter = result

        # Print each quarter
        win_marker = "[W]" if is_win else "[L]"
        print(f"  {year} Q{q} | {strategy.value:30s} | VIX {vix:5.1f} | "
              f"SPX {spx_start:8.2f}->{spx_end:8.2f} | "
              f"P&L: ${pnl:+8.2f} | Cum: ${cumulative_pnl:+10.2f} {win_marker}")

    # Summary
    total = len(results)
    win_rate = total_wins / total * 100 if total > 0 else 0

    # Calculate Sharpe
    returns = [r["pnl"] / 10000 for r in results]
    avg_ret = sum(returns) / len(returns) if returns else 0
    std_ret = (sum((r - avg_ret) ** 2 for r in returns) / max(len(returns) - 1, 1)) ** 0.5
    sharpe = (avg_ret / std_ret * (4 ** 0.5)) if std_ret > 0 else 0

    # Strategy breakdown
    strategy_stats = {}
    for r in results:
        s = r["strategy"]
        if s not in strategy_stats:
            strategy_stats[s] = {"wins": 0, "losses": 0, "total_pnl": 0, "uses": 0}
        strategy_stats[s]["uses"] += 1
        strategy_stats[s]["total_pnl"] += r["pnl"]
        if r["is_win"]:
            strategy_stats[s]["wins"] += 1
        else:
            strategy_stats[s]["losses"] += 1

    print("\n" + "=" * 70)
    print("SECOND PASS SIMULATION RESULTS")
    print("=" * 70)
    print(f"  Total Quarters:    {total}")
    print(f"  Wins:              {total_wins}")
    print(f"  Losses:            {total_losses}")
    print(f"  Win Rate:          {win_rate:.1f}%")
    print(f"  Cumulative P&L:    ${cumulative_pnl:+,.2f}")
    print(f"  Avg Qtr Return:    {avg_ret * 100:+.2f}%")
    print(f"  Sharpe (Ann.):     {sharpe:.3f}")
    print(f"  Best Quarter:      {best_quarter['year']} Q{best_quarter['quarter']} "
          f"${best_quarter['pnl']:+,.2f} ({best_quarter['strategy']})")
    print(f"  Worst Quarter:     {worst_quarter['year']} Q{worst_quarter['quarter']} "
          f"${worst_quarter['pnl']:+,.2f} ({worst_quarter['strategy']})")

    print("\n  Strategy Breakdown:")
    for s, stats in sorted(strategy_stats.items(), key=lambda x: x[1]["total_pnl"], reverse=True):
        wr = stats["wins"] / stats["uses"] * 100 if stats["uses"] > 0 else 0
        print(f"    {s:35s} | Uses: {stats['uses']:3d} | "
              f"Wins: {stats['wins']:3d} | WR: {wr:5.1f}% | "
              f"P&L: ${stats['total_pnl']:+,.2f}")

    # Compare to first pass
    print("\n" + "-" * 70)
    print("COMPARISON: FIRST PASS vs SECOND PASS")
    print("-" * 70)
    print(f"  {'Metric':<25s} {'First Pass':>15s} {'Second Pass':>15s} {'Delta':>15s}")
    print(f"  {'Win Rate':<25s} {'75.5%':>15s} {f'{win_rate:.1f}%':>15s} "
          f"{f'{win_rate - 75.5:+.1f}%':>15s}")
    print(f"  {'Cumulative P&L':<25s} {'$11,645.72':>15s} {f'${cumulative_pnl:,.2f}':>15s} "
          f"{f'${cumulative_pnl - 11645.72:+,.2f}':>15s}")
    print(f"  {'Avg Qtr Return':<25s} {'1.06%':>15s} {f'{avg_ret * 100:.2f}%':>15s} "
          f"{f'{avg_ret * 100 - 1.06:+.2f}%':>15s}")

    print("\n" + "=" * 70)
    print("SECOND PASS COMPLETE")
    print("=" * 70)

    # Export results
    export_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "kernel_memory", "hoard", "raw_shards",
                                "CCID_SWDS_SECOND_PASS_20260929.json")
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    with open(export_path, "w", encoding="utf-8") as f:
        json.dump({
            "ccid": "CCID_SWDS_SECOND_PASS_20260929",
            "total_quarters": total,
            "win_rate": win_rate,
            "cumulative_pnl": cumulative_pnl,
            "avg_quarterly_return": avg_ret * 100,
            "sharpe_annualized": sharpe,
            "strategy_stats": strategy_stats,
            "quarters": results,
        }, f, indent=2)
    print(f"\nResults exported to: {export_path}")


if __name__ == "__main__":
    run_second_pass()
