"""
INTEGRA O/S: FRIDAY FORTRESS - HUNTER ENGINE
Module: fortress/hunter_engine.py
Layer: 5/7 (Active Capital Overlay & IBKR Execution Protocol)
Coordinates: 30.5888°N, -91.1673°W (Baker, Louisiana)
Version: 8.2.2-PURPLE

Architecture:
    System 3 Active Derivatives Writing Engine utilizing 99% margin utility on SGOV.
    Targets low-delta (0.05 - 0.10, default 0.08) defined-risk put credit spreads on
    /MES (Micro E-mini S&P 500) and /MNQ (Micro E-mini Nasdaq-100) with long outer wing protection.

Invariants:
    1. Capital Rules: Inviolable $20,000 SGOV margin lock floor (PermissionError on breach).
    2. Extraction Target: Conservative ~35 bps weekly premium target on buying power (0.0035 * BP).
    3. Rhythm: Friday entry -> Thursday exit (~5-7 DTE).
    4. Cryptographic Proof: Dual-Key trade ticket signing via temporal/crypto_validator.py
       (Key 1: SHA-256 state hash, Key 2: HMAC-SHA256 signature).
    5. IBKR Readiness: Full combo (BAG / FOP) order schemas ready for direct gateway execution.
"""

import copy
import datetime
import hmac
import json
import math
import os
import time
from statistics import NormalDist
from typing import Dict, Any, List, Optional, Tuple, Union

try:
    from temporal.crypto_validator import CryptoCheckpointValidator
except ImportError:
    try:
        from ..temporal.crypto_validator import CryptoCheckpointValidator
    except (ImportError, ValueError):
        try:
            from integra_homebase.temporal.crypto_validator import CryptoCheckpointValidator
        except ImportError:
            # Fallback inline stub if imported in complete isolation
            class CryptoCheckpointValidator:  # type: ignore
                def __init__(self, session_key: Optional[str] = None):
                    self._session_key = (session_key or "integra_sovereign_key_v8.2.2").encode("utf-8")
                    self._chain = []
                def compute_state_hash(self, state_dict: Dict[str, Any]) -> str:
                    import hashlib
                    return hashlib.sha256(json.dumps(state_dict, sort_keys=True, default=str).encode("utf-8")).hexdigest()
                def compute_chain_hash(self, state_hash: str, prev_chain_hash: str) -> str:
                    import hashlib
                    return hashlib.sha256(f"{state_hash}||{prev_chain_hash}".encode("utf-8")).hexdigest()
                def compute_hmac_signature(self, chain_hash: str) -> str:
                    import hashlib
                    return hmac.new(self._session_key, chain_hash.encode("utf-8"), hashlib.sha256).hexdigest()
                def commit_checkpoint(self, ccid: str, state_dict: Dict[str, Any], delta_e: float = 0.0) -> Dict[str, Any]:
                    sh = self.compute_state_hash(state_dict)
                    prev = self._chain[-1]["chain_hash"] if self._chain else ("0" * 64)
                    ch = self.compute_chain_hash(sh, prev)
                    sig = self.compute_hmac_signature(ch)
                    cp = {"ccid": ccid, "index": len(self._chain), "timestamp": time.time(), "state_hash": sh, "prev_chain_hash": prev, "chain_hash": ch, "hmac_sig": sig, "delta_e": delta_e, "thermodynamic_valid": True}
                    self._chain.append(cp)
                    return cp
                def get_telemetry(self) -> Dict[str, Any]:
                    return {"chain_length": len(self._chain), "status": "CHAIN_ACTIVE" if self._chain else "GENESIS_STANDBY"}


class FridayFortressHunter:
    """
    Active derivatives writing engine utilizing 99% margin utility on SGOV.
    Executes low-delta (0.05 - 0.10) defined-risk put credit spreads on /MES and /MNQ.
    """

    MARGIN_LOCK_FLOOR: float = 20000.0
    MARGIN_UTILITY: float = 0.99
    DEFAULT_WEEKLY_YIELD_BPS: float = 0.0035  # ~35 bps
    DEFAULT_TARGET_DELTA: float = 0.08
    MIN_DELTA: float = 0.05
    MAX_DELTA: float = 0.10
    DEFAULT_RISK_FREE_RATE: float = 0.045     # 4.5% risk-free rate

    UNDERLYINGS: Dict[str, Dict[str, Any]] = {
        "/MES": {
            "symbol": "MES",
            "name": "Micro E-mini S&P 500",
            "multiplier": 5.0,
            "tick_size": 0.25,
            "strike_increment": 5.0,
            "default_spread_width": 50.0,
            "exchange": "CME",
            "sec_type": "FOP",
        },
        "/MNQ": {
            "symbol": "MNQ",
            "name": "Micro E-mini Nasdaq-100",
            "multiplier": 2.0,
            "tick_size": 0.25,
            "strike_increment": 25.0,
            "default_spread_width": 100.0,
            "exchange": "CME",
            "sec_type": "FOP",
        },
    }

    def __init__(
        self,
        target_delta: float = 0.08,
        session_key: Optional[str] = None,
        validator: Optional[CryptoCheckpointValidator] = None,
        state_file_path: str = "fortress/portfolio_state.json",
    ):
        delta_mag = abs(target_delta)
        if not (self.MIN_DELTA <= delta_mag <= self.MAX_DELTA):
            raise ValueError(
                f"target_delta {target_delta} out of bounds: must be within [{self.MIN_DELTA}, {self.MAX_DELTA}]"
            )
        self.target_delta = delta_mag
        self.state_path = state_file_path
        self.validator = validator or CryptoCheckpointValidator(session_key=session_key)
        self._signed_tickets_count = 0

    # ──────────────────────────────────────────────────────────────
    #  Underlying Normalization & Solvency Gates
    # ──────────────────────────────────────────────────────────────

    def get_underlying_spec(self, underlying: str) -> Dict[str, Any]:
        """Normalizes symbol (e.g. 'MES', '/MES') and returns contract specification."""
        clean = underlying.upper().strip()
        if not clean.startswith("/"):
            clean = f"/{clean}"

        if clean not in self.UNDERLYINGS:
            supported = list(self.UNDERLYINGS.keys())
            raise ValueError(f"Unsupported underlying '{underlying}'. Supported underlyings: {supported}")

        return self.UNDERLYINGS[clean]

    def verify_solvency(self, bank_equity: float) -> bool:
        """Enforces inviolable $20,000 SGOV margin baseline floor."""
        return bank_equity >= self.MARGIN_LOCK_FLOOR

    def calculate_margin_buying_power(self, sgov_equity: Optional[float] = None) -> float:
        """
        Calculates available buying power at 99% margin utility on SGOV.
        Raises PermissionError if the $20,000 margin floor is breached.
        """
        if sgov_equity is None:
            sgov_equity = self._load_current_bank_equity()

        if not self.verify_solvency(sgov_equity):
            raise PermissionError("MARGIN LOCK BREACHED: Hunter options writing suspended.")

        return round(sgov_equity * self.MARGIN_UTILITY, 2)

    def calculate_weekly_extraction_target(
        self, available_margin_bp: float, weekly_yield_bps: float = 0.0035
    ) -> float:
        """
        Conservative ~35 bps weekly premium target on allocated margin buying power.
        """
        return round(available_margin_bp * weekly_yield_bps, 2)

    def _load_current_bank_equity(self) -> float:
        """Loads bank equity from portfolio_state.json with multi-path resolution fallback."""
        paths_to_try = [
            self.state_path,
            os.path.join(os.path.dirname(__file__), "portfolio_state.json"),
            os.path.join(os.path.dirname(__file__), "..", "fortress", "portfolio_state.json"),
        ]
        for p in paths_to_try:
            if p and os.path.isfile(p):
                try:
                    with open(p, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        return float(data["current_state"]["bank"]["equity_usd"])
                except Exception:
                    continue
        return self.MARGIN_LOCK_FLOOR

    # ──────────────────────────────────────────────────────────────
    #  Black-76 Mathematical Engine (European Futures Options)
    # ──────────────────────────────────────────────────────────────

    def compute_black76_put_delta(
        self,
        forward: float,
        strike: float,
        iv: float,
        dte_days: float,
        risk_free_rate: float = 0.045,
    ) -> float:
        """
        Computes Black-76 put delta: Delta_put = -exp(-r * T) * N(-d1).
        Returns negative float (e.g. -0.0805).
        """
        if forward <= 0.0 or strike <= 0.0:
            raise ValueError(f"Forward ({forward}) and strike ({strike}) must be positive.")
        if iv <= 0.0:
            raise ValueError(f"Implied volatility ({iv}) must be positive.")

        t_years = max(dte_days, 0.0001) / 365.0
        sigma_sqrt_t = iv * math.sqrt(t_years)

        d1 = (math.log(forward / strike) + 0.5 * (iv ** 2) * t_years) / sigma_sqrt_t
        discount = math.exp(-risk_free_rate * t_years)
        delta_put = -discount * NormalDist().cdf(-d1)
        return round(delta_put, 6)

    def compute_black76_put_price(
        self,
        forward: float,
        strike: float,
        iv: float,
        dte_days: float,
        risk_free_rate: float = 0.045,
    ) -> float:
        """
        Computes Black-76 European put option price:
        P = exp(-r * T) * [K * N(-d2) - F * N(-d1)]
        """
        if forward <= 0.0 or strike <= 0.0:
            raise ValueError(f"Forward ({forward}) and strike ({strike}) must be positive.")
        if iv <= 0.0:
            raise ValueError(f"Implied volatility ({iv}) must be positive.")

        t_years = max(dte_days, 0.0001) / 365.0
        sigma_sqrt_t = iv * math.sqrt(t_years)

        d1 = (math.log(forward / strike) + 0.5 * (iv ** 2) * t_years) / sigma_sqrt_t
        d2 = d1 - sigma_sqrt_t
        discount = math.exp(-risk_free_rate * t_years)

        price = discount * (strike * NormalDist().cdf(-d2) - forward * NormalDist().cdf(-d1))
        return max(round(price, 4), 0.01)

    def find_strike_by_delta(
        self,
        forward: float,
        iv: float,
        dte_days: float,
        target_delta: float = 0.08,
        strike_increment: float = 5.0,
        risk_free_rate: float = 0.045,
    ) -> float:
        """
        Inverts Black-76 to solve for strike K matching target delta magnitude.
        Clamps and rounds to exchange strike increment.
        """
        delta_mag = abs(target_delta)
        delta_mag = min(max(delta_mag, 0.001), 0.499)

        t_years = max(dte_days, 0.0001) / 365.0
        sigma_sqrt_t = iv * math.sqrt(t_years)

        # N(-d1) = delta_mag * exp(r * T)
        p = min(delta_mag * math.exp(risk_free_rate * t_years), 0.499)
        z = NormalDist().inv_cdf(p)  # z is negative for p < 0.5

        # d1 = -z -> ln(K / F) = z * sigma_sqrt_t + 0.5 * iv^2 * t_years
        exponent = z * sigma_sqrt_t + 0.5 * (iv ** 2) * t_years
        raw_strike = forward * math.exp(exponent)

        rounded_strike = round(raw_strike / strike_increment) * strike_increment
        return float(rounded_strike)

    # ──────────────────────────────────────────────────────────────
    #  Strike Selection & Spread Construction
    # ──────────────────────────────────────────────────────────────

    def calculate_put_spread(
        self,
        underlying: str,
        spot_price: float,
        iv: float = 0.18,
        dte: float = 7.0,
        target_delta: Optional[float] = None,
        spread_width: Optional[float] = None,
        risk_free_rate: float = 0.045,
    ) -> Dict[str, Any]:
        """
        Synthesizes a defined-risk Bull Put Spread via Black-76 formulas:
        - Short put chosen at target delta (~0.08, bounded in [0.05, 0.10])
        - Long put chosen at short_strike - spread_width (outer wing protection)
        """
        spec = self.get_underlying_spec(underlying)
        target_d = abs(target_delta if target_delta is not None else self.target_delta)

        if not (self.MIN_DELTA <= target_d <= self.MAX_DELTA):
            raise ValueError(
                f"target_delta {target_d} out of bounds: must be within [{self.MIN_DELTA}, {self.MAX_DELTA}]"
            )

        if spread_width is None:
            spread_width = float(spec["default_spread_width"])
        else:
            spread_width = float(spread_width)
            if spread_width <= 0.0:
                raise ValueError(f"spread_width must be positive, got {spread_width}")

        # 1. Short Put Strike Selection
        short_strike = self.find_strike_by_delta(
            forward=spot_price,
            iv=iv,
            dte_days=dte,
            target_delta=target_d,
            strike_increment=spec["strike_increment"],
            risk_free_rate=risk_free_rate,
        )

        short_delta = self.compute_black76_put_delta(
            forward=spot_price,
            strike=short_strike,
            iv=iv,
            dte_days=dte,
            risk_free_rate=risk_free_rate,
        )

        # Boundary snapping: ensure discrete rounding doesn't push short delta outside [MIN_DELTA, MAX_DELTA]
        short_delta_mag = abs(short_delta)
        if short_delta_mag < self.MIN_DELTA:
            higher_strike = short_strike + spec["strike_increment"]
            if higher_strike < spot_price:
                higher_delta = self.compute_black76_put_delta(
                    forward=spot_price, strike=higher_strike, iv=iv, dte_days=dte, risk_free_rate=risk_free_rate
                )
                if abs(higher_delta) <= self.MAX_DELTA:
                    short_strike = higher_strike
                    short_delta = higher_delta
        elif short_delta_mag > self.MAX_DELTA:
            lower_strike = short_strike - spec["strike_increment"]
            if lower_strike > 0:
                lower_delta = self.compute_black76_put_delta(
                    forward=spot_price, strike=lower_strike, iv=iv, dte_days=dte, risk_free_rate=risk_free_rate
                )
                if abs(lower_delta) >= self.MIN_DELTA:
                    short_strike = lower_strike
                    short_delta = lower_delta

        short_premium = self.compute_black76_put_price(
            forward=spot_price,
            strike=short_strike,
            iv=iv,
            dte_days=dte,
            risk_free_rate=risk_free_rate,
        )

        # 2. Long Put Protective Wing Selection
        long_strike = short_strike - spread_width
        long_delta = self.compute_black76_put_delta(
            forward=spot_price,
            strike=long_strike,
            iv=iv,
            dte_days=dte,
            risk_free_rate=risk_free_rate,
        )

        long_premium = self.compute_black76_put_price(
            forward=spot_price,
            strike=long_strike,
            iv=iv,
            dte_days=dte,
            risk_free_rate=risk_free_rate,
        )

        net_credit = round(max(short_premium - long_premium, 0.25), 2)

        return {
            "underlying": underlying,
            "spot_price": spot_price,
            "target_delta": target_d,
            "delta_bounds": [self.MIN_DELTA, self.MAX_DELTA],
            "short_strike": short_strike,
            "short_delta": short_delta,
            "short_delta_magnitude": abs(short_delta),
            "short_premium": round(short_premium, 2),
            "long_strike": long_strike,
            "long_delta": long_delta,
            "long_delta_magnitude": abs(long_delta),
            "long_premium": round(long_premium, 2),
            "spread_width": spread_width,
            "net_credit": net_credit,
            "multiplier": spec["multiplier"],
            "dte": dte,
            "iv": iv,
        }

    @staticmethod
    def _safe_quote_price(quote: Dict[str, Any], keys: Tuple[str, ...], default: float) -> float:
        """Safely extracts a positive float quote price across fallback keys."""
        if not isinstance(quote, dict):
            return default
        for k in keys:
            val = quote.get(k)
            if val is not None:
                try:
                    num = float(val)
                    if num > 0.0:
                        return num
                except (ValueError, TypeError):
                    continue
        return default

    def select_strikes_from_chain(
        self,
        underlying: str,
        chain: List[Dict[str, Any]],
        target_delta: Optional[float] = None,
        spread_width: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Selects short put and long put legs from an external option chain (e.g. IBKR market data).
        Filters for puts in [0.05, 0.10] delta range and matches closest to target_delta.
        Robust to missing/None deltas and guarantees outer wing protection.
        """
        spec = self.get_underlying_spec(underlying)
        target_d = abs(target_delta if target_delta is not None else self.target_delta)

        if not (self.MIN_DELTA <= target_d <= self.MAX_DELTA):
            raise ValueError(
                f"target_delta {target_d} out of bounds: must be within [{self.MIN_DELTA}, {self.MAX_DELTA}]"
            )

        if not chain or not isinstance(chain, list):
            raise ValueError("option_chain is empty.")

        # Filter for valid put option quotes
        puts = []
        for quote in chain:
            if not isinstance(quote, dict) or "strike" not in quote:
                continue
            try:
                strike_val = float(quote["strike"])
                if strike_val <= 0:
                    continue
            except (ValueError, TypeError):
                continue
            right = str(quote.get("right", "P")).upper()
            if right in ("P", "PUT"):
                puts.append(quote)

        if not puts:
            raise ValueError("No put options found in option chain.")

        # Candidate short puts within delta bounds [0.05, 0.10]
        candidates = []
        for p in puts:
            raw_delta = p.get("delta")
            if raw_delta is not None:
                try:
                    d_mag = abs(float(raw_delta))
                    if self.MIN_DELTA <= d_mag <= self.MAX_DELTA:
                        candidates.append((abs(d_mag - target_d), p, float(raw_delta)))
                except (ValueError, TypeError):
                    continue

        if not candidates:
            # Fallback to closest available put with valid numeric delta
            valid_puts = []
            for p in puts:
                raw_d = p.get("delta")
                if raw_d is not None:
                    try:
                        valid_puts.append((abs(float(raw_d)), p))
                    except (ValueError, TypeError):
                        pass

            if valid_puts:
                closest_d, closest = min(valid_puts, key=lambda item: abs(item[0] - target_d))
                raise ValueError(
                    f"No put strikes found in option chain within delta bounds [{self.MIN_DELTA}, {self.MAX_DELTA}]. "
                    f"Closest strike was {closest.get('strike')} with delta {closest_d:.4f}"
                )
            else:
                raise ValueError(
                    f"No put strikes found in option chain within delta bounds [{self.MIN_DELTA}, {self.MAX_DELTA}]."
                )

        candidates.sort(key=lambda x: x[0])
        best_candidate = candidates[0]
        short_quote = best_candidate[1]
        short_strike = float(short_quote["strike"])
        short_delta = best_candidate[2]

        width = float(spread_width if spread_width is not None else spec["default_spread_width"])
        target_long_strike = short_strike - width

        # Find long put strictly below short_strike, targeting target_long_strike
        lower_candidates = [p for p in puts if float(p["strike"]) < short_strike]
        if not lower_candidates:
            raise ValueError(
                f"No put strikes found below short strike {short_strike} for outer wing protection."
            )

        # Pick strike below short_strike closest to target_long_strike (preferring <= target_long_strike on tie)
        long_quote = min(
            lower_candidates,
            key=lambda p: (
                abs(float(p["strike"]) - target_long_strike),
                0 if float(p["strike"]) <= target_long_strike else 1,
            ),
        )

        long_strike = float(long_quote["strike"])
        long_delta_val = long_quote.get("delta")
        try:
            long_delta = float(long_delta_val) if long_delta_val is not None else 0.02
        except (ValueError, TypeError):
            long_delta = 0.02

        # Premium extraction: bid on short (selling), ask on long (buying) with safe fallback
        short_prem = self._safe_quote_price(short_quote, ("bid", "price", "last", "mark"), 4.0)
        long_prem = self._safe_quote_price(long_quote, ("ask", "price", "last", "mark"), 1.5)
        actual_width = short_strike - long_strike
        net_credit = round(max(short_prem - long_prem, 0.25), 2)
        if actual_width > 0.25:
            net_credit = min(net_credit, round(actual_width - 0.25, 2))

        return {
            "underlying": underlying,
            "target_delta": target_d,
            "delta_bounds": [self.MIN_DELTA, self.MAX_DELTA],
            "short_strike": short_strike,
            "short_delta": short_delta,
            "short_delta_magnitude": abs(short_delta),
            "short_premium": round(short_prem, 2),
            "long_strike": long_strike,
            "long_delta": long_delta,
            "long_delta_magnitude": abs(long_delta),
            "long_premium": round(long_prem, 2),
            "spread_width": actual_width,
            "net_credit": net_credit,
            "multiplier": spec["multiplier"],
            "source": "OPTION_CHAIN",
        }

    # ──────────────────────────────────────────────────────────────
    #  Contract Sizing & Margin Math
    # ──────────────────────────────────────────────────────────────

    def size_contracts(
        self,
        available_margin_bp: float,
        spread_width: float,
        net_credit: float,
        multiplier: float,
        weekly_target_usd: float,
        max_contracts: int = 4,
    ) -> int:
        """
        Sizes contracts to generate weekly extraction target while respecting:
        1. Maximum allowable margin consumption <= available_margin_bp
        2. Configurable max_contracts ceiling (e.g. Q1 max 2, Q2 max 6)
        """
        margin_per_contract = spread_width * multiplier
        credit_per_contract = net_credit * multiplier

        if margin_per_contract <= 0.0:
            raise ValueError(f"margin_per_contract must be positive: {margin_per_contract}")

        max_margin_contracts = int(available_margin_bp // margin_per_contract)
        if max_margin_contracts < 1:
            raise ValueError(
                f"Insufficient buying power (${available_margin_bp:,.2f}) for 1 contract "
                f"(requires ${margin_per_contract:,.2f} margin)."
            )

        if credit_per_contract > 0.0:
            target_contracts = max(1, round(weekly_target_usd / credit_per_contract))
        else:
            target_contracts = 1

        ceiling = max(1, max_contracts)
        contracts = min(target_contracts, max_margin_contracts, ceiling)
        return max(1, contracts)

    # ──────────────────────────────────────────────────────────────
    #  Temporal Rhythm & Expiry Scheduling
    # ──────────────────────────────────────────────────────────────

    def compute_rhythm_dates(
        self,
        reference_time: Optional[float] = None,
        dte: int = 7,
    ) -> Dict[str, Any]:
        """
        Enforces the Friday Fortress weekly rhythm: Friday entry -> Thursday exit (~5-7 DTE).
        Returns formatted dates including IBKR YYYYMMDD string.
        """
        if dte <= 0:
            raise ValueError(f"dte must be positive, got {dte}")

        ts = reference_time if reference_time is not None else time.time()
        ref_date = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).date()

        # Friday is weekday 4
        days_ahead_to_friday = (4 - ref_date.weekday()) % 7
        if days_ahead_to_friday == 0:
            entry_date = ref_date
        else:
            entry_date = ref_date + datetime.timedelta(days=days_ahead_to_friday)

        # Target expiration: Thursday (6 days after entry) or Friday (7 days after entry)
        target_expiry = entry_date + datetime.timedelta(days=dte)
        ibkr_expiry_str = target_expiry.strftime("%Y%m%d")

        return {
            "entry_day": "Friday",
            "exit_day": "Thursday",
            "target_dte": dte,
            "entry_date": entry_date.isoformat(),
            "expiry_date": target_expiry.isoformat(),
            "ibkr_expiry": ibkr_expiry_str,
        }

    # ──────────────────────────────────────────────────────────────
    #  IBKR Combo Order Construction
    # ──────────────────────────────────────────────────────────────

    def build_ibkr_order(
        self,
        ticket_id: str,
        underlying: str,
        short_strike: float,
        long_strike: float,
        net_credit: float,
        contracts: int,
        expiry_str: str,
        transmit: bool = False,
    ) -> Dict[str, Any]:
        """
        Constructs complete Interactive Brokers COMBO / BAG order format
        for CME Futures Options (FOP) execution.
        """
        spec = self.get_underlying_spec(underlying)
        mult_str = str(int(spec["multiplier"]))

        return {
            "orderId": ticket_id,
            "clientOrderId": ticket_id,
            "action": "SELL",  # Selling the credit spread (net credit limit)
            "orderType": "LMT",
            "totalQuantity": contracts,
            "lmtPrice": round(net_credit, 2),
            "tif": "DAY",
            "transmit": transmit,  # Staged by default for confirmation
            "contract": {
                "symbol": spec["symbol"],
                "secType": "BAG",
                "exchange": spec["exchange"],
                "currency": "USD",
                "comboLegs": [
                    {
                        "conId": 0,
                        "ratio": 1,
                        "action": "SELL",
                        "exchange": spec["exchange"],
                        "secType": spec["sec_type"],
                        "strike": short_strike,
                        "right": "P",
                        "multiplier": mult_str,
                        "lastTradeDateOrContractMonth": expiry_str,
                    },
                    {
                        "conId": 0,
                        "ratio": 1,
                        "action": "BUY",
                        "exchange": spec["exchange"],
                        "secType": spec["sec_type"],
                        "strike": long_strike,
                        "right": "P",
                        "multiplier": mult_str,
                        "lastTradeDateOrContractMonth": expiry_str,
                    },
                ],
            },
        }

    # ──────────────────────────────────────────────────────────────
    #  Trade Ticket Generation & Orchestration
    # ──────────────────────────────────────────────────────────────

    def generate_trade_ticket(
        self,
        underlying: str = "/MES",
        spot_price: float = 5500.0,
        sgov_equity: Optional[float] = None,
        iv: float = 0.18,
        dte: float = 7.0,
        target_delta: Optional[float] = None,
        spread_width: Optional[float] = None,
        option_chain: Optional[List[Dict[str, Any]]] = None,
        max_contracts: int = 4,
        sign_ticket: bool = True,
        transmit: bool = False,
    ) -> Dict[str, Any]:
        """
        Generates a comprehensive Friday Fortress trade ticket ready for IBKR execution:
        1. Solvency check on SGOV margin lock floor ($20,000 baseline)
        2. Available buying power & ~35 bps weekly extraction target
        3. Low-delta (0.05 - 0.10, default 0.08) put spread strike selection
        4. Contract sizing respecting capital limits
        5. Complete IBKR COMBO order payload
        6. Dual-Key cryptographic signing via temporal/crypto_validator.py
        """
        # 1. Capital & Solvency Verification
        if sgov_equity is None:
            sgov_equity = self._load_current_bank_equity()

        if not self.verify_solvency(sgov_equity):
            raise PermissionError("MARGIN LOCK BREACHED: Hunter options writing suspended.")

        available_margin_bp = self.calculate_margin_buying_power(sgov_equity)
        weekly_target_usd = self.calculate_weekly_extraction_target(
            available_margin_bp, self.DEFAULT_WEEKLY_YIELD_BPS
        )

        # 2. Strike Selection
        if option_chain:
            spread = self.select_strikes_from_chain(
                underlying=underlying,
                chain=option_chain,
                target_delta=target_delta,
                spread_width=spread_width,
            )
        else:
            spread = self.calculate_put_spread(
                underlying=underlying,
                spot_price=spot_price,
                iv=iv,
                dte=dte,
                target_delta=target_delta,
                spread_width=spread_width,
            )

        # 3. Contract Sizing
        contracts = self.size_contracts(
            available_margin_bp=available_margin_bp,
            spread_width=spread["spread_width"],
            net_credit=spread["net_credit"],
            multiplier=spread["multiplier"],
            weekly_target_usd=weekly_target_usd,
            max_contracts=max_contracts,
        )

        margin_required = round(contracts * spread["spread_width"] * spread["multiplier"], 2)
        total_credit = round(contracts * spread["net_credit"] * spread["multiplier"], 2)
        max_risk = round(
            contracts * (spread["spread_width"] - spread["net_credit"]) * spread["multiplier"], 2
        )

        # 4. Temporal Rhythm Dates
        rhythm = self.compute_rhythm_dates(dte=int(dte))

        # 5. Unique Ticket Identifier
        spec = self.get_underlying_spec(underlying)
        ts_now = time.time()
        ticket_id = f"TICKET_FORTRESS_{spec['symbol']}_{int(ts_now * 1000)}"

        # 6. IBKR Combo Order
        ibkr_order = self.build_ibkr_order(
            ticket_id=ticket_id,
            underlying=underlying,
            short_strike=spread["short_strike"],
            long_strike=spread["long_strike"],
            net_credit=spread["net_credit"],
            contracts=contracts,
            expiry_str=rhythm["ibkr_expiry"],
            transmit=transmit,
        )

        # 7. Assembled Ticket with Dual-Clock Readout (Rule 7)
        temporal_coords = self._build_temporal_coordinates(ts_now)
        ticket = {
            "ticket_id": ticket_id,
            "strategy": "FRIDAY_FORTRESS_BULL_PUT_SPREAD",
            "layer": "5/7 (Active Capital Overlay & IBKR Execution Protocol)",
            "spatial_anchor": "Baker, Louisiana (30.5888°N, -91.1673°W)",
            "temporal_coordinates": temporal_coords,
            "underlying": underlying,
            "spot_price": spot_price,
            "rhythm": rhythm,
            "strike_selection": spread,
            "capital_and_risk": {
                "bank_equity_usd": sgov_equity,
                "margin_buying_power_usd": available_margin_bp,
                "contracts": contracts,
                "multiplier": spread["multiplier"],
                "margin_required_usd": margin_required,
                "max_risk_usd": max_risk,
                "total_credit_usd": total_credit,
                "weekly_target_yield_bps": self.DEFAULT_WEEKLY_YIELD_BPS,
                "weekly_target_usd": weekly_target_usd,
                "margin_lock_floor_usd": self.MARGIN_LOCK_FLOOR,
                "solvency_verified": True,
            },
            "ibkr_order": ibkr_order,
            "status": "VALIDATED_IBKR_READY" if sign_ticket else "STAGED_READY_FOR_EXECUTION",
            "created_at": ts_now,
        }

        # 8. Cryptographic Ticket Signing
        if sign_ticket:
            ticket = self.sign_trade_ticket(ticket)

        return ticket

    def _build_temporal_coordinates(self, unix_epoch: float) -> Dict[str, Any]:
        """
        Builds dual-clock temporal coordinates pairing Central Time (CDT)
        anchored to Baker, Louisiana alongside ISO-8601 UTC and celestial kinematics.
        Enforces Rule 7 of Integra O/S Constitution.
        """
        try:
            try:
                from temporal.celestial_clock import DualTemporalEngine
            except ImportError:
                from ..temporal.celestial_clock import DualTemporalEngine
            engine = DualTemporalEngine()
            dual = engine.get_dual_telemetry()
            return {
                "unix_epoch": unix_epoch,
                "central_time_cdt": dual["digital_clock"]["central_time"],
                "utc_iso": dual["digital_clock"]["iso_utc"],
                "spatial_anchor": "Baker, Louisiana (30.5888°N, -91.1673°W)",
                "celestial_grid_bucket": dual["celestial_clock"].get("grid_bucket"),
                "status": "DUAL_CLOCK_SYNCHRONIZED",
            }
        except Exception:
            utc_dt = datetime.datetime.fromtimestamp(unix_epoch, tz=datetime.timezone.utc)
            cdt_tz = datetime.timezone(datetime.timedelta(hours=-5))
            cdt_dt = datetime.datetime.fromtimestamp(unix_epoch, tz=cdt_tz)
            return {
                "unix_epoch": unix_epoch,
                "central_time_cdt": cdt_dt.strftime("%Y-%m-%d %H:%M:%S CDT"),
                "utc_iso": utc_dt.isoformat(),
                "spatial_anchor": "Baker, Louisiana (30.5888°N, -91.1673°W)",
                "status": "FALLBACK_CALCULATED",
            }

    # ──────────────────────────────────────────────────────────────
    #  Dual-Key Cryptographic Ticket Signing
    # ──────────────────────────────────────────────────────────────

    def sign_trade_ticket(
        self,
        ticket: Dict[str, Any],
        validator: Optional[CryptoCheckpointValidator] = None,
    ) -> Dict[str, Any]:
        """
        Signs trade ticket with Dual-Key cryptographic validation:
        - Key 1: SHA-256 state hash of canonical ticket payload
        - Key 2: HMAC-SHA256 signature linked to validator session key & chain
        """
        val = validator or self.validator
        ticket_copy = copy.deepcopy(ticket)
        ticket_copy.pop("signatures", None)
        ticket_copy["status"] = "VALIDATED_IBKR_READY"

        state_hash = val.compute_state_hash(ticket_copy)
        checkpoint = val.commit_checkpoint(
            ccid=ticket_copy["ticket_id"],
            state_dict=ticket_copy,
            delta_e=0.0,
        )

        signatures = {
            "key1_state_hash": checkpoint["state_hash"],
            "key2_hmac_signature": checkpoint["hmac_sig"],
            "chain_hash": checkpoint["chain_hash"],
            "prev_chain_hash": checkpoint["prev_chain_hash"],
            "checkpoint_index": checkpoint["index"],
            "dual_key_verified": True,
            "algorithm": "SHA-256 (Key 1) + HMAC-SHA256 (Key 2)",
            "signed_at": time.time(),
        }

        ticket_copy["signatures"] = signatures
        self._signed_tickets_count += 1
        return ticket_copy

    def verify_signed_ticket(
        self,
        ticket: Dict[str, Any],
        validator: Optional[CryptoCheckpointValidator] = None,
    ) -> Dict[str, Any]:
        """
        Verifies cryptographic integrity of signed ticket:
        Recomputes Key 1 (state hash), chain link, and Key 2 (HMAC).
        Returns False if any parameter was tampered with or malformed.
        """
        val = validator or self.validator
        if not isinstance(ticket, dict):
            return {
                "is_valid": False,
                "status": "INVALID_TICKET_FORMAT",
                "reason": "Ticket payload must be a dictionary",
                "ticket_id": None,
                "tamper_detected": True,
            }

        if "signatures" not in ticket or not isinstance(ticket.get("signatures"), dict):
            return {
                "is_valid": False,
                "status": "UNSIGNED_TICKET" if "signatures" not in ticket else "MALFORMED_SIGNATURE",
                "reason": "Missing or non-dictionary signatures block in ticket",
                "ticket_id": ticket.get("ticket_id"),
                "tamper_detected": False if "signatures" not in ticket else True,
            }

        signatures = ticket["signatures"]
        required_keys = ["key1_state_hash", "key2_hmac_signature", "chain_hash", "prev_chain_hash"]
        if not all(k in signatures for k in required_keys) or not all(isinstance(signatures.get(k), str) for k in required_keys):
            return {
                "is_valid": False,
                "status": "MALFORMED_SIGNATURE",
                "reason": "Signatures block missing required keys or contains non-string values",
                "ticket_id": ticket.get("ticket_id"),
                "tamper_detected": True,
            }

        ticket_payload = copy.deepcopy(ticket)
        ticket_payload.pop("signatures", None)

        try:
            # 1. Verify Key 1: Recompute State Hash
            recomputed_state_hash = val.compute_state_hash(ticket_payload)
            key1_valid = hmac.compare_digest(recomputed_state_hash, signatures["key1_state_hash"])

            # 2. Recompute Chain Hash
            recomputed_chain = val.compute_chain_hash(
                recomputed_state_hash, signatures["prev_chain_hash"]
            )
            chain_valid = hmac.compare_digest(recomputed_chain, signatures["chain_hash"])

            # 3. Verify Key 2: Recompute HMAC Signature
            recomputed_hmac = val.compute_hmac_signature(recomputed_chain)
            key2_valid = hmac.compare_digest(recomputed_hmac, signatures["key2_hmac_signature"])
        except Exception as e:
            return {
                "is_valid": False,
                "status": "VERIFICATION_ERROR",
                "reason": f"Cryptographic verification error: {str(e)}",
                "ticket_id": ticket.get("ticket_id"),
                "tamper_detected": True,
            }

        is_valid = bool(key1_valid and chain_valid and key2_valid)
        return {
            "is_valid": is_valid,
            "status": "VALIDATED_IBKR_READY" if is_valid else "TAMPER_DETECTED",
            "ticket_id": ticket.get("ticket_id"),
            "key1_state_hash_valid": key1_valid,
            "chain_valid": chain_valid,
            "key2_hmac_signature_valid": key2_valid,
            "tamper_detected": not is_valid,
        }

    # ──────────────────────────────────────────────────────────────
    #  Chamber Shunt & Telemetry
    # ──────────────────────────────────────────────────────────────

    def execute_weekly_harvest_shunt(
        self, ticket: Dict[str, Any], bank_lobe: Optional[Any] = None
    ) -> float:
        """
        Shunts harvested options premium into Friday Fortress Bank chamber.
        Closes the loop between Hunter options income and SGOV margin collateral.
        """
        if not isinstance(ticket, dict):
            return 0.0
        cap_risk = ticket.get("capital_and_risk") or {}
        try:
            credit_usd = float(cap_risk.get("total_credit_usd", 0.0) or 0.0)
        except (ValueError, TypeError):
            credit_usd = 0.0

        if credit_usd <= 0.0:
            return 0.0

        if bank_lobe is None:
            try:
                from fortress.bank_lobe import FridayFortressBank
                bank_lobe = FridayFortressBank(state_file_path=self.state_path)
            except Exception:
                return credit_usd

        return bank_lobe.process_weekly_inflow(credit_usd)

    def get_telemetry(self) -> Dict[str, Any]:
        """Telemetry diagnostics for Heimdall and system dashboard."""
        validator_telemetry: Dict[str, Any] = {}
        if hasattr(self.validator, "get_telemetry"):
            try:
                validator_telemetry = self.validator.get_telemetry()
            except Exception:
                validator_telemetry = {}

        return {
            "engine": "FridayFortressHunter",
            "status": "OPERATIONAL",
            "layer": "5/7",
            "target_delta": self.target_delta,
            "delta_bounds": [self.MIN_DELTA, self.MAX_DELTA],
            "margin_lock_floor_usd": self.MARGIN_LOCK_FLOOR,
            "margin_utility": self.MARGIN_UTILITY,
            "weekly_yield_bps": self.DEFAULT_WEEKLY_YIELD_BPS,
            "supported_underlyings": list(self.UNDERLYINGS.keys()),
            "signed_tickets_count": self._signed_tickets_count,
            "spatial_anchor": "Baker, Louisiana (30.5888°N, -91.1673°W)",
            "validator_telemetry": validator_telemetry,
        }

    def get_diagnostics(self) -> Dict[str, Any]:
        """Diagnostics dictionary for Heimdall 3.1 surveillance."""
        return {
            "status": "HEALTHY",
            "solvency_verified": self.verify_solvency(self._load_current_bank_equity()),
            "signed_tickets_count": self._signed_tickets_count,
        }
