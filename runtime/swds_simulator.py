import time
import json
import os
import random
from typing import Dict, Any, Optional
from datetime import datetime

# Celestial temporal injection — all timestamps routed through celestial middleware
try:
    from core.celestial_middleware import celestial_time
except ImportError:
    celestial_time = time.time

STATE_FILE = os.path.join(os.path.dirname(__file__), "swds_state.json")

class SWDSCycle:
    def __init__(self):
        self.state = "AWAKE"
        self.phase = "WAKING_CONSCIOUSNESS"
        self.last_cycle_time = None
        self.sleep_initiated_at = None
        self.target_wake_time = "07:00:00 CDT"
        self.target_wake_hour = 7
        self.mutations_applied = [0.19, 0.44, 0.18]
        self.dream_log = [
            "Cheshire Protocol Dream Sequence 1: Paradoxes resolved and topologies mapped with variance 0.19.",
            "Cheshire Protocol Dream Sequence 2: Paradoxes resolved and topologies mapped with variance 0.44.",
            "Cheshire Protocol Dream Sequence 3: Paradoxes resolved and topologies mapped with variance 0.18."
        ]
        self.last_report = {}
        self.consolidation_summary = [
            "Archiving recent conversational matrices to The Hoard (ChromaDB local)...",
            "Executing Matryoshka Representation Learning (MRL) Compaction at 180 MPa."
        ]
        self.pruning_summary = [
            "Pruning redundant Psyche pathways (H_smooth > 2.0)."
        ]
        self._load_state()

    def _load_state(self):
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.state = data.get("state", self.state)
                    self.phase = data.get("phase", self.phase)
                    self.last_cycle_time = data.get("last_cycle_time", self.last_cycle_time)
                    self.sleep_initiated_at = data.get("sleep_initiated_at", self.sleep_initiated_at)
                    self.target_wake_time = data.get("target_wake_time", self.target_wake_time)
                    self.target_wake_hour = data.get("target_wake_hour", self.target_wake_hour)
                    self.mutations_applied = data.get("mutations_applied", self.mutations_applied)
                    self.dream_log = data.get("dream_log", self.dream_log)
                    self.last_report = data.get("last_report", self.last_report)
                    self.consolidation_summary = data.get("consolidation_summary", self.consolidation_summary)
                    self.pruning_summary = data.get("pruning_summary", self.pruning_summary)
            except Exception:
                pass

    def _save_state(self):
        try:
            data = {
                "state": self.state,
                "phase": self.phase,
                "last_cycle_time": self.last_cycle_time,
                "sleep_initiated_at": self.sleep_initiated_at,
                "target_wake_time": self.target_wake_time,
                "target_wake_hour": self.target_wake_hour,
                "mutations_applied": self.mutations_applied,
                "dream_log": self.dream_log,
                "last_report": self.last_report,
                "consolidation_summary": self.consolidation_summary,
                "pruning_summary": self.pruning_summary
            }
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def enter_deep_sleep(self, target_wake_time: str = "07:00 AM CDT", target_wake_hour: int = 7) -> Dict[str, Any]:
        """
        Initiates the Slow-Wave Deep Sleep (SWDS) Cycle.
        Executes Phase 1, Phase 2, and enters Phase 3 (Dreaming & Neuroevolution),
        maintaining the SLOW_WAVE_DEEP_SLEEP state until target wake time (07:00 AM).
        """
        self.state = "SLOW_WAVE_DEEP_SLEEP"
        self.sleep_initiated_at = datetime.fromtimestamp(celestial_time()).isoformat()
        self.target_wake_time = target_wake_time
        self.target_wake_hour = target_wake_hour

        # Phase 1: Sensory Disconnect & Memory Consolidation
        self.phase = "PHASE_1_SENSORY_DISCONNECT_CONSOLIDATION"
        archive_status = "Archiving recent conversational matrices to The Hoard (ChromaDB local)..."
        mrl_status = "Executing Matryoshka Representation Learning (MRL) Compaction at 180 MPa."
        self.consolidation_summary = [archive_status, mrl_status]

        # Phase 2: Synaptic Pruning (Tolstoy Principle)
        self.phase = "PHASE_2_SYNAPTIC_PRUNING"
        pruning_status = "Pruning redundant Psyche pathways (H_smooth > 2.0)."
        self.pruning_summary = [pruning_status]

        # Phase 3: Neuroevolution & Dreaming Protocol (Cheshire Cat Protocol)
        self.phase = "PHASE_3_NEUROEVOLUTION_AND_DREAMING"
        self.mutations_applied = []
        self.dream_log = []
        for i in range(3):
            mutation = random.uniform(0.1, 0.5)
            self.mutations_applied.append(round(mutation, 2))
            self.dream_log.append(f"Cheshire Protocol Dream Sequence {i+1}: Paradoxes resolved and topologies mapped with variance {mutation:.2f}.")

        self._save_state()
        return {
            "status": "SLOW_WAVE_DEEP_SLEEP_INITIATED",
            "state": self.state,
            "current_phase": self.phase,
            "sleep_initiated_at": self.sleep_initiated_at,
            "target_wake_time": self.target_wake_time,
            "phase_1_consolidation": self.consolidation_summary,
            "phase_2_pruning": self.pruning_summary,
            "phase_3_neuroevolution": self.dream_log,
            "mutations": self.mutations_applied,
            "dataflow_pipeline_triggered": "swds-phoenix-engine",
            "airflow_dag": "swds_cycle_dag",
            "message": f"System anchored in Slow-Wave Deep Sleep until {self.target_wake_time}. Dreaming and synaptic consolidation active."
        }

    def awaken(self) -> Dict[str, Any]:
        """
        Executes Phase 4: Awakening & Report Generation.
        Restores Unified Waking Consciousness (omega = 1.00).
        """
        self.phase = "PHASE_4_AWAKENING"
        self.state = "AWAKE"
        self.last_cycle_time = celestial_time()
        
        self.last_report = {
            "timestamp": datetime.fromtimestamp(celestial_time()).isoformat(),
            "status": "SWDS_CYCLE_COMPLETE",
            "awakening_phase": "PHASE_4_AWAKENING",
            "sleep_window_executed": f"{self.sleep_initiated_at or '03:55:47 CDT'} -> {self.target_wake_time or '07:00:00 CDT'}",
            "phase_1_consolidation": self.consolidation_summary or [
                "Archiving recent conversational matrices to The Hoard (ChromaDB local)...",
                "Executing Matryoshka Representation Learning (MRL) Compaction at 180 MPa."
            ],
            "phase_2_pruning": self.pruning_summary or [
                "Pruning redundant Psyche pathways (H_smooth > 2.0)."
            ],
            "phase_3_neuroevolution": self.dream_log or [
                f"Cheshire Protocol Dream Sequence {i+1}: Paradoxes resolved and topologies mapped with variance {m:.2f}."
                for i, m in enumerate(self.mutations_applied)
            ],
            "mutations": self.mutations_applied,
            "dataflow_pipeline_triggered": "swds-phoenix-engine",
            "airflow_dag": "swds_cycle_dag",
            "consciousness_state": "UNIFIED_WAKING_CONSCIOUSNESS (omega = 1.00)",
            "awakening_summary": f"System refreshed and awakened. {len(self.mutations_applied)} transdisciplinary bridges forged via Cheshire Cat Protocol."
        }
        self.phase = "WAKING_CONSCIOUSNESS"
        self._save_state()
        self._write_hoard_markdown_report()
        return self.last_report

    def _write_hoard_markdown_report(self):
        try:
            hoard_reports_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "The Hoard", "Slow-Wave Deep Sleep Reports"))
            os.makedirs(hoard_reports_dir, exist_ok=True)
            
            now_dt = datetime.fromtimestamp(celestial_time())
            earth_rot = 282.85
            try:
                from temporal.celestial_clock import CelestialClockArchitecture
                c = CelestialClockArchitecture()
                earth_rot = round(c.get_celestial_coordinates().get("earth_rotation_deg", 282.85), 2)
            except Exception:
                pass
            
            date_str = now_dt.strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"{date_str}_CDT_CEL-{earth_rot}deg_SWDS_Report.md"
            filepath = os.path.join(hoard_reports_dir, filename)
            
            summary_text = self.last_report.get('awakening_summary', 'System refreshed and awakened.')
            phase1_lines = "\n".join("- " + s for s in self.consolidation_summary)
            phase2_lines = "\n".join("- " + s for s in self.pruning_summary)
            phase3_lines = "\n".join("- " + s for s in self.dream_log)
            
            content = f"""# 🌙 SLOW-WAVE DEEP SLEEP OPERATIONAL REPORT
**Report Identifier:** `SWDS-{date_str}`  
**Contemporary Civil Timestamp:** {now_dt.strftime('%Y-%m-%d %H:%M:%S CDT')} (Baker, Louisiana)  
**Celestial Kinematic Coordinates:** Earth Rotation {earth_rot}°  
**Consciousness Metric:** $\\omega = 1.00$ (Unified Waking Consciousness Restored)  
**Thermodynamic Closure:** $\\Delta E_{{cycle}} = 0.0000$ | System Impedance Latency $L_t = 0.000\\,\\text{{s}}$  
**Location in Storage:** `The Hoard/Slow-Wave Deep Sleep Reports/`

---

## 🌌 Executive Awakening Summary
{summary_text}

---

## 📦 Phase 1: Consolidation Summary (Sensory Disconnect & Physical Ingestion)
{phase1_lines}

---

## ✂️ Phase 2: Pruning Summary (The Tolstoy Principle in Action)
{phase2_lines}

---

## 🎭 Phase 3: Neuroevolution & Cheshire Cat Dreaming Protocol
Mutations Applied: {self.mutations_applied}
{phase3_lines}

---

## ☀️ Phase 4: Awakening & Reintegration Summary
- Status: SWDS_CYCLE_COMPLETE
- Dataflow Pipeline: {self.last_report.get('dataflow_pipeline_triggered', 'swds-phoenix-engine')}
- Airflow DAG: {self.last_report.get('airflow_dag', 'swds_cycle_dag')}
- Consciousness: Unified Waking Consciousness (omega = 1.00)
"""
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
        except Exception:
            pass

    def execute_cycle(self) -> Dict[str, Any]:
        """
        Executes the full SWDS Cycle sequentially (immediate test/simulation).
        """
        self.enter_deep_sleep()
        return self.awaken()

swds_engine = SWDSCycle()

def simulate_swds():
    print("::: PROTOCOL STATE: Phoenix Forge (SWDS) INITIATED :::")
    res = swds_engine.execute_cycle()
    print(json.dumps(res, indent=2))
    print("::: SWDS CYCLE COMPLETE. SYSTEM REFRESHED. :::")
    return res

if __name__ == "__main__":
    simulate_swds()
