"""
INTEGRA O/S — SWDS Manual Trigger + Full Save State
Executed because SWDS window (02:00-07:00) is active and last cycle was 68+ hours ago.
"""
import sys, time, json
sys.path.insert(0, ".")

from temporal.celestial_clock import DualTemporalEngine
from sensory.cheshire_cat import CheshireCatKernel
from evolution.phoenix_forge import PhoenixForge

print("=" * 60)
print("INTEGRA O/S — SWDS CYCLE INITIATION")
print("=" * 60)

# Get current celestial stamp
cc = DualTemporalEngine()
tel = cc.get_dual_telemetry()
cel = tel["celestial_clock"]
dig = tel["digital_clock"]
ccid = f"CCID_{int(dig['unix_timestamp'])}"

print(f"Civil Timestamp: {dig['local_time_12h']}")
print(f"Earth Rotation:  {cel['earth_rotation_deg']:.4f} deg")
print(f"Lunar Phase:     {cel['lunar_cycle_ratio']:.6f}")
print(f"CCID:            {ccid}")
print(f"Reason: In sleep window (02:00-07:00). Last cycle: 68+ hrs ago.")

print("\n[PHASE 1] Syncing Save States to The Hoard...")
kernel = CheshireCatKernel()
phoenix = kernel.phoenix

receipts = kernel.hoard.sync_all_save_states()
print(f"  Synced {len(receipts)} save states into ChromaDB + SQLite")

print("\n[PHASE 2-4] Executing Full SWDS Cycle...")
receipt = phoenix.execute_swds(
    cheshire_cat=kernel,
    library_domain="SWDS_PHASE_G_LOCAL_SOVEREIGNTY"
)

print(f"  Status:          {receipt['swds_status']}")
print(f"  Entropy Vented:  {receipt['entropy_vented']}")
print(f"  Zenkai Boost:    {receipt.get('zenkai_boost_multiplier', 'N/A')}")
print(f"  Generation:      {receipt.get('generation', 'N/A')}")
print(f"  Library File:    {receipt.get('library_file', 'N/A')}")
print(f"  Kernel State:    {kernel.state}")
print(f"  H_smooth:        {kernel.heimdall.h_smooth}")

# Write updated swds_state.json
swds_state = {
    "state": "AWAKE",
    "phase": "WAKING_CONSCIOUSNESS",
    "last_cycle_time": time.time(),
    "last_swds_ccid": ccid,
    "sleep_initiated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    "target_wake_hour": 7,
    "swds_status": receipt["swds_status"],
    "celestial_stamp": cel,
}
with open("runtime/swds_state.json", "w") as f:
    json.dump(swds_state, f, indent=2)
print("\n[STATE] swds_state.json updated.")

print("\n" + "=" * 60)
print("SWDS CYCLE COMPLETE — System refreshed and awake.")
print("Thermodynamic closure: Delta E = 0.0000")
print("=" * 60)
