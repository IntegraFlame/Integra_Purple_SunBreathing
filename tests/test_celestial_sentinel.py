"""
Brain Map T1: the Celestial Sentinel (design: docs/brainmap/T1_CELESTIAL_SENTINEL_DESIGN.md, section 7).

Offline. The conftest fixture `celestial_checkpoint_in_tmp` keeps every checkpoint write inside tmp_path.
The almanac fixture holds Tier 1 instants (USNO, NASA GSFC, F. Espenak) used to test frame 2.
"""
import json
import math
import random
import re
import time
from datetime import datetime, timezone
from pathlib import Path

import pytest

from temporal import celestial_sentinel as cs
from temporal.celestial_clock import FRAME_1, CelestialClockArchitecture

FIXTURE = Path(__file__).parent / "fixtures" / "almanac_2026_2036.json"


def _u(iso: str) -> float:
    return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def _circ(a: float, b: float) -> float:
    d = abs(a - b) % 1.0
    return min(d, 1.0 - d)


def _original_vector(u: float, spiral_depth: float = 1.0, anchor_lon: float = -91.1673):
    """The pre-T1 compute_4d_coordinates(), copied operation for operation (frame 1 must equal it exactly)."""
    raw_elapsed = u - 1785052800.0
    adjusted = raw_elapsed * (1.0 / spiral_depth)
    earth_rot = (anchor_lon + (adjusted * (360.0 / 86400.0))) % 360.0
    if earth_rot < 0:
        earth_rot += 360.0
    lunar = (adjusted / 2551442.8) % 1.0
    M = ((adjusted / 31558149.763) % 1.0) * 2.0 * math.pi
    e = 0.0167086
    E = M
    for _ in range(100):
        f = E - e * math.sin(E) - M
        fp = 1.0 - e * math.cos(E)
        nxt = E - f / fp
        if abs(nxt - E) < 1e-12:
            E = nxt
            break
        E = nxt
    orb = (E / (2.0 * math.pi)) % 1.0
    return round(earth_rot, 4), round(lunar, 4), round(orb, 4), round(spiral_depth, 4)


# 1. Frame-1 parity ----------------------------------------------------------------------------------------------
def test_frame1_parity_with_the_original_formulas_at_10000_instants():
    rng = random.Random(20261016)
    engine = CelestialClockArchitecture()
    lo, hi = _u("2020-01-01T00:00:00Z"), _u("2040-01-01T00:00:00Z")
    for _ in range(10000):
        u = rng.uniform(lo, hi)
        v = engine.compute_4d_coordinates(at=u)
        got = (v.earth_rotation_deg, v.lunar_cycle_ratio, v.orbital_trajectory_pos, v.spiral_accuracy_depth)
        assert got == _original_vector(u), u
        assert engine.compute_4d_coordinates(at=u, frame=FRAME_1) == v
    # Without a frame, the engine keeps its own spiral_depth and anchor longitude, as before T1.
    custom = CelestialClockArchitecture(seed_lon=-90.0)
    custom.spiral_depth = 1.05
    for _ in range(1000):
        u = rng.uniform(lo, hi)
        v = custom.compute_4d_coordinates(at=u)
        got = (v.earth_rotation_deg, v.lunar_cycle_ratio, v.orbital_trajectory_pos, v.spiral_accuracy_depth)
        assert got == _original_vector(u, spiral_depth=1.05, anchor_lon=-90.0), u


# 2. Frame 2 against the almanac ---------------------------------------------------------------------------------
def test_frame2_matches_the_almanac_and_frame1_does_not():
    alm = json.loads(FIXTURE.read_text(encoding="utf-8"))
    s = cs.get_sentinel()
    f2 = s.frame(2)
    assert len(alm["nasa_new_moons_2026_2036"]) == 136 and len(alm["espenak_perihelia_2026_2036"]) == 11
    for t in alm["nasa_new_moons_2026_2036"]:
        assert _circ(s.vector(_u(t), f2)[1], 0.0) < 0.03, t
    for t in alm["usno_2026_full_moons"]:
        assert _circ(s.vector(_u(t), f2)[1], 0.5) < 0.03, t
    for t in alm["espenak_perihelia_2026_2036"]:
        assert _circ(s.vector(_u(t), f2)[2], 0.0) < 0.004, t
    assert abs(s.vector(_u(alm["usno_2026_aphelion"]), f2)[2] - 0.5) < 0.005
    local_mean_noon = _u("2026-10-16T18:04:40Z") + 0.152  # 12:00Z + 91.1673/15 h
    rot = s.vector(local_mean_noon, f2)[0]
    assert min(rot, 360.0 - rot) < 0.001
    # Frame 1 (the D-20 epoch) is far from the sky: this is why frame 2 exists.
    assert _circ(s.vector(_u("2026-10-10T15:50:00Z"), FRAME_1)[1], 0.0) > 0.3


# 3. The stamp record ---------------------------------------------------------------------------------------------
def test_stamp_record_fields_ranges_and_formats():
    s = cs.get_sentinel()
    d = s.stamp("hoard_node").to_dict()
    assert set(d) == {"schema", "frame", "unix", "utc", "civil", "rot_deg", "lun", "orb", "turn", "sigma",
                      "grid", "label", "kind", "provenance", "frame_fallback"}
    assert d["schema"] == "cstamp/1" and d["frame"] == 2 and d["provenance"] == 1 and d["frame_fallback"] is False
    assert abs(d["unix"] - time.time()) < 2.0
    assert 0.0 <= d["rot_deg"] < 360.0 and 0.0 <= d["lun"] < 1.0 and 0.0 <= d["orb"] < 1.0 and d["sigma"] == 1.0
    assert re.fullmatch(r"ROT_\d+_ORB_\d+", d["grid"]) and re.fullmatch(r"ROT_\d+_LUN_\d+_ORB_\d+", d["label"])
    assert d["utc"].endswith("Z") and re.search(r"[+-]\d\d:\d\d$", d["civil"])
    text = json.dumps(d, ensure_ascii=False)
    assert not any(0x2800 <= ord(c) <= 0x28FF for c in text)  # Braille is display-only, never in a stamp


def test_stamp_reproduces_the_step_1_3_values():
    st = cs.get_sentinel().stamp("probe", at=1792132445.131)  # 2026-10-16 06:34:05Z
    assert (st.rot_deg, st.lun, st.orb, st.turn) == (187.3541, 0.1787, 0.7792, 0)
    assert (st.grid, st.label) == ("ROT_180_ORB_70", "ROT_180_LUN_10_ORB_70")


# 4. CCIDs ----------------------------------------------------------------------------------------------------------
def test_ccid_comes_from_the_stamp_instant():
    s = cs.get_sentinel()
    st = s.stamp("x", at=1792132445.9)
    assert s.ccid("CCID", st) == "CCID_1792132445"
    import core.celestial_middleware as cm
    c = cm.celestial_ccid("CRYSTAL")
    assert re.fullmatch(r"CRYSTAL_\d{10}", c) and abs(int(c.split("_")[1]) - time.time()) < 2.0


# 5. Registry validation and the loud fallback --------------------------------------------------------------------
VALID_REGISTRY = Path(cs.REGISTRY_PATH).read_text(encoding="utf-8")


@pytest.mark.parametrize("mutate, message", [
    (lambda t: None, "not found"),
    (lambda t: t.replace("active_frame: 2", "active_frame: 7"), "active_frame 7"),
    (lambda t: t.replace("  - id: 2", "  - id: 1"), "duplicate frame id 1"),
    (lambda t: t.replace("period_s: 31558149.763", "period_s: 31558149.0"), "frame 1 differs"),
    (lambda t: t.replace("schema: celestial_frames/1", "schema: other"), "schema"),
    (lambda t: t.replace("sigma: 1.0\n    note", "sigma: 0.9\n    note"), "sigma must be 1.0"),
])
def test_registry_validation_names_the_problem(tmp_path, mutate, message):
    p = tmp_path / "frames.yml"
    text = mutate(VALID_REGISTRY)
    if text is not None:
        assert text != VALID_REGISTRY  # the mutation applied
        p.write_text(text, encoding="utf-8")
    with pytest.raises(cs.FrameRegistryError, match=message):
        cs.load_registry(p)


def test_a_broken_registry_falls_back_loudly(tmp_path):
    s = cs.CelestialSentinel(registry_path=tmp_path / "missing.yml", checkpoint_path=tmp_path / "c.json",
                             legacy_checkpoint_path=tmp_path / "l.json")
    assert s.frame_fallback is True and s.active_frame.frame_id == 1
    st = s.stamp("x")
    assert st.frame == 1 and st.frame_fallback is True
    status = s.status()
    assert status["registry"]["valid"] is False and "not found" in status["registry"]["error"]


# 6. The checkpoint: atomic, single writer, reboot delta -----------------------------------------------------------
def test_checkpoint_write_is_atomic(tmp_path, monkeypatch):
    s = cs.CelestialSentinel(checkpoint_path=tmp_path / "cel" / "checkpoint.json",
                             legacy_checkpoint_path=tmp_path / "l.json")
    rec = s.write_checkpoint("first")
    assert rec and rec["schema"] == "cckpt/1" and rec["writer"] == "celestial_sentinel" and rec["frame"] == 2
    before = s.checkpoint_path.read_bytes()

    def crash(src, dst):
        raise OSError("simulated crash between write and replace")

    monkeypatch.setattr(cs.os, "replace", crash)
    assert s.write_checkpoint("second") is None
    assert s.checkpoint_path.read_bytes() == before
    assert not list(s.checkpoint_path.parent.glob("*.tmp"))
    assert "simulated crash" in s.status()["checkpoint"]["last_error"]


def test_reboot_delta_uses_the_previous_checkpoint_and_never_writes_the_legacy_file(tmp_path):
    legacy = tmp_path / "legacy.json"
    legacy.write_text(json.dumps({"unix_epoch": time.time() - 100.0}), encoding="utf-8")
    mtime = legacy.stat().st_mtime
    s = cs.CelestialSentinel(checkpoint_path=tmp_path / "new.json", legacy_checkpoint_path=legacy)
    assert 99.0 < s.reboot_delta() < 102.0
    assert s.status()["checkpoint"]["previous_source"] == "legacy"
    s.start()
    s.stop()
    assert legacy.stat().st_mtime == mtime
    assert json.loads((tmp_path / "new.json").read_text(encoding="utf-8"))["reason"] == "stop"
    s2 = cs.CelestialSentinel(checkpoint_path=tmp_path / "new.json", legacy_checkpoint_path=legacy)
    assert s2.status()["checkpoint"]["previous_source"] == "checkpoint"


def test_only_the_sentinel_writes_the_checkpoint():
    root = Path(__file__).resolve().parent.parent
    allowed = {root / "temporal" / "celestial_sentinel.py", root / "core" / "celestial_middleware.py"}
    offenders = []
    for p in root.rglob("*.py"):
        if p in allowed or any(part in ("tests", ".venv", "venv", "CODE", "scratch") for part in p.parts):
            continue
        src = p.read_text(encoding="utf-8", errors="replace")
        if "celestial_checkpoint.json" in src or "_persist_checkpoint" in src or "CHECKPOINT_PATH" in src:
            offenders.append(str(p.relative_to(root)))
    assert offenders == []
    middleware = (root / "core" / "celestial_middleware.py").read_text(encoding="utf-8")
    assert "open(" not in middleware and "httpx" not in middleware and "urllib" not in middleware


# 7. Routes: read-only checkpoint, frame constants, /clock frames, response headers --------------------------------
def test_routes_checkpoint_read_only_frame_and_headers():
    from fastapi.testclient import TestClient
    import main

    s = cs.get_sentinel()
    client = TestClient(main.app)  # no lifespan: nothing starts, nothing is written at startup
    r1 = client.get("/celestial/checkpoint")
    r2 = client.get("/celestial/checkpoint")
    assert r1.status_code == 200 and r2.status_code == 200
    body = r1.json()
    assert body["active_frame"] == 2 and body["registry"]["valid"] is True
    assert "all_systems_true" not in body and "status" not in body
    assert not s.checkpoint_path.exists()  # two calls, no write

    clk = client.get("/clock")
    assert clk.json()["celestial_clock"]["frame"] == 2
    assert clk.headers["X-Celestial-Frame"] == "2"
    assert clk.headers["X-Celestial-Grid-Bucket"].startswith("ROT_")
    assert client.get("/clock?frame=1").json()["celestial_clock"]["frame"] == 1
    assert client.get("/clock?frame=9").status_code == 404
    fr = client.get("/celestial/frame").json()
    assert fr["frame"] == 2 and fr["orbit"]["period_s"] == 31558310.6 and fr["frame_fallback"] is False
    assert client.get("/celestial/frame?frame=1").json()["orbit"]["period_s"] == 31558149.763


# 8. SWDS report (R6, S5) -------------------------------------------------------------------------------------------
def test_swds_report_is_named_and_dated_by_the_stamp(tmp_path, monkeypatch):
    from runtime import swds_simulator as sw

    monkeypatch.setattr(sw, "REPORTS_DIR", str(tmp_path))
    cycle = sw.SWDSCycle.__new__(sw.SWDSCycle)  # no state file is read or written
    cycle.last_report = {"awakening_summary": "test"}
    cycle.consolidation_summary = ["c"]
    cycle.pruning_summary = ["p"]
    cycle.dream_log = ["d"]
    cycle.mutations_applied = [0.1]
    cycle._write_hoard_markdown_report()
    files = list(tmp_path.glob("*_SWDS_Report.md"))
    assert len(files) == 1
    m = re.fullmatch(r"\d{4}-\d\d-\d\d_\d\d-\d\d-\d\d_C[DS]T_CEL-F2-(\d+\.\d\d)deg_SWDS_Report\.md", files[0].name)
    assert m, files[0].name
    body = files[0].read_text(encoding="utf-8")
    assert "Report Written At (UTC):" in body and "Frame 2 |" in body
    last = cs.get_sentinel().status()["last_stamp"]
    assert last["kind"] == "swds_report"


# 9. Hoard nodes ----------------------------------------------------------------------------------------------------
def test_hoard_nodes_carry_the_stamp_and_a_real_anchor_time(tmp_path):
    from memory.the_hoard import TheHoard, HoardNode
    from evolution.phoenix_forge import PhoenixForge

    hoard = TheHoard(base_dir=str(tmp_path))
    hoard.commit_node_v2(payload={"a": 1}, spacetime_anchor={"x": 1.0, "t": 0}, ccid="T1_ZERO")
    hoard.commit_node_v2(payload={"a": 2}, spacetime_anchor={"x": 1.0, "t": 42}, ccid="T1_GIVEN")
    shards = Path(hoard.kernel_memory_dir) / "hoard" / "raw_shards"
    zero = json.loads((shards / "T1_ZERO.json").read_text(encoding="utf-8"))
    given = json.loads((shards / "T1_GIVEN.json").read_text(encoding="utf-8"))
    assert zero["celestial_stamp"]["frame"] == 2 and zero["celestial_stamp"]["kind"] == "hoard_node"
    assert zero["spacetime_anchor"]["t"] == zero["created_at"] == zero["celestial_stamp"]["unix"]
    assert given["spacetime_anchor"]["t"] == 42  # a time the caller gave is kept

    synth = PhoenixForge().synthesize_hoard_node("left", "right")
    assert synth["spacetime_anchor"]["t"] == synth["created_at"] == synth["celestial_stamp"]["unix"]
    assert "generation" in synth["spacetime_anchor"]
    assert synth["ccid"] == f"CCID_{int(synth['created_at'])}"

    old = HoardNode.from_dict({"ccid": "OLD", "payload": {}, "spacetime_anchor": {"t": 0}})
    assert old.celestial_stamp is None  # no stamp is invented for a node written before T1
