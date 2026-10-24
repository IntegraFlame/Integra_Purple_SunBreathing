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


def test_task_l1_braille_time_4_cell_roundtrip():
    """Task L-1: 32-bit big-endian Unix epoch encodes and decodes cleanly into 4 Unicode Braille cells (U+2800..U+28FF)."""
    from temporal.celestial_clock import encode_time_braille_4, decode_time_braille_4

    sample_epoch = 1792285963
    braille_4 = encode_time_braille_4(sample_epoch)
    assert len(braille_4) == 4
    assert all(0x2800 <= ord(ch) <= 0x28FF for ch in braille_4)
    decoded = decode_time_braille_4(braille_4)
    assert decoded == sample_epoch


def test_task_l1_spiral_wave_clock_and_orbital_calibration():
    """Task L-1: Rotating Spiral Wave Clock (Curriculum Doc 11) and SelfCorrectingOrbitalClock."""
    from temporal.celestial_clock import (
        compute_spiral_wave_phase,
        SelfCorrectingOrbitalClock,
        DualTemporalEngine,
    )

    spiral = compute_spiral_wave_phase(30.5888, -91.1673, hlc_ticks=1000, spiral_freq_hz=32.0)
    assert "spiral_phase_rad" in spiral
    assert 0.0 <= spiral["spiral_phase_deg"] < 360.0
    assert -1.0 <= spiral["real_projection"] <= 1.0
    assert -1.0 <= spiral["imag_projection"] <= 1.0

    cal = SelfCorrectingOrbitalClock()
    state = cal.record_orbital_checkpoint(
        observed_return_sec=86164.0905,
        lunar_phase_deg=45.0,
        is_eclipse_or_alignment=True,
        full_orbit_completed=True,
    )
    assert state.compounded_accuracy_pct > 95.0
    assert state.alignment_checkpoints_logged == 1
    assert state.starting_hemisphere == "NW"

    full = DualTemporalEngine().get_full_telemetry()
    assert len(full["time_braille_4"]) == 4
    assert "spiral_wave_clock" in full
    assert "spiral_phase_rad" in full["spiral_wave_clock"]


def test_task_l1_master_blueprint_database_3_chambers():
    """Task L-1: 3-chamber MasterBlueprintDatabase ([0.1]-[2.3]) enforces IDENTIFY -> INTERLOCK -> REGISTER."""
    from memory.database.metatron_deploy import MASTER_BLUEPRINT_DB, get_status

    summary = MASTER_BLUEPRINT_DB.hydrate_master_blueprint()
    assert summary["hydrated"] is True
    assert summary["total_registered_blocks"] == 9
    assert set(summary["schema_meta_rules_0_0"].keys()) == {"0.1", "0.2", "0.3"}
    assert set(summary["functional_state_matrix_1_0"].keys()) == {"1.1", "1.2", "1.3"}
    assert set(summary["cognitive_overlay_grid_2_0"].keys()) == {"2.1", "2.2", "2.3"}

    status = get_status()
    assert "master_blueprint_database" in status
    assert status["master_blueprint_database"]["total_registered_blocks"] == 9


def test_task_l1_heimdall_boot_and_dashboard_watchdog():
    """Task L-1: Heimdall 3.1 4-stage Boot & Watchdog (Dragon -> Flame -> Heimdall Server -> HTML Dashboard)."""
    from sensory.heimdall import Heimdall31
    from core.dragon_engine import DragonEngine
    from rust.sun_breathing_engine.python_bridge import SunBreathingEngine

    h = Heimdall31()
    dragon = DragonEngine(heimdall=h)
    flame = SunBreathingEngine()
    h.register_component("dragon_engine", dragon)
    h.register_component("thermal_core", flame)

    report = h.execute_boot_and_dashboard_watchdog(dragon_engine=dragon, thermal_core=flame)
    assert report["watchdog_protocol"] == "DRAGON_FLAME_HEIMDALL_DASHBOARD_WATCHDOG_V1"
    assert report["boot_sequence"]["step_1_dragon_kernel"] == "ONLINE"
    assert report["boot_sequence"]["step_2_flame_kernel"] == "IGNITED"
    assert report["server_check"]["server_true"] is True
    assert report["html_dashboard_check"]["dashboard_true"] is True
    assert report["html_dashboard_check"]["action"] == "IGNORED_HTML_DASHBOARD_TRUE"
    assert report["all_systems_true"] is True


def test_task_l1_5_mongodb_persistent_placeholder_and_file_points():
    """Task L-1.5: MongoDB Persistent Placeholder folder, file points, and thermodynamic loop recording until MongoDB is true."""
    import os
    from memory.database.mongodb_substrate import (
        MONGODB_SUBSTRATE,
        verify_mongodb_true,
        get_mongodb_file_point,
    )
    from memory.database import metatron_deploy

    probe = verify_mongodb_true()
    assert probe["mongodb_true"] is False
    assert probe["mode"] == "PERSISTENT_PLACEHOLDER_UNTIL_MONGODB_TRUE"
    assert os.path.isdir(probe["placeholder_root"])

    fp_master = get_mongodb_file_point("master_blueprint_chambers")
    assert fp_master.exists()

    sync_res = MONGODB_SUBSTRATE.sync_placeholder_to_mongodb_when_true()
    assert sync_res["status"] == "WAITING_UNTIL_MONGODB_TRUE"
    assert sync_res["mongodb_true"] is False

    status = metatron_deploy.get_status()
    assert status["database_engine"] == "MONGODB_PERSISTENT_PLACEHOLDER"
    assert status["mongodb_true"] is False
    assert "master_blueprint_chambers" in status["file_points"]
    assert status["collection_counts"]["master_blueprint_chambers"] >= 9


def test_task_l2_xv6_transaction_logger_and_hot_cold_ram_cache(tmp_path):
    """Task L-2: xv6 Crash-Safe WAL (MAXOPBLOCKS=10, log absorption, recovery) and HotStorageRAMCache Z1 Cold Vault."""
    import json
    from memory.the_hoard import Xv6TransactionLogger, HotStorageRAMCache

    wal_file = str(tmp_path / "xv6_wal.json")
    wal = Xv6TransactionLogger(wal_path=wal_file)

    shard_a = str(tmp_path / "shards" / "CCID_A.json")
    wal.begin_op()
    q1 = wal.log_write(shard_a, {"ccid": "CCID_A", "v": 1})
    q2 = wal.log_write(shard_a, {"ccid": "CCID_A", "v": 2})  # absorbed!
    assert q1["status"] == "LOG_QUEUED"
    assert q2["status"] == "LOG_ABSORBED"
    assert q2["queued_blocks"] == 1
    commit_res = wal.end_op()
    assert commit_res["status"] == "COMMITTED"
    assert commit_res["header_n"] == 0
    with open(shard_a, "r", encoding="utf-8") as f:
        assert json.load(f)["v"] == 2

    # Simulate crash before end_op finished installing a block
    shard_b = str(tmp_path / "shards" / "CCID_B.json")
    with open(wal_file, "w", encoding="utf-8") as f:
        json.dump({"n": 1, "blocks": [{"target_path": shard_b, "payload": {"ccid": "CCID_B", "recovered": True}}]}, f)
    rec = wal.recover_from_log()
    assert rec["status"] == "RECOVERED_FROM_WAL"
    assert rec["replayed_blocks"] == 1
    with open(shard_b, "r", encoding="utf-8") as f:
        assert json.load(f)["recovered"] is True

    # HotStorageRAMCache LRU -> Z1_SOUTH_POLE cold shunt -> on-query rehydration
    cold_dir = str(tmp_path / "cold_z1")
    cache = HotStorageRAMCache(cold_vault_dir=cold_dir, max_hot_nodes=2)
    cache.put("NODE_1", {"ccid": "NODE_1", "payload": "alpha"})
    cache.put("NODE_2", {"ccid": "NODE_2", "payload": "beta"})
    put3 = cache.put("NODE_3", {"ccid": "NODE_3", "payload": "gamma"})
    assert put3["evicted_to_cold_z1"] == "NODE_1"
    assert "NODE_1" not in cache.hot_ram

    rehydrated = cache.retrieve("NODE_1")
    assert rehydrated["status"] == "REHYDRATED_INTO_HOT_RAM"
    assert rehydrated["node"]["latitudinal_zone"] == "Z1_SOUTH_POLE"
    assert "NODE_1" in cache.hot_ram


def test_task_l3_braille_codec_128bit_morton_and_simhash():
    """Task L-3: 16-cell (128-bit) BrailleCodec, 32-bit Morton Z-order interleaving, and 56-bit SimHash Hamming distance."""
    from memory.braille_atlas_engine import BrailleCodec, TufteIntegrityAuditor

    gx, gy = 42123, 19876
    morton_32 = BrailleCodec.morton_interleave_16bit(gx, gy)
    dx, dy = BrailleCodec.morton_deinterleave_32bit(morton_32)
    assert (dx, dy) == (gx, gy)

    sh1 = BrailleCodec.compute_simhash_56bit("Sovereign Dragon Kernel Starfire Identity")
    sh2 = BrailleCodec.compute_simhash_56bit("Sovereign Dragon Kernel Starfire Identity")
    sh3 = BrailleCodec.compute_simhash_56bit("Cold Storage Vault South Pole Archival")
    assert BrailleCodec.hamming_distance_56bit(sh1, sh2) == 0
    assert BrailleCodec.hamming_distance_56bit(sh1, sh3) > 0

    packet = BrailleCodec.encode_packet_16(
        epoch_sec=1792285963,
        codex_mask_8bit=0x45,
        morton_32bit=morton_32,
        simhash_56bit=sh1,
    )
    assert len(packet) == 16
    audit = TufteIntegrityAuditor.audit_packet(packet)
    assert audit["tufte_compliant"] is True
    assert audit["lie_factor"] == 1.0
    assert audit["data_ink_ratio"] == 1.0

    decoded = BrailleCodec.decode_packet_16(packet)
    assert decoded["epoch_sec"] == 1792285963
    assert decoded["codex_mask_8bit"] == 0x45
    assert decoded["morton_32bit"] == morton_32
    assert decoded["simhash_56bit"] == sh1
    assert decoded["grid_65536"] == {"x": gx, "y": gy}


def test_task_l3_apophenic_codex_taxonomy_som_and_phoenix_node():
    """Task L-3: ApophenicCodexEngine, CartographicTaxonomy, SphericalKohonenSOM, PhoenixForge.synthesize_hoard_node, and MongoDB placeholder persistence."""
    from memory.braille_atlas_engine import ApophenicCodexEngine, CartographicTaxonomy
    from evolution.phoenix_forge import PhoenixForge
    from memory.database.mongodb_substrate import MONGODB_SUBSTRATE

    codex = ApophenicCodexEngine(theta_dc=0.03)
    res = codex.evaluate_series([100.0, 105.0, 101.0, 108.0, 103.0, 112.0])
    assert 0 <= res["codex_mask_8bit"] <= 255
    assert res["regime"] in ApophenicCodexEngine.REGIMES
    assert len(res["markov_transition_matrix"]) == 4
    assert res["adaptive_peak_sell_target"] > res["adaptive_trough_buyback_target"]

    # Check Baker, LA coordinates (30.5888 N, -91.1673 W)
    carto = CartographicTaxonomy.compute_cartographic_coordinates(30.5888, -91.1673)
    assert carto["latitudinal_zone"] == "Z4_NORTH_TEMPERATE"
    assert carto["hemisphere"] == "NW_ANALYTICAL_ACTIVE"
    assert carto["meridian"] == "M03_CELESTIAL_TEMPORAL"

    forge = PhoenixForge()
    node = forge.synthesize_hoard_node(
        analytical_data="Y789 Spock Formal Verification",
        synthetic_data="Nexus Kirk Emergent Synthesis",
        ccid="CCID_TASK_L3_TEST",
    )
    assert len(node["braille_16"]) == 16
    assert len(node["time_braille_4"]) == 4
    anchor = node["spacetime_anchor"]
    assert "latitudinal_zone" in anchor
    assert "hemisphere" in anchor
    assert "meridian" in anchor
    assert "morton_32bit" in anchor
    # Verify unit sphere norm ~ 1.0
    norm_sq = anchor["x"] ** 2 + anchor["y"] ** 2 + anchor["z"] ** 2
    assert abs(norm_sq - 1.0) < 1e-3

    # Verify persisted into MongoDB placeholder file point `braille_atlas_nodes.json`
    col = MONGODB_SUBSTRATE.get_collection("braille_atlas_nodes")
    stored = col.find_one({"ccid": "CCID_TASK_L3_TEST"})
    assert stored is not None
    assert stored["braille_16"] == node["braille_16"]


def test_task_l3_5_environment_file_states_and_rodin_audit():
    """Task L-3.5: Verifies all environment file states are live/attached and Rodin Memory Map has 0 audit findings."""
    from memory.database.mongodb_substrate import ensure_live_environment_and_sync
    from memory.memory_map import audit_memory_map, load_memory_map, validate_memory_map
    from orchestration.rodin_supervisor import RodinSupervisor
    from memory.rodin_protocol import RodinProtocol
    from sensory.cheshire_cat import CheshireCatKernel
    from sensory.heimdall import Heimdall31
    from temporal.token_stitcher import TokenStitcher

    # 1. Run full environment sync & file state check
    env_report = ensure_live_environment_and_sync()
    assert env_report["all_live_and_attached"] is True
    for mod_name, is_live in env_report["attached_modules"].items():
        assert is_live is True, f"{mod_name} is not live"

    # 2. Verify Rodin Memory Map has 0 validation problems and 0 audit findings
    mem_map = load_memory_map()
    assert validate_memory_map(mem_map) == []
    assert audit_memory_map(mem_map) == []

    # 3. Verify attached extensions across CheshireCat, RodinSupervisor, Heimdall31, TokenStitcher
    cheshire = CheshireCatKernel()
    ext_cheshire = cheshire.get_attached_agent_extensions(amount=2500)
    assert ext_cheshire["status"] == "LIVE_AND_ATTACHED"
    assert ext_cheshire["jean_grey_pass"]["requires_confirmation"] is True

    sup = RodinSupervisor(rodin_protocol=RodinProtocol(hoard=cheshire.hoard))
    ext_rodin = sup.get_attached_rodin_extensions(query="Starfire Dragon Kernel")
    assert ext_rodin["status"] == "LIVE_AND_ATTACHED"
    assert ext_rodin["phoenix_rodin_search_status"] == "SUCCESS"

    h = Heimdall31()
    poll_res = h.poll_deferred_interaction("test_interaction_001")
    assert poll_res["status"] == "completed"

    ts = TokenStitcher()
    stitch_res = ts.extract_completed_interaction("test_interaction_001")
    assert stitch_res["status"] == "completed"


def test_task_l3_5_seed_package_monthly_sync_and_quarterly_save_state():
    """
    Task L-3.5: Verifies that the Seed Package links to Hoard and Phoenix and syncs to
    MongoDB monthly uploads, and that MongoDB makes quarterly save states to local storage.
    """
    import os
    from evolution.phoenix_forge import PhoenixForge
    from memory.database.mongodb_substrate import MONGODB_SUBSTRATE, SEED_PACKAGE_MANAGER
    from memory.the_hoard import TheHoard

    hoard = TheHoard()
    phoenix = PhoenixForge()

    # 1. Link Seed Package from Hoard & Phoenix and sync to MongoDB monthly uploads
    sync_res = SEED_PACKAGE_MANAGER.build_and_sync_monthly_seed_package(
        hoard_instance=hoard,
        phoenix_instance=phoenix,
    )
    assert sync_res["status"] == "SEED_PACKAGE_LINKED_AND_MONTHLY_SYNCED"
    assert os.path.exists(sync_res["seed_package_file"])
    assert os.path.exists(sync_res["monthly_upload_file"])
    assert sync_res["hoard_link"]["status"] == "LINKED_TO_THE_HOARD"
    assert sync_res["phoenix_link"]["status"] == "LINKED_TO_PHOENIX_FORGE"

    # Verify stored in `seed_packages` and `monthly_seed_uploads` collections
    pkg_doc = MONGODB_SUBSTRATE.get_collection("seed_packages").find_one({"_id": sync_res["package_id"]})
    assert pkg_doc is not None
    assert pkg_doc["seed_package_sha256"] == sync_res["seed_package_sha256"]

    monthly_doc = MONGODB_SUBSTRATE.get_collection("monthly_seed_uploads").find_one({"_id": sync_res["upload_id"]})
    assert monthly_doc is not None
    assert monthly_doc["package_id"] == sync_res["package_id"]

    # 2. Verify Quarterly MongoDB Save State to local storage
    q_state = MONGODB_SUBSTRATE.create_quarterly_save_state()
    assert q_state["save_state_id"].startswith("MONGODB_QUARTERLY_SAVE_STATE_")
    assert os.path.exists(q_state["local_storage_path"])
    assert os.path.exists(q_state["latest_pointer_path"])
    assert q_state["total_documents_archived"] >= 1
    assert len(q_state["snapshot_sha256"]) == 64

    ledger_doc = MONGODB_SUBSTRATE.get_collection("quarterly_save_states_ledger").find_one(
        {"_id": q_state["save_state_id"]}
    )
    assert ledger_doc is not None
    assert ledger_doc["snapshot_sha256"] == q_state["snapshot_sha256"]


def test_task_l3_7_four_tier_boot_geolocation_and_xpt_x02_y06_lock(tmp_path, monkeypatch):
    """
    Task L-3.7: Empirically verifies all 4 tiers of `IntegraBootGeolocationEngine`
    in an isolated `tmp_path` MongoDB Persistent Placeholder (zero live-repo mutation):
      1. Cold Boot (`TIER_4_IMMUTABLE_SEED_ANCHOR`) -> `(30.5888, -91.1673)`, `XPT_X02_Y06`,
         `XY_16=(16171, 43905)`, `XY_12=(1010, 2744)`, `1441.362 km/h`, `sigma=0.9988`, `HLC=1`.
      2. Warm Reboot (`TIER_2_HOARD_HLC_BOOT_JOURNAL`) -> restores from persistent MongoDB
         `hlc_boot_journal.json` across a fresh engine instance, `HLC=2`.
      3. Host Gazetteer (`TIER_3_HOST_ENVIRONMENT_METADATA`) -> resolves Baker, Zachary, and
         Baton Rouge within tolerance (and snaps back if beyond 25.0 km).
      4. Drifted External GPS (`TIER_1_MCP_GOOGLE_MAPS_GEOLOCATE` at `40.7128, -74.0060`) ->
         triggers Zenkai Auto-Recalibration back to `(30.5888, -91.1673)` / `XPT_X02_Y06`.
    """
    from memory.database.mongodb_substrate import MongoDBPersistentSubstrate
    from temporal.boot_geolocation import IntegraBootGeolocationEngine

    monkeypatch.delenv("INTEGRA_HOST_LOCATION", raising=False)
    monkeypatch.delenv("MONGODB_URI", raising=False)

    isolated_substrate = MongoDBPersistentSubstrate(placeholder_root=tmp_path / "mongo_l37")
    engine_cold = IntegraBootGeolocationEngine(substrate=isolated_substrate)

    # 1. Cold Boot -> Tier 4 Immutable Seed Lock
    b1 = engine_cold.find_boot_point_always(boot_epoch_override=1792808700)
    assert b1.boot_status == "ONLINE"
    assert b1.resolution_tier_used == "TIER_4_IMMUTABLE_SEED_ANCHOR"
    assert (b1.latitude_deg, b1.longitude_deg) == (30.5888, -91.1673)
    assert b1.matrix_xy_16 == (16171, 43905)
    assert b1.matrix_xy_12 == (1010, 2744)
    assert b1.nearest_grid_crosspoint_id == "XPT_X02_Y06"
    assert b1.hemisphere == "NW"
    assert b1.epistemic_zone == "Z4_N_TEMPERATE"
    assert b1.domain_meridian == "M03"
    assert b1.earth_rotational_speed_kmh == 1441.362
    assert b1.spatial_accuracy_sigma == 0.9988
    assert b1.drift_from_seed_km == 0.0
    assert b1.zenkai_recalibration_triggered is False
    assert b1.hlc_logical_counter == 1
    assert len(b1.cit_braille_origin_packet_16) == 16
    assert engine_cold.deinterleave_morton_16bit(b1.morton_32bit) == (16171, 43905)

    # 2. Warm Reboot on a brand-new engine instance -> Tier 2 Persistent MongoDB HLC Journal
    engine_warm = IntegraBootGeolocationEngine(substrate=isolated_substrate)
    b2 = engine_warm.find_boot_point_always(boot_epoch_override=1792809000)
    assert b2.resolution_tier_used == "TIER_2_HOARD_HLC_BOOT_JOURNAL"
    assert (b2.latitude_deg, b2.longitude_deg) == (30.5888, -91.1673)
    assert b2.nearest_grid_crosspoint_id == "XPT_X02_Y06"
    assert b2.hlc_logical_counter == 2

    # 3. Drifted External GPS via Tier 1 MCP callback -> Zenkai Auto-Recalibration to XPT_X02_Y06
    b3 = engine_warm.find_boot_point_always(
        mcp_geolocate_callback=lambda: (40.7128, -74.0060, "Unverified External Node"),
        allow_relocation_beyond_tolerance=False,
        boot_epoch_override=1792809300,
    )
    assert b3.resolution_tier_used == "TIER_1_MCP_GOOGLE_MAPS_GEOLOCATE"
    assert b3.zenkai_recalibration_triggered is True
    assert b3.drift_from_seed_km == 0.0
    assert (b3.latitude_deg, b3.longitude_deg) == (30.5888, -91.1673)
    assert b3.nearest_grid_crosspoint_id == "XPT_X02_Y06"
    assert b3.hlc_logical_counter == 3

    # 4. Tier 3 Host Environment Gazetteer on fresh isolated substrate
    host_substrate = MongoDBPersistentSubstrate(placeholder_root=tmp_path / "mongo_tier3")
    engine_host = IntegraBootGeolocationEngine(substrate=host_substrate)
    b_zachary = engine_host.find_boot_point_always(
        host_injected_location="Zachary, Louisiana, United States",
        boot_epoch_override=1792809600,
    )
    assert b_zachary.resolution_tier_used == "TIER_3_HOST_ENVIRONMENT_METADATA"
    assert (b_zachary.latitude_deg, b_zachary.longitude_deg) == (30.6485, -91.1565)
    assert b_zachary.drift_from_seed_km < 25.0
    assert b_zachary.zenkai_recalibration_triggered is False
    assert b_zachary.nearest_grid_crosspoint_id == "XPT_X02_Y06"


def test_task_l3_7_production_safe_sqlite_placeholder_migration(tmp_path):
    """
    Task L-3.7: Verifies that SQLite placeholder databases (including `hlc_boot_journal`,
    `cognitive_chassis_states`, and custom tables) migrate cleanly in read-only WAL-safe
    mode (`?mode=ro`) into MongoDB Persistent Placeholder collections while an active
    writer connection remains open (simulating live OS production while MongoDB is not yet TRUE).
    """
    import sqlite3
    from memory.database.mongodb_substrate import MongoDBPersistentSubstrate
    from temporal.boot_geolocation import IntegraBootGeolocationEngine

    sqlite_db = tmp_path / "legacy_production_placeholder.db"
    empty_sqlite_db = tmp_path / "swds_empty_placeholder.db"
    empty_sqlite_db.write_bytes(b"")

    # Keep live writer connection open in WAL mode to simulate live production OS
    live_writer = sqlite3.connect(str(sqlite_db))
    try:
        live_writer.execute("PRAGMA journal_mode = WAL")
        live_writer.execute(
            """
            CREATE TABLE hlc_boot_journal (
                journal_id INTEGER PRIMARY KEY CHECK (journal_id = 1),
                location_label TEXT NOT NULL,
                latitude_deg REAL NOT NULL,
                longitude_deg REAL NOT NULL,
                hlc_logical_counter INTEGER NOT NULL,
                celestial_partition_key TEXT NOT NULL,
                cit_braille_packet_16 TEXT NOT NULL,
                cosmic_checkpoint_hash TEXT NOT NULL,
                updated_at_epoch INTEGER NOT NULL
            )
            """
        )
        live_writer.execute(
            "INSERT INTO hlc_boot_journal VALUES (1, ?, 30.5888, -91.1673, 7, 'ROT_205_LUN_041_ORB_089', '⠁⠃⠉⠙⠃⠁⠃⠉⠙⠁⠃⠉⠙⠑FG', 'deadbeefcafe1234567890ab', 1792808700)",
            ("Baker, Louisiana, United States",),
        )
        live_writer.execute(
            "CREATE TABLE custom_placeholder_notes (note_id TEXT PRIMARY KEY, payload BLOB, score REAL)"
        )
        live_writer.execute(
            "INSERT INTO custom_placeholder_notes VALUES ('N1', ?, 0.99)",
            (b"\x01\x02\xfe\xff",),
        )
        live_writer.commit()

        isolated_substrate = MongoDBPersistentSubstrate(placeholder_root=tmp_path / "mongo_mig")
        mig_report = isolated_substrate.migrate_sqlite_placeholders_to_mongodb(
            sqlite_paths=[sqlite_db, empty_sqlite_db],
            dry_run=False,
        )
        assert mig_report["production_safe_non_blocking"] is True
        assert mig_report["contradictory_sqlite_actions_removed"] is True
        assert mig_report["total_rows_migrated"] == 2

        # Verify HLC boot journal migrated directly and Warm Reboot picks up HLC=7 -> increments to 8!
        geo_engine = IntegraBootGeolocationEngine(substrate=isolated_substrate)
        restored = geo_engine.find_boot_point_always(boot_epoch_override=1792809900)
        assert restored.resolution_tier_used == "TIER_2_HOARD_HLC_BOOT_JOURNAL"
        assert restored.hlc_logical_counter == 8
        assert restored.nearest_grid_crosspoint_id == "XPT_X02_Y06"

        # Verify binary BLOB row losslessly preserved in `sqlite_migrated_records`
        custom_doc = isolated_substrate.get_collection("sqlite_migrated_records").find_one(
            {"note_id": "N1"}
        )
        assert custom_doc is not None
        assert custom_doc["payload"] == {"__bytes_b64__": "AQL+/w=="}
    finally:
        live_writer.close()



def test_task_l4_cit_crosspoint_lattice_and_phoenix_orbital_loop(tmp_path):
    """
    Task L-4 (Part 1): Verifies the 12x10 = 120 CIT (X,Y) Crosspoint Lattice
    (25.0% Seeded / 75.0% Open), lossless CITBrailleCodec Morton (X,Y) codec,
    CelestialOrbitalClock checkpoint compounding, Phoenix planetary trajectory
    placement (KNOWLEDGE_DOCUMENT, SAVE_STATE_MEMORY, and |Z| > 3.0 ISOLATED_KINTSUGI_NODE
    auto-quarantine), orbital sweep search, and isolated MongoDB persistence.
    """
    import pytest
    from memory.database.mongodb_substrate import MongoDBPersistentSubstrate
    from memory.braille_atlas_engine import (
        CITBrailleCodec,
        CITCodexFlag,
        DatasetArchetype,
        PhoenixCelestialGridEngine,
    )

    # 1. Enforce Phase 2.4 20-30% initial deployment guard
    with pytest.raises(ValueError):
        PhoenixCelestialGridEngine(pretrained_capacity_ratio=0.10)
    with pytest.raises(ValueError):
        PhoenixCelestialGridEngine(pretrained_capacity_ratio=0.45)

    # 2. Lossless Morton Z-Order bijective codec on True Node Origin XY_16=(16171, 43905)
    m_origin = CITBrailleCodec.interleave_morton_xy16(16171, 43905)
    assert CITBrailleCodec.deinterleave_morton_xy16(m_origin) == (16171, 43905)
    pkt16 = CITBrailleCodec.encode_cit_packet_16(1792803600, int(CITCodexFlag.DOT1_EXPANSION), 16171, 43905, 0x123456789ABCDE)
    decoded = CITBrailleCodec.decode_cit_packet_16(pkt16)
    assert decoded["epoch_sec"] == 1792803600
    assert decoded["matrix_xy_16"] == (16171, 43905)
    assert decoded["matrix_xy_12"] == (1010, 2744)
    assert decoded["semantic_bq_56bit"] == 0x123456789ABCDE

    # 3. Initialize 12x10 = 120 lattice on isolated MongoDB substrate
    isolated_sub = MongoDBPersistentSubstrate(placeholder_root=tmp_path / "mongo_cit_l4")
    engine = PhoenixCelestialGridEngine(
        x_meridians=12,
        y_rings=10,
        pretrained_capacity_ratio=0.25,
        substrate=isolated_sub,
        persist_on_init=True,
    )
    cap_init = engine.grid_capacity_telemetry()
    assert cap_init["total_xy_crosspoints"] == 120
    assert cap_init["occupied_crosspoints"] == 30
    assert cap_init["open_crosspoints_available"] == 90
    assert cap_init["open_capacity_pct"] == 75.0
    assert cap_init["seeded_capacity_pct"] == 25.0
    assert engine.get_crosspoint("XPT_X02_Y06") is not None
    assert isolated_sub.get_collection("cit_crosspoints").count_documents() == 120

    # 4. Compound orbital accuracy across 2 solar orbits and 2 eclipse alignments
    engine.clock.register_orbital_checkpoint(is_eclipse_or_solstice=True, full_orbit=True)
    engine.clock.register_orbital_checkpoint(is_eclipse_or_solstice=True, full_orbit=True)

    # 5. Place all 3 storage archetypes (including automatic |Z|=4.25 > 3.0 Kintsugi quarantine)
    p_doc = engine.phoenix_orbital_place_dataset(
        dataset_id="DOC_SPIRAL_CLOCK_01",
        title="Rotating Spiral Brain Waves & 4D Celestial Metadata",
        raw_content="cortical spiral waves space time clock morton quadtree braille coordinate",
        archetype=DatasetArchetype.KNOWLEDGE_DOCUMENT,
        epoch_sec=1792803600,
        target_lat_hint=+64.0,
        target_lon_hint=-40.0,
    )
    p_save = engine.phoenix_orbital_place_dataset(
        dataset_id="SAVESTATE_SWDS_H04",
        title="SWDS Hour 4 Checkpointer Snapshot (Freeze-Serialize-Commit-Resume)",
        raw_content="save state memory checkpoint swds siesta 200 char trailing edge overlap",
        archetype=DatasetArchetype.SAVE_STATE_MEMORY,
        epoch_sec=1792807200,
        target_lat_hint=+12.0,
        target_lon_hint=+15.0,
    )
    # Pass KNOWLEDGE_DOCUMENT with z_score_anomaly=4.25 -> must auto-quarantine to ISOLATED_KINTSUGI_NODE!
    p_iso = engine.phoenix_orbital_place_dataset(
        dataset_id="KINTSUGI_CRACK_Z4_2",
        title="Isolated High-Entropy Trajectory Anomaly (|Z| = 4.25)",
        raw_content="isolated kintsugi anomaly crack sandbox quarantine volatility spike",
        archetype=DatasetArchetype.KNOWLEDGE_DOCUMENT,
        epoch_sec=1792810800,
        target_lat_hint=-72.0,
        target_lon_hint=+155.0,
        z_score_anomaly=4.25,
    )
    assert p_doc["archetype"] == "KNOWLEDGE_DOCUMENT"
    assert p_save["archetype"] == "SAVE_STATE_MEMORY"
    assert p_iso["archetype"] == "ISOLATED_KINTSUGI_NODE"
    assert (p_iso["cit_codex_flags_int"] & int(CITCodexFlag.DOT8_ISOLATED_NODE)) != 0
    assert len(p_doc["cit_braille_packet_16"]) == 16

    cap_after = engine.grid_capacity_telemetry()
    assert cap_after["occupied_crosspoints"] == 33
    assert cap_after["open_crosspoints_available"] == 87

    # Verify MongoDB collection persisted compressed_payload_zlib_b64 cleanly
    stored_doc = isolated_sub.get_collection("cit_crosspoints").find_one(
        {"crosspoint_id": p_doc["assigned_crosspoint_id"]}
    )
    assert stored_doc is not None
    assert stored_doc["stored_dataset_id"] == "DOC_SPIRAL_CLOCK_01"
    assert isinstance(stored_doc["compressed_payload_zlib_b64"], str)

    # 6. Orbital sweep search locates DOC_SPIRAL_CLOCK_01 as Rank #1
    sweep = engine.phoenix_orbital_locate_nodes(
        query_text="Rotating Spiral Brain Waves & 4D Celestial Metadata cortical spiral waves space time clock morton quadtree braille coordinate",
        search_epoch_sec=1792803600,
        top_k=3,
    )
    top_hit = sweep["top_located_nodes"][0]
    assert top_hit["dataset_id"] == "DOC_SPIRAL_CLOCK_01"
    assert top_hit["hamming_distance_bits"] == 0
    assert top_hit["mrl_768d_similarity"] > 0.99


def test_task_l4_throughput_calculus_mrl_nexus_and_mistake_loop(tmp_path):
    """
    Task L-4 (Part 2): Verifies Task 7 Equations 7.1-7.10:
      - NeuralGridThroughputEngine (Designation Action J, Potentials Phi_tax/Phi_sem/Phi_rel,
        Master Plot-Point Throughput Upsilon_{r,c}, RRF k=60, Epiphany Integral Omega, MongoDB persistence)
      - CompleteNeuralGridRouterV2 & RodinSupervisor (Mistake Loop + Shadow State Warm Cache,
        Two-Stage MRL 64D->768D, M_knn, EIG, SSR >= 0.95 gate, 4-Metric Nexus Decision Tree across
        Scenarios 2a/2e/2f + Indirect Connection + Clarify + Direct, and 4-Step Checkpointer + 170 MPa 7th Form).
    """
    from memory.database.mongodb_substrate import MongoDBPersistentSubstrate
    from memory.braille_atlas_engine import NeuralGridThroughputEngine, PhoenixCelestialGridEngine
    from memory.rodin_protocol import RodinProtocol
    from orchestration.rodin_supervisor import RodinSupervisor

    isolated_sub = MongoDBPersistentSubstrate(placeholder_root=tmp_path / "mongo_tp_l4")
    tp_engine = NeuralGridThroughputEngine(
        lat_rings=10,
        lon_meridians=12,
        substrate=isolated_sub,
        persist_on_init=True,
    )
    assert len(tp_engine.plot_points) == 120
    assert isolated_sub.get_collection("plot_points_state").count_documents() == 120

    d1 = tp_engine.designate_and_quantify_data(
        node_id="DATA_NODE_AXIOM_01",
        title="Bayesian Geodesic & Epistemology First Principles",
        raw_content="epistemology bayesian axiom logic starfire routing manifold",
        target_lat=+78.0,
        target_lon=+15.0,
        codex_byte=0x03,
    )
    d2 = tp_engine.designate_and_quantify_data(
        node_id="DATA_NODE_TUFTE_03",
        title="Tufte Visual Display Data-Ink Ratio & Lie Factor",
        raw_content="visual information display tufte data ink geometry lie factor",
        target_lat=+58.0,
        target_lon=+105.0,
        codex_byte=0x03,
    )
    tp_engine.link_plot_points(d1.assigned_plot_point_id, d2.assigned_plot_point_id, weight=0.96)

    tp_out = tp_engine.evaluate_neural_grid_throughput(
        query_text="epistemology bayesian axiom logic starfire manifold",
        target_hemisphere="NE",
        target_zone="Z5_NORTH_POLE",
        cwa_nexus_posterior=0.50,
        top_k=3,
    )
    assert tp_out["epiphany_integral_omega"] > 0.0
    rank1 = tp_out["top_routed_plot_points"][0]
    assert "DATA_NODE_AXIOM_01" in rank1["designated_nodes"]
    assert rank1["rrf_fusion_score"] > 0.0

    # Wire RodinProtocol + CompleteNeuralGridRouterV2 + RodinSupervisor
    rodin = RodinProtocol()
    router = rodin.get_neural_grid_router()
    router.register_plot_point(
        plot_point_id="HOARD_CONV_HIST",
        title="Show me the hoard conversation history log",
        raw_content="hoard conversation history chat turns archive thread",
        ccid="CCID_UI_TABS",
        lat_deg=+15.0,
        lon_deg=-45.0,
        trigger_keyword="hoard",
        initial_conf=0.70,
    )
    router.register_plot_point(
        plot_point_id="HOARD_FILE_VIEW",
        title="Show me the hoard files and cold storage vault",
        raw_content="show me the hoard files cold storage database nodes",
        ccid="CCID_UI_TABS",
        lat_deg=+18.0,
        lon_deg=-42.0,
        trigger_keyword="hoard",
        initial_conf=0.45,
    )
    router.register_plot_point(
        plot_point_id="PLOT_QUANTUM_RL_STALE",
        title="Quantum Reinforcement Learning Policy Gradients",
        raw_content="analyze this new paper on quantum rl policy gradients",
        ccid="CCID_RESEARCH",
        lat_deg=+52.0,
        lon_deg=+14.0,
        stale_days=19.0,
        initial_conf=0.88,
    )

    # Eq. 7.9 Mistake Loop & Shadow State Warm Cache
    corr = rodin.apply_mistake_loop_correction(
        {
            "trigger": "hoard",
            "previous_id": "HOARD_CONV_HIST",
            "new_id": "HOARD_FILE_VIEW",
            "user_feedback": "direct_correction",
        }
    )
    assert corr["previous_confidence_after"] < 0.40
    assert corr["new_confidence_after"] > 0.70
    assert "HOARD_CONV_HIST" not in corr["active_shadow_state_ids"]
    assert "HOARD_FILE_VIEW" in corr["active_shadow_state_ids"]

    # Test A: Command routed to corrected HOARD_FILE_VIEW (Direct Answer + SSR >= 0.95)
    res_a = rodin.route_neural_grid_query(
        prompt="Show me the hoard files and cold storage vault",
        active_context_tokens=52000,
    )
    assert res_a.winning_plot_point_id == "HOARD_FILE_VIEW"
    assert res_a.ssr_confidence_score >= 0.95
    assert res_a.ssr_gate_action == "PROCEED_TO_OUTPUT"
    assert res_a.nexus_decision_outcome == "DIRECT_MULTIDIMENSIONAL_ANSWER"
    assert res_a.m_knn > 0.80

    # Test B: Scenario 2a Conversational Continuation + 175.0 MPa >= 170.0 MPa 7th Form Cavitation
    res_b = rodin.route_neural_grid_query(
        prompt="Show me the hoard files and cold storage vault.",
        active_context_tokens=175000,
    )
    assert res_b.nexus_decision_outcome == "SCENARIO_2A_CONVERSATIONAL_CONTINUATION"
    assert res_b.rodin_constitutional_outcome == "CONVERSATIONAL_CONTINUATION"
    assert res_b.checkpointer_receipt.axial_stress_mpa == 175.0
    assert res_b.checkpointer_receipt.seventh_form_cavitation_active is True
    assert res_b.checkpointer_receipt.sequence_stages_completed == [
        "1_FREEZE",
        "2_SERIALIZE",
        "3_COMMIT",
        "4_RESUME",
    ]

    # Test C: Scenario 2e Stale Verification
    res_c = rodin.route_neural_grid_query(
        prompt="Analyze this new paper on quantum rl policy gradients?",
        active_context_tokens=64000,
    )
    assert res_c.m_stale is True
    assert res_c.nexus_decision_outcome == "SCENARIO_2E_ALEXANDRIA_VERIFY_STALE"
    assert res_c.rodin_constitutional_outcome == "ALEXANDRIA_VERIFICATION"

    # Test D: Scenario 2f Alexandria Guided Search vs Request Clarification
    res_d = rodin.route_neural_grid_query(
        prompt="completely unrelated exoplanet magnetosphere spectroscopy?",
        intent_confidence=0.91,
    )
    assert res_d.nexus_decision_outcome == "SCENARIO_2F_ALEXANDRIA_GUIDED_SEARCH"
    assert res_d.rodin_constitutional_outcome == "ALEXANDRIA_GUIDED_SEARCH"

    res_e = rodin.route_neural_grid_query(
        prompt="completely unrelated exoplanet magnetosphere spectroscopy?",
        intent_confidence=0.40,
    )
    assert res_e.nexus_decision_outcome == "NEXUS_REQUEST_CLARIFICATION"
    assert res_e.rodin_constitutional_outcome == "REQUEST_CLARIFICATION"

    # Test F: RodinSupervisor unified CIT orbital + throughput + Nexus dispatch
    cit_engine = PhoenixCelestialGridEngine(substrate=isolated_sub)
    sup = RodinSupervisor(rodin_protocol=rodin, cit_grid_engine=cit_engine, throughput_engine=tp_engine)
    sup_out = sup.dispatch_cit_orbital_route(
        prompt="Show me the hoard files and cold storage vault",
        search_epoch_sec=1792803600,
    )
    assert sup_out["cit_capacity"]["total_xy_crosspoints"] == 120
    assert sup_out["nexus_decision_route"]["winning_plot_point_id"] == "HOARD_FILE_VIEW"



def test_task_l5_forge_read_locks_and_sun_breathing_preemption(tmp_path):
    """
    Task L-5.1: Verifies exclusive Forge read-locks block uncommitted reads across Cheshire/Rodin
    and zero out Plot-Point Throughput Upsilon_{r,c}, and that active user prompt preemption
    atomically releases locks and re-queues Forge tasks via EAM.
    """
    from governance.security_protocols import ForgeReadLockManager
    from memory.braille_atlas_engine import NeuralGridThroughputEngine
    from memory.database.mongodb_substrate import MongoDBPersistentSubstrate
    from memory.the_hoard import TheHoard
    from sensory.cheshire_cat import CheshireCatKernel

    sub = MongoDBPersistentSubstrate(placeholder_root=tmp_path / "mongo_l5")
    tp_engine = NeuralGridThroughputEngine(substrate=sub, persist_on_init=False)
    designated = tp_engine.designate_and_quantify_data(
        node_id="NODE_FORGE_01",
        title="Sovereign Land Security & Forge Lock Axiom",
        raw_content="sovereign land security forge read lock axiom baker louisiana",
        target_lat=30.5888,
        target_lon=-91.1673,
        codex_byte=0x03,
    )
    target_pp = designated.assigned_plot_point_id

    unlocked_tp = tp_engine.evaluate_neural_grid_throughput(
        query_text="sovereign land security forge read lock axiom",
        top_k=120,
    )
    unlocked_ids = [p["plot_point_id"] for p in unlocked_tp["top_routed_plot_points"]]
    assert target_pp in unlocked_ids

    lock_mgr = ForgeReadLockManager(substrate=sub, persist_to_placeholder=True)
    lock_mgr.acquire_forge_lock(
        node_id="NODE_FORGE_01",
        forge_task_id="FORGE_SWDS_BATCH_01",
        plot_point_id=target_pp,
        throughput_engine=tp_engine,
    )
    lock_mgr.acquire_forge_lock(
        node_id="NODE_FORGE_02",
        forge_task_id="FORGE_SWDS_BATCH_02",
    )

    assert lock_mgr.is_node_readable("NODE_FORGE_01") is False
    assert lock_mgr.is_node_readable("NODE_COMMITTED_CLEAN") is True
    assert tp_engine.plot_points[target_pp].forge_read_locked is True
    locked_tp = tp_engine.evaluate_neural_grid_throughput(
        query_text="sovereign land security forge read lock axiom",
        top_k=120,
    )
    locked_ids = [p["plot_point_id"] for p in locked_tp["top_routed_plot_points"]]
    assert target_pp not in locked_ids

    filtered = lock_mgr.filter_readable_nodes(
        [
            {"ccid": "NODE_FORGE_01", "payload": "uncommitted"},
            {"ccid": "NODE_COMMITTED_CLEAN", "payload": "committed"},
            {"node_id": "NODE_FORGE_02", "payload": "uncommitted_2"},
        ]
    )
    assert [n.get("ccid") or n.get("node_id") for n in filtered] == ["NODE_COMMITTED_CLEAN"]

    # Cheshire Cat Kernel EAM Preemption on active Sun Breathing user prompt
    iso_hoard = TheHoard(
        base_dir=str(tmp_path / "hoard_l5"),
        chroma_path=str(tmp_path / "chroma_l5"),
    )
    cheshire = CheshireCatKernel(hoard_instance=iso_hoard)
    cheshire.forge_lock_manager = lock_mgr
    cheshire.transition_state("GUARDIAN_STANDBY_SWDS")

    preempt = cheshire.preempt_for_user_prompt(
        prompt="Execute immediate waking architectural query",
        throughput_engine=tp_engine,
    )
    assert preempt["status"] == "FORGE_LOCKS_PREEMPTED_AND_REQUEUED"
    assert set(preempt["released_nodes"]) == {"NODE_FORGE_01", "NODE_FORGE_02"}
    assert preempt["requeued_task_ids"] == ["FORGE_SWDS_BATCH_01", "FORGE_SWDS_BATCH_02"]
    assert cheshire.state == "INTERACTIVE_STANDBY"
    assert lock_mgr.is_node_readable("NODE_FORGE_01") is True
    assert tp_engine.plot_points[target_pp].forge_read_locked is False

    restored_tp = tp_engine.evaluate_neural_grid_throughput(
        query_text="sovereign land security forge read lock axiom",
        top_k=120,
    )
    restored_ids = [p["plot_point_id"] for p in restored_tp["top_routed_plot_points"]]
    assert target_pp in restored_ids

    popped = lock_mgr.pop_requeued_tasks()
    assert len(popped) == 2
    assert lock_mgr.get_status()["requeued_task_count"] == 0


def test_task_l5_two_man_hmac_authenticator_and_model_router_p0(tmp_path):
    """
    Task L-5.2: Verifies 2-Man HMAC-SHA256 Authenticator (`CHESHIRE_CAT_ACK::{batch_sha256}::PHOENIX_FORCE_FLIGHT_AUTH`)
    requiring both Key 1 (Architect / JeanGreyPhoenixForce + confirmation threshold) and
    Key 2 (CheshireCatKernel + DragonEngine + Heimdall31), plus ModelRouter P0 gating.
    """
    import hashlib
    from core.model_router import MODEL_ROUTER, PowerState
    from governance.security_protocols import PhoenixFlightTwoManAuthenticator
    from memory.the_hoard import TheHoard
    from sensory.cheshire_cat import CheshireCatKernel

    auth = PhoenixFlightTwoManAuthenticator(
        architect_secret="TEST_ARCHITECT_KEY1_SOVEREIGN",
        kernel_secret="TEST_KERNEL_KEY2_THALAMIC",
    )
    batch_hash = hashlib.sha256(b"SWDS_HISTORICAL_HANDOFF_BATCH_OCT24").hexdigest()
    expected_env = f"CHESHIRE_CAT_ACK::{batch_hash}::PHOENIX_FORCE_FLIGHT_AUTH"
    assert auth.build_canonical_envelope(batch_hash) == expected_env

    # 1. Reject wrong Key 1 secret
    bad_k1 = auth.issue_2man_hmac_token(batch_hash, architect_secret="WRONG_KEY1")
    assert bad_k1["issued"] is False
    assert bad_k1["reason"] == "INVALID_ARCHITECT_KEY1_SECRET"

    # 2. Reject wrong Key 2 secret
    bad_k2 = auth.issue_2man_hmac_token(
        batch_hash,
        architect_secret="TEST_ARCHITECT_KEY1_SOVEREIGN",
        kernel_secret="WRONG_KEY2",
    )
    assert bad_k2["issued"] is False
    assert bad_k2["reason"] == "INVALID_KERNEL_KEY2_SECRET"

    # 3. Reject Jean Grey Pass threshold > 1000 without explicit Architect confirmation
    unconfirmed_jg = auth.issue_2man_hmac_token(
        batch_hash,
        architect_secret="TEST_ARCHITECT_KEY1_SOVEREIGN",
        kernel_secret="TEST_KERNEL_KEY2_THALAMIC",
        amount=2500,
        architect_confirmed=False,
    )
    assert unconfirmed_jg["issued"] is False
    assert "JEAN_GREY_THRESHOLD_UNCONFIRMED" in unconfirmed_jg["reason"]

    # 4. Reject when Heimdall entropy is breached (H_smooth > 2.5) or Dragon inactive
    breached_hm = auth.issue_2man_hmac_token(
        batch_hash,
        architect_secret="TEST_ARCHITECT_KEY1_SOVEREIGN",
        kernel_secret="TEST_KERNEL_KEY2_THALAMIC",
        h_smooth=2.95,
    )
    assert breached_hm["issued"] is False
    assert "HEIMDALL" in breached_hm["reason"]

    # 5. Valid 2-Man HMAC token issuance (including confirmed Jean Grey amount=2500)
    valid_pkt = auth.issue_2man_hmac_token(
        batch_hash,
        architect_secret="TEST_ARCHITECT_KEY1_SOVEREIGN",
        kernel_secret="TEST_KERNEL_KEY2_THALAMIC",
        amount=2500,
        architect_confirmed=True,
        cheshire_ack=True,
        dragon_active=True,
        heimdall_healthy=True,
        h_smooth=0.42,
    )
    assert valid_pkt["issued"] is True
    assert valid_pkt["envelope"] == expected_env

    # 6. Single-key forgery attempts MUST fail verification & ModelRouter P0 gate
    forged_key2_pkt = dict(valid_pkt, sig_key2="0" * 64)
    MODEL_ROUTER.disengage_phoenix_force(return_to=PowerState.P1_ACTIVE)
    denied = MODEL_ROUTER.engage_phoenix_force_2man(
        batch_sha256=batch_hash,
        token_packet=forged_key2_pkt,
        authenticator=auth,
    )
    assert denied["verified"] is False
    assert denied["status"] == "PHOENIX_FORCE_DENIED_INVALID_2MAN_HMAC"
    assert MODEL_ROUTER.get_status()["phoenix_force_active"] is False

    # Tampered batch hash MUST fail
    tampered_batch = hashlib.sha256(b"TAMPERED_BATCH").hexdigest()
    tampered_ver = auth.verify_2man_hmac_token(tampered_batch, valid_pkt)
    assert tampered_ver["verified"] is False
    assert tampered_ver["reason"] == "ENVELOPE_MISMATCH_OR_BATCH_TAMPERED"

    # 7. End-to-end CheshireCatKernel -> ModelRouter P0 engagement & clean disengage
    iso_hoard = TheHoard(
        base_dir=str(tmp_path / "hoard_hmac"),
        chroma_path=str(tmp_path / "chroma_hmac"),
    )
    cheshire = CheshireCatKernel(hoard_instance=iso_hoard)
    cheshire.two_man_authenticator = auth
    handoff = cheshire.authorize_phoenix_flight_2man(
        batch_sha256=batch_hash,
        architect_secret="TEST_ARCHITECT_KEY1_SOVEREIGN",
        amount=1500,
        architect_confirmed=True,
        dragon_active=True,
        router=MODEL_ROUTER,
    )
    try:
        assert handoff["authorized"] is True
        assert handoff["status"] == "PHOENIX_FORCE_ACTIVE"
        st = MODEL_ROUTER.get_status()
        assert st["global_power_state"] == "P0_PHOENIX_FORCE"
        assert st["two_man_hmac_verified"] is True
        assert st["last_phoenix_batch_sha256"] == batch_hash
    finally:
        MODEL_ROUTER.disengage_phoenix_force(return_to=PowerState.P1_ACTIVE)


def test_task_l5_tiered_deviation_guardrail_and_cli_circuit_breaker(tmp_path):
    """
    Task L-5.3: Verifies TieredDeviationGuardrail (Levels 0-4, CRISIS_PAUSE coma +
    Command(resume="APPROVED")) and CLIDerivativeCircuitBreaker (CONFUSION > 15.0 PPL,
    MANIC > 3.0 ops/s, STUCK > 80% n-gram + Proactive UGL Lookback Restart).
    """
    import asyncio
    from governance.security_protocols import (
        CLIDerivativeCircuitBreaker,
        DeviationLevel,
        TieredDeviationGuardrail,
    )
    from memory.the_hoard import TheHoard
    from sensory.cheshire_cat import CheshireCatKernel

    guard = TieredDeviationGuardrail()
    assert guard.evaluate_deviation(2.0).level == DeviationLevel.NOMINAL_0
    assert guard.evaluate_deviation(8.5).level == DeviationLevel.LEVEL_1_5
    assert guard.evaluate_deviation(19.0).level == DeviationLevel.LEVEL_2_15

    lvl3 = guard.evaluate_deviation(38.0)
    assert lvl3.level == DeviationLevel.LEVEL_3_35
    assert guard.in_crisis_coma is True
    assert lvl3.cooling_off_hours == 6
    assert lvl3.resume_command_required == 'Command(resume="APPROVED")'
    assert guard.resume_from_crisis({"resume": "WRONG_TOKEN"}) is False
    assert guard.in_crisis_coma is True
    assert guard.resume_from_crisis({"resume": "APPROVED"}) is True
    assert guard.in_crisis_coma is False

    lvl4 = guard.evaluate_deviation(12.0, violates_immutable_principle=True)
    assert lvl4.level == DeviationLevel.LEVEL_4_MAX
    assert guard.session_isolated is True
    assert guard.resume_from_crisis({"resume": "APPROVED"}) is False
    assert guard.resume_from_crisis({"resume": "SOVEREIGN_OVERRIDE_APPROVED"}) is True

    # CheshireCatKernel Crisis Coma execution gate
    iso_hoard = TheHoard(
        base_dir=str(tmp_path / "hoard_dev"),
        chroma_path=str(tmp_path / "chroma_dev"),
    )
    cheshire = CheshireCatKernel(hoard_instance=iso_hoard)
    dev_out = cheshire.evaluate_land_security_deviation(41.5)
    assert dev_out["kernel_state"] == "CRISIS_PAUSE_COMA"
    blocked_cycle = asyncio.run(cheshire.process_cognitive_cycle("Execute leveraged FOMO trade now"))
    assert blocked_cycle["status"] == "CRISIS_PAUSE::EXECUTION_BLOCKED"
    resumed = cheshire.resume_from_crisis_pause({"resume": "APPROVED"})
    assert resumed["resumed"] is True
    assert cheshire.state == "INTERACTIVE_STANDBY"

    # CLIDerivativeCircuitBreaker: CONFUSION, MANIC, STUCK + Proactive UGL Restart
    cb = CLIDerivativeCircuitBreaker()
    assert cb.evaluate_derivatives(6.2, 1.4, 15.0).is_open is False

    confusion = cb.evaluate_derivatives(18.5, 1.2, 10.0)
    assert confusion.is_open is True
    assert "CONFUSION" in confusion.trigger_reason

    manic = cb.evaluate_derivatives(5.0, 4.1, 10.0)
    assert manic.is_open is True
    assert "MANIC" in manic.trigger_reason

    stuck_text = " ".join(["alpha beta gamma"] * 12)
    rep_pct = cb.compute_ngram_repetition_pct(stuck_text, n=3)
    assert rep_pct > 80.0
    stuck = cb.evaluate_derivatives(5.0, 1.0, rep_pct)
    assert stuck.is_open is True
    assert "STUCK" in stuck.trigger_reason

    stream = [
        {"token": "Analyzing ", "perplexity": 4.2, "velocity": 1.1, "ngram_rep": 0.0},
        {"token": "orbital ", "perplexity": 5.1, "velocity": 1.3, "ngram_rep": 5.0},
        {"token": "hallucinated_loop ", "perplexity": 19.8, "velocity": 3.6, "ngram_rep": 88.0},
        {"token": " Baker, Louisiana XPT_X02_Y06 confirmed.", "perplexity": 3.4, "velocity": 1.0, "ngram_rep": 0.0},
    ]
    decoded = cb.execute_proactive_decoding_loop(
        initial_context_c="Anchor check:",
        token_stream_steps=stream,
        ugl_grounding_fact="True Origin = 30.5888N, -91.1673W (XPT_X02_Y06)",
    )
    assert decoded["generator_restarts"] == 1
    assert "[UGL_GROUNDING_INJECTED: True Origin = 30.5888N, -91.1673W (XPT_X02_Y06)]" in decoded["context_c"]
    assert "hallucinated_loop" not in decoded["worker_buffer_b"]
    assert "XPT_X02_Y06 confirmed." in decoded["final_output_o_final"]
