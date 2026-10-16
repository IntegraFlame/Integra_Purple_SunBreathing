"""
ADR-001 regression: one trustworthy clock.

celestial_time() must equal the system clock even when the persisted checkpoint is stale
(the 2026-10-06 20:59:42 checkpoint froze every boot before the fix). The checkpoint is kept
only for get_reboot_delta() (downtime), never for the current time.
"""
import time

import core.celestial_middleware as cm

STALE_EPOCH = 1791338382.5569623  # 2026-10-06 20:59:42 CDT -- the historical frozen checkpoint


def test_celestial_time_ignores_a_stale_checkpoint(monkeypatch):
    monkeypatch.setattr(cm._middleware, "_last_checkpoint", {"unix_epoch": STALE_EPOCH})
    monkeypatch.setattr(cm._middleware, "_boot_time", time.time() - 60.0)  # simulate a boot 60 s ago
    before = time.time()
    t = cm.celestial_time()
    after = time.time()
    assert before <= t <= after


def test_celestial_timestamp_is_live_even_with_a_stale_checkpoint(monkeypatch):
    """Brain Map T1: get_celestial_timestamp() comes from a Sentinel stamp (no cached /clock response, no HTTP)."""
    import asyncio

    monkeypatch.setattr(cm._middleware, "_last_checkpoint", {"unix_epoch": STALE_EPOCH})
    ts = asyncio.run(cm.get_celestial_timestamp())
    assert abs(ts.unix_epoch - time.time()) < 2.0
    assert ts.mode == "SOVEREIGN"
    assert ts.celestial_vector["frame"] == 2


def test_reboot_delta_still_uses_the_checkpoint(monkeypatch):
    monkeypatch.setattr(cm._middleware, "_last_checkpoint", {"unix_epoch": STALE_EPOCH})
    delta = cm.get_reboot_delta()
    assert delta is not None and abs(delta - (time.time() - STALE_EPOCH)) < 1.0


def test_celestial_ccid_is_stamped_with_real_time():
    ccid = cm.celestial_ccid("TEST")
    assert ccid.startswith("TEST_") and abs(int(ccid.split("_")[1]) - time.time()) < 2.0


def test_build_sovereign_timestamp_maps_canonical_clock_full_keys():
    """
    Task 1 regression: /clock/full returns 'digital_clock' and 'celestial_clock'.
    Previously _build_sovereign_timestamp looked up 'digital_numerical_clock' and
    'celestial_spacetime_vector', producing celestial_vector={} and grid_bucket=None.
    """
    from temporal.celestial_clock import DualTemporalEngine

    full_telemetry = DualTemporalEngine().get_full_telemetry()
    ts = cm._middleware._build_sovereign_timestamp(full_telemetry)

    assert ts.mode == "SOVEREIGN"
    assert ts.civil_dt == full_telemetry["digital_clock"]["local_time_24h"]
    assert ts.utc_iso == full_telemetry["digital_clock"]["iso_8601_utc"]
    assert ts.celestial_vector is not None and len(ts.celestial_vector) >= 4
    assert "earth_rotation_deg" in ts.celestial_vector
    assert "lunar_cycle_ratio" in ts.celestial_vector
    assert "orbital_trajectory_pos" in ts.celestial_vector
    assert ts.grid_bucket is not None and ts.grid_bucket.startswith("ROT_")


def test_get_celestial_metadata_sync_and_stamp_helper():
    """Task 1: Synchronous metadata helper and payload stamper verify all_systems_true."""
    payload = {"node_id": "NODE_TASK1"}
    stamped = cm.stamp_celestial_metadata(payload, payload_title="TASK1_VERIFICATION")

    assert "celestial_metadata" in stamped
    meta = stamped["celestial_metadata"]
    assert meta["all_systems_true"] is True
    assert meta["sync_isolation_verified"] is True
    assert meta["grid_bucket"].startswith("ROT_")
    assert "earth_rotation_deg" in meta["celestial_vector"]
    assert "sacred_day_of_year" in meta["sacred_calendar"]
    assert len(meta["cosmic_checkpoint_hash"]) == 64
    assert abs(stamped["created_at"] - time.time()) < 2.0


def test_sync_celestial_checkpoint_now_persists_full_vector():
    """
    sync_celestial_checkpoint_now() has the Sentinel (the only writer) write its checkpoint, which carries the
    full vector and the frame. The conftest fixture points the Sentinel's paths into tmp_path, so this test
    never writes the checkpoint of the tree it runs in (the 10/16 finding: it used to overwrite the live file).
    """
    import json
    from temporal.celestial_sentinel import get_sentinel

    sentinel = get_sentinel()
    legacy_before = cm._CHECKPOINT_PATH.stat().st_mtime if cm._CHECKPOINT_PATH.exists() else None
    meta = cm.sync_celestial_checkpoint_now()
    assert sentinel.checkpoint_path.exists()
    with open(sentinel.checkpoint_path, "r", encoding="utf-8") as f:
        persisted = json.load(f)

    assert persisted["schema"] == "cckpt/1"
    assert persisted["writer"] == "celestial_sentinel"
    assert persisted["frame"] == 2
    assert abs(persisted["unix_epoch"] - time.time()) < 5.0
    assert persisted["grid_bucket"].startswith("ROT_")
    assert "earth_rotation_deg" in persisted["celestial_vector"]
    assert "CDT" in persisted["civil_dt"] or "CST" in persisted["civil_dt"]
    assert meta["frame"] == persisted["frame"]
    legacy_after = cm._CHECKPOINT_PATH.stat().st_mtime if cm._CHECKPOINT_PATH.exists() else None
    assert legacy_after == legacy_before  # the tracked legacy checkpoint is never written

