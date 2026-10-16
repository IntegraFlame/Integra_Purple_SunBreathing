"""T1 step 1.1 / 1.3 evidence: how far are the clock's phase-0 instants from real astronomy?

Stdlib only, no network, writes nothing. Scratchpad script, not part of the repo.
New moons: Meeus, Astronomical Algorithms ch. 49, main periodic terms only (no planetary
terms) => accuracy of a few minutes. DERIVED, not Tier 1.
Perihelion instant: taken from NASA APOD / USNO via search summary (grade B), not computed.
"""
import math
import sys
from datetime import datetime, timedelta, timezone

sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv[1])  # path to the isolated snapshot
import temporal.celestial_clock as cc  # noqa: E402  (pure module, no side effects on import)

UTC = timezone.utc
BASE_EPOCH = cc.BASE_EPOCH
LAB_EPOCH = datetime(2026, 7, 15, 12, 0, tzinfo=UTC).timestamp()
P_L = cc.LUNAR_CYCLE_SEC
P_SID = cc.SIDEREAL_YEAR_SEC
D = 86400.0
rad = math.radians


def jde_to_dt(jde):
    # JD 2440587.5 = 1970-01-01T00:00Z ; ignore delta-T (~69 s in 2026) for this purpose
    return datetime(1970, 1, 1, tzinfo=UTC) + timedelta(days=jde - 2440587.5)


def new_moon_jde(k):
    T = k / 1236.85
    jde = (2451550.09766 + 29.530588861 * k + 0.00015437 * T**2
           - 0.000000150 * T**3 + 0.00000000073 * T**4)
    E = 1 - 0.002516 * T - 0.0000074 * T**2
    M = rad(2.5534 + 29.10535670 * k - 0.0000014 * T**2 - 0.00000011 * T**3)
    Mp = rad(201.5643 + 385.81693528 * k + 0.0107582 * T**2 + 0.00001238 * T**3 - 0.000000058 * T**4)
    F = rad(160.7108 + 390.67050284 * k - 0.0016118 * T**2 - 0.00000227 * T**3 + 0.000000011 * T**4)
    Om = rad(124.7746 - 1.56375588 * k + 0.0020672 * T**2 + 0.00000215 * T**3)
    c = (-0.40720 * math.sin(Mp) + 0.17241 * E * math.sin(M) + 0.01608 * math.sin(2 * Mp)
         + 0.01039 * math.sin(2 * F) + 0.00739 * E * math.sin(Mp - M) - 0.00514 * E * math.sin(Mp + M)
         + 0.00208 * E**2 * math.sin(2 * M) - 0.00111 * math.sin(Mp - 2 * F) - 0.00057 * math.sin(Mp + 2 * F)
         + 0.00056 * E * math.sin(2 * Mp + M) - 0.00042 * math.sin(3 * Mp) + 0.00042 * E * math.sin(M + 2 * F)
         + 0.00038 * E * math.sin(M - 2 * F) - 0.00024 * E * math.sin(2 * Mp - M) - 0.00017 * math.sin(Om)
         - 0.00007 * math.sin(Mp + 2 * M))
    return jde + c


nm = {}
for k in range(326, 337):
    dt = jde_to_dt(new_moon_jde(k))
    nm[k] = dt
    print(f"k={k}  new moon {dt:%Y-%m-%d %H:%M}Z")

# --- A. Is BASE_EPOCH (or its label) near a new moon?
def nearest_nm(ts):
    t = datetime.fromtimestamp(ts, tz=UTC)
    k = min(nm, key=lambda x: abs((nm[x] - t).total_seconds()))
    return nm[k], (t - nm[k]).total_seconds() / D

for name, ts in (("BASE_EPOCH value 2026-07-26T08:00Z", BASE_EPOCH), ("label 2026-07-15T12:00Z", LAB_EPOCH)):
    n, off = nearest_nm(ts)
    print(f"\n{name}: nearest new moon {n:%Y-%m-%d %H:%M}Z, offset {off:+.3f} d = {off*D/P_L:+.4f} cycle (true age fraction {(off*D/P_L)%1:.4f})")

# --- B. perihelion vs the clock's orbital phase 0
PERI = datetime(2026, 1, 3, 17, 16, tzinfo=UTC)  # NASA APOD 17:16 UTC; USNO 09:15 ST(UTC-8)=17:15Z
ANOM_YEAR_D = 365.259636  # CLAIMED (standard value), not fetched this session
for name, ts in (("BASE_EPOCH value", BASE_EPOCH), ("label", LAB_EPOCH)):
    dt = datetime.fromtimestamp(ts, tz=UTC)
    days = (dt - PERI).total_seconds() / D
    print(f"{name}: {days:.2f} d after the 2026 perihelion = {days/ANOM_YEAR_D:.4f} of an anomalistic year "
          f"(the clock calls this instant orbit phase 0)")

# --- C. Clock vs astronomy at the recorded live stamp and at 'now'
def clock_at(ts):
    import time as _t
    real = _t.time
    _t.time = lambda: ts
    try:
        v = cc.CelestialClockArchitecture().compute_4d_coordinates()
    finally:
        _t.time = real
    return v

def true_age_frac(dt):
    prev = max(n for n in nm.values() if n <= dt)
    return ((dt - prev).total_seconds() / D) / 29.530588861, prev

for label, dt in (("recorded live stamp 2026-10-12T01:54:25Z", datetime(2026, 10, 12, 1, 54, 25, tzinfo=UTC)),
                  ("container now", datetime.now(UTC))):
    v = clock_at(dt.timestamp())
    tf, prev = true_age_frac(dt)
    days_peri = (dt - PERI).total_seconds() / D
    true_orbit_frac = (days_peri / ANOM_YEAR_D) % 1  # mean-anomaly fraction since true perihelion
    print(f"\n{label}")
    print(f"  clock : lunar {v.lunar_cycle_ratio:.4f}  orbit(E/2pi) {v.orbital_trajectory_pos:.4f}  rot {v.earth_rotation_deg:.4f}")
    print(f"  true  : lunar age fraction {tf:.4f} (last new moon {prev:%m-%d %H:%M}Z)  mean-anomaly fraction since perihelion {true_orbit_frac:.4f}")
    print(f"  clock minus true: lunar {((v.lunar_cycle_ratio - tf + .5) % 1) - .5:+.4f} cycle   orbit(mean-anomaly-equivalent) differs by about {((cc.EllipticalKeplerEngine().compute_mean_anomaly(dt.timestamp()-BASE_EPOCH)/(2*math.pi)) - true_orbit_frac + .5) % 1 - .5:+.4f} cycle")

# --- D. Year-constant spread
print("\nYear definitions (days / seconds):")
for n, sec in (("code SIDEREAL_YEAR_SEC", P_SID), ("spec P_E (labelled 'Sidereal')", 31556952.0),
               ("anomalistic 365.259636 d (CLAIMED)", 365.259636 * D), ("tropical 365.24219 d (CLAIMED)", 365.24219 * D),
               ("sacred year 364 d (calendar)", 364 * D)):
    print(f"  {n:38} {sec:16,.3f} s  {sec/D:10.5f} d")
d = P_SID - 31556952.0
print(f"code minus spec = {d:,.3f} s per year = {d/60:.2f} min; as a phase = {d/P_SID:.2e} cycle/yr = {d/P_SID*360:.4f} deg/yr")
print(f"orbit_pos rounds to 4 decimals (1e-4 cycle): this alone reaches one rounding unit after {1e-4/(d/P_SID):.1f} yr")
print("\n364-day sacred year vs sidereal: drift", f"{(P_SID-364*D)/D:.4f} d/yr; 964 d jubilee:", f"{964/(P_SID/D):.4f} sidereal yr")
