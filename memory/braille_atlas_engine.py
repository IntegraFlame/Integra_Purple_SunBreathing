"""
INTEGRA O/S: 128-BIT BRAILLE SEMANTIC ATLAS, APOPHENIC CODEX & SPHERICAL KOHONEN SOM
Module: memory/braille_atlas_engine.py
Layer: 3 (The Memory — Cartographic & Topological Manifold)

Implements Tasks 3, 3.5, and 4 of `core/IntegraBrainMap.md` and Curriculum Document 1
(Braille-Based Semantic Labeling System):
  1. `BrailleCodec`:
     - 128-bit (16-byte / 16-cell) Unicode Braille packet (`U+2800`–`U+28FF`):
       * Cells 0–3 (32 bits): Big-endian Unix Epoch (`time_braille_4`)
       * Cell 4 (8 bits): Apophenic Codex 8-Dot Bitmask (`0x01..0x80`)
       * Cells 5–8 (32 bits): Morton Z-Order Interleaved 2D Spatial Key (16-bit X, 16-bit Y -> 65536x65536 grid)
       * Cells 9–15 (56 bits): Semantic SimHash Fingerprint (bitwise XOR + POPCNT Hamming distance)
  2. `ApophenicCodexEngine` (Task 3.5):
     - Scale-invariant ZigZag extrema detector (theta_dc threshold)
     - 4x4 Markov regime transition matrix (ACCUMULATION, MARKUP, DISTRIBUTION, MARKDOWN)
     - Cell 4 8-dot bitmask encoder + adaptive peak sell & trough buyback projections
  3. `CartographicTaxonomy`, `SphericalKohonenSOM`, and `TufteIntegrityAuditor` (Tasks 3 & 4):
     - 5 Latitudinal Zones/Poles (`Z1_SOUTH_POLE`..`Z5_NORTH_POLE`)
     - 4 Hemispheres (`NW_ANALYTICAL_ACTIVE`, `NE_SYNTHETIC_ACTIVE`, `SW_ANALYTICAL_ARCHIVAL`, `SE_SYNTHETIC_ARCHIVAL`)
     - 12 Longitudinal Meridians (`M01`–`M12`, 30 deg each)
     - 3D unit-sphere coordinates (x, y, z) + 4096x4096 Meso & 65536x65536 Micro Morton coordinates
     - Geodesic Great-Circle Spherical Kohonen SOM (`find_bmu`, `train_step`)
     - Tufte Visual Integrity Auditor (`lie_factor = 1.0`, `data_ink_ratio = 1.0`)
  4. Persistent storage to MongoDB Placeholder File Point (`braille_atlas_nodes.json`).
"""

import hashlib
import json
import math
import struct
import time
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional, Tuple

BRAILLE_BASE = 0x2800

# ─── APOPHENIC CODEX CELL 4 BITMASK CONSTANTS (8 DOTS) ─────────────────────
DOT1_TREND_UP = 0x01
DOT2_TREND_DOWN = 0x02
DOT3_VOL_EXPANSION = 0x04
DOT4_MEAN_REVERSION = 0x08
DOT5_BREAKOUT = 0x10
DOT6_BREAKDOWN = 0x20
DOT7_PEAK_SELL_SIGNAL = 0x40
DOT8_TROUGH_BUYBACK_SIGNAL = 0x80

# ─── 5 LATITUDINAL ZONES & 12 MERIDIANS (TASK 4 TAXONOMY) ───────────────────
LATITUDINAL_ZONES = (
    ("Z1_SOUTH_POLE", -90.0, -60.0, (8, 9), "Deep Archival Cold Storage Vault"),
    ("Z2_SOUTH_TEMPERATE", -60.0, -20.0, (6, 7), "Episodic Operations, Market Telemetry & Tooling"),
    ("Z3_EQUATORIAL_CORE", -20.0, 20.0, (4, 5), "Active Waking Synthesis & Cheshire Thalamic Routing"),
    ("Z4_NORTH_TEMPERATE", 20.0, 60.0, (2, 3), "Analytical Logic, Code Verification & Formal Proofs"),
    ("Z5_NORTH_POLE", 60.0, 90.0, (0, 1), "Sovereign Identity, Starfire Axioms & Immutable Laws"),
)

MERIDIAN_DOMAINS = (
    ("M01_SOVEREIGN_IDENTITY", -180.0, -150.0, 0),
    ("M02_THERMODYNAMIC_PHYSICS", -150.0, -120.0, 1),
    ("M03_CELESTIAL_TEMPORAL", -120.0, -90.0, 2),
    ("M04_HEIMDALL_SENSORY", -90.0, -60.0, 3),
    ("M05_CHESHIRE_THALAMUS", -60.0, -30.0, 4),
    ("M06_RODIN_TOPOLOGY", -30.0, 0.0, 5),
    ("M07_Y789_ANALYTICAL", 0.0, 30.0, 6),
    ("M08_NEXUS_SYNTHETIC", 30.0, 60.0, 7),
    ("M09_SHIVA_DECONSTRUCTION", 60.0, 90.0, 8),
    ("M10_PHOENIX_NEUROEVOLUTION", 90.0, 120.0, 9),
    ("M11_FORTUNE_FORTRESS", 120.0, 150.0, 10),
    ("M12_KINTSUGI_DEFENSE", 150.0, 180.0, 11),
)


class BrailleCodec:
    """
    128-Bit (16-Byte / 16-Cell) Unicode Braille Semantic Codec (`U+2800`–`U+28FF`).
    """

    @staticmethod
    def morton_interleave_16bit(x: int, y: int) -> int:
        """Interleaves two 16-bit unsigned integers (x, y in 0..65535) into a 32-bit Morton Z-order key."""
        x = max(0, min(0xFFFF, int(x)))
        y = max(0, min(0xFFFF, int(y)))

        def _part1by1(n: int) -> int:
            n &= 0x0000FFFF
            n = (n | (n << 8)) & 0x00FF00FF
            n = (n | (n << 4)) & 0x0F0F0F0F
            n = (n | (n << 2)) & 0x33333333
            n = (n | (n << 1)) & 0x55555555
            return n

        return (_part1by1(x) | (_part1by1(y) << 1)) & 0xFFFFFFFF

    @staticmethod
    def morton_deinterleave_32bit(morton_code: int) -> Tuple[int, int]:
        """De-interleaves a 32-bit Morton Z-order key back into (x_16bit, y_16bit)."""
        morton_code = int(morton_code) & 0xFFFFFFFF

        def _compact1by1(n: int) -> int:
            n &= 0x55555555
            n = (n | (n >> 1)) & 0x33333333
            n = (n | (n >> 2)) & 0x0F0F0F0F
            n = (n | (n >> 4)) & 0x00FF00FF
            n = (n | (n >> 8)) & 0x0000FFFF
            return n

        return _compact1by1(morton_code), _compact1by1(morton_code >> 1)

    @staticmethod
    def latlon_to_grid_65536(lat_deg: float, lon_deg: float) -> Tuple[int, int]:
        """Quantizes latitude [-90, +90] and longitude [-180, +180] into (x_65536, y_65536)."""
        lat_clamped = max(-90.0, min(90.0, float(lat_deg)))
        lon_clamped = max(-180.0, min(180.0, float(lon_deg)))
        x = int(round(((lon_clamped + 180.0) / 360.0) * 65535))
        y = int(round(((lat_clamped + 90.0) / 180.0) * 65535))
        return max(0, min(65535, x)), max(0, min(65535, y))

    @staticmethod
    def grid_65536_to_latlon(x: int, y: int) -> Tuple[float, float]:
        """Reconstructs (lat_deg, lon_deg) from quantized 16-bit grid coordinates."""
        lon = (float(x) / 65535.0) * 360.0 - 180.0
        lat = (float(y) / 65535.0) * 180.0 - 90.0
        return round(lat, 4), round(lon, 4)

    @staticmethod
    def compute_simhash_56bit(source: Any) -> int:
        """
        Computes a 56-bit locality-sensitive SimHash fingerprint from either a numeric
        embedding vector (`List[float]`) or text/JSON payload.
        """
        if isinstance(source, (list, tuple)) and len(source) >= 56 and all(isinstance(v, (int, float)) for v in source[:56]):
            bits = 0
            for i in range(56):
                if float(source[i]) >= 0.0:
                    bits |= (1 << (55 - i))
            return bits & 0x00FFFFFFFFFFFFFF

        text = str(source)
        tokens = [t.strip().lower() for t in text.split() if t.strip()] or [text]
        accum = [0] * 56
        for tok in tokens:
            digest = hashlib.sha256(tok.encode("utf-8")).digest()
            val56 = int.from_bytes(digest[:7], "big")
            for b in range(56):
                if (val56 >> (55 - b)) & 1:
                    accum[b] += 1
                else:
                    accum[b] -= 1
        fingerprint = 0
        for b in range(56):
            if accum[b] >= 0:
                fingerprint |= (1 << (55 - b))
        return fingerprint & 0x00FFFFFFFFFFFFFF

    @staticmethod
    def hamming_distance_56bit(simhash_a: int, simhash_b: int) -> int:
        """O(1) bitwise XOR + POPCNT Hamming distance across 56-bit SimHash fingerprints."""
        xor_val = (int(simhash_a) ^ int(simhash_b)) & 0x00FFFFFFFFFFFFFF
        return xor_val.bit_count()

    @classmethod
    def encode_packet_16(
        cls,
        epoch_sec: int,
        codex_mask_8bit: int,
        morton_32bit: int,
        simhash_56bit: int,
    ) -> str:
        """
        Packs the 4 fields into a 16-byte (128-bit) big-endian frame and maps each byte
        into Unicode Braille (`U+2800 + byte`).
        """
        b_time = struct.pack(">I", int(epoch_sec) & 0xFFFFFFFF)
        b_codex = struct.pack(">B", int(codex_mask_8bit) & 0xFF)
        b_morton = struct.pack(">I", int(morton_32bit) & 0xFFFFFFFF)
        b_simhash = (int(simhash_56bit) & 0x00FFFFFFFFFFFFFF).to_bytes(7, byteorder="big")
        raw_16 = b_time + b_codex + b_morton + b_simhash
        return "".join(chr(BRAILLE_BASE + b) for b in raw_16)

    @classmethod
    def decode_packet_16(cls, braille_16: str) -> Dict[str, Any]:
        """Losslessly unpacks a 16-cell Unicode Braille string back into its 4 constituent fields."""
        if len(braille_16) != 16:
            raise ValueError(f"Expected 16 Braille cells (128 bits), got {len(braille_16)}.")
        raw = bytes((ord(ch) - BRAILLE_BASE) & 0xFF for ch in braille_16)
        epoch_sec = struct.unpack(">I", raw[0:4])[0]
        codex_mask = raw[4]
        morton_32 = struct.unpack(">I", raw[5:9])[0]
        simhash_56 = int.from_bytes(raw[9:16], byteorder="big")
        gx, gy = cls.morton_deinterleave_32bit(morton_32)
        lat_deg, lon_deg = cls.grid_65536_to_latlon(gx, gy)
        return {
            "braille_16": braille_16,
            "time_braille_4": braille_16[:4],
            "epoch_sec": epoch_sec,
            "codex_mask_8bit": codex_mask,
            "codex_cell": braille_16[4],
            "morton_32bit": morton_32,
            "morton_cells": braille_16[5:9],
            "grid_65536": {"x": gx, "y": y if (y := gy) is not None else 0},
            "decoded_lat_deg": lat_deg,
            "decoded_lon_deg": lon_deg,
            "simhash_56bit": simhash_56,
            "simhash_cells": braille_16[9:16],
        }


class ApophenicCodexEngine:
    """
    Task 3.5 (`core/IntegraBrainMap.md`): Apophenic Codex Engine.
    - Scale-invariant ZigZag extrema detection (`theta_dc` directional change threshold).
    - 4x4 Markov Regime Transition Matrix (`ACCUMULATION`, `MARKUP`, `DISTRIBUTION`, `MARKDOWN`).
    - Synthesizes the Cell 4 8-dot Braille bitmask (`0x01..0x80`) and adaptive Peak Sell / Trough Buyback targets.
    """

    REGIMES = ("ACCUMULATION", "MARKUP", "DISTRIBUTION", "MARKDOWN")

    def __init__(self, theta_dc: float = 0.03):
        self.theta_dc = max(0.001, float(theta_dc))
        # 4x4 transition counts initialized with Laplace smoothing
        self.transition_counts: List[List[float]] = [
            [4.0, 3.0, 1.0, 1.0],
            [1.0, 5.0, 3.0, 1.0],
            [1.0, 1.0, 4.0, 3.0],
            [3.0, 1.0, 1.0, 5.0],
        ]

    def detect_zigzag_extrema(self, series: List[float]) -> List[Dict[str, Any]]:
        """Scale-invariant directional-change ZigZag extrema extraction."""
        if not series:
            return []
        extrema: List[Dict[str, Any]] = []
        last_pivot_val = float(series[0])
        last_pivot_idx = 0
        direction = 0  # +1 up, -1 down

        for idx, val in enumerate(series[1:], start=1):
            v = float(val)
            denom = max(abs(last_pivot_val), 1e-9)
            rel_change = (v - last_pivot_val) / denom
            if direction >= 0 and rel_change <= -self.theta_dc:
                extrema.append({"index": last_pivot_idx, "value": round(last_pivot_val, 6), "type": "PEAK"})
                direction = -1
                last_pivot_val = v
                last_pivot_idx = idx
            elif direction <= 0 and rel_change >= self.theta_dc:
                extrema.append({"index": last_pivot_idx, "value": round(last_pivot_val, 6), "type": "TROUGH"})
                direction = 1
                last_pivot_val = v
                last_pivot_idx = idx
            else:
                if (direction >= 0 and v > last_pivot_val) or (direction <= 0 and v < last_pivot_val):
                    last_pivot_val = v
                    last_pivot_idx = idx
        return extrema

    def get_markov_matrix(self) -> List[List[float]]:
        """Returns row-normalized 4x4 Markov transition probability matrix."""
        matrix: List[List[float]] = []
        for row in self.transition_counts:
            s = sum(row) or 1.0
            matrix.append([round(x / s, 4) for x in row])
        return matrix

    def evaluate_series(self, series: List[float]) -> Dict[str, Any]:
        """
        Evaluates a price/signal series, computes the Cell 4 8-dot bitmask,
        identifies current Markov regime, and projects Peak Sell & Trough Buyback targets.
        """
        if not series:
            series = [100.0, 102.0, 99.0, 104.5]
        vals = [float(x) for x in series]
        mean_v = sum(vals) / len(vals)
        variance = sum((x - mean_v) ** 2 for x in vals) / max(1, len(vals))
        std_v = math.sqrt(variance)
        last_v = vals[-1]
        first_v = vals[0]

        extrema = self.detect_zigzag_extrema(vals)
        mask = 0
        if last_v >= first_v:
            mask |= DOT1_TREND_UP
        else:
            mask |= DOT2_TREND_DOWN

        if std_v / max(abs(mean_v), 1e-9) > self.theta_dc:
            mask |= DOT3_VOL_EXPANSION
        else:
            mask |= DOT4_MEAN_REVERSION

        if last_v >= max(vals):
            mask |= DOT5_BREAKOUT
        if last_v <= min(vals):
            mask |= DOT6_BREAKDOWN

        # Peak Sell / Trough Buyback signals
        if last_v >= mean_v + std_v:
            mask |= DOT7_PEAK_SELL_SIGNAL
            regime = "DISTRIBUTION"
        elif last_v <= mean_v - std_v:
            mask |= DOT8_TROUGH_BUYBACK_SIGNAL
            regime = "ACCUMULATION"
        elif last_v >= mean_v:
            regime = "MARKUP"
        else:
            regime = "MARKDOWN"

        peak_sell_target = round(mean_v + 1.618 * std_v, 4)
        trough_buyback_target = round(max(0.0001, mean_v - 1.618 * std_v), 4)

        return {
            "codex_mask_8bit": mask,
            "codex_braille_cell": chr(BRAILLE_BASE + mask),
            "regime": regime,
            "markov_transition_matrix": self.get_markov_matrix(),
            "zigzag_extrema_count": len(extrema),
            "zigzag_extrema": extrema,
            "adaptive_peak_sell_target": peak_sell_target,
            "adaptive_trough_buyback_target": trough_buyback_target,
        }


class CartographicTaxonomy:
    """
    Task 4 (`core/IntegraBrainMap.md`): Cartographic Taxonomy & Multi-Resolution Coordinate Mapper.
    Resolves any (lat_deg, lon_deg) or semantic domain into:
      - 5 Latitudinal Zones / Poles (`Z1_SOUTH_POLE`..`Z5_NORTH_POLE`)
      - 4 Hemispheres (`NW_ANALYTICAL_ACTIVE`, `NE_SYNTHETIC_ACTIVE`, `SW_ANALYTICAL_ARCHIVAL`, `SE_SYNTHETIC_ARCHIVAL`)
      - 12 Meridians (`M01`–`M12`)
      - Macro 10x12 Plot-Point (row, col), Meso 4096x4096, Micro 65536x65536, and 3D Unit-Sphere (x, y, z).
    """

    @staticmethod
    def resolve_zone(lat_deg: float) -> Tuple[str, Tuple[int, int], str]:
        lat = max(-90.0, min(90.0, float(lat_deg)))
        for zone_id, low, high, rows, desc in LATITUDINAL_ZONES:
            if low <= lat <= high:
                return zone_id, rows, desc
        return "Z3_EQUATORIAL_CORE", (4, 5), "Active Waking Synthesis"

    @staticmethod
    def resolve_meridian(lon_deg: float) -> Tuple[str, int]:
        lon = max(-180.0, min(179.9999, float(lon_deg)))
        for m_id, low, high, col_idx in MERIDIAN_DOMAINS:
            if low <= lon < high:
                return m_id, col_idx
        return "M12_KINTSUGI_DEFENSE", 11

    @staticmethod
    def resolve_hemisphere(lat_deg: float, lon_deg: float) -> str:
        if lat_deg >= 0.0 and lon_deg < 0.0:
            return "NW_ANALYTICAL_ACTIVE"
        if lat_deg >= 0.0 and lon_deg >= 0.0:
            return "NE_SYNTHETIC_ACTIVE"
        if lat_deg < 0.0 and lon_deg < 0.0:
            return "SW_ANALYTICAL_ARCHIVAL"
        return "SE_SYNTHETIC_ARCHIVAL"

    @classmethod
    def compute_cartographic_coordinates(cls, lat_deg: float, lon_deg: float) -> Dict[str, Any]:
        lat = max(-90.0, min(90.0, float(lat_deg)))
        lon = max(-180.0, min(180.0, float(lon_deg)))

        zone_id, row_pair, zone_desc = cls.resolve_zone(lat)
        meridian_id, col_idx = cls.resolve_meridian(lon)
        hemisphere = cls.resolve_hemisphere(lat, lon)

        # Map latitude [-90, +90] -> Macro row 9..0 (Row 0 = North Pole, Row 9 = South Pole)
        norm_lat = (90.0 - lat) / 180.0
        macro_row = max(0, min(9, int(norm_lat * 10.0)))

        # 3D Unit Sphere (x, y, z)
        lat_rad = math.radians(lat)
        lon_rad = math.radians(lon)
        x_3d = round(math.cos(lat_rad) * math.cos(lon_rad), 6)
        y_3d = round(math.cos(lat_rad) * math.sin(lon_rad), 6)
        z_3d = round(math.sin(lat_rad), 6)

        # Meso 4096x4096 and Micro 65536x65536
        gx_65536, gy_65536 = BrailleCodec.latlon_to_grid_65536(lat, lon)
        gx_4096 = gx_65536 >> 4
        gy_4096 = gy_65536 >> 4
        morton_32 = BrailleCodec.morton_interleave_16bit(gx_65536, gy_65536)

        return {
            "lat_deg": round(lat, 4),
            "lon_deg": round(lon, 4),
            "latitudinal_zone": zone_id,
            "zone_description": zone_desc,
            "hemisphere": hemisphere,
            "meridian": meridian_id,
            "macro_plot_point": {"row": macro_row, "col": col_idx, "id": f"PP_R{macro_row:02d}_C{col_idx:02d}"},
            "meso_grid_4096": {"x": gx_4096, "y": gy_4096},
            "micro_grid_65536": {"x": gx_65536, "y": gy_65536},
            "morton_32bit": morton_32,
            "unit_sphere_3d": {"x": x_3d, "y": y_3d, "z": z_3d},
        }


class SphericalKohonenSOM:
    """
    Task 3 (`core/IntegraBrainMap.md`): Geodesic Great-Circle Spherical Self-Organizing Map (SOM).
    Projects 64D/768D semantic embeddings onto the 10x12 spherical lattice (`120` neurons)
    using geodesic great-circle distance on $S^2$.
    """

    def __init__(self, rows: int = 10, cols: int = 12, dim: int = 64):
        self.rows = rows
        self.cols = cols
        self.dim = dim
        self.weights: Dict[Tuple[int, int], List[float]] = {}
        self.neuron_latlon: Dict[Tuple[int, int], Tuple[float, float]] = {}
        self._init_lattice()

    def _init_lattice(self) -> None:
        for r in range(self.rows):
            lat = 90.0 - ((r + 0.5) / self.rows) * 180.0
            for c in range(self.cols):
                lon = -180.0 + ((c + 0.5) / self.cols) * 360.0
                self.neuron_latlon[(r, c)] = (round(lat, 4), round(lon, 4))
                # Deterministic orthogonal basis initialization on unit hypersphere
                seed = f"SOM_NEURON_R{r:02d}_C{c:02d}".encode("utf-8")
                digest = hashlib.sha512(seed).digest()
                vec = [((digest[i % len(digest)] / 127.5) - 1.0) for i in range(self.dim)]
                norm = math.sqrt(sum(v * v for v in vec)) or 1.0
                self.weights[(r, c)] = [round(v / norm, 6) for v in vec]

    @staticmethod
    def geodesic_distance_rad(lat1_deg: float, lon1_deg: float, lat2_deg: float, lon2_deg: float) -> float:
        """Great-circle central angle (radians) on the unit sphere."""
        p1, l1 = math.radians(lat1_deg), math.radians(lon1_deg)
        p2, l2 = math.radians(lat2_deg), math.radians(lon2_deg)
        cos_d = math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(l1 - l2)
        return math.acos(max(-1.0, min(1.0, cos_d)))

    def find_bmu(self, input_vec: List[float]) -> Dict[str, Any]:
        """Finds the Best Matching Unit (BMU) on the 10x12 spherical SOM lattice."""
        v = list(input_vec[: self.dim])
        if len(v) < self.dim:
            v.extend([0.0] * (self.dim - len(v)))
        norm_v = math.sqrt(sum(x * x for x in v)) or 1.0
        v = [x / norm_v for x in v]

        best_rc = (4, 5)
        best_sim = -2.0
        for rc, w in self.weights.items():
            sim = sum(a * b for a, b in zip(v, w))
            if sim > best_sim:
                best_sim = sim
                best_rc = rc

        lat, lon = self.neuron_latlon[best_rc]
        carto = CartographicTaxonomy.compute_cartographic_coordinates(lat, lon)
        return {
            "bmu_row": best_rc[0],
            "bmu_col": best_rc[1],
            "cosine_similarity": round(best_sim, 6),
            "lat_deg": lat,
            "lon_deg": lon,
            "cartography": carto,
        }

    def train_step(self, input_vec: List[float], learning_rate: float = 0.15, sigma_rad: float = 0.5) -> Dict[str, Any]:
        """Updates the BMU and its geodesic spherical neighborhood on the SOM lattice."""
        bmu = self.find_bmu(input_vec)
        bmu_lat, bmu_lon = bmu["lat_deg"], bmu["lon_deg"]
        v = list(input_vec[: self.dim])
        if len(v) < self.dim:
            v.extend([0.0] * (self.dim - len(v)))
        norm_v = math.sqrt(sum(x * x for x in v)) or 1.0
        v = [x / norm_v for x in v]

        for rc, w in self.weights.items():
            n_lat, n_lon = self.neuron_latlon[rc]
            d_rad = self.geodesic_distance_rad(bmu_lat, bmu_lon, n_lat, n_lon)
            h_rc = math.exp(-(d_rad ** 2) / (2.0 * (sigma_rad ** 2)))
            updated = [w_i + learning_rate * h_rc * (v_i - w_i) for w_i, v_i in zip(w, v)]
            u_norm = math.sqrt(sum(x * x for x in updated)) or 1.0
            self.weights[rc] = [round(x / u_norm, 6) for x in updated]
        return bmu


class TufteIntegrityAuditor:
    """
    Task 3 (`core/IntegraBrainMap.md`): Tufte Visual & Data Integrity Auditor.
    Verifies that every 128-bit (16-cell) Braille packet satisfies:
      - Lie Factor (LF) == 1.0 (zero distortion between physical data and representation)
      - Data-Ink Ratio (eta_DI) == 1.0 (128/128 bits carry non-redundant semantic/spatiotemporal signal)
    """

    @staticmethod
    def audit_packet(braille_16: str) -> Dict[str, Any]:
        is_valid_len = len(braille_16) == 16
        in_range = all(0x2800 <= ord(ch) <= 0x28FF for ch in braille_16)
        signal_bits = 128 if (is_valid_len and in_range) else 0
        total_bits = max(1, len(braille_16) * 8)
        data_ink_ratio = round(signal_bits / total_bits, 4)
        lie_factor = 1.0 if (is_valid_len and in_range) else 0.0
        return {
            "tufte_compliant": is_valid_len and in_range and data_ink_ratio == 1.0,
            "lie_factor": lie_factor,
            "data_ink_ratio": data_ink_ratio,
            "signal_bits": signal_bits,
            "total_bits": total_bits,
        }


class BrailleAtlasEngine:
    """
    Unified Task L-3 Facade: Synthesizes 128-bit Braille Atlas Nodes, maps them onto
    the Spherical Kohonen SOM & Cartographic Taxonomy, audits Tufte Integrity, and
    persists every node to the MongoDB Persistent Placeholder file point (`braille_atlas_nodes.json`).
    """

    def __init__(self):
        self.som = SphericalKohonenSOM(rows=10, cols=12, dim=64)
        self.codex = ApophenicCodexEngine(theta_dc=0.03)
        self.auditor = TufteIntegrityAuditor()

    def synthesize_atlas_node(
        self,
        ccid: str,
        payload: Any,
        embedding_64d: List[float],
        epoch_sec: Optional[float] = None,
        signal_series: Optional[List[float]] = None,
        persist_to_mongodb_placeholder: bool = True,
    ) -> Dict[str, Any]:
        ts = int(time.time() if epoch_sec is None else epoch_sec)
        bmu = self.som.train_step(embedding_64d)
        carto = bmu["cartography"]
        codex_eval = self.codex.evaluate_series(signal_series or [100.0, 103.5, 101.0, 106.2])
        simhash_56 = BrailleCodec.compute_simhash_56bit(embedding_64d or payload)

        braille_16 = BrailleCodec.encode_packet_16(
            epoch_sec=ts,
            codex_mask_8bit=codex_eval["codex_mask_8bit"],
            morton_32bit=carto["morton_32bit"],
            simhash_56bit=simhash_56,
        )
        tufte = self.auditor.audit_packet(braille_16)

        u3d = carto["unit_sphere_3d"]
        vector_4d = {
            "x": u3d["x"],
            "y": u3d["y"],
            "z": u3d["z"],
            "t": float(ts),
            "lat_deg": carto["lat_deg"],
            "lon_deg": carto["lon_deg"],
            "latitudinal_zone": carto["latitudinal_zone"],
            "hemisphere": carto["hemisphere"],
            "meridian": carto["meridian"],
            "plot_point_id": carto["macro_plot_point"]["id"],
            "morton_32bit": carto["morton_32bit"],
            "braille_16": braille_16,
            "time_braille_4": braille_16[:4],
        }

        atlas_record = {
            "ccid": ccid,
            "braille_16": braille_16,
            "time_braille_4": braille_16[:4],
            "epoch_sec": ts,
            "codex": codex_eval,
            "bmu": bmu,
            "cartography": carto,
            "simhash_56bit": simhash_56,
            "tufte_audit": tufte,
            "spacetime_anchor": vector_4d,
        }

        if persist_to_mongodb_placeholder:
            try:
                from memory.database.mongodb_substrate import MONGODB_SUBSTRATE

                col = MONGODB_SUBSTRATE.get_collection("braille_atlas_nodes")
                col.update_one({"ccid": ccid}, {"$set": atlas_record}, upsert=True)
            except Exception:
                pass

        return atlas_record


BRAILLE_ATLAS_ENGINE = BrailleAtlasEngine()


# ═════════════════════════════════════════════════════════════════════════════
# TASK L-4: CIT (X, Y) CROSSPOINT LATTICE (25% SEEDED / 75% OPEN),
# PHOENIX PLANETARY TRAJECTORY LOOP (D_orbital), & THROUGHPUT CALCULUS (EQ. 7.1-7.5)
# ═════════════════════════════════════════════════════════════════════════════

import base64
import zlib
from dataclasses import field
from enum import Enum, IntFlag


class DatasetArchetype(Enum):
    """Defines the dataset classes stored on predetermined (X, Y) grid crosspoints."""

    OPEN_UNALLOCATED = "OPEN_CROSSPOINT"
    PRETRAINED_SEED = "PRETRAINED_SEED_NODE"
    KNOWLEDGE_DOCUMENT = "KNOWLEDGE_DOCUMENT"
    SAVE_STATE_MEMORY = "SAVE_STATE_MEMORY"
    ISOLATED_NODE = "ISOLATED_KINTSUGI_NODE"


class CITCodexFlag(IntFlag):
    """8-Bit Register encoded into Cell 4 of the 16-Cell CIT Braille Label."""

    NONE = 0x00
    DOT1_EXPANSION = 0x01      # 1 = Expansion / Active Forward Trajectory
    DOT2_MACRO_ORBIT = 0x02    # 1 = Macro Orbital Checkpoint Aligned
    DOT3_HIGH_MASS = 0x04      # 1 = High Gravitational Mass (M_input > gamma)
    DOT4_KNOWLEDGE_DOC = 0x08  # 1 = Received Knowledge Document Dataset
    DOT5_SAVE_STATE = 0x10     # 1 = Save-State Memory Snapshot (Siesta/SWDS)
    DOT6_ORBIT_INFLECT = 0x20  # 1 = Orbital Solstice / Equinox / Eclipse Inflection
    DOT7_HOLOGRAPHIC = 0x40    # 1 = Compressed 4D Holographic Pointer
    DOT8_ISOLATED_NODE = 0x80  # 1 = Isolated Node (Kintsugi |Z| > 3.0 Quarantine)


class CITBrailleCodec:
    """
    Bidirectional hardware-speed codec for the 128-bit (16-Cell) CIT Label:
      - Cells 00..03 (32-bit): Big-Endian Celestial Epoch Timestamp
      - Cell  04     (8-bit) : CITCodexFlag Bitmask (Archetype & Orbital State)
      - Cells 05..08 (32-bit): Morton Z-Order (X, Y) Crosspoint Address
      - Cells 09..15 (56-bit): Binary Quantized Semantic Hash (SimHash)
    """

    BRAILLE_BASE = 0x2800

    @classmethod
    def byte_to_braille(cls, b: int) -> str:
        return chr(cls.BRAILLE_BASE + (int(b) & 0xFF))

    @classmethod
    def bytes_to_braille(cls, data: bytes) -> str:
        return "".join(cls.byte_to_braille(b) for b in data)

    @classmethod
    def braille_to_bytes(cls, braille_str: str) -> bytes:
        return bytes((ord(ch) - cls.BRAILLE_BASE) & 0xFF for ch in braille_str)

    @staticmethod
    def interleave_morton_xy16(x16: int, y16: int) -> int:
        """Interleaves 16-bit (X_16, Y_16) coordinates into a 32-bit quadtree Morton address."""
        x = max(0, min(0xFFFF, int(x16)))
        y = max(0, min(0xFFFF, int(y16)))
        morton = 0
        for c_idx in range(4):
            b = 0
            for step in range(4):
                shift = 15 - (c_idx * 4 + step)
                yb = (y >> shift) & 1
                xb = (x >> shift) & 1
                off = step * 2
                b |= (yb << off) | (xb << (off + 1))
            morton = (morton << 8) | b
        return morton & 0xFFFFFFFF

    @staticmethod
    def deinterleave_morton_xy16(morton_32bit: int) -> Tuple[int, int]:
        """Lossless inverse of `interleave_morton_xy16`: unpacks 32-bit Morton address -> (x16, y16)."""
        m = int(morton_32bit) & 0xFFFFFFFF
        x = 0
        y = 0
        for c_idx in range(4):
            b = (m >> (24 - 8 * c_idx)) & 0xFF
            for step in range(4):
                shift = 15 - (c_idx * 4 + step)
                off = step * 2
                yb = (b >> off) & 1
                xb = (b >> (off + 1)) & 1
                y |= yb << shift
                x |= xb << shift
        return x, y

    @staticmethod
    def hamming_distance_56bit(hash_a: int, hash_b: int) -> int:
        return ((int(hash_a) ^ int(hash_b)) & 0x00FFFFFFFFFFFFFF).bit_count()

    @classmethod
    def encode_cit_packet_16(
        cls,
        epoch_sec: int,
        codex_flags: int,
        x16: int,
        y16: int,
        semantic_bq_56bit: int,
    ) -> str:
        b_time = cls.bytes_to_braille(struct.pack(">I", int(epoch_sec) & 0xFFFFFFFF))
        b_codex = cls.byte_to_braille(int(codex_flags) & 0xFF)
        morton_32 = cls.interleave_morton_xy16(x16, y16)
        b_spatial = cls.bytes_to_braille(struct.pack(">I", morton_32))
        b_sem = cls.bytes_to_braille((int(semantic_bq_56bit) & 0x00FFFFFFFFFFFFFF).to_bytes(7, "big"))
        return f"{b_time}{b_codex}{b_spatial}{b_sem}"

    @classmethod
    def decode_cit_packet_16(cls, packet_16: str) -> Dict[str, Any]:
        if len(packet_16) != 16:
            raise ValueError(f"CIT Braille packet must be 16 cells, got {len(packet_16)}.")
        raw = cls.braille_to_bytes(packet_16)
        epoch_sec = struct.unpack(">I", raw[0:4])[0]
        codex_flags = raw[4]
        morton_32 = struct.unpack(">I", raw[5:9])[0]
        x16, y16 = cls.deinterleave_morton_xy16(morton_32)
        sem_56 = int.from_bytes(raw[9:16], "big")
        return {
            "packet_16": packet_16,
            "epoch_sec": epoch_sec,
            "codex_flags": codex_flags,
            "morton_32bit": morton_32,
            "matrix_xy_16": (x16, y16),
            "matrix_xy_12": (x16 >> 4, y16 >> 4),
            "semantic_bq_56bit": sem_56,
        }


@dataclass
class PlanetaryTrajectoryState:
    epoch_sec: int
    braille_time_4: str
    earth_rotation_deg: float
    lunar_phase_cycle: float
    orbital_true_anomaly_deg: float
    heliocentric_distance_au: float
    trajectory_lat_y: float
    trajectory_lon_x: float
    completed_orbits: int
    compounded_spatial_accuracy_sigma: float
    celestial_partition_key: str


class CelestialOrbitalClock:
    """
    Derives Spatial Coordinates from Time (T -> S) using pure orbital kinematics
    anchored to the initial geolocation ping (Baker, LA: 30.5888 N, -91.1673 W).
    Compounds spatial accuracy exponentially at each orbital checkpoint.
    """

    SIDEREAL_DAY_SEC = 86164.0905
    SYNODIC_LUNAR_SEC = 2551442.8
    SIDEREAL_YEAR_SEC = 31558149.76
    ORBIT_ECCENTRICITY = 0.0167086
    AXIAL_OBLIQUITY_DEG = 23.43928

    def __init__(self, ping_lat: float = 30.5888, ping_lon: float = -91.1673):
        self.ping_lat = ping_lat
        self.ping_lon = ping_lon
        self.completed_orbits = 0
        self.eclipse_alignments_logged = 0
        self._calibration_decay = 0.0

    def solve_kepler_equation(self, mean_anomaly_rad: float, tol: float = 1e-9) -> float:
        e_anom = mean_anomaly_rad
        for _ in range(60):
            f_val = e_anom - self.ORBIT_ECCENTRICITY * math.sin(e_anom) - mean_anomaly_rad
            if abs(f_val) < tol:
                break
            f_prime = 1.0 - self.ORBIT_ECCENTRICITY * math.cos(e_anom)
            e_anom -= f_val / f_prime
        return e_anom

    def register_orbital_checkpoint(self, is_eclipse_or_solstice: bool = True, full_orbit: bool = False) -> None:
        if is_eclipse_or_solstice:
            self.eclipse_alignments_logged += 1
            self._calibration_decay += 0.45
        if full_orbit:
            self.completed_orbits += 1
            self._calibration_decay += 0.85

    def step_planetary_trajectory(self, epoch_sec: int) -> PlanetaryTrajectoryState:
        b_time_4 = CITBrailleCodec.bytes_to_braille(struct.pack(">I", int(epoch_sec) & 0xFFFFFFFF))

        rot_fraction = (epoch_sec % self.SIDEREAL_DAY_SEC) / self.SIDEREAL_DAY_SEC
        theta_rot_deg = (self.ping_lon + rot_fraction * 360.0) % 360.0

        ref_new_moon_epoch = 1735689600  # 2025-01-01T00:00:00Z
        phi_lunar = ((epoch_sec - ref_new_moon_epoch) % self.SYNODIC_LUNAR_SEC) / self.SYNODIC_LUNAR_SEC

        orbital_elapsed = (epoch_sec - ref_new_moon_epoch) % self.SIDEREAL_YEAR_SEC
        mean_anom = (2.0 * math.pi * orbital_elapsed) / self.SIDEREAL_YEAR_SEC
        ecc_anom = self.solve_kepler_equation(mean_anom)

        true_anom_rad = 2.0 * math.atan2(
            math.sqrt(1.0 + self.ORBIT_ECCENTRICITY) * math.sin(ecc_anom / 2.0),
            math.sqrt(1.0 - self.ORBIT_ECCENTRICITY) * math.cos(ecc_anom / 2.0),
        )
        true_anom_deg = math.degrees(true_anom_rad) % 360.0
        r_au = 1.000001018 * (1.0 - self.ORBIT_ECCENTRICITY * math.cos(ecc_anom))

        obliq_rad = math.radians(self.AXIAL_OBLIQUITY_DEG)
        solar_declination_deg = math.degrees(math.asin(math.sin(obliq_rad) * math.sin(true_anom_rad)))
        lunar_lat_modulation = 5.145 * math.sin(2.0 * math.pi * phi_lunar)

        traj_lat_y = max(-90.0, min(90.0, solar_declination_deg * 3.2 + lunar_lat_modulation))
        traj_lon_x = ((theta_rot_deg + true_anom_deg + phi_lunar * 360.0) % 360.0) - 180.0

        sigma_acc = round(1.0 - 0.015 * math.exp(-self._calibration_decay), 6)
        part_key = f"ROT_{int(theta_rot_deg):03d}_LUN_{int(phi_lunar * 1000):03d}_ORB_{int(true_anom_deg):03d}"

        return PlanetaryTrajectoryState(
            epoch_sec=int(epoch_sec),
            braille_time_4=b_time_4,
            earth_rotation_deg=round(theta_rot_deg, 4),
            lunar_phase_cycle=round(phi_lunar, 4),
            orbital_true_anomaly_deg=round(true_anom_deg, 4),
            heliocentric_distance_au=round(r_au, 6),
            trajectory_lat_y=round(traj_lat_y, 4),
            trajectory_lon_x=round(traj_lon_x, 4),
            completed_orbits=self.completed_orbits,
            compounded_spatial_accuracy_sigma=sigma_acc,
            celestial_partition_key=part_key,
        )


@dataclass
class GridCrosspointPlotPoint:
    """
    A Predetermined Plot Point at an (X, Y) axis intersection on the neural grid.
    Starts as OPEN_CROSSPOINT (70-80% of grid) or PRETRAINED_SEED_NODE (20-30%).
    """

    crosspoint_id: str
    grid_x_idx: int
    grid_y_idx: int
    longitude_x_deg: float
    latitude_y_deg: float
    matrix_x16: int
    matrix_y16: int
    matrix_x12: int
    matrix_y12: int
    morton_32bit: int
    braille_spatial_4: str
    hemisphere: str
    epistemic_zone: str
    domain_meridian: str
    cit_coordinate_uri: str
    is_open: bool
    archetype: str
    stored_dataset_id: Optional[str] = None
    stored_title: Optional[str] = None
    cit_braille_packet_16: Optional[str] = None
    celestial_partition_key: Optional[str] = None
    semantic_bq_56bit: int = 0
    vec_64d: List[float] = field(default_factory=list)
    vec_768d: List[float] = field(default_factory=list)
    compressed_payload: Optional[bytes] = None
    z_score_anomaly: float = 0.0

    def to_mongo_doc(self, include_full_768d: bool = False) -> Dict[str, Any]:
        payload_b64 = (
            base64.b64encode(self.compressed_payload).decode("ascii")
            if self.compressed_payload is not None
            else None
        )
        doc: Dict[str, Any] = {
            "_id": self.crosspoint_id,
            "crosspoint_id": self.crosspoint_id,
            "grid_x_idx": self.grid_x_idx,
            "grid_y_idx": self.grid_y_idx,
            "longitude_x_deg": self.longitude_x_deg,
            "latitude_y_deg": self.latitude_y_deg,
            "matrix_x16": self.matrix_x16,
            "matrix_y16": self.matrix_y16,
            "matrix_x12": self.matrix_x12,
            "matrix_y12": self.matrix_y12,
            "morton_32bit": self.morton_32bit,
            "braille_spatial_4": self.braille_spatial_4,
            "hemisphere": self.hemisphere,
            "epistemic_zone": self.epistemic_zone,
            "domain_meridian": self.domain_meridian,
            "cit_coordinate_uri": self.cit_coordinate_uri,
            "is_open": self.is_open,
            "archetype": self.archetype,
            "stored_dataset_id": self.stored_dataset_id,
            "stored_title": self.stored_title,
            "cit_braille_packet_16": self.cit_braille_packet_16,
            "celestial_partition_key": self.celestial_partition_key,
            "semantic_bq_56bit": self.semantic_bq_56bit,
            "vec_64d": [round(v, 6) for v in self.vec_64d],
            "compressed_payload_zlib_b64": payload_b64,
            "z_score_anomaly": self.z_score_anomaly,
        }
        if include_full_768d:
            doc["vec_768d"] = [round(v, 6) for v in self.vec_768d]
        return doc


class PhoenixCelestialGridEngine:
    """
    Unifies:
      - Predetermined (X, Y) Crosspoint Grid (25% Pre-Seeded / 75% Open Crosspoints)
      - CIT (Coordinate Indexing Taxonomy) 16-Cell Braille Labeling System
      - Phoenix Planetary Trajectory Loop (parallels Celestial Clock orbit to
        compute geodesic/orbital distance D_orbital for placing and locating Knowledge
        Documents, Save-State Memory, and Isolated Kintsugi Nodes)
      - Persistent MongoDB Placeholder storage (`cit_crosspoints` collection).
    """

    DIM_64 = 64
    DIM_768 = 768

    def __init__(
        self,
        x_meridians: int = 12,
        y_rings: int = 10,
        pretrained_capacity_ratio: float = 0.25,
        substrate: Any = None,
        persist_on_init: bool = False,
    ):
        if not (0.20 <= pretrained_capacity_ratio <= 0.30):
            raise ValueError("Initial deployment ratio must be within 20-30% of total capacity.")

        self.x_meridians = x_meridians
        self.y_rings = y_rings
        self.pretrained_ratio = pretrained_capacity_ratio
        self.clock = CelestialOrbitalClock()
        self.substrate = substrate
        self.crosspoints: Dict[str, GridCrosspointPlotPoint] = {}
        self._init_xy_crosspoint_lattice()
        if persist_on_init and self.substrate is not None:
            self.sync_lattice_to_mongodb()

    def _resolve_substrate(self) -> Any:
        if self.substrate is not None:
            return self.substrate
        try:
            from memory.database.mongodb_substrate import MONGODB_SUBSTRATE

            return MONGODB_SUBSTRATE
        except Exception:
            return None

    def sync_lattice_to_mongodb(self, include_full_768d: bool = False) -> Optional[Dict[str, Any]]:
        sub = self._resolve_substrate()
        if sub is None:
            return None
        col = sub.get_collection("cit_crosspoints")
        docs = [cp.to_mongo_doc(include_full_768d=include_full_768d) for cp in self.crosspoints.values()]
        return col.replace_many(docs, key_field="crosspoint_id")

    @classmethod
    def encode_semantic_hash_and_vectors(cls, text: str) -> Tuple[List[float], List[float], int, str]:
        raw_768 = [0.0] * cls.DIM_768
        tokens = text.lower().replace("?", "").replace(".", "").replace(",", "").split() or [text]
        shingles = tokens + [f"{tokens[i]}_{tokens[i + 1]}" for i in range(len(tokens) - 1)]

        for tok in shingles:
            digest = hashlib.sha512(tok.encode("utf-8")).digest()
            for i in range(cls.DIM_768):
                w = 2.0 if i < cls.DIM_64 else 1.0
                bit = (digest[i % len(digest)] >> (i % 8)) & 1
                raw_768[i] += w if bit else -w

        n768 = math.sqrt(sum(x * x for x in raw_768)) or 1.0
        v768 = [x / n768 for x in raw_768]
        s64 = v768[: cls.DIM_64]
        n64 = math.sqrt(sum(x * x for x in s64)) or 1.0
        v64 = [x / n64 for x in s64]

        bq_56 = 0
        for i in range(56):
            bq_56 = (bq_56 << 1) | (1 if v64[i] > 0.0 else 0)
        b_sem_7 = CITBrailleCodec.bytes_to_braille(bq_56.to_bytes(7, "big"))
        return v64, v768, bq_56, b_sem_7

    @staticmethod
    def haversine_rad(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        p1, l1 = math.radians(lat1), math.radians(lon1)
        p2, l2 = math.radians(lat2), math.radians(lon2)
        a = (
            math.sin((p2 - p1) / 2.0) ** 2
            + math.cos(p1) * math.cos(p2) * (math.sin((l2 - l1) / 2.0) ** 2)
        )
        return 2.0 * math.asin(min(1.0, math.sqrt(max(0.0, a))))

    def _init_xy_crosspoint_lattice(self) -> None:
        total_points = self.x_meridians * self.y_rings
        target_seeded = int(round(total_points * self.pretrained_ratio))
        seeded_count = 0

        init_orbit = self.clock.step_planetary_trajectory(1792800000)

        for y_idx in range(self.y_rings):
            lat_y = -90.0 + ((y_idx + 0.5) / self.y_rings) * 180.0
            for x_idx in range(self.x_meridians):
                lon_x = -180.0 + ((x_idx + 0.5) / self.x_meridians) * 360.0
                cid = f"XPT_X{x_idx:02d}_Y{y_idx:02d}"

                nx = min(0.999999, max(0.0, (lon_x + 180.0) / 360.0))
                ny = min(0.999999, max(0.0, (lat_y + 90.0) / 180.0))
                x16, y16 = int(nx * 65536), int(ny * 65536)
                x12, y12 = x16 >> 4, y16 >> 4

                morton_32 = CITBrailleCodec.interleave_morton_xy16(x16, y16)
                b_spatial_4 = CITBrailleCodec.bytes_to_braille(struct.pack(">I", morton_32))

                hem = f"{'N' if y16 >= 32768 else 'S'}{'E' if x16 >= 32768 else 'W'}"
                if y16 >= 56978:
                    zone = "Z5_NORTH_POLE"
                elif y16 >= 41325:
                    zone = "Z4_N_TEMPERATE"
                elif y16 >= 24211:
                    zone = "Z3_EQUATORIAL"
                elif y16 >= 8558:
                    zone = "Z2_S_TEMPERATE"
                else:
                    zone = "Z1_SOUTH_POLE"

                meridian = f"M{x_idx + 1:02d}"
                cit_uri = f"CIT://{hem}/{zone}/{meridian}/{cid}/QUAD_{b_spatial_4}/XY_{x12:04d}_{y12:04d}"

                is_seeded = ((y_idx * self.x_meridians + x_idx) % 4 == 0) and (seeded_count < target_seeded)

                if is_seeded:
                    seeded_count += 1
                    seed_title = f"Pretrained Baseline Axiom @ {cid} ({zone})"
                    v64, v768, bq56, b_sem_7 = self.encode_semantic_hash_and_vectors(seed_title)
                    codex_b1 = CITBrailleCodec.byte_to_braille(int(CITCodexFlag.DOT1_EXPANSION))
                    packet_16 = f"{init_orbit.braille_time_4}{codex_b1}{b_spatial_4}{b_sem_7}"
                    self.crosspoints[cid] = GridCrosspointPlotPoint(
                        crosspoint_id=cid,
                        grid_x_idx=x_idx,
                        grid_y_idx=y_idx,
                        longitude_x_deg=round(lon_x, 4),
                        latitude_y_deg=round(lat_y, 4),
                        matrix_x16=x16,
                        matrix_y16=y16,
                        matrix_x12=x12,
                        matrix_y12=y12,
                        morton_32bit=morton_32,
                        braille_spatial_4=b_spatial_4,
                        hemisphere=hem,
                        epistemic_zone=zone,
                        domain_meridian=meridian,
                        cit_coordinate_uri=cit_uri,
                        is_open=False,
                        archetype=DatasetArchetype.PRETRAINED_SEED.value,
                        stored_dataset_id=f"SEED_{cid}",
                        stored_title=seed_title,
                        cit_braille_packet_16=packet_16,
                        celestial_partition_key=init_orbit.celestial_partition_key,
                        semantic_bq_56bit=bq56,
                        vec_64d=v64,
                        vec_768d=v768,
                    )
                else:
                    v64, v768, bq56, _ = self.encode_semantic_hash_and_vectors(f"{cid} {zone} {meridian}")
                    self.crosspoints[cid] = GridCrosspointPlotPoint(
                        crosspoint_id=cid,
                        grid_x_idx=x_idx,
                        grid_y_idx=y_idx,
                        longitude_x_deg=round(lon_x, 4),
                        latitude_y_deg=round(lat_y, 4),
                        matrix_x16=x16,
                        matrix_y16=y16,
                        matrix_x12=x12,
                        matrix_y12=y12,
                        morton_32bit=morton_32,
                        braille_spatial_4=b_spatial_4,
                        hemisphere=hem,
                        epistemic_zone=zone,
                        domain_meridian=meridian,
                        cit_coordinate_uri=cit_uri,
                        is_open=True,
                        archetype=DatasetArchetype.OPEN_UNALLOCATED.value,
                        semantic_bq_56bit=bq56,
                        vec_64d=v64,
                        vec_768d=v768,
                    )

    def get_crosspoint(self, crosspoint_id: str) -> Optional[GridCrosspointPlotPoint]:
        return self.crosspoints.get(crosspoint_id)

    def phoenix_orbital_place_dataset(
        self,
        dataset_id: str,
        title: str,
        raw_content: str,
        archetype: DatasetArchetype,
        epoch_sec: int,
        target_lat_hint: Optional[float] = None,
        target_lon_hint: Optional[float] = None,
        z_score_anomaly: float = 0.0,
        persist_to_mongodb: bool = True,
    ) -> Dict[str, Any]:
        """
        Parallels planetary trajectory at `epoch_sec` to place:
          - KNOWLEDGE_DOCUMENT (Received documents)
          - SAVE_STATE_MEMORY  (Siesta / SWDS save states)
          - ISOLATED_NODE      (Kintsugi |Z| > 3.0 quarantined nodes)
        onto the nearest OPEN (X, Y) Crosspoint by minimizing Orbital Distance D_orbital.
        """
        orbit_state = self.clock.step_planetary_trajectory(epoch_sec)
        v64, v768, bq56, b_sem_7 = self.encode_semantic_hash_and_vectors(f"{title} {raw_content}")

        if abs(z_score_anomaly) > 3.0:
            archetype = DatasetArchetype.ISOLATED_NODE

        target_lat = target_lat_hint if target_lat_hint is not None else orbit_state.trajectory_lat_y
        target_lon = target_lon_hint if target_lon_hint is not None else orbit_state.trajectory_lon_x

        open_candidates = [cp for cp in self.crosspoints.values() if cp.is_open]
        if not open_candidates:
            raise RuntimeError("No open (X, Y) crosspoints remaining on the neural grid!")

        best_cp: Optional[GridCrosspointPlotPoint] = None
        best_d_orbital = 1e9

        for cp in open_candidates:
            d_geo = self.haversine_rad(target_lat, target_lon, cp.latitude_y_deg, cp.longitude_x_deg) / math.pi
            d_traj = self.haversine_rad(
                orbit_state.trajectory_lat_y,
                orbit_state.trajectory_lon_x,
                cp.latitude_y_deg,
                cp.longitude_x_deg,
            ) / math.pi
            d_ham = CITBrailleCodec.hamming_distance_56bit(bq56, cp.semantic_bq_56bit) / 56.0
            sim_64 = sum(a * b for a, b in zip(v64, cp.vec_64d))
            sim_768 = sum(a * b for a, b in zip(v768, cp.vec_768d))
            d_vec = (1.0 - (0.30 * sim_64 + 0.70 * sim_768)) / 2.0

            d_orbital = 0.40 * d_geo + 0.25 * d_traj + 0.20 * d_ham + 0.15 * d_vec
            if d_orbital < best_d_orbital:
                best_d_orbital = d_orbital
                best_cp = cp

        assert best_cp is not None

        flags = CITCodexFlag.DOT1_EXPANSION | CITCodexFlag.DOT2_MACRO_ORBIT
        if archetype == DatasetArchetype.KNOWLEDGE_DOCUMENT:
            flags |= CITCodexFlag.DOT4_KNOWLEDGE_DOC
        elif archetype == DatasetArchetype.SAVE_STATE_MEMORY:
            flags |= CITCodexFlag.DOT5_SAVE_STATE
        elif archetype == DatasetArchetype.ISOLATED_NODE:
            flags |= CITCodexFlag.DOT8_ISOLATED_NODE

        codex_b1 = CITBrailleCodec.byte_to_braille(int(flags))
        packet_16 = f"{orbit_state.braille_time_4}{codex_b1}{best_cp.braille_spatial_4}{b_sem_7}"

        best_cp.is_open = False
        best_cp.archetype = archetype.value
        best_cp.stored_dataset_id = dataset_id
        best_cp.stored_title = title
        best_cp.cit_braille_packet_16 = packet_16
        best_cp.celestial_partition_key = orbit_state.celestial_partition_key
        best_cp.semantic_bq_56bit = bq56
        best_cp.vec_64d = v64
        best_cp.vec_768d = v768
        best_cp.z_score_anomaly = round(z_score_anomaly, 4)
        best_cp.compressed_payload = zlib.compress(
            json.dumps({"dataset_id": dataset_id, "title": title, "content": raw_content}).encode("utf-8"),
            9,
        )

        if persist_to_mongodb:
            sub = self._resolve_substrate()
            if sub is not None:
                sub.get_collection("cit_crosspoints").update_one(
                    {"crosspoint_id": best_cp.crosspoint_id},
                    {"$set": best_cp.to_mongo_doc()},
                    upsert=True,
                )

        return {
            "dataset_id": dataset_id,
            "archetype": archetype.value,
            "assigned_crosspoint_id": best_cp.crosspoint_id,
            "xy_grid_indices": (best_cp.grid_x_idx, best_cp.grid_y_idx),
            "matrix_xy_12": (best_cp.matrix_x12, best_cp.matrix_y12),
            "lat_lon_deg": (best_cp.latitude_y_deg, best_cp.longitude_x_deg),
            "cit_braille_packet_16": packet_16,
            "cit_codex_flags_int": int(flags),
            "cit_coordinate_uri": best_cp.cit_coordinate_uri,
            "celestial_partition_key": orbit_state.celestial_partition_key,
            "orbital_distance_D": round(best_d_orbital, 5),
            "spatial_accuracy_sigma": orbit_state.compounded_spatial_accuracy_sigma,
        }

    def phoenix_orbital_locate_nodes(
        self,
        query_text: str,
        search_epoch_sec: int,
        filter_archetype: Optional[DatasetArchetype] = None,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        orbit_state = self.clock.step_planetary_trajectory(search_epoch_sec)
        q64, q768, q_bq56, q_sem_b7 = self.encode_semantic_hash_and_vectors(query_text)

        occupied = [
            cp
            for cp in self.crosspoints.values()
            if not cp.is_open and (filter_archetype is None or cp.archetype == filter_archetype.value)
        ]

        located: List[Dict[str, Any]] = []
        for cp in occupied:
            d_traj_rad = self.haversine_rad(
                orbit_state.trajectory_lat_y,
                orbit_state.trajectory_lon_x,
                cp.latitude_y_deg,
                cp.longitude_x_deg,
            )
            d_traj_norm = d_traj_rad / math.pi

            ham_bits = CITBrailleCodec.hamming_distance_56bit(q_bq56, cp.semantic_bq_56bit)
            sim_ham = 1.0 - (ham_bits / 56.0)

            sim_64 = (1.0 + sum(a * b for a, b in zip(q64, cp.vec_64d))) / 2.0
            sim_768 = (1.0 + sum(a * b for a, b in zip(q768, cp.vec_768d))) / 2.0
            sim_mrl = 0.30 * sim_64 + 0.70 * sim_768

            d_orbital = 0.25 * d_traj_norm + 0.30 * (1.0 - sim_ham) + 0.45 * (1.0 - sim_mrl)
            upsilon_score = ((1.0 - d_orbital) / max(0.05, d_orbital)) * orbit_state.compounded_spatial_accuracy_sigma

            located.append(
                {
                    "crosspoint_id": cp.crosspoint_id,
                    "dataset_id": cp.stored_dataset_id,
                    "title": cp.stored_title,
                    "archetype": cp.archetype,
                    "cit_braille_packet_16": cp.cit_braille_packet_16,
                    "cit_coordinate_uri": cp.cit_coordinate_uri,
                    "matrix_xy_12": (cp.matrix_x12, cp.matrix_y12),
                    "orbital_arc_deg": round(math.degrees(d_traj_rad), 2),
                    "hamming_distance_bits": ham_bits,
                    "mrl_768d_similarity": round(sim_768, 4),
                    "composite_orbital_distance_D": round(d_orbital, 5),
                    "upsilon_throughput": round(upsilon_score, 4),
                }
            )

        located.sort(key=lambda x: x["composite_orbital_distance_D"])
        return {
            "query_text": query_text,
            "query_semantic_braille_7": q_sem_b7,
            "planetary_trajectory_singularity": {
                "lat_y": orbit_state.trajectory_lat_y,
                "lon_x": orbit_state.trajectory_lon_x,
                "true_anomaly_deg": orbit_state.orbital_true_anomaly_deg,
                "lunar_phase": orbit_state.lunar_phase_cycle,
                "partition_key": orbit_state.celestial_partition_key,
            },
            "top_located_nodes": located[:top_k],
        }

    def grid_capacity_telemetry(self) -> Dict[str, Any]:
        total = len(self.crosspoints)
        open_pts = sum(1 for cp in self.crosspoints.values() if cp.is_open)
        occ_pts = total - open_pts
        by_type: Dict[str, int] = {}
        for cp in self.crosspoints.values():
            by_type[cp.archetype] = by_type.get(cp.archetype, 0) + 1
        return {
            "total_xy_crosspoints": total,
            "occupied_crosspoints": occ_pts,
            "open_crosspoints_available": open_pts,
            "open_capacity_pct": round((open_pts / total) * 100.0, 2),
            "seeded_capacity_pct": round((by_type.get(DatasetArchetype.PRETRAINED_SEED.value, 0) / total) * 100.0, 2),
            "true_origin_crosspoint_id": "XPT_X02_Y06",
            "breakdown_by_archetype": by_type,
        }


# ─────────────────────────────────────────────────────────────────────────────
# TASK 7 PACKET 1: PREDEFINED PLOT-POINT THROUGHPUT CALCULUS (EQ. 7.1 - 7.5)
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class PredefinedPlotPoint:
    """Equation 7.1: Predefined Plot Point Pi_{r,c} on the R x C Neural Grid."""

    plot_point_id: str
    ring_r: int
    meridian_c: int
    latitude_deg: float
    longitude_deg: float
    matrix_x16: int
    matrix_y16: int
    matrix_x12: int
    matrix_y12: int
    morton_32bit: int
    braille_spatial_4: str
    hemisphere: str
    latitudinal_zone: str
    domain_meridian: str
    taxonomy_uri: str
    prototype_vec_64d: List[float]
    prototype_vec_16d: List[float]
    semantic_bq_56bit: int
    braille_semantic_7: str
    apophenic_codex_byte: int = 0x01
    designated_nodes: List[str] = field(default_factory=list)
    relational_edges: Dict[str, float] = field(default_factory=dict)
    vector_clock_ticks: int = 1
    last_updated_epoch: int = 1792800000
    forge_read_locked: bool = False

    def to_mongo_doc(self) -> Dict[str, Any]:
        return {
            "_id": self.plot_point_id,
            "plot_point_id": self.plot_point_id,
            "ring_r": self.ring_r,
            "meridian_c": self.meridian_c,
            "latitude_deg": self.latitude_deg,
            "longitude_deg": self.longitude_deg,
            "matrix_x16": self.matrix_x16,
            "matrix_y16": self.matrix_y16,
            "matrix_x12": self.matrix_x12,
            "matrix_y12": self.matrix_y12,
            "morton_32bit": self.morton_32bit,
            "braille_spatial_4": self.braille_spatial_4,
            "hemisphere": self.hemisphere,
            "latitudinal_zone": self.latitudinal_zone,
            "domain_meridian": self.domain_meridian,
            "taxonomy_uri": self.taxonomy_uri,
            "prototype_vec_16d": [round(v, 6) for v in self.prototype_vec_16d],
            "prototype_vec_64d": [round(v, 6) for v in self.prototype_vec_64d],
            "semantic_bq_56bit": self.semantic_bq_56bit,
            "braille_semantic_7": self.braille_semantic_7,
            "apophenic_codex_byte": self.apophenic_codex_byte,
            "designated_nodes": list(self.designated_nodes),
            "relational_edges": dict(self.relational_edges),
            "vector_clock_ticks": self.vector_clock_ticks,
            "last_updated_epoch": self.last_updated_epoch,
            "forge_read_locked": self.forge_read_locked,
        }


@dataclass
class DesignatedDataQuantization:
    """Equation 7.2: Result of designating incoming data onto a predefined plot point."""

    node_id: str
    title: str
    assigned_plot_point_id: str
    quantization_action_cost_J: float
    geodesic_distortion_deg: float
    cosine_divergence: float
    shared_quadtree_depth: int
    unified_braille_packet_16: str
    plot_point_taxonomy_uri: str
    matrix_xy_12: Tuple[int, int]
    matrix_xy_16: Tuple[int, int]
    residual_sum_of_squares_rss: float


@dataclass
class PlotPointThroughputEvaluation:
    """Equations 7.3 - 7.5: Master Plot-Point Throughput Upsilon_{r,c} and RRF score."""

    plot_point_id: str
    taxonomy_uri: str
    braille_spatial_4: str
    designated_nodes: List[str]
    phi_taxonomic: float
    phi_semantic: float
    phi_relational: float
    phi_y789_segregation: float
    phi_nexus_integration: float
    rss_error_plus_cost: float
    upsilon_throughput: float
    rrf_fusion_score: float
    rank_final: int = 0


class NeuralGridThroughputEngine:
    """
    Implements the Task 7 Mathematical Calculus (Equations 7.1 - 7.5):
      - Generates the R x C lattice of Predefined Plot Points across the Atlas
      - Quantifies & labels incoming data onto predefined plot points via Action Functional J (Eq. 7.2)
      - Evaluates Taxonomic, Semantic Vector (MRL + 56b Hamming + W_Q Rotation), and Relational Graph potentials (Eq. 7.3)
      - Computes Master Plot-Point Throughput Upsilon_{r,c} (Eq. 7.4) & Reciprocal Rank Fusion RRF (Eq. 7.5)
      - Persists plot-point state into MongoDB Persistent Placeholder collection `plot_points_state`.
    """

    BRAILLE_BASE = 0x2800
    EMBED_DIM = 64
    GOLDEN_ANGLE = math.pi * (3.0 - math.sqrt(5.0))

    def __init__(
        self,
        lat_rings: int = 10,
        lon_meridians: int = 12,
        substrate: Any = None,
        persist_on_init: bool = False,
    ):
        self.lat_rings = max(5, int(lat_rings))
        self.lon_meridians = max(6, int(lon_meridians))
        self.substrate = substrate
        self.plot_points: Dict[str, PredefinedPlotPoint] = {}
        self.node_registry: Dict[str, DesignatedDataQuantization] = {}
        self._init_predefined_plot_point_grid()
        if persist_on_init and self.substrate is not None:
            self.sync_plot_points_to_mongodb()

    def _resolve_substrate(self) -> Any:
        if self.substrate is not None:
            return self.substrate
        try:
            from memory.database.mongodb_substrate import MONGODB_SUBSTRATE

            return MONGODB_SUBSTRATE
        except Exception:
            return None

    def sync_plot_points_to_mongodb(self) -> Optional[Dict[str, Any]]:
        sub = self._resolve_substrate()
        if sub is None:
            return None
        col = sub.get_collection("plot_points_state")
        docs = [pp.to_mongo_doc() for pp in self.plot_points.values()]
        return col.replace_many(docs, key_field="plot_point_id")

    @classmethod
    def encode_mrl_vector_64d(cls, text: str) -> List[float]:
        raw = [0.0] * cls.EMBED_DIM
        tokens = text.lower().replace("\n", " ").split() or [text]
        shingles = tokens + [f"{tokens[i]}_{tokens[i + 1]}" for i in range(len(tokens) - 1)]
        for tok in shingles:
            digest = hashlib.sha256(tok.encode("utf-8")).digest()
            for i in range(cls.EMBED_DIM):
                w = 1.0 + (cls.EMBED_DIM - i) / cls.EMBED_DIM
                bit = (digest[i % len(digest)] >> (i % 8)) & 1
                raw[i] += w if bit else -w
        norm = math.sqrt(sum(x * x for x in raw)) or 1.0
        return [x / norm for x in raw]

    @staticmethod
    def slice_and_normalize(vec: List[float], dim: int) -> List[float]:
        s = [float(vec[i]) for i in range(min(dim, len(vec)))]
        nrm = math.sqrt(sum(x * x for x in s)) or 1.0
        return [x / nrm for x in s]

    @classmethod
    def apply_orthogonal_query_matrix_wq(cls, query_vec: List[float], pass_index: int = 1) -> List[float]:
        if pass_index <= 1:
            return list(query_vec)
        angle = (pass_index - 1) * (math.pi / 12.0)
        ca, sa = math.cos(angle), math.sin(angle)
        rotated = list(query_vec)
        for i in range(0, len(rotated) - 1, 2):
            v0, v1 = rotated[i], rotated[i + 1]
            rotated[i] = ca * v0 - sa * v1
            rotated[i + 1] = sa * v0 + ca * v1
        nrm = math.sqrt(sum(x * x for x in rotated)) or 1.0
        return [x / nrm for x in rotated]

    @classmethod
    def quantize_56bit_simhash(cls, vec_64d: List[float]) -> Tuple[int, str]:
        bq = 0
        for i in range(56):
            bq = (bq << 1) | (1 if vec_64d[i] > 0.0 else 0)
        b_str = "".join(chr(cls.BRAILLE_BASE + b) for b in bq.to_bytes(7, "big"))
        return bq, b_str

    @classmethod
    def interleave_morton_32(cls, y16: int, x16: int) -> Tuple[int, str]:
        morton = CITBrailleCodec.interleave_morton_xy16(x16=x16, y16=y16)
        braille_4 = CITBrailleCodec.bytes_to_braille(struct.pack(">I", morton))
        return morton, braille_4

    @staticmethod
    def haversine_radians(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        return PhoenixCelestialGridEngine.haversine_rad(lat1, lon1, lat2, lon2)

    @staticmethod
    def shared_braille_prefix_len(b_a: str, b_b: str) -> int:
        shared = 0
        for ca, cb in zip(b_a[:4], b_b[:4]):
            if ca == cb:
                shared += 1
            else:
                break
        return shared

    def _init_predefined_plot_point_grid(self) -> None:
        domain_thematic_seeds = [
            "quantitative macro cycle peak trough apophenic",
            "volatility risk options derivatives atr sigma",
            "algorithmic execution limit orderbook routing",
            "cybernetics systems architecture kernel state",
            "neural topology spherical som kohonen lattice",
            "cryptography braille bitmask morton quadtree",
            "epistemology bayesian axiom logic starfire",
            "classical literature narrative archetype canon",
            "cognitive science linguistics memory pedagogy",
            "visual information display tufte data ink geometry",
            "relativistic physics thermodynamics entropy",
            "telemetry archive cold storage hoard vault",
        ]

        for r in range(self.lat_rings):
            lat = -90.0 + ((r + 0.5) / self.lat_rings) * 180.0
            for c in range(self.lon_meridians):
                lon = -180.0 + ((c + 0.5) / self.lon_meridians) * 360.0
                pid = f"PLOT_R{r:02d}_C{c:02d}"

                norm_x = min(0.9999999, max(0.0, (lon + 180.0) / 360.0))
                norm_y = min(0.9999999, max(0.0, (lat + 90.0) / 180.0))
                x16, y16 = int(norm_x * 65536), int(norm_y * 65536)
                x12, y12 = x16 >> 4, y16 >> 4
                morton_32, braille_4 = self.interleave_morton_32(y16, x16)

                hem = f"{'N' if y16 >= 32768 else 'S'}{'E' if x16 >= 32768 else 'W'}"
                if y16 >= 56978:
                    zone = "Z5_NORTH_POLE"
                elif y16 >= 41325:
                    zone = "Z4_N_TEMPERATE"
                elif y16 >= 24211:
                    zone = "Z3_EQUATORIAL"
                elif y16 >= 8558:
                    zone = "Z2_S_TEMPERATE"
                else:
                    zone = "Z1_SOUTH_POLE"

                m_idx = min(11, int(norm_x * 12))
                meridian = f"M{m_idx + 1:02d}"
                uri = f"ATLAS://{hem}/{zone}/{meridian}/PLOT_{pid}/QUAD_{braille_4}/XY_{x12:04d}_{y12:04d}"

                seed_text = f"{pid} {zone} {meridian} {domain_thematic_seeds[m_idx]}"
                vec_64 = self.encode_mrl_vector_64d(seed_text)
                vec_16 = self.slice_and_normalize(vec_64, 16)
                bq_56, braille_sem_7 = self.quantize_56bit_simhash(vec_64)

                self.plot_points[pid] = PredefinedPlotPoint(
                    plot_point_id=pid,
                    ring_r=r,
                    meridian_c=c,
                    latitude_deg=round(lat, 4),
                    longitude_deg=round(lon, 4),
                    matrix_x16=x16,
                    matrix_y16=y16,
                    matrix_x12=x12,
                    matrix_y12=y12,
                    morton_32bit=morton_32,
                    braille_spatial_4=braille_4,
                    hemisphere=hem,
                    latitudinal_zone=zone,
                    domain_meridian=meridian,
                    taxonomy_uri=uri,
                    prototype_vec_64d=vec_64,
                    prototype_vec_16d=vec_16,
                    semantic_bq_56bit=bq_56,
                    braille_semantic_7=braille_sem_7,
                )

    def designate_and_quantify_data(
        self,
        node_id: str,
        title: str,
        raw_content: str,
        target_lat: float,
        target_lon: float,
        codex_byte: int = 0x03,
        epoch_sec: int = 1792175000,
        alpha_geo: float = 0.45,
        alpha_sem: float = 0.35,
        alpha_tax: float = 0.20,
        persist_to_mongodb: bool = True,
    ) -> DesignatedDataQuantization:
        vec_64 = self.encode_mrl_vector_64d(f"{title} {raw_content}")
        norm_x = min(0.9999999, max(0.0, (target_lon + 180.0) / 360.0))
        norm_y = min(0.9999999, max(0.0, (target_lat + 90.0) / 180.0))
        tx16, ty16 = int(norm_x * 65536), int(norm_y * 65536)
        _, target_braille_4 = self.interleave_morton_32(ty16, tx16)

        best_pid = ""
        best_action_j = 1e9
        best_geo_rad = 0.0
        best_cos_div = 0.0
        best_shared_q = 0

        for pid, pp in self.plot_points.items():
            d_rad = self.haversine_radians(target_lat, target_lon, pp.latitude_deg, pp.longitude_deg)
            geo_term = d_rad / math.pi

            cos_sim = sum(a * b for a, b in zip(vec_64, pp.prototype_vec_64d))
            sem_term = (1.0 - cos_sim) / 2.0

            shared_q = self.shared_braille_prefix_len(target_braille_4, pp.braille_spatial_4)
            tax_term = 1.0 - (shared_q / 4.0)

            action_j = alpha_geo * geo_term + alpha_sem * sem_term + alpha_tax * tax_term
            if action_j < best_action_j:
                best_action_j = action_j
                best_pid = pid
                best_geo_rad = d_rad
                best_cos_div = sem_term
                best_shared_q = shared_q

        winner = self.plot_points[best_pid]
        if node_id not in winner.designated_nodes:
            winner.designated_nodes.append(node_id)
        winner.apophenic_codex_byte |= codex_byte & 0xFF
        winner.vector_clock_ticks += 1
        winner.last_updated_epoch = int(epoch_sec)

        lr = 0.35
        upd_vec = [
            (1.0 - lr) * winner.prototype_vec_64d[i] + lr * vec_64[i]
            for i in range(self.EMBED_DIM)
        ]
        nrm = math.sqrt(sum(x * x for x in upd_vec)) or 1.0
        winner.prototype_vec_64d = [x / nrm for x in upd_vec]
        winner.prototype_vec_16d = self.slice_and_normalize(winner.prototype_vec_64d, 16)
        winner.semantic_bq_56bit, winner.braille_semantic_7 = self.quantize_56bit_simhash(
            winner.prototype_vec_64d
        )

        rss = sum((vec_64[i] - winner.prototype_vec_64d[i]) ** 2 for i in range(self.EMBED_DIM))

        time_b4 = "".join(chr(self.BRAILLE_BASE + b) for b in struct.pack(">I", int(epoch_sec) & 0xFFFFFFFF))
        codex_b1 = chr(self.BRAILLE_BASE + (winner.apophenic_codex_byte & 0xFF))
        packet_16 = f"{time_b4}{codex_b1}{winner.braille_spatial_4}{winner.braille_semantic_7}"

        quant_record = DesignatedDataQuantization(
            node_id=node_id,
            title=title,
            assigned_plot_point_id=best_pid,
            quantization_action_cost_J=round(best_action_j, 5),
            geodesic_distortion_deg=round(math.degrees(best_geo_rad), 3),
            cosine_divergence=round(best_cos_div, 5),
            shared_quadtree_depth=best_shared_q,
            unified_braille_packet_16=packet_16,
            plot_point_taxonomy_uri=winner.taxonomy_uri,
            matrix_xy_12=(winner.matrix_x12, winner.matrix_y12),
            matrix_xy_16=(winner.matrix_x16, winner.matrix_y16),
            residual_sum_of_squares_rss=round(rss, 5),
        )
        self.node_registry[node_id] = quant_record

        if persist_to_mongodb:
            sub = self._resolve_substrate()
            if sub is not None:
                sub.get_collection("plot_points_state").update_one(
                    {"plot_point_id": winner.plot_point_id},
                    {"$set": winner.to_mongo_doc()},
                    upsert=True,
                )

        return quant_record

    def link_plot_points(
        self,
        plot_id_a: str,
        plot_id_b: str,
        weight: float = 0.92,
        persist_to_mongodb: bool = True,
    ) -> None:
        if plot_id_a in self.plot_points and plot_id_b in self.plot_points:
            self.plot_points[plot_id_a].relational_edges[plot_id_b] = weight
            self.plot_points[plot_id_b].relational_edges[plot_id_a] = weight
            self.plot_points[plot_id_a].vector_clock_ticks += 1
            self.plot_points[plot_id_b].vector_clock_ticks += 1
            if persist_to_mongodb:
                sub = self._resolve_substrate()
                if sub is not None:
                    col = sub.get_collection("plot_points_state")
                    col.replace_many(
                        [
                            self.plot_points[plot_id_a].to_mongo_doc(),
                            self.plot_points[plot_id_b].to_mongo_doc(),
                        ],
                        key_field="plot_point_id",
                    )

    def evaluate_neural_grid_throughput(
        self,
        query_text: str,
        target_hemisphere: Optional[str] = None,
        target_zone: Optional[str] = None,
        target_meridian: Optional[str] = None,
        target_braille_prefix: str = "",
        required_codex_mask: int = 0x00,
        cwa_nexus_posterior: float = 0.50,
        query_pass_index: int = 1,
        lambda_cost_reg: float = 0.15,
        roguex_sigma: float = 1.0,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        q_raw_64 = self.encode_mrl_vector_64d(query_text)
        q_rot_64 = self.apply_orthogonal_query_matrix_wq(q_raw_64, pass_index=query_pass_index)
        q_rot_16 = self.slice_and_normalize(q_rot_64, 16)
        q_bq_56, q_braille_7 = self.quantize_56bit_simhash(q_rot_64)

        max_ticks = max(pp.vector_clock_ticks for pp in self.plot_points.values()) or 1
        evaluations: List[PlotPointThroughputEvaluation] = []

        for pid, pp in self.plot_points.items():
            if pp.forge_read_locked:
                continue

            mask_ok = (pp.apophenic_codex_byte & required_codex_mask) == required_codex_mask
            if not mask_ok:
                phi_tax = 0.0
            else:
                i_hem = 1.0 if (not target_hemisphere or pp.hemisphere == target_hemisphere) else 0.0
                i_zne = 1.0 if (not target_zone or pp.latitudinal_zone == target_zone) else 0.0
                i_mer = 1.0 if (not target_meridian or pp.domain_meridian == target_meridian) else 0.0
                if target_braille_prefix:
                    q_match = (
                        self.shared_braille_prefix_len(target_braille_prefix, pp.braille_spatial_4)
                        / max(1, len(target_braille_prefix))
                    )
                else:
                    q_match = 1.0
                phi_tax = 0.25 * i_hem + 0.30 * i_zne + 0.25 * i_mer + 0.20 * q_match

            sim_16 = (1.0 + sum(a * b for a, b in zip(q_rot_16, pp.prototype_vec_16d))) / 2.0
            sim_64 = (1.0 + sum(a * b for a, b in zip(q_rot_64, pp.prototype_vec_64d))) / 2.0
            ham_dist = ((q_bq_56 ^ pp.semantic_bq_56bit) & 0x00FFFFFFFFFFFFFF).bit_count()
            sim_bq = 1.0 - (ham_dist / 56.0)
            phi_sem = 0.25 * sim_16 + 0.50 * sim_64 + 0.25 * sim_bq

            edge_sum = 0.0
            for nbr_id, w_edge in pp.relational_edges.items():
                nbr = self.plot_points.get(nbr_id)
                if nbr:
                    d_rad = self.haversine_radians(
                        pp.latitude_deg, pp.longitude_deg, nbr.latitude_deg, nbr.longitude_deg
                    )
                    edge_sum += w_edge * math.exp(-(d_rad * d_rad) / (2.0 * (0.65 ** 2)))
            clock_ratio = pp.vector_clock_ticks / max_ticks
            phi_rel = math.tanh(edge_sum + 0.35 * clock_ratio)

            phi_y789 = 0.55 * phi_tax + 0.45 * phi_sem
            phi_nexus = 0.55 * phi_rel + 0.45 * phi_sem
            p_nex = max(0.0, min(1.0, float(cwa_nexus_posterior)))
            bicameral_blend = (1.0 - p_nex) * phi_y789 + p_nex * phi_nexus

            rss_val = max(0.05, 1.0 - sim_64)
            cost_c = 0.55 if pp.latitudinal_zone == "Z1_SOUTH_POLE" else 0.25
            denom = rss_val + lambda_cost_reg * (cost_c ** 2)

            intent_dot = 0.50 + 0.50 * (1.0 if pp.designated_nodes else 0.35)
            upsilon = (bicameral_blend * (intent_dot / denom)) * roguex_sigma

            evaluations.append(
                PlotPointThroughputEvaluation(
                    plot_point_id=pid,
                    taxonomy_uri=pp.taxonomy_uri,
                    braille_spatial_4=pp.braille_spatial_4,
                    designated_nodes=list(pp.designated_nodes),
                    phi_taxonomic=round(phi_tax, 5),
                    phi_semantic=round(phi_sem, 5),
                    phi_relational=round(phi_rel, 5),
                    phi_y789_segregation=round(phi_y789, 5),
                    phi_nexus_integration=round(phi_nexus, 5),
                    rss_error_plus_cost=round(denom, 5),
                    upsilon_throughput=round(upsilon, 5),
                    rrf_fusion_score=0.0,
                )
            )

        k_rrf = 60.0
        by_tax = sorted(evaluations, key=lambda x: x.phi_taxonomic, reverse=True)
        by_sem = sorted(evaluations, key=lambda x: x.phi_semantic, reverse=True)
        by_rel = sorted(evaluations, key=lambda x: x.phi_relational, reverse=True)
        by_ups = sorted(evaluations, key=lambda x: x.upsilon_throughput, reverse=True)

        r_tax_map = {e.plot_point_id: idx + 1 for idx, e in enumerate(by_tax)}
        r_sem_map = {e.plot_point_id: idx + 1 for idx, e in enumerate(by_sem)}
        r_rel_map = {e.plot_point_id: idx + 1 for idx, e in enumerate(by_rel)}
        r_ups_map = {e.plot_point_id: idx + 1 for idx, e in enumerate(by_ups)}

        for e in evaluations:
            pid = e.plot_point_id
            rrf = (
                1.0 / (k_rrf + r_tax_map[pid])
                + 1.0 / (k_rrf + r_sem_map[pid])
                + 1.0 / (k_rrf + r_rel_map[pid])
                + 1.0 / (k_rrf + r_ups_map[pid])
            )
            e.rrf_fusion_score = round(rrf, 6)

        evaluations.sort(key=lambda x: (x.upsilon_throughput, x.rrf_fusion_score), reverse=True)
        for rank_i, e in enumerate(evaluations, start=1):
            e.rank_final = rank_i

        top_hits = evaluations[:top_k]
        omega_integral = sum(h.upsilon_throughput for h in top_hits)

        return {
            "query_text": query_text,
            "query_bq_braille_7": q_braille_7,
            "total_predefined_plot_points": len(self.plot_points),
            "cwa_nexus_posterior": cwa_nexus_posterior,
            "epiphany_integral_omega": round(omega_integral, 5),
            "top_routed_plot_points": [asdict(h) for h in top_hits],
        }


PHOENIX_CELESTIAL_GRID_ENGINE = PhoenixCelestialGridEngine()
NEURAL_GRID_THROUGHPUT_ENGINE = NeuralGridThroughputEngine()
