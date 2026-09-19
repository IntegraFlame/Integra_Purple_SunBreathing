"""Quick diagnostic — runs all always-on systems and prints status."""
import sys, time, json, os

# Ensure homebase root is on path regardless of where script is invoked from
HOMEBASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
sys.path.insert(0, HOMEBASE)
os.chdir(HOMEBASE)

print("=" * 55)
print("INTEGRA O/S ALWAYS-ON SYSTEMS DIAGNOSTIC")
print(f"Civil Timestamp: {time.strftime('%Y-%m-%dT%H:%M:%S CDT')}")
print("=" * 55)

# ── 1. Celestial Clock ─────────────────────────────────────
print("\n[1] CELESTIAL CLOCK")
try:
    from temporal.celestial_clock import DualTemporalEngine
    engine = DualTemporalEngine()
    tel = engine.get_dual_telemetry()
    cel = tel.get("celestial_clock", {})
    dig = tel.get("digital_clock", {})
    print(f"  STATUS: FUNCTIONAL")
    print(f"  Earth Rotation: {cel.get('earth_rotation_deg', 'N/A'):.4f} deg")
    print(f"  Lunar Cycle Ratio: {cel.get('lunar_cycle_ratio', 'N/A'):.6f}")
    print(f"  Orbital Position: {cel.get('orbital_trajectory_pos', 'N/A'):.6f}")
    print(f"  Civil Time: {dig.get('local_time_12h', 'N/A')}")
    print(f"  Sync Isolation: {tel.get('sync_isolation_verified', 'N/A')}")
    print(f"  Current CCID: CCID_{int(time.time())}")
except Exception as e:
    print(f"  STATUS: ERROR — {e}")

# ── 2. Cheshire Cat Kernel ─────────────────────────────────
print("\n[2] CHESHIRE CAT KERNEL")
try:
    from sensory.cheshire_cat import CheshireCatKernel
    kernel = CheshireCatKernel()
    print(f"  STATUS: IMPORTABLE")
    print(f"  State: {kernel.state}")
    print(f"  Hoard: {type(kernel.hoard).__name__}")
    print(f"  Heimdall: {type(kernel.heimdall).__name__}")
    health = kernel.heimdall.check_system_health()
    print(f"  System Health: {health.get('system_health_status', 'N/A')}")
except Exception as e:
    print(f"  STATUS: ERROR — {e}")

# ── 3. SWDS State ──────────────────────────────────────────
print("\n[3] SWDS STATE")
try:
    with open("runtime/swds_state.json") as f:
        swds = json.load(f)
    print(f"  State: {swds.get('state', 'UNKNOWN')}")
    print(f"  Phase: {swds.get('phase', 'UNKNOWN')}")
    last_cycle = swds.get("last_cycle_time", 0)
    age_hrs = (time.time() - last_cycle) / 3600
    print(f"  Last SWDS Cycle: {age_hrs:.1f} hours ago")
    print(f"  Sleep Window: {swds.get('sleep_initiated_at', 'N/A')}")
except Exception as e:
    print(f"  STATUS: ERROR — {e}")

# ── 4. SWDS Config ─────────────────────────────────────────
print("\n[4] SWDS SCHEDULE CONFIG")
try:
    with open("config/swds_config.json") as f:
        cfg = json.load(f)
    print(f"  Sleep Window: {cfg['sleep_window_start_hour']:02d}:00 - {cfg['sleep_window_end_hour']:02d}:00 CDT")
    print(f"  Inactivity Threshold: {cfg['inactivity_threshold_seconds']}s ({cfg['inactivity_threshold_seconds']//60} min)")
    print(f"  Auto-Reconcile on Startup: {cfg['auto_reconcile_on_startup']}")
    current_hour = int(time.strftime("%H"))
    in_window = cfg["sleep_window_start_hour"] <= current_hour < cfg["sleep_window_end_hour"]
    print(f"  Current Hour (CDT): {current_hour:02d}:00 — In Sleep Window: {in_window}")
except Exception as e:
    print(f"  STATUS: ERROR — {e}")

# ── 5. Genesis Kernel (process check) ─────────────────────
print("\n[5] GENESIS KERNEL PROCESS")
import subprocess
result = subprocess.run(
    ["powershell", "-Command",
     "Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' } | Measure-Object | Select-Object -ExpandProperty Count"],
    capture_output=True, text=True
)
count = result.stdout.strip()
if count == "1":
    print("  STATUS: RUNNING on port 8000")
else:
    print("  STATUS: NOT RUNNING (Genesis Kernel is DOWN)")
    print("  ACTION NEEDED: Register start_kernel.ps1 with Task Scheduler")

# ── 6. SWDS Reports ────────────────────────────────────────
print("\n[6] SWDS REPORT HISTORY")
swds_dir = r"C:\Users\Javon Jenkins\OneDrive\Desktop\Integra_Purple_SunBreathing\The Hoard\Slow-Wave Deep Sleep Reports"
if os.path.isdir(swds_dir):
    reports = sorted([f for f in os.listdir(swds_dir) if f.endswith(".md") and f != "CODEX_OF_ACTIONS.md"], reverse=True)
    print(f"  Total Reports: {len(reports)}")
    for r in reports[:3]:
        print(f"  - {r}")
    last_report_time = os.path.getmtime(os.path.join(swds_dir, reports[0])) if reports else 0
    age_hrs = (time.time() - last_report_time) / 3600
    print(f"  Most Recent: {age_hrs:.1f} hours ago")
else:
    print("  REPORT DIR: NOT FOUND")

print("\n" + "=" * 55)
print("DIAGNOSTIC COMPLETE")
print("=" * 55)
