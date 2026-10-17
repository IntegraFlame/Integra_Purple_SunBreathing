"""Integra Atlas reference implementation (Brain Map Task 10 unification script).

Standard library only. Imports nothing from the Integra kernel and writes nothing to disk.
Run:  python -I -B integra_atlas_reference.py --selftest   (property tests, exit 0 on success)
      python -I -B integra_atlas_reference.py --demo       (one worked example, printed)

It is the executable form of the Task 10 master document (TASK10_MASTER_DOCUMENT.md, same folder).
Each section names the task it serves and the curriculum law it applies:

  L1 identity is invariant, labels are coordinates      (Einstein via doc 10, xv6 inodes, Buzsaki junctions)
  L2 file by taxonomy, find by relation                 (Tufte, Buzsaki, the 2026-10-15 Braille assessment)
  L3 evidence must be independent of the beneficiary    (Tufte galaxy map, KNN doc, InternAgent, metacognition)
  L4 phase orders work, the clock records it, one writer (Buzsaki, xv6 ticks, rotating waves, Purple3 clocks)
  L5 every signal and threshold is a measured claim     (Tufte Lie Factor, metacognition survey and brief)

Provenance of constants: FRAME_1/FRAME_2 copy config/celestial_frames.yml (live, 2026-10-16). Pointer v1 copies
the layout in ~/.claude/plans/structured-spinning-codd.md (a design, not yet a spec). Everything marked
PROVISIONAL (zones, meridians, kind bands, thresholds) is a proposal awaiting the Architect's ruling.
"""

from __future__ import annotations

import argparse
import hashlib
import math
import random
import sys
from array import array
from collections import OrderedDict
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

# ─── 1. CELESTIAL FRAMES (T1; L4) ─────────────────────────────────────────────────────────────────
# Same formulas as temporal/celestial_clock.py compute_4d_coordinates(); a frame only names reference
# instants and periods. Stamps of different frames are never compared.


@dataclass(frozen=True)
class Frame:
    frame_id: int
    rot_ref_unix: float
    lunar_ref_unix: float
    orbit_ref_unix: float
    orbit_period_s: float
    lunar_period_s: float = 2551442.8
    rot_period_s: float = 86400.0
    eccentricity: float = 0.0167086
    anchor_lon: float = -91.1673


FRAME_1 = Frame(1, 1785052800.0, 1785052800.0, 1785052800.0, 31558149.763)
FRAME_2 = Frame(2, 1784116800.0, 1784022180.0, 1767460500.0, 31558310.6)  # USNO refs, ruling R1-R6
FRAMES = {1: FRAME_1, 2: FRAME_2}


def _kepler_eccentric_anomaly(mean_anomaly: float, e: float) -> float:
    big_e = mean_anomaly if e < 0.8 else math.pi
    for _ in range(100):
        f_prime = 1.0 - e * math.cos(big_e)
        if f_prime == 0.0:
            break
        nxt = big_e - (big_e - e * math.sin(big_e) - mean_anomaly) / f_prime
        if abs(nxt - big_e) < 1e-12:
            return nxt
        big_e = nxt
    return big_e


def celestial_vector(unix: float, frame: Frame = FRAME_2) -> Tuple[float, float, float]:
    """(rotation degrees [0,360), lunar fraction [0,1), orbit fraction [0,1)) at true UTC instant `unix`."""
    rot = (frame.anchor_lon + (unix - frame.rot_ref_unix) * (360.0 / frame.rot_period_s)) % 360.0
    lun = ((unix - frame.lunar_ref_unix) / frame.lunar_period_s) % 1.0
    mean_anomaly = ((unix - frame.orbit_ref_unix) / frame.orbit_period_s) % 1.0 * 2.0 * math.pi
    orb = (_kepler_eccentric_anomaly(mean_anomaly, frame.eccentricity) / (2.0 * math.pi)) % 1.0
    return rot, lun, orb


def grid_bucket(unix: float, frame: Frame = FRAME_2) -> str:
    """The live kernel's label: 30-degree rotation and 10 % orbit buckets (celestial_clock.py:364-368)."""
    rot, _, orb = celestial_vector(unix, frame)
    rot, orb = round(rot, 4), round(orb, 4)
    return f"ROT_{int(rot // 30) * 30}_ORB_{int(orb * 100 // 10) * 10}"


# ─── 2. CELESTIAL WORD AND POINTER v1 (T2/T3.5; L1, L4) ───────────────────────────────────────────
# Word (MSB first): TURN+32 (6 bits) | ORB 0-999 (10) | LUN 0-99 (7) | ROT 0-359 (9). 0xFFFFFFFF = unknown.

WORD_UNKNOWN = 0xFFFFFFFF


def celestial_word(unix: Optional[float], frame: Frame = FRAME_2) -> int:
    if unix is None:
        return WORD_UNKNOWN
    rot, lun, orb = celestial_vector(unix, frame)
    turn = math.floor((unix - frame.orbit_ref_unix) / frame.orbit_period_s)
    if not -32 <= turn <= 31:
        raise ValueError(f"TURN {turn} outside -32..31")
    rot_i, lun_i, orb_i = min(int(rot), 359), min(int(lun * 100), 99), min(int(orb * 1000), 999)
    return ((turn + 32) << 26) | (orb_i << 16) | (lun_i << 9) | rot_i


def decode_word(word: int) -> Optional[Dict[str, int]]:
    if word == WORD_UNKNOWN:
        return None
    turn, orb, lun, rot = (word >> 26) - 32, (word >> 16) & 0x3FF, (word >> 9) & 0x7F, word & 0x1FF
    if orb > 999 or lun > 99 or rot > 359:
        raise ValueError("celestial word out of range")
    return {"turn": turn, "orb": orb, "lun": lun, "rot": rot}


# Memory-map codes. Stores: pointer v1 table. Kinds: 01..0F in memory-map order (live map 2026-10-16).
STORE_CODES = {
    "ram_embedding_cache": 0x11, "ram_hoard_cache": 0x12, "rolling_context": 0x13, "claude_memory_index": 0x14,
    "chroma_active": 0x21, "chroma_legacy": 0x22, "vectors_dir": 0x23, "raw_shards": 0x31, "memory_db": 0x32,
    "libraries": 0x41, "metatron_db": 0x51, "save_states_root": 0x61, "swds_reports": 0x62,
    "antigravity_archive": 0x71, "core_identity": 0x81, "modules": 0x82, "docs_blueprint": 0x83,
    "reading_ledger": 0x84, "tasks": 0x85, "drop_in": 0x91,
}
KIND_ORDER = ["identity", "working_context", "assistant_note", "node", "save_state", "crystallization",
              "thermo_loop", "swds_report", "library_book", "lobe_chunk", "conversation_archive", "ruling",
              "reading_ledger_row", "task", "handoff"]  # "secret" has no code and is never encodable
KIND_CODES = {k: i + 1 for i, k in enumerate(KIND_ORDER)}
RETIRED_KINDS = {"crystallization", "thermo_loop", "lobe_chunk"}  # ruled 2026-10-16; map change built, not applied
PROVENANCE = {"unknown": 0, "true_clock": 1, "ccid_true_clock": 2, "civil_id": 3, "file_time": 4,
              "git_first_add": 5, "frozen_clock": 6}
FLAG_TRUSTED, FLAG_STALE, FLAG_EMBED_PENDING = 0x01, 0x02, 0x04
OUTCOME_BITS = {"unknown": 0, "failure": 1, "success": 2, "other": 3}  # bits 3-4; bits 5-7 reserved = 0


def node_key(ccid: str) -> bytes:
    """48-bit opaque key: first 6 bytes of SHA-256 of the UTF-8 CCID. The node's invariant identity (L1)."""
    return hashlib.sha256(ccid.encode("utf-8")).digest()[:6]


@dataclass(frozen=True)
class PointerV1:
    frame_id: int
    provenance: int
    store: int
    kind: int
    flags: int
    space: int
    word: int
    key: bytes

    def encode(self) -> bytes:
        if not (1 <= self.frame_id <= 15 and 0 <= self.provenance <= 15):
            raise ValueError("frame/provenance nibble out of range")
        if self.flags & 0xE0:
            raise ValueError("flag bits 5-7 are reserved and never assignable")
        if len(self.key) != 6:
            raise ValueError("node key must be 6 bytes")
        if self.provenance in (0, 6) and self.word != WORD_UNKNOWN:
            raise ValueError("untrusted or unknown instants must carry the sentinel word")
        return bytes([0xC1, (self.frame_id << 4) | self.provenance, self.store, self.kind, self.flags,
                      self.space]) + self.word.to_bytes(4, "big") + self.key

    @staticmethod
    def decode(raw: bytes) -> "PointerV1":
        if len(raw) != 16 or raw[0] != 0xC1:
            raise ValueError("not a pointer v1")
        return PointerV1(raw[1] >> 4, raw[1] & 0x0F, raw[2], raw[3], raw[4], raw[5],
                         int.from_bytes(raw[6:10], "big"), bytes(raw[10:16]))


# ─── 3. ATLAS GRID AND TAXONOMY (T3, T3.5, T4; L2) ───────────────────────────────────────────────
# Equal-area: latitude bins are uniform in z = sin(latitude), so every cell at one depth has the same area
# (Tufte's blot-map flaw: no region gets weight from its size). Longitude wraps (Marey). The address is a
# Morton (Z-order) code, MSB first, like a radix page table: each level adds one bit of z and one of lon.
# Lat/lon here is a FILING address only, never a semantic-neighbour index (assessment: 8.8 % agreement).

MAX_DEPTH = 14  # 2^14 x 2^14 cells; 28 Morton bits


def _interleave(z_bin: int, lon_bin: int, depth: int) -> int:
    code = 0
    for i in range(depth - 1, -1, -1):
        code = (code << 2) | (((z_bin >> i) & 1) << 1) | ((lon_bin >> i) & 1)
    return code


def _deinterleave(code: int, depth: int) -> Tuple[int, int]:
    z_bin = lon_bin = 0
    for i in range(depth - 1, -1, -1):
        pair = (code >> (2 * i)) & 3
        z_bin, lon_bin = (z_bin << 1) | (pair >> 1), (lon_bin << 1) | (pair & 1)
    return z_bin, lon_bin


@dataclass(frozen=True)
class AtlasCell:
    depth: int
    morton: int

    def bins(self) -> Tuple[int, int]:
        return _deinterleave(self.morton, self.depth)

    def center(self) -> Tuple[float, float]:
        """(latitude degrees, longitude degrees) of the cell centre."""
        n = 1 << self.depth
        z_bin, lon_bin = self.bins()
        z = -1.0 + (z_bin + 0.5) * 2.0 / n
        return math.degrees(math.asin(z)), (lon_bin + 0.5) * 360.0 / n

    def word(self) -> int:
        """ATLAS word (32 bits): depth nibble, then the Morton code left-aligned in 28 bits."""
        return (self.depth << 28) | (self.morton << (2 * (MAX_DEPTH - self.depth)))

    @staticmethod
    def from_word(word: int) -> "AtlasCell":
        depth = word >> 28
        if not 0 <= depth <= MAX_DEPTH:
            raise ValueError("depth out of range")
        shift = 2 * (MAX_DEPTH - depth)
        if word & ((1 << shift) - 1):
            raise ValueError("bits below the stated depth must be zero")
        return AtlasCell(depth, (word & 0x0FFFFFFF) >> shift)

    def parent(self) -> "AtlasCell":
        return AtlasCell(self.depth - 1, self.morton >> 2) if self.depth else self


def atlas_cell(latitude: float, longitude: float, depth: int) -> AtlasCell:
    if not 0 <= depth <= MAX_DEPTH:
        raise ValueError("depth out of range")
    n = 1 << depth
    z = math.sin(math.radians(max(-90.0, min(90.0, latitude))))
    z_bin = min(n - 1, int((z + 1.0) * n / 2.0))
    lon_bin = min(n - 1, int((longitude % 360.0) * n / 360.0))
    return AtlasCell(depth, _interleave(z_bin, lon_bin, depth))


def taxonomic_distance(a: AtlasCell, b: AtlasCell) -> int:
    """Levels below the deepest common ancestor (0 = same cell). A tree distance, not a semantic one."""
    depth = min(a.depth, b.depth)
    ma, mb = a.morton >> (2 * (a.depth - depth)), b.morton >> (2 * (b.depth - depth))
    common = depth
    while common and (ma >> (2 * (depth - common))) != (mb >> (2 * (depth - common))):
        common -= 1
    return max(a.depth, b.depth) - common


# PROVISIONAL taxonomy (rulings open: the meridian list and the kind -> band mapping, To-Do T4).
# Zones in z = sin(lat): poles, temperate belts, equator. North = consolidated / invariant knowledge;
# south = time-bound records (Buzsaki: semantic junctions vs episodes). Promotion moves a node north.
ZONES = {  # name: (z_low, z_high); dyadic edges so zone boundaries fall on grid edges at depth >= 4.
    # Widths 0.25/0.375/0.75/0.375/0.25 -> 12.5/18.75/37.5/18.75/12.5 % of the sphere's area.
    "north_pole": (0.75, 1.0), "north_temperate": (0.375, 0.75), "equator": (-0.375, 0.375),
    "south_temperate": (-0.75, -0.375), "south_pole": (-1.0, -0.75),
}
MIN_PLACE_DEPTH = 4  # zone edges (multiples of 1/8 in z) and the 8 meridians align from depth 4
KIND_BAND = {  # kind: (zone, hemisphere sign used inside the equator: +1 north half, -1 south half)
    "identity": ("north_pole", 1), "ruling": ("north_pole", 1), "library_book": ("north_temperate", 1),
    "semantic_junction": ("equator", 1), "task": ("equator", 1), "handoff": ("equator", 1),
    "reading_ledger_row": ("equator", 1), "node": ("equator", -1), "save_state": ("equator", -1),
    "working_context": ("equator", -1), "assistant_note": ("equator", -1),
    "swds_report": ("south_temperate", -1), "conversation_archive": ("south_temperate", -1),
    "drop_in": ("south_pole", -1),
}
MERIDIANS = ["time", "memory", "cognition", "governance", "evolution", "research", "identity", "operations"]


def place(kind: str, domain: str, level: float = 0.5, offset: float = 0.5, depth: int = 10) -> AtlasCell:
    """Taxonomic placement. level in [0,1): position inside the band, poleward as it grows (north: support
    from independent episodes; south: recency) - a declared variable, never a hash. offset in [0,1): position
    inside the meridian sector. Raises KeyError for retired or unknown kinds and unknown domains."""
    if kind in RETIRED_KINDS:
        raise KeyError(f"kind {kind!r} is retired")
    zone, hemi = KIND_BAND[kind]
    sector = MERIDIANS.index(domain)
    if not (0.0 <= level < 1.0 and 0.0 <= offset < 1.0):
        raise ValueError("level and offset must be in [0, 1)")
    if not MIN_PLACE_DEPTH <= depth <= MAX_DEPTH:
        raise ValueError(f"placement depth must be {MIN_PLACE_DEPTH}..{MAX_DEPTH}")
    z_lo, z_hi = ZONES[zone]
    if zone == "equator":
        z_lo, z_hi = (0.0, z_hi) if hemi > 0 else (z_lo, 0.0)
    n = 1 << depth
    b_lo, b_hi = round((z_lo + 1.0) * n / 2.0), round((z_hi + 1.0) * n / 2.0)  # exact: edges are dyadic
    rows = b_hi - b_lo
    z_bin = b_lo + int(level * rows) if hemi > 0 else b_hi - 1 - int(level * rows)  # poleward as level grows
    per_sector = n // len(MERIDIANS)
    lon_bin = sector * per_sector + int(offset * per_sector)
    return AtlasCell(depth, _interleave(z_bin, lon_bin, depth))


def zone_of(cell: AtlasCell) -> str:
    lat, _ = cell.center()
    z = math.sin(math.radians(lat))
    for name, (lo, hi) in ZONES.items():
        if lo <= z < hi or (name == "north_pole" and z == 1.0):
            return name
    raise AssertionError("unreachable")


def meridian_of(cell: AtlasCell) -> str:
    _, lon = cell.center()
    return MERIDIANS[int(lon * len(MERIDIANS) / 360.0) % len(MERIDIANS)]


# ─── 4. ATLAS POINTER (PROPOSED v2 = pointer v1 + ATLAS word, 20 bytes) AND DISPLAYS (L1, L5) ────────


def encode_atlas_pointer(p: PointerV1, cell: AtlasCell) -> bytes:
    return p.encode() + cell.word().to_bytes(4, "big")


def decode_atlas_pointer(raw: bytes) -> Tuple[PointerV1, AtlasCell]:
    if len(raw) != 20:
        raise ValueError("an atlas pointer is 20 bytes")
    return PointerV1.decode(raw[:16]), AtlasCell.from_word(int.from_bytes(raw[16:], "big"))


def braille_display(raw: bytes) -> str:
    """Display only (8-dot cell = one byte, dot n = bit n-1). Never stored, parsed, logged or put in
    prompts or file names; there is deliberately no inverse function."""
    return "".join(chr(0x2800 + b) for b in raw)


def human_label(p: PointerV1, cell: Optional[AtlasCell] = None) -> str:
    """Words, not a puzzle (Tufte): every field spelled out."""
    store = next((s for s, c in STORE_CODES.items() if c == p.store), f"store{p.store:02x}")
    kind = KIND_ORDER[p.kind - 1] if 1 <= p.kind <= len(KIND_ORDER) else f"kind{p.kind:02x}"
    w = decode_word(p.word)
    sky = "SKY_UNKNOWN" if w is None else f"ROT_{w['rot'] // 30 * 30}_LUN_{w['lun'] // 10 * 10}_ORB_{w['orb'] // 100 * 10}"
    trust = "trusted" if p.flags & FLAG_TRUSTED else "untrusted"
    text = f"{sky} · {store}/{kind} · f{p.frame_id} · {trust} · key {p.key.hex()}"
    if cell is not None:
        text += f" · atlas {zone_of(cell)}/{meridian_of(cell)} d{cell.depth}"
    return text


# ─── 5. LOGICAL CLOCKS (T1/T6; L4) ───────────────────────────────────────────────────────────────


class HybridLogicalClock:
    """Kulkarni et al. HLC. The physical part comes from the one time writer (the Sentinel); the logical
    counter orders events whose physical readings tie or run backwards."""

    def __init__(self, physical: Callable[[], float]):
        self.physical, self.l, self.c = physical, 0.0, 0

    def tick(self) -> Tuple[float, int]:
        pt, prev = self.physical(), self.l
        self.l = max(prev, pt)
        self.c = self.c + 1 if self.l == prev else 0
        return self.l, self.c

    def receive(self, ml: float, mc: int) -> Tuple[float, int]:
        pt, prev = self.physical(), self.l
        self.l = max(prev, ml, pt)
        if self.l == prev == ml:
            self.c = max(self.c, mc) + 1
        elif self.l == prev:
            self.c += 1
        elif self.l == ml:
            self.c = mc + 1
        else:
            self.c = 0
        return self.l, self.c


def vector_order(a: Sequence[int], b: Sequence[int]) -> str:
    """'before', 'after', 'equal' or 'concurrent' (Fidge-Mattern)."""
    le = all(x <= y for x, y in zip(a, b))
    ge = all(x >= y for x, y in zip(a, b))
    return "equal" if le and ge else "before" if le else "after" if ge else "concurrent"


def matrix_clock_min(seen: Dict[str, int]) -> int:
    """Lowest version every reader has absorbed (matrix-clock column minimum)."""
    return min(seen.values()) if seen else -1


def safe_to_prune(nlink: int, ref: int, seen: Dict[str, int], node_version: int, approved: bool) -> Tuple[bool, str]:
    """xv6 inode rule + matrix clock + the Architect's key (To-Do: deletions are approval-gated)."""
    if nlink > 0:
        return False, "still named by a label or store"
    if ref > 0:
        return False, "still held by a reader"
    if matrix_clock_min(seen) < node_version:
        return False, "not every reader has absorbed it"
    if not approved:
        return False, "needs the Architect's approval"
    return True, "prunable"


# ─── 6. EVIDENCE: KNN VOTE, PATTERN LINKS, JUNCTIONS, STALENESS (T3.5/T7/T8; L2, L3) ──────────────

INDEPENDENT_PROVENANCE = {"outcome", "external_check"}  # self-written or inferred-from-words labels excluded


def knn_vote(neighbours: Iterable[Tuple[float, Optional[int], str]], sigma: float = 0.5, tau: float = 0.85,
             min_weight: float = 0.5, min_count: int = 3) -> Tuple[str, float, int]:
    """Normalised distance-weighted vote over (cosine distance, outcome 1/0/None, label provenance).
    Only independent labels vote (L3). Returns (PASS|HALT|ABSTAIN, score in [0,1], voters).
    tau is UNCALIBRATED (L5): fit it on held-out outcomes before use."""
    num = den = 0.0
    used = 0
    for distance, outcome, provenance in neighbours:
        if outcome is None or provenance not in INDEPENDENT_PROVENANCE:
            continue
        w = math.exp(-(distance ** 2) / sigma ** 2)
        num, den, used = num + w * outcome, den + w, used + 1
    if used < min_count or den < min_weight:
        return "ABSTAIN", 0.0, used
    score = num / den
    return ("PASS" if score >= tau else "HALT"), score, used


def _log_binom_tail(k: int, n: int, p: float) -> float:
    """log P(X >= k), X ~ Binomial(n, p), computed exactly in log space."""
    if k <= 0:
        return 0.0
    if p <= 0.0:
        return -math.inf
    if p >= 1.0:
        return 0.0
    terms = [math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * math.log(p)
             + (n - i) * math.log1p(-p) for i in range(k, n + 1)]
    top = max(terms)
    return top + math.log(sum(math.exp(t - top) for t in terms))


def pattern_links(windows: Sequence[set], alpha: float = 0.05, min_count: int = 3) -> List[Tuple[str, str, int, float]]:
    """Apophenic Engine as decided: pattern links (edges) only. A pair co-occurring in reader windows is kept
    if its count beats the independence null (binomial upper tail) after Benjamini-Hochberg at alpha.
    The galaxy-map lesson: the eye finds filaments in noise, so every link must beat chance."""
    w = len(windows)
    freq: Dict[str, int] = {}
    pair: Dict[Tuple[str, str], int] = {}
    for win in windows:
        items = sorted(win)
        for x in items:
            freq[x] = freq.get(x, 0) + 1
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                pair[(items[i], items[j])] = pair.get((items[i], items[j]), 0) + 1
    tested = []
    for (a, b), c in pair.items():
        if c < min_count:
            continue
        p = (freq[a] / w) * (freq[b] / w)
        tested.append((math.exp(_log_binom_tail(c, w, p)), a, b, c))
    tested.sort()
    m, kept, cutoff = len(tested), [], 0
    for rank, (pv, *_rest) in enumerate(tested, 1):
        if pv <= alpha * rank / m:
            cutoff = rank
    for pv, a, b, c in tested[:cutoff]:
        kept.append((a, b, c, pv))
    return kept


def junctions(episodes: Sequence[Tuple[str, str, set]], min_episodes: int = 3, min_days: int = 2) -> List[str]:
    """Buzsaki: semantic memory forms where many episode trajectories cross. episodes = (episode_id, civil
    day, items). An item seen in >= min_episodes distinct episodes over >= min_days days is promoted north."""
    seen_eps: Dict[str, set] = {}
    seen_days: Dict[str, set] = {}
    for ep_id, day, items in episodes:
        for it in items:
            seen_eps.setdefault(it, set()).add(ep_id)
            seen_days.setdefault(it, set()).add(day)
    return sorted(i for i in seen_eps if len(seen_eps[i]) >= min_episodes and len(seen_days[i]) >= min_days)


HALF_LIFE_DAYS = {  # PROVISIONAL (L5): episodes fade, invariants do not
    "node": 30.0, "working_context": 1.0, "assistant_note": 7.0, "save_state": 90.0, "swds_report": 180.0,
    "conversation_archive": 365.0, "task": 14.0, "handoff": 14.0, "reading_ledger_row": 90.0,
    "identity": math.inf, "ruling": math.inf, "library_book": math.inf, "semantic_junction": math.inf,
}


def freshness(kind: str, age_days: float) -> float:
    """Weight in (0, 1]: 2^(-age / half-life); 1.0 for kinds with no half-life."""
    h = HALF_LIFE_DAYS[kind]
    return 1.0 if math.isinf(h) else 2.0 ** (-max(0.0, age_days) / h)


# ─── 7. METACOGNITION AND INTEGRITY MEASURES (T6.5/T8 gates; L5) ─────────────────────────────────


def brier(conf: Sequence[float], correct: Sequence[int]) -> float:
    return sum((c - y) ** 2 for c, y in zip(conf, correct)) / len(conf)


def ece(conf: Sequence[float], correct: Sequence[int], bins: int = 10) -> float:
    total, err = len(conf), 0.0
    for b in range(bins):
        idx = [i for i, c in enumerate(conf) if (b / bins <= c < (b + 1) / bins) or (b == bins - 1 and c == 1.0)]
        if idx:
            err += len(idx) / total * abs(sum(conf[i] for i in idx) / len(idx) - sum(correct[i] for i in idx) / len(idx))
    return err


def auroc(conf: Sequence[float], correct: Sequence[int]) -> float:
    """Type-2 sensitivity: P(confidence of a right answer > that of a wrong one), ties count half."""
    pos = [c for c, y in zip(conf, correct) if y]
    neg = [c for c, y in zip(conf, correct) if not y]
    if not pos or not neg:
        return float("nan")
    wins = sum((p > n) + 0.5 * (p == n) for p in pos for n in neg)
    return wins / (len(pos) * len(neg))


def confidence_lie_factor(conf: Sequence[float], correct: Sequence[int]) -> float:
    """Stated confidence / observed accuracy; 1.0 is honest, > 1 overconfident (Tufte x metacognition)."""
    acc = sum(correct) / len(correct)
    return (sum(conf) / len(conf)) / acc if acc else math.inf


def lie_factor(shown_start: float, shown_end: float, data_start: float, data_end: float) -> float:
    """Tufte: size of effect shown / size of effect in data. Outside 0.95-1.05 is substantial distortion."""
    return ((shown_end - shown_start) / shown_start) / ((data_end - data_start) / data_start)


# ─── 8. RODIN HOT TIER: DEMAND PAGING OVER THE COLD HOARD (T8; xv6 buffer cache) ─────────────────


@dataclass
class HotEntry:
    vector: array
    tokens: int
    cell: AtlasCell


class HotTier:
    """Resident set with least-recently-routed eviction under node and token budgets. A miss is a page
    fault: `loader(key)` fetches from the cold store and the entry becomes resident. float32 vectors
    (4 bytes per dimension) - the measured cheap RAM win."""

    def __init__(self, max_nodes: int, max_tokens: int, loader: Callable[[bytes], HotEntry]):
        self.max_nodes, self.max_tokens, self.loader = max_nodes, max_tokens, loader
        self.resident: "OrderedDict[bytes, HotEntry]" = OrderedDict()
        self.tokens = self.hits = self.misses = self.evictions = 0

    def get(self, key: bytes) -> HotEntry:
        if key in self.resident:
            self.hits += 1
            self.resident.move_to_end(key)
            return self.resident[key]
        self.misses += 1
        entry = self.loader(key)
        if entry.tokens > self.max_tokens:
            raise ValueError("entry larger than the whole token budget")
        self.resident[key] = entry
        self.tokens += entry.tokens
        while len(self.resident) > self.max_nodes or self.tokens > self.max_tokens:
            _, old = self.resident.popitem(last=False)
            self.tokens -= old.tokens
            self.evictions += 1
        return entry

    def pressure(self) -> float:
        """For Heimdall: the larger of node and token occupancy, in [0, 1]."""
        return max(len(self.resident) / self.max_nodes, self.tokens / self.max_tokens)


# ─── 9. SWDS SWEEP AND THE RITUAL-DANCE CASCADE (T5.5/T9; L4) ───────────────────────────────────
# Template: NewCurriculum2026/theritualdance.md - 10 units (hours 1-10), totality (11), master document (12),
# verification (13). Pause on an active conversation; resume after 1 h of inactivity or at the nearer of
# 05:00 / 23:00 local, whichever comes first (INTERPRETATION, ruling needed). Dry run only: nothing is
# registered with Task Scheduler. Local time is a fixed offset (CDT = UTC-5 until 2026-11-01).

CDT = timezone(timedelta(hours=-5))


def sweep_order(start_unix: float, frame: Frame = FRAME_2) -> List[str]:
    """Rotating-wave sweep: start at the meridian under the current rotation phase, then go east through all
    of them, so successive nights begin at different meridians (external clock anchors, internal phase runs)."""
    rot, _, _ = celestial_vector(start_unix, frame)
    first = int(rot * len(MERIDIANS) / 360.0) % len(MERIDIANS)
    return [MERIDIANS[(first + i) % len(MERIDIANS)] for i in range(len(MERIDIANS))]


def _next_anchor(t: datetime) -> datetime:
    cands = []
    for day in (0, 1):
        for hour in (5, 23):
            a = (t + timedelta(days=day)).replace(hour=hour, minute=0, second=0, microsecond=0)
            if a > t:
                cands.append(a)
    return min(cands)


def ritual_dance_plan(start: datetime, units: Sequence[str], activity: Sequence[Tuple[datetime, datetime]],
                      frame: Frame = FRAME_2) -> List[Dict[str, str]]:
    """Per-hour ledger for the 13-hour cascade. Each row carries a dual stamp (civil + celestial)."""
    steps = [f"unit {i + 1}/{len(units)}: {u}" for i, u in enumerate(units)] + [
        "totality study", "master document", "verification"]
    ledger, t = [], start
    quiet = timedelta(hours=1)

    def active_at(x: datetime) -> Optional[Tuple[datetime, datetime]]:
        """A conversation counts as active until one quiet hour has passed since its last interaction."""
        return next(((a, b) for a, b in activity if a <= x < b + quiet), None)

    for step in steps:
        while (busy := active_at(t)) is not None:
            after_quiet, anchor = busy[1] + quiet, _next_anchor(t)
            resume = min(after_quiet, anchor)
            ledger.append({"step": "PAUSE", "at": t.isoformat(), "resume": resume.isoformat(),
                           "reason": "active conversation" + (" (anchor override)" if anchor < after_quiet else "")})
            t = resume
            if anchor < after_quiet:
                break  # anchor reached: resume even if the conversation continues
        u = t.astimezone(timezone.utc).timestamp()
        rot, lun, orb = celestial_vector(u, frame)
        ledger.append({"step": step, "at": t.isoformat(),
                       "celestial": f"f{frame.frame_id} rot {rot:.2f} lun {lun:.4f} orb {orb:.4f} {grid_bucket(u, frame)}"})
        t += timedelta(hours=1)
    return ledger


SWDS_PHASES = ["open", "defragment_archive", "conceptual_synthesis", "label_and_place", "blueprint_refinement",
               "exploration", "close", "wake_report"]


def cycle_closed(ledger: Sequence[Dict[str, object]]) -> Tuple[bool, str]:
    """The 13th Form as a checkable invariant (dE_cycle = 0): phases in order, each ledgered with a receipt,
    no transaction left open, and the end state meets the next cycle's precondition."""
    phases = [r["phase"] for r in ledger]
    if phases != SWDS_PHASES:
        return False, f"phase order {phases}"
    for r in ledger:
        if not r.get("receipt"):
            return False, f"no receipt for {r['phase']}"
        if float(r["end"]) < float(r["start"]):  # type: ignore[arg-type]
            return False, f"{r['phase']} ends before it starts"
    last = ledger[-1]
    if last.get("open_transactions", 0):
        return False, "open transaction at wake"
    if last.get("state") != "AWAKE_READY":
        return False, "end state does not meet the next cycle's precondition"
    return True, "closed"


# ─── 10. SELF-TEST ─────────────────────────────────────────────────────────────────────────────────

LIVE_READING = {  # GET /clock, HTTP 200, 2026-10-16 20:05:34 CDT (MEASURED this session)
    "unix": 1792199134.7, "rot": 105.2273, "lunar": 0.2048, "orbit": 0.7813, "bucket": "ROT_90_ORB_70"}


def _random_pointer(rng: random.Random) -> PointerV1:
    prov = rng.choice([1, 2, 3, 4, 5])
    u = rng.uniform(FRAME_2.orbit_ref_unix - 20 * FRAME_2.orbit_period_s,
                    FRAME_2.orbit_ref_unix + 20 * FRAME_2.orbit_period_s)
    return PointerV1(2, prov, rng.choice(list(STORE_CODES.values())), rng.randint(1, 15),
                     rng.randint(0, 31), rng.randint(0, 1), celestial_word(u, FRAME_2),
                     bytes(rng.randrange(256) for _ in range(6)))


def selftest(n_round_trips: int = 100_000) -> int:
    rng = random.Random(20261016)
    checks: List[Tuple[str, bool, str]] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append((name, ok, detail))

    # Celestial math reproduces the live kernel reading (T1).
    rot, lun, orb = celestial_vector(LIVE_READING["unix"], FRAME_2)
    check("frame 2 reproduces live /clock", abs(rot - LIVE_READING["rot"]) < 1e-4
          and abs(lun - LIVE_READING["lunar"]) < 1e-4 and abs(orb - LIVE_READING["orbit"]) < 1e-4,
          f"rot {rot:.4f} lun {lun:.4f} orb {orb:.4f}")
    check("grid bucket matches live", grid_bucket(LIVE_READING["unix"]) == LIVE_READING["bucket"],
          grid_bucket(LIVE_READING["unix"]))

    # Celestial word round trip and sentinel.
    ok = True
    for _ in range(20_000):
        u = rng.uniform(FRAME_2.orbit_ref_unix - 31 * FRAME_2.orbit_period_s,
                        FRAME_2.orbit_ref_unix + 31 * FRAME_2.orbit_period_s)
        d = decode_word(celestial_word(u))
        r, lu, ob = celestial_vector(u)
        ok &= d is not None and d["rot"] == min(int(r), 359) and d["lun"] == min(int(lu * 100), 99) \
            and d["orb"] == min(int(ob * 1000), 999)
    check("celestial word round trip (20k)", ok)
    check("sentinel decodes to unknown", decode_word(WORD_UNKNOWN) is None)
    order_ok = all(celestial_word(u) < celestial_word(u + FRAME_2.orbit_period_s)
                   for u in (FRAME_2.orbit_ref_unix + k * 1e6 for k in range(30)))
    check("word sorts by turn first", order_ok)

    # Pointer v1 + ATLAS word round trip on 10^5 random points (T3.5 done-when).
    ok, bad = True, 0
    for _ in range(n_round_trips):
        p = _random_pointer(rng)
        cell = AtlasCell(d := rng.randint(0, MAX_DEPTH), rng.randrange(1 << (2 * d)) if d else 0)
        raw = encode_atlas_pointer(p, cell)
        p2, c2 = decode_atlas_pointer(raw)
        if (p2, c2) != (p, cell) or len(raw) != 20:
            ok, bad = False, bad + 1
    check(f"atlas pointer round trip ({n_round_trips:,})", ok, f"{bad} failures")
    for bad_ptr, why in ((PointerV1(2, 6, 0x31, 4, 0, 0, 123, b"\0" * 6), "frozen instant with a word"),
                         (PointerV1(2, 1, 0x31, 4, 0x20, 0, 0, b"\0" * 6), "reserved flag bit")):
        try:
            bad_ptr.encode()
            check(f"rejects {why}", False)
        except ValueError:
            check(f"rejects {why}", True)

    # Atlas grid properties.
    ok = True
    for _ in range(n_round_trips):
        depth = rng.randint(1, MAX_DEPTH)
        zb, lb = rng.randrange(1 << depth), rng.randrange(1 << depth)
        ok &= _deinterleave(_interleave(zb, lb, depth), depth) == (zb, lb)
    check(f"Morton interleave round trip ({n_round_trips:,})", ok)
    ok = True
    for _ in range(20_000):
        lat, lon, depth = rng.uniform(-90, 90), rng.uniform(0, 360), rng.randint(1, 12)
        cell = atlas_cell(lat, lon, depth)
        clat, clon = cell.center()
        n = 1 << depth
        ok &= abs(math.sin(math.radians(clat)) - math.sin(math.radians(lat))) <= 1.0 / n + 1e-12
        ok &= abs(clon - lon) <= 180.0 / n + 1e-9 and atlas_cell(clat, clon, depth) == cell
        ok &= cell.parent() == atlas_cell(lat, lon, depth - 1)
    check("cell centre maps back to its cell; parents nest", ok)
    n6 = 1 << 6  # cell area on the unit sphere = d(lon) x (sin(lat_hi) - sin(lat_lo)), from latitude edges
    lat_edges = [math.degrees(math.asin(-1.0 + k * 2.0 / n6)) for k in range(n6 + 1)]
    areas = {round(math.radians(360.0 / n6) * (math.sin(math.radians(lat_edges[k + 1]))
                                               - math.sin(math.radians(lat_edges[k]))), 12) for k in range(n6)}
    spans = {round(lat_edges[k + 1] - lat_edges[k], 6) for k in range(n6)}
    check("equal-area cells despite unequal latitude spans", len(areas) == 1 and len(spans) > 1,
          f"{len(spans)} distinct latitude spans, 1 area")
    a, b = atlas_cell(10, 10, 8), atlas_cell(10, 10, 8)
    check("taxonomic distance 0 for same cell", taxonomic_distance(a, b) == 0)
    check("taxonomic distance grows across hemispheres",
          taxonomic_distance(atlas_cell(60, 10, 8), atlas_cell(-60, 10, 8)) == 8)

    # Taxonomy: every kind lands in its zone and meridian; retired kinds refused.
    ok = True
    for kind, (zone, hemi) in KIND_BAND.items():
        for dom in MERIDIANS:
            for level in (0.0, 0.5, 0.99):
                cell = place(kind, dom, level=level, depth=10)
                lat, _ = cell.center()
                ok &= zone_of(cell) == zone and meridian_of(cell) == dom
                ok &= (lat >= 0) == (hemi > 0) if zone == "equator" else True
    check("placement lands in declared zone, hemisphere and meridian", ok)
    north = [place("library_book", "research", level=x / 10, depth=10).center()[0] for x in range(10)]
    south = [place("swds_report", "research", level=x / 10, depth=10).center()[0] for x in range(10)]
    check("level moves a node poleward in both hemispheres",
          all(a < b for a, b in zip(north, north[1:])) and all(a > b for a, b in zip(south, south[1:])))
    try:
        place("crystallization", "memory")
        check("retired kind refused", False)
    except KeyError:
        check("retired kind refused", True)

    # Displays.
    sample = encode_atlas_pointer(_random_pointer(rng), place("node", "memory"))
    br = braille_display(sample)
    check("braille: one cell per byte, U+2800 block", len(br) == 20 and all(0x2800 <= ord(ch) <= 0x28FF for ch in br))
    check("Lie Factor of an honest display is 1", abs(lie_factor(18, 27.5, 18, 27.5) - 1.0) < 1e-12)
    check("Tufte fuel-economy example ~14.8", abs(lie_factor(0.6, 5.3, 18.0, 27.5) - 14.8) < 0.1,
          f"{lie_factor(0.6, 5.3, 18.0, 27.5):.2f}")

    # Clocks.
    readings = iter([100.0, 100.0, 99.0, 98.0, 101.0, 101.0])
    hlc = HybridLogicalClock(lambda: next(readings))
    stamps = [hlc.tick() for _ in range(4)]
    check("HLC monotonic when physical time stalls or runs back", all(x < y for x, y in zip(stamps, stamps[1:])), str(stamps))
    got = hlc.receive(200.0, 7)
    check("HLC receive adopts a later message", got == (200.0, 8), str(got))
    check("vector order", [vector_order([1, 0], [1, 1]), vector_order([2, 0], [1, 1]), vector_order([1, 1], [1, 1])]
          == ["before", "concurrent", "equal"])
    check("prune refused while named", not safe_to_prune(1, 0, {"y": 9}, 3, True)[0])
    check("prune refused until all readers absorbed", not safe_to_prune(0, 0, {"y": 9, "n": 2}, 3, True)[0])
    check("prune refused without approval", not safe_to_prune(0, 0, {"y": 9}, 3, False)[0])
    check("prune allowed when every condition holds", safe_to_prune(0, 0, {"y": 9}, 3, True)[0])

    # Evidence rules.
    decision, score, used = knn_vote([(0.01, 1, "self")] * 10)
    check("KNN: self-written labels never vote", decision == "ABSTAIN" and used == 0)
    decision, score, used = knn_vote([(0.1, 1, "outcome"), (0.2, 1, "outcome"), (0.3, 0, "outcome"), (0.1, 1, "self")])
    check("KNN: bounded normalised score", 0.0 <= score <= 1.0 and used == 3, f"{decision} {score:.3f}")
    windows = []
    for i in range(400):
        win = {f"x{rng.randrange(60)}" for _ in range(6)}
        if i % 4 == 0:
            win |= {"alpha", "beta"}
        windows.append(win)
    links = pattern_links(windows)
    check("pattern links: planted pair found", any({a, b} == {"alpha", "beta"} for a, b, *_ in links), f"{len(links)} kept")
    null_windows = [{f"x{rng.randrange(60)}" for _ in range(6)} for _ in range(400)]
    null_links = pattern_links(null_windows)
    check("pattern links: noise yields (almost) nothing", len(null_links) <= 2, f"{len(null_links)} kept")
    eps = [("e1", "d1", {"atlas", "clock", "burst"}), ("e2", "d1", {"atlas", "burst"}),
           ("e3", "d2", {"atlas", "noise"}), ("e4", "d2", {"clock"}), ("e5", "d1", {"burst"})]
    check("junction promotion needs episodes and days (a one-day burst is not promoted)",
          junctions(eps) == ["atlas"], str(junctions(eps)))
    check("semantic kinds never go stale", freshness("library_book", 10_000) == 1.0
          and abs(freshness("node", 30) - 0.5) < 1e-12)

    # Metacognition measures.
    conf = [rng.random() for _ in range(5000)]
    correct = [1 if rng.random() < c else 0 for c in conf]
    check("calibrated signal: ECE small", ece(conf, correct) < 0.03, f"{ece(conf, correct):.4f}")
    check("informative signal: AUROC > 0.5", auroc(conf, correct) > 0.7, f"{auroc(conf, correct):.3f}")
    noise = [rng.random() for _ in range(5000)]
    check("uninformative signal: AUROC ~ 0.5", abs(auroc(noise, correct) - 0.5) < 0.03, f"{auroc(noise, correct):.3f}")
    over = [min(1.0, c + 0.3) for c in conf]
    check("overconfidence shows as confidence Lie Factor > 1", confidence_lie_factor(over, correct) > 1.2,
          f"{confidence_lie_factor(over, correct):.2f}")
    check("Brier of perfect confidence is 0", brier([1.0, 0.0], [1, 0]) == 0.0)

    # Hot tier.
    def loader(key: bytes) -> HotEntry:
        return HotEntry(array("f", [0.0] * 768), tokens=50 + key[0] % 50, cell=place("node", "memory"))
    tier = HotTier(max_nodes=32, max_tokens=2000, loader=loader)
    ok = True
    keys = [bytes([i % 200, i // 200, 0, 0, 0, 0]) for i in range(400)]
    for _ in range(5000):
        k = keys[min(399, int(rng.expovariate(0.05)))]  # skewed access = locality of reference
        tier.get(k)
        ok &= len(tier.resident) <= tier.max_nodes and tier.tokens <= tier.max_tokens
    check("hot tier never exceeds node or token budget", ok)
    check("locality gives hits", tier.hits > tier.misses, f"hits {tier.hits} misses {tier.misses}")
    check("float32 vector is 4 bytes per dimension", array("f").itemsize == 4)

    # Schedule and cycle closure.
    start = datetime(2026, 10, 19, 2, 0, tzinfo=CDT)
    units = [f"U{i}" for i in range(1, 11)]
    plan = ritual_dance_plan(start, units, [])
    check("quiet night: 13 contiguous hours", len(plan) == 13 and plan[-1]["at"] == (start + timedelta(hours=12)).isoformat())
    plan = ritual_dance_plan(start, units, [(start + timedelta(hours=3, minutes=10), start + timedelta(hours=3, minutes=40))])
    pauses = [r for r in plan if r["step"] == "PAUSE"]
    check("conversation pauses then resumes 1 h after it ends",
          len(pauses) == 1 and pauses[0]["resume"] == (start + timedelta(hours=4, minutes=40)).isoformat(), str(pauses))
    long_talk = [(start + timedelta(minutes=30), start + timedelta(hours=7))]
    plan = ritual_dance_plan(start, units, long_talk)
    pauses = [r for r in plan if r["step"] == "PAUSE"]
    check("long conversation: resumes at the 05:00 anchor", pauses and pauses[0]["resume"].startswith("2026-10-19T05:00"), str(pauses[:1]))
    check("sweep visits every meridian once", sorted(sweep_order(LIVE_READING["unix"])) == sorted(MERIDIANS))
    good = [{"phase": p, "start": i, "end": i + 1, "receipt": f"r{i}"} for i, p in enumerate(SWDS_PHASES)]
    good[-1].update({"state": "AWAKE_READY", "open_transactions": 0})
    check("closed night passes the cycle invariant", cycle_closed(good)[0])
    broken = [dict(r) for r in good]
    broken[3]["receipt"] = ""
    check("missing receipt breaks the cycle invariant", not cycle_closed(broken)[0])
    broken = [dict(r) for r in good]
    broken[-1]["open_transactions"] = 1
    check("open transaction at wake breaks the cycle invariant", not cycle_closed(broken)[0])

    width = max(len(n) for n, _, _ in checks)
    for name, ok, detail in checks:
        print(f"{'PASS' if ok else 'FAIL'}  {name:<{width}}  {detail}")
    failed = sum(1 for _, ok, _ in checks if not ok)
    print(f"\n{len(checks) - failed} passed, {failed} failed")
    return 1 if failed else 0


def demo() -> None:
    u = LIVE_READING["unix"]
    ptr = PointerV1(2, PROVENANCE["true_clock"], STORE_CODES["raw_shards"], KIND_CODES["node"],
                    FLAG_TRUSTED | (OUTCOME_BITS["unknown"] << 3), 1, celestial_word(u), node_key("CCID_1792199134"))
    cell = place("node", "memory", level=0.5, offset=0.5, depth=10)
    raw = encode_atlas_pointer(ptr, cell)
    print("instant      2026-10-17T01:05:34.7Z (= 20:05:34 CDT), frame 2")
    print("vector       rot %.4f  lun %.4f  orb %.4f   bucket %s" % (*celestial_vector(u), grid_bucket(u)))
    print("pointer hex  " + raw.hex())
    print("human label  " + human_label(ptr, cell))
    try:
        print("braille      " + braille_display(raw) + "   (display only)")
    except UnicodeEncodeError:
        print("braille      (console cannot encode U+2800; hex above is canonical)")
    print("sweep        " + " -> ".join(sweep_order(u)))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--demo", action="store_true")
    parser.add_argument("--n", type=int, default=100_000, help="round trips for the property tests")
    args = parser.parse_args()
    if args.demo:
        demo()
    if args.selftest or not args.demo:
        sys.exit(selftest(args.n))
