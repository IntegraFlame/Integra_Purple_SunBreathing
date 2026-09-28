"""
INTEGRA O/S: FRIDAY FORTRESS - HUNTER ENGINE TEST SUITE
Module: tests/test_fortress_hunter.py
Layer: 5/7 (Active Capital Overlay & IBKR Execution Protocol)
Coordinates: 30.5888°N, -91.1673°W (Baker, Louisiana)
"""

import copy
import os
import sys
import pytest

# Ensure homebase root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fortress.hunter_engine import FridayFortressHunter
from fortress.bank_lobe import FridayFortressBank
from temporal.crypto_validator import CryptoCheckpointValidator


# ──────────────────────────────────────────────────────────────
#  1. SOLVENCY & CAPITAL MARGIN LOCK TESTS
# ──────────────────────────────────────────────────────────────

def test_solvency_and_margin_lock_floor():
    hunter = FridayFortressHunter()
    assert hunter.verify_solvency(20000.0) is True
    assert hunter.verify_solvency(25000.0) is True
    assert hunter.verify_solvency(19999.99) is False
    assert hunter.verify_solvency(0.0) is False


def test_margin_buying_power_calculation():
    hunter = FridayFortressHunter()
    # Nominal baseline: $20,000 * 0.99 = $19,800
    bp = hunter.calculate_margin_buying_power(20000.0)
    assert bp == 19800.0

    # Scaled equity: $50,000 * 0.99 = $49,500
    assert hunter.calculate_margin_buying_power(50000.0) == 49500.0


def test_margin_lock_floor_breach_raises_permission_error():
    hunter = FridayFortressHunter()
    with pytest.raises(PermissionError, match="MARGIN LOCK BREACHED: Hunter options writing suspended."):
        hunter.calculate_margin_buying_power(19999.0)

    with pytest.raises(PermissionError, match="MARGIN LOCK BREACHED: Hunter options writing suspended."):
        hunter.generate_trade_ticket(underlying="/MES", sgov_equity=15000.0)


def test_weekly_extraction_target_35bps():
    hunter = FridayFortressHunter()
    # 35 bps on $19,800 buying power = $69.30
    target = hunter.calculate_weekly_extraction_target(19800.0, weekly_yield_bps=0.0035)
    assert target == 69.30

    # Custom bps
    target_50bps = hunter.calculate_weekly_extraction_target(20000.0, weekly_yield_bps=0.0050)
    assert target_50bps == 100.0


# ──────────────────────────────────────────────────────────────
#  2. UNDERLYING SPECIFICATIONS & TARGET DELTA BOUNDS
# ──────────────────────────────────────────────────────────────

def test_underlying_specifications():
    hunter = FridayFortressHunter()

    # /MES specifications
    mes_spec = hunter.get_underlying_spec("/MES")
    assert mes_spec["symbol"] == "MES"
    assert mes_spec["multiplier"] == 5.0
    assert mes_spec["strike_increment"] == 5.0
    assert mes_spec["default_spread_width"] == 50.0
    assert mes_spec["exchange"] == "CME"

    # Normalized 'MES' without slash
    assert hunter.get_underlying_spec("MES") == mes_spec

    # /MNQ specifications
    mnq_spec = hunter.get_underlying_spec("/MNQ")
    assert mnq_spec["symbol"] == "MNQ"
    assert mnq_spec["multiplier"] == 2.0
    assert mnq_spec["strike_increment"] == 25.0
    assert mnq_spec["default_spread_width"] == 100.0
    assert mnq_spec["exchange"] == "CME"

    assert hunter.get_underlying_spec("MNQ") == mnq_spec


def test_unsupported_underlying_raises_value_error():
    hunter = FridayFortressHunter()
    with pytest.raises(ValueError, match="Unsupported underlying"):
        hunter.get_underlying_spec("SPY")

    with pytest.raises(ValueError, match="Unsupported underlying"):
        hunter.generate_trade_ticket(underlying="/ES")


def test_target_delta_bounds_validation():
    # Valid delta ranges: [0.05, 0.10]
    hunter_default = FridayFortressHunter(target_delta=0.08)
    assert hunter_default.target_delta == 0.08

    hunter_low = FridayFortressHunter(target_delta=0.05)
    assert hunter_low.target_delta == 0.05

    hunter_high = FridayFortressHunter(target_delta=0.10)
    assert hunter_high.target_delta == 0.10

    # Negative delta representation accepted via magnitude
    hunter_neg = FridayFortressHunter(target_delta=-0.08)
    assert hunter_neg.target_delta == 0.08

    # Out of bounds delta values
    with pytest.raises(ValueError, match="out of bounds"):
        FridayFortressHunter(target_delta=0.04)

    with pytest.raises(ValueError, match="out of bounds"):
        FridayFortressHunter(target_delta=0.15)


# ──────────────────────────────────────────────────────────────
#  3. BLACK-76 MATH & PUT SPREAD SYNTHESIS
# ──────────────────────────────────────────────────────────────

def test_black76_put_delta_and_pricing():
    hunter = FridayFortressHunter()
    spot = 5500.0
    iv = 0.18
    dte = 7.0

    # OTM Put: strike 5300
    delta_otm = hunter.compute_black76_put_delta(spot, 5300.0, iv, dte)
    price_otm = hunter.compute_black76_put_price(spot, 5300.0, iv, dte)

    assert -1.0 < delta_otm < 0.0
    assert abs(delta_otm) < 0.20  # Far OTM
    assert price_otm > 0.0

    # ATM Put: strike 5500
    delta_atm = hunter.compute_black76_put_delta(spot, 5500.0, iv, dte)
    price_atm = hunter.compute_black76_put_price(spot, 5500.0, iv, dte)

    assert abs(delta_atm + 0.50) < 0.05  # Around -0.50
    assert price_atm > price_otm


def test_find_strike_by_delta():
    hunter = FridayFortressHunter()
    spot = 5500.0
    iv = 0.18
    dte = 7.0
    target_d = 0.08

    strike = hunter.find_strike_by_delta(
        forward=spot,
        iv=iv,
        dte_days=dte,
        target_delta=target_d,
        strike_increment=5.0,
    )

    # Strike must be OTM (K < F) and aligned to 5.0 increment
    assert strike < spot
    assert strike % 5.0 == 0.0

    # Verify actual delta of found strike falls within [0.05, 0.10]
    actual_delta = hunter.compute_black76_put_delta(spot, strike, iv, dte)
    assert 0.05 <= abs(actual_delta) <= 0.10


def test_calculate_put_spread_mes():
    hunter = FridayFortressHunter(target_delta=0.08)
    spot = 5500.0
    spread = hunter.calculate_put_spread("/MES", spot_price=spot, iv=0.18, dte=7.0)

    assert spread["underlying"] == "/MES"
    assert spread["multiplier"] == 5.0
    assert spread["spread_width"] == 50.0
    assert spread["short_strike"] < spot
    assert spread["long_strike"] == spread["short_strike"] - 50.0

    # Delta of short strike must satisfy the 0.05-0.10 constraint
    assert 0.05 <= spread["short_delta_magnitude"] <= 0.10
    # Long strike is further OTM, so long delta magnitude must be smaller than short delta
    assert spread["long_delta_magnitude"] < spread["short_delta_magnitude"]

    # Net credit must be positive (short premium > long premium)
    assert spread["net_credit"] > 0.0
    assert spread["short_premium"] > spread["long_premium"]


def test_calculate_put_spread_mnq():
    hunter = FridayFortressHunter(target_delta=0.08)
    spot = 19500.0
    spread = hunter.calculate_put_spread("/MNQ", spot_price=spot, iv=0.22, dte=7.0)

    assert spread["underlying"] == "/MNQ"
    assert spread["multiplier"] == 2.0
    assert spread["spread_width"] == 100.0
    assert spread["short_strike"] < spot
    assert spread["long_strike"] == spread["short_strike"] - 100.0
    assert 0.05 <= spread["short_delta_magnitude"] <= 0.10
    assert spread["net_credit"] > 0.0


# ──────────────────────────────────────────────────────────────
#  4. OPTION CHAIN STRIKE SELECTION
# ──────────────────────────────────────────────────────────────

def test_select_strikes_from_chain_success():
    hunter = FridayFortressHunter(target_delta=0.08)
    mock_chain = [
        {"strike": 5400.0, "delta": -0.22, "bid": 18.0, "ask": 18.5, "right": "P"},
        {"strike": 5350.0, "delta": -0.14, "bid": 10.0, "ask": 10.5, "right": "P"},
        {"strike": 5320.0, "delta": -0.095, "bid": 6.5, "ask": 7.0, "right": "P"},
        {"strike": 5310.0, "delta": -0.081, "bid": 5.25, "ask": 5.5, "right": "P"},  # Ideal 0.08 delta
        {"strike": 5300.0, "delta": -0.068, "bid": 4.0, "ask": 4.25, "right": "P"},
        {"strike": 5260.0, "delta": -0.032, "bid": 2.25, "ask": 2.5, "right": "P"},  # Long wing (50 pt spread)
        {"strike": 5200.0, "delta": -0.015, "bid": 1.0, "ask": 1.25, "right": "P"},
    ]

    selected = hunter.select_strikes_from_chain("/MES", mock_chain, spread_width=50.0)

    assert selected["short_strike"] == 5310.0
    assert selected["short_delta"] == -0.081
    assert selected["long_strike"] == 5260.0
    assert selected["spread_width"] == 50.0
    # Net credit: short bid (5.25) - long ask (2.5) = 2.75
    assert selected["net_credit"] == 2.75


def test_select_strikes_from_chain_no_matches_raises():
    hunter = FridayFortressHunter(target_delta=0.08)
    chain_high_deltas = [
        {"strike": 5500.0, "delta": -0.50, "bid": 30.0, "ask": 31.0, "right": "P"},
        {"strike": 5450.0, "delta": -0.35, "bid": 20.0, "ask": 21.0, "right": "P"},
    ]
    with pytest.raises(ValueError, match="No put strikes found in option chain within delta bounds"):
        hunter.select_strikes_from_chain("/MES", chain_high_deltas)


# ──────────────────────────────────────────────────────────────
#  5. CONTRACT SIZING & RISK MATH
# ──────────────────────────────────────────────────────────────

def test_size_contracts():
    hunter = FridayFortressHunter()
    available_bp = 19800.0
    spread_width = 50.0
    net_credit = 2.50
    multiplier = 5.0
    weekly_target = 69.30

    contracts = hunter.size_contracts(
        available_margin_bp=available_bp,
        spread_width=spread_width,
        net_credit=net_credit,
        multiplier=multiplier,
        weekly_target_usd=weekly_target,
        max_contracts=4,
    )

    # Margin per contract: 50 * 5 = $250
    # Credit per contract: 2.50 * 5 = $12.50
    # Target contracts: 69.30 / 12.50 = ~6 contracts, capped by max_contracts=4
    assert contracts == 4

    # Test when buying power allows fewer contracts
    tight_bp = 500.0  # Only covers 2 contracts ($250 * 2 = $500)
    tight_contracts = hunter.size_contracts(
        available_margin_bp=tight_bp,
        spread_width=spread_width,
        net_credit=net_credit,
        multiplier=multiplier,
        weekly_target_usd=weekly_target,
        max_contracts=10,
    )
    assert tight_contracts == 2


def test_size_contracts_insufficient_margin_raises():
    hunter = FridayFortressHunter()
    with pytest.raises(ValueError, match="Insufficient buying power"):
        hunter.size_contracts(
            available_margin_bp=200.0,  # Less than $250 needed for 1 /MES contract
            spread_width=50.0,
            net_credit=2.50,
            multiplier=5.0,
            weekly_target_usd=69.30,
        )


# ──────────────────────────────────────────────────────────────
#  6. TEMPORAL RHYTHM & IBKR SCHEDULING
# ──────────────────────────────────────────────────────────────

def test_compute_rhythm_dates():
    hunter = FridayFortressHunter()
    rhythm = hunter.compute_rhythm_dates(dte=7)

    assert rhythm["entry_day"] == "Friday"
    assert rhythm["exit_day"] == "Thursday"
    assert rhythm["target_dte"] == 7
    assert len(rhythm["ibkr_expiry"]) == 8  # YYYYMMDD
    assert rhythm["ibkr_expiry"].isdigit()


# ──────────────────────────────────────────────────────────────
#  7. IBKR COMBO ORDER FORMULATION
# ──────────────────────────────────────────────────────────────

def test_build_ibkr_order_format():
    hunter = FridayFortressHunter()
    order = hunter.build_ibkr_order(
        ticket_id="TICKET_TEST_001",
        underlying="/MES",
        short_strike=5310.0,
        long_strike=5260.0,
        net_credit=2.75,
        contracts=2,
        expiry_str="20261002",
    )

    assert order["orderId"] == "TICKET_TEST_001"
    assert order["action"] == "SELL"
    assert order["orderType"] == "LMT"
    assert order["lmtPrice"] == 2.75
    assert order["totalQuantity"] == 2
    assert order["transmit"] is False

    contract = order["contract"]
    assert contract["symbol"] == "MES"
    assert contract["secType"] == "BAG"
    assert contract["exchange"] == "CME"
    assert contract["currency"] == "USD"
    assert len(contract["comboLegs"]) == 2

    # Leg 1: Short Put
    leg1 = contract["comboLegs"][0]
    assert leg1["action"] == "SELL"
    assert leg1["ratio"] == 1
    assert leg1["strike"] == 5310.0
    assert leg1["right"] == "P"
    assert leg1["multiplier"] == "5"
    assert leg1["lastTradeDateOrContractMonth"] == "20261002"

    # Leg 2: Long Put (Protective Wing)
    leg2 = contract["comboLegs"][1]
    assert leg2["action"] == "BUY"
    assert leg2["ratio"] == 1
    assert leg2["strike"] == 5260.0
    assert leg2["right"] == "P"
    assert leg2["multiplier"] == "5"
    assert leg2["lastTradeDateOrContractMonth"] == "20261002"


# ──────────────────────────────────────────────────────────────
#  8. DUAL-KEY CRYPTOGRAPHIC SIGNING & TAMPER EVIDENCE
# ──────────────────────────────────────────────────────────────

def test_generate_and_sign_trade_ticket():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(
        underlying="/MES",
        spot_price=5500.0,
        sgov_equity=20000.0,
        iv=0.18,
        dte=7.0,
        sign_ticket=True,
    )

    assert ticket["status"] == "VALIDATED_IBKR_READY"
    assert ticket["strategy"] == "FRIDAY_FORTRESS_BULL_PUT_SPREAD"
    assert "signatures" in ticket

    sigs = ticket["signatures"]
    assert "key1_state_hash" in sigs
    assert "key2_hmac_signature" in sigs
    assert "chain_hash" in sigs
    assert "prev_chain_hash" in sigs
    assert sigs["dual_key_verified"] is True
    assert len(sigs["key1_state_hash"]) == 64
    assert len(sigs["key2_hmac_signature"]) == 64

    # Verification must pass
    verification = hunter.verify_signed_ticket(ticket)
    assert verification["is_valid"] is True
    assert verification["key1_state_hash_valid"] is True
    assert verification["chain_valid"] is True
    assert verification["key2_hmac_signature_valid"] is True
    assert verification["tamper_detected"] is False
    assert verification["status"] == "VALIDATED_IBKR_READY"


def test_tamper_detection_on_contract_modification():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(
        underlying="/MES",
        spot_price=5500.0,
        sgov_equity=20000.0,
        sign_ticket=True,
    )

    # Tamper with contract count
    tampered_ticket = copy.deepcopy(ticket)
    tampered_ticket["capital_and_risk"]["contracts"] = 999

    res = hunter.verify_signed_ticket(tampered_ticket)
    assert res["is_valid"] is False
    assert res["key1_state_hash_valid"] is False
    assert res["tamper_detected"] is True
    assert res["status"] == "TAMPER_DETECTED"


def test_tamper_detection_on_strike_price_modification():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(
        underlying="/MES",
        spot_price=5500.0,
        sgov_equity=20000.0,
        sign_ticket=True,
    )

    tampered_ticket = copy.deepcopy(ticket)
    tampered_ticket["strike_selection"]["short_strike"] = 6000.0

    res = hunter.verify_signed_ticket(tampered_ticket)
    assert res["is_valid"] is False
    assert res["tamper_detected"] is True


def test_tamper_detection_on_ibkr_order_modification():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(
        underlying="/MES",
        spot_price=5500.0,
        sgov_equity=20000.0,
        sign_ticket=True,
    )

    tampered_ticket = copy.deepcopy(ticket)
    tampered_ticket["ibkr_order"]["lmtPrice"] = 99.99

    res = hunter.verify_signed_ticket(tampered_ticket)
    assert res["is_valid"] is False
    assert res["tamper_detected"] is True


def test_tamper_detection_on_hmac_forgery():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(
        underlying="/MES",
        spot_price=5500.0,
        sgov_equity=20000.0,
        sign_ticket=True,
    )

    tampered_ticket = copy.deepcopy(ticket)
    # Alter the HMAC signature string
    tampered_ticket["signatures"]["key2_hmac_signature"] = "0" * 64

    res = hunter.verify_signed_ticket(tampered_ticket)
    assert res["is_valid"] is False
    assert res["key2_hmac_signature_valid"] is False
    assert res["tamper_detected"] is True


def test_unsigned_ticket_verification():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(
        underlying="/MES",
        spot_price=5500.0,
        sgov_equity=20000.0,
        sign_ticket=False,
    )

    assert "signatures" not in ticket
    res = hunter.verify_signed_ticket(ticket)
    assert res["is_valid"] is False
    assert res["status"] == "UNSIGNED_TICKET"


def test_cross_session_key_verification_fails():
    validator1 = CryptoCheckpointValidator(session_key="session_alpha")
    validator2 = CryptoCheckpointValidator(session_key="session_beta")

    hunter1 = FridayFortressHunter(validator=validator1)
    hunter2 = FridayFortressHunter(validator=validator2)

    ticket1 = hunter1.generate_trade_ticket(underlying="/MES", sgov_equity=20000.0, sign_ticket=True)

    # Valid under hunter1
    assert hunter1.verify_signed_ticket(ticket1)["is_valid"] is True

    # Invalid under hunter2 due to mismatched HMAC session key
    assert hunter2.verify_signed_ticket(ticket1)["is_valid"] is False


# ──────────────────────────────────────────────────────────────
#  9. MNQ TRADE TICKET GENERATION
# ──────────────────────────────────────────────────────────────

def test_mnq_trade_ticket_generation():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(
        underlying="/MNQ",
        spot_price=19500.0,
        sgov_equity=25000.0,
        iv=0.22,
        dte=7.0,
        max_contracts=4,
        sign_ticket=True,
    )

    assert ticket["underlying"] == "/MNQ"
    assert ticket["capital_and_risk"]["multiplier"] == 2.0
    assert ticket["ibkr_order"]["contract"]["symbol"] == "MNQ"
    assert ticket["status"] == "VALIDATED_IBKR_READY"

    # Verify signature
    assert hunter.verify_signed_ticket(ticket)["is_valid"] is True


# ──────────────────────────────────────────────────────────────
#  10. TELEMETRY & CHAMBER INFLOW SHUNT
# ──────────────────────────────────────────────────────────────

def test_telemetry_and_diagnostics():
    hunter = FridayFortressHunter(target_delta=0.08)
    telemetry = hunter.get_telemetry()

    assert telemetry["engine"] == "FridayFortressHunter"
    assert telemetry["status"] == "OPERATIONAL"
    assert telemetry["target_delta"] == 0.08
    assert telemetry["margin_lock_floor_usd"] == 20000.0
    assert "/MES" in telemetry["supported_underlyings"]
    assert "/MNQ" in telemetry["supported_underlyings"]

    diagnostics = hunter.get_diagnostics()
    assert diagnostics["status"] == "HEALTHY"
    assert diagnostics["solvency_verified"] is True


def test_chamber_harvest_shunt(tmp_path):
    # Test shunt into FridayFortressBank
    state_file = tmp_path / "portfolio_state.json"
    bank = FridayFortressBank(state_file_path=str(state_file))

    hunter = FridayFortressHunter(state_file_path=str(state_file))
    ticket = hunter.generate_trade_ticket(
        underlying="/MES",
        spot_price=5500.0,
        sgov_equity=20000.0,
        sign_ticket=True,
    )

    credit = ticket["capital_and_risk"]["total_credit_usd"]
    new_total = hunter.execute_weekly_harvest_shunt(ticket, bank_lobe=bank)
    assert new_total >= 20000.0 + credit


# ──────────────────────────────────────────────────────────────
#  11. EDGE CASES & DEFENSIVE ROBUSTNESS TESTS
# ──────────────────────────────────────────────────────────────

def test_select_strikes_from_chain_none_and_invalid_deltas():
    hunter = FridayFortressHunter(target_delta=0.08)
    chain = [
        {"strike": 5400.0, "delta": None, "bid": 18.0, "ask": 18.5, "right": "P"},
        {"strike": 5350.0, "delta": "corrupt_data", "bid": 10.0, "ask": 10.5, "right": "P"},
        {"strike": 5310.0, "delta": -0.081, "bid": 5.25, "ask": 5.5, "right": "P"},
        {"strike": 5260.0, "delta": -0.032, "bid": 2.25, "ask": 2.5, "right": "P"},
    ]
    selected = hunter.select_strikes_from_chain("/MES", chain, spread_width=50.0)
    assert selected["short_strike"] == 5310.0
    assert selected["long_strike"] == 5260.0
    assert selected["net_credit"] == 2.75


def test_select_strikes_from_chain_out_of_bounds_target_delta():
    hunter = FridayFortressHunter(target_delta=0.08)
    chain = [
        {"strike": 5310.0, "delta": -0.081, "bid": 5.25, "ask": 5.5, "right": "P"},
        {"strike": 5260.0, "delta": -0.032, "bid": 2.25, "ask": 2.5, "right": "P"},
    ]
    with pytest.raises(ValueError, match="out of bounds"):
        hunter.select_strikes_from_chain("/MES", chain, target_delta=0.02)
    with pytest.raises(ValueError, match="out of bounds"):
        hunter.select_strikes_from_chain("/MES", chain, target_delta=0.18)


def test_compute_rhythm_dates_invalid_dte():
    hunter = FridayFortressHunter()
    with pytest.raises(ValueError, match="dte must be positive"):
        hunter.compute_rhythm_dates(dte=0)
    with pytest.raises(ValueError, match="dte must be positive"):
        hunter.compute_rhythm_dates(dte=-5)


def test_telemetry_safe_without_validator_telemetry_method():
    class BareValidator:
        pass
    hunter = FridayFortressHunter(validator=BareValidator())
    telemetry = hunter.get_telemetry()
    assert telemetry["engine"] == "FridayFortressHunter"
    assert telemetry["validator_telemetry"] == {}


def test_outer_wing_protection_invariant_strictly_lower_strike():
    hunter = FridayFortressHunter(target_delta=0.08)
    chain_single = [
        {"strike": 5310.0, "delta": -0.08, "bid": 5.0, "ask": 5.5, "right": "P"}
    ]
    with pytest.raises(ValueError, match="No put strikes found below short strike"):
        hunter.select_strikes_from_chain("/MES", chain_single, spread_width=50.0)


def test_spatial_anchor_and_layer_in_ticket():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(underlying="/MES", sgov_equity=20000.0)
    assert "Baker, Louisiana" in ticket["spatial_anchor"]
    assert ticket["layer"].startswith("5/7")


def test_dual_clock_temporal_coordinates_in_ticket():
    hunter = FridayFortressHunter(target_delta=0.08)
    ticket = hunter.generate_trade_ticket(underlying="/MES", sgov_equity=20000.0)
    assert "temporal_coordinates" in ticket
    tc = ticket["temporal_coordinates"]
    assert "central_time_cdt" in tc
    assert "utc_iso" in tc
    assert "Baker, Louisiana" in tc["spatial_anchor"]
    assert tc["unix_epoch"] > 0.0


def test_verify_ticket_defensive_malformed_and_none_signatures():
    hunter = FridayFortressHunter(target_delta=0.08)

    # 1. Non-dict ticket
    res_nondict = hunter.verify_signed_ticket("not_a_dict")  # type: ignore
    assert res_nondict["is_valid"] is False
    assert res_nondict["status"] == "INVALID_TICKET_FORMAT"

    # 2. None signatures field
    ticket_null_sig = hunter.generate_trade_ticket(underlying="/MES", sgov_equity=20000.0, sign_ticket=False)
    ticket_null_sig["signatures"] = None
    res_null_sig = hunter.verify_signed_ticket(ticket_null_sig)
    assert res_null_sig["is_valid"] is False
    assert res_null_sig["status"] == "MALFORMED_SIGNATURE"

    # 3. String signatures field
    ticket_str_sig = copy.deepcopy(ticket_null_sig)
    ticket_str_sig["signatures"] = "corrupt_signatures_string"
    res_str_sig = hunter.verify_signed_ticket(ticket_str_sig)
    assert res_str_sig["is_valid"] is False
    assert res_str_sig["status"] == "MALFORMED_SIGNATURE"

    # 4. Signatures dict with None values
    ticket_null_field = copy.deepcopy(ticket_null_sig)
    ticket_null_field["signatures"] = {
        "key1_state_hash": None,
        "key2_hmac_signature": "0" * 64,
        "chain_hash": "0" * 64,
        "prev_chain_hash": "0" * 64,
    }
    res_null_field = hunter.verify_signed_ticket(ticket_null_field)
    assert res_null_field["is_valid"] is False
    assert res_null_field["status"] == "MALFORMED_SIGNATURE"


def test_select_strikes_from_chain_null_and_missing_quote_prices():
    hunter = FridayFortressHunter(target_delta=0.08)
    chain = [
        {"strike": 5310.0, "delta": -0.081, "bid": None, "price": None, "right": "P"},
        {"strike": 5260.0, "delta": -0.032, "ask": None, "price": None, "right": "P"},
        None,  # non-dict item to test resilience
        {"corrupt": "data"},
    ]
    selected = hunter.select_strikes_from_chain("/MES", chain, spread_width=50.0)
    assert selected["short_strike"] == 5310.0
    assert selected["long_strike"] == 5260.0
    assert selected["short_premium"] > 0.0
    assert selected["long_premium"] > 0.0
    assert selected["net_credit"] >= 0.25


def test_select_strikes_from_chain_closest_outer_wing_fallback():
    hunter = FridayFortressHunter(target_delta=0.08)
    # Target long strike is 5310 - 50 = 5260.
    # No strike <= 5260 exists. Strikes below 5310 are 5270 and 4000.
    # Engine should pick 5270 (closest to 5260), NOT 4000 (minimum of chain).
    chain = [
        {"strike": 5310.0, "delta": -0.081, "bid": 5.0, "ask": 5.5, "right": "P"},
        {"strike": 5270.0, "delta": -0.040, "bid": 2.5, "ask": 3.0, "right": "P"},
        {"strike": 4000.0, "delta": -0.001, "bid": 0.5, "ask": 1.0, "right": "P"},
    ]
    selected = hunter.select_strikes_from_chain("/MES", chain, spread_width=50.0)
    assert selected["short_strike"] == 5310.0
    assert selected["long_strike"] == 5270.0
    assert selected["spread_width"] == 40.0


def test_boundary_delta_snapping_mes_and_mnq():
    hunter = FridayFortressHunter(target_delta=0.08)
    # Test boundary 0.05
    spread_05 = hunter.calculate_put_spread("/MES", spot_price=5500.0, iv=0.18, dte=7.0, target_delta=0.05)
    assert 0.05 <= spread_05["short_delta_magnitude"] <= 0.10

    # Test boundary 0.10
    spread_10 = hunter.calculate_put_spread("/MES", spot_price=5500.0, iv=0.18, dte=7.0, target_delta=0.10)
    assert 0.05 <= spread_10["short_delta_magnitude"] <= 0.10


def test_execute_weekly_harvest_shunt_defensive_handling():
    hunter = FridayFortressHunter()
    assert hunter.execute_weekly_harvest_shunt("invalid_ticket") == 0.0  # type: ignore
    assert hunter.execute_weekly_harvest_shunt({"capital_and_risk": None}) == 0.0
    assert hunter.execute_weekly_harvest_shunt({}) == 0.0


