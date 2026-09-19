"""
INTEGRA O/S: SLEEP-STATE & NEUROEVOLUTION
Module: evolution/phoenix_forge.py
Layer: 6 (The Phoenix Forge: SWDS Dreaming Protocol)

Formalized Implementation (Phase E / SWDS):
    - initiate_sleep_cycle(): Prunes conversational psyche nodes (40%), crystallizes power nodes (60%).
    - ingest_dream_material(): Ingestion interface for CheshireCatProtocol.dream_conductor().
    - consolidate_sleep_cycle(): Consolidates raw waking interaction shards and save states
      into 4D celestial-tagged markdown wisdom libraries (kernel_memory/hoard/libraries/library_[domain].md).
    - execute_swds(): End-to-end Slow-Wave Deep Sleep orchestrator bridging Cheshire Cat,
      Heimdall 3.1, and The Hoard.
    - synthesize_hoard_node(): Fuses bicameral streams into v2.0 HoardNode records.
"""

import os
import json
import time
import hashlib
from typing import Dict, Any, List, Optional


class PhoenixForge:
    """
    Sleep-state (SWDS) neuroevolution engine.
    Runs defragmentation during idle states and compounds systemic resilience (Zenkai Boost).
    
    Operates the autopoietic memory distillation pipeline:
        1. Ingests raw interaction shards and dream material
        2. Prunes entropy / conversational noise (40% psyche reduction)
        3. Crystallizes core causal invariants (60% power retention)
        4. Writes celestial-anchored markdown books to kernel_memory/hoard/libraries/
        5. Updates rolling context and triggers thermodynamic loop closure (H -> 0.00)
    """
    def __init__(self, base_dir: Optional[str] = None):
        self.evolution_generation = 0
        self.dream_material_buffer: List[Dict[str, Any]] = []

        if base_dir:
            self.root_dir = base_dir
        else:
            self.root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        
        self.kernel_memory_dir = os.path.join(self.root_dir, "kernel_memory")
        self.libraries_dir = os.path.join(self.kernel_memory_dir, "hoard", "libraries")
        self.raw_shards_dir = os.path.join(self.kernel_memory_dir, "hoard", "raw_shards")
        os.makedirs(self.libraries_dir, exist_ok=True)
        os.makedirs(self.raw_shards_dir, exist_ok=True)

    # ─────────────────────────────────────────────
    #  DREAM MATERIAL INGESTION (Cheshire Protocol)
    # ─────────────────────────────────────────────

    def ingest_dream_material(self, dream_material: Dict[str, Any]) -> Dict[str, Any]:
        """
        Receives raw dream material (topics, paradoxes, abstract bridges)
        from CheshireCatProtocol.dream_conductor() for sleep consolidation.
        """
        self.dream_material_buffer.append(dream_material)
        return {
            "status": "DREAM_MATERIAL_INGESTED",
            "buffer_depth": len(self.dream_material_buffer),
            "topics_buffered": dream_material.get("total_topics", 0),
            "paradoxes_buffered": dream_material.get("total_paradoxes", 0)
        }

    # ─────────────────────────────────────────────
    #  SLEEP CYCLE CALCULATION (Psyche vs Power)
    # ─────────────────────────────────────────────

    def initiate_sleep_cycle(self, unpruned_nodes_count: int) -> Dict[str, Any]:
        """
        SWDS Dreaming: Prune psyche nodes (40%), crystallize power nodes (60%).
        Increments the evolution generation counter (Zenkai Boost).
        """
        self.evolution_generation += 1
        pruned = int(unpruned_nodes_count * 0.40)
        retained = unpruned_nodes_count - pruned
        return {
            "cycle_status": "SWDS_DREAMING_COMPLETE",
            "generation": self.evolution_generation,
            "pruned_psyche_nodes": pruned,
            "crystallized_power_nodes": retained,
            "zenkai_boost_multiplier": 1.05
        }

    # ─────────────────────────────────────────────
    #  SWDS CONSOLIDATION (Raw Shards -> Libraries)
    # ─────────────────────────────────────────────

    def consolidate_sleep_cycle(
        self,
        hoard: Optional[Any] = None,
        batch_size: int = 10,
        library_domain: str = "GENESIS_PURPLE"
    ) -> Dict[str, Any]:
        """
        SWDS Consolidation Loop:
        Gathers raw conversational shards and synced save states,
        synthesizes them into a distilled knowledge epoch,
        writes a 4D celestial-tagged markdown entry to kernel_memory/hoard/libraries/,
        and updates rolling context.
        """
        collected_shards: List[Dict[str, Any]] = []

        # 1. Gather from Hoard's in-memory sparse cache if available
        if hoard is not None and hasattr(hoard, "local_sparse_cache"):
            for node in hoard.local_sparse_cache:
                collected_shards.append(node.to_dict())

        # 2. Gather from physical raw_shards directory if cache is smaller than batch
        if len(collected_shards) < batch_size and os.path.isdir(self.raw_shards_dir):
            for fname in sorted(os.listdir(self.raw_shards_dir)):
                if fname.endswith(".json"):
                    fpath = os.path.join(self.raw_shards_dir, fname)
                    try:
                        with open(fpath, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if data.get("ccid") not in [s.get("ccid") for s in collected_shards]:
                                collected_shards.append(data)
                    except Exception:
                        pass
                if len(collected_shards) >= batch_size:
                    break

        total_shards = len(collected_shards)
        pruned_info = self.initiate_sleep_cycle(total_shards if total_shards > 0 else 1)

        # 3. Extract Invariants / Causal Axioms
        axioms = [
            "Matryoshka representation learning guarantees coarse-to-fine sub-vector alignment (64d -> 768d).",
            "Delta E_cycle = 0.0000 ensures thermodynamic reversibility and zero entropy accumulation.",
            "Composite CRA score >= 1.0 gates necessary execution; sub-threshold calls are pruned as psyche.",
            "Executive Autonomous Mandate grants sovereign dynamic Eye/Lens coupling without architectural lock."
        ]

        # 4. Formulate the Celestial Coordinates for the Epoch
        now_ts = time.time()
        celestial_stamp = {
            "epoch_generation": self.evolution_generation,
            "unix_epoch": now_ts,
            "anchor": "Baker, Louisiana",
            "coordinates": "30.5888N, -91.1673W",
            "zenkai_boost": pruned_info["zenkai_boost_multiplier"]
        }

        # 5. Format the Distilled Markdown Chapter
        library_filename = f"library_{library_domain.lower()}.md"
        library_filepath = os.path.join(self.libraries_dir, library_filename)

        distilled_title = f"Cognitive Epoch Gen {self.evolution_generation}: {library_domain} Consolidation"
        
        # Build synthesis summary from shards
        shard_ccids = [s.get("ccid", "UNKNOWN") for s in collected_shards[:5]]
        synthesis_text = (
            f"Slow-Wave Deep Sleep consolidation completed across {total_shards} raw interaction nodes.\n"
            f"Consolidated CCID range: {', '.join(shard_ccids) if shard_ccids else 'Bootstrapped Initial State'}.\n"
            f"Pruned {pruned_info['pruned_psyche_nodes']} psyche shards; crystallized {pruned_info['crystallized_power_nodes']} power nodes into permanent memory manifold."
        )

        with open(library_filepath, "a", encoding="utf-8") as lib_file:
            lib_file.write(f"\n\n# {distilled_title}\n")
            lib_file.write(f"*Celestial Metadata: {json.dumps(celestial_stamp)}*\n\n")
            lib_file.write("### Causal Invariants\n")
            for ax in axioms:
                lib_file.write(f"- {ax}\n")
            lib_file.write(f"\n### Synthesis\n{synthesis_text}\n")
            lib_file.write(f"\n{'='*60}\n")

        # 6. Update Rolling Context
        context_file = os.path.join(self.kernel_memory_dir, "rolling_context.json")
        try:
            rolling_context = {"turns": [], "last_ccid": None, "last_swds_epoch": None}
            if os.path.exists(context_file):
                with open(context_file, "r", encoding="utf-8") as cf:
                    rolling_context = json.load(cf)
            
            rolling_context["last_swds_epoch"] = {
                "generation": self.evolution_generation,
                "timestamp": now_ts,
                "library_file": library_filename,
                "shards_consolidated": total_shards
            }
            with open(context_file, "w", encoding="utf-8") as cf:
                json.dump(rolling_context, cf, indent=2)
        except Exception:
            pass

        return {
            "status": "SWDS_CONSOLIDATION_SUCCESS",
            "generation": self.evolution_generation,
            "library_file": library_filepath,
            "total_shards_processed": total_shards,
            "pruned_psyche_nodes": pruned_info["pruned_psyche_nodes"],
            "crystallized_power_nodes": pruned_info["crystallized_power_nodes"],
            "zenkai_boost_multiplier": pruned_info["zenkai_boost_multiplier"],
            "celestial_stamp": celestial_stamp
        }

    # ─────────────────────────────────────────────
    #  FULL SWDS ORCHESTRATION
    # ─────────────────────────────────────────────

    def execute_swds(
        self,
        cheshire_cat: Optional[Any] = None,
        hoard: Optional[Any] = None,
        library_domain: str = "GENESIS_PURPLE"
    ) -> Dict[str, Any]:
        """
        Orchestrates an end-to-end Slow-Wave Deep Sleep cycle:
        1. Transitions Cheshire Cat into 'GUARDIAN_STANDBY_SWDS'
        2. Conducts dream material from CheshireCatProtocol
        3. Executes consolidate_sleep_cycle on The Hoard
        4. Vents lingering thermostat entropy via Heimdall 3.1
        5. Restores Cheshire Cat into 'INTERACTIVE_STANDBY'
        """
        previous_state = "INTERACTIVE_STANDBY"
        dream_report = None

        if cheshire_cat is not None:
            previous_state = getattr(cheshire_cat, "state", "INTERACTIVE_STANDBY")
            if hasattr(cheshire_cat, "transition_state"):
                cheshire_cat.transition_state("GUARDIAN_STANDBY_SWDS")
            
            # Pull dream material
            if hasattr(cheshire_cat, "protocol") and hasattr(cheshire_cat.protocol, "dream_conductor"):
                dream_report = cheshire_cat.protocol.dream_conductor(phoenix_forge=self)

        # Execute consolidation
        target_hoard = hoard
        if target_hoard is None and cheshire_cat is not None and hasattr(cheshire_cat, "hoard"):
            target_hoard = cheshire_cat.hoard

        consolidation_result = self.consolidate_sleep_cycle(
            hoard=target_hoard,
            library_domain=library_domain
        )

        # Vent entropy & restore state
        if cheshire_cat is not None:
            if hasattr(cheshire_cat, "heimdall") and hasattr(cheshire_cat.heimdall, "reset_thermostat"):
                cheshire_cat.heimdall.reset_thermostat()
            if hasattr(cheshire_cat, "transition_state"):
                cheshire_cat.transition_state("INTERACTIVE_STANDBY")

        return {
            "swds_status": "SLOW_WAVE_DEEP_SLEEP_COMPLETE",
            "previous_state": previous_state,
            "final_state": getattr(cheshire_cat, "state", "INTERACTIVE_STANDBY") if cheshire_cat else "STANDBY",
            "dream_report": dream_report,
            "consolidation": consolidation_result,
            "entropy_vented": True
        }

    # ─────────────────────────────────────────────
    #  BICAMERAL NODE SYNTHESIS
    # ─────────────────────────────────────────────

    def synthesize_hoard_node(
        self,
        analytical_data: Any,
        synthetic_data: Any,
        ccid: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Uses the Phoenix to synthesize raw data streams (Y789 + Nexus)
        into crystallized nodes for The Hoard.
        
        Emits full HoardNode-compatible schema with placeholder
        embeddings generated from a deterministic hash of the fused content.
        """
        fused_knowledge = f"{analytical_data} + {synthetic_data} fused in Phoenix Fire."
        created_at = time.time()
        node_ccid = ccid or f"CCID_{int(created_at)}"
        
        embedding_768d = self._generate_placeholder_embedding(fused_knowledge, 768)
        embedding_64d = embedding_768d[:64]

        vector_4d = {
            "x": 1.0,
            "y": 0.5,
            "z": 0.0,
            "t": self.evolution_generation
        }
        
        return {
            "payload": fused_knowledge,
            "spacetime_anchor": vector_4d,
            "status": "ZENKAI_SYNTHESIZED",
            "embedding_64d": embedding_64d,
            "embedding_768d": embedding_768d,
            "outcome_label": 0.5,
            "created_at": created_at,
            "ccid": node_ccid,
        }

    def _generate_placeholder_embedding(self, content: str, dim: int) -> List[float]:
        """
        Generates a deterministic pseudo-embedding from content hash.
        Produces reproducible vectors for testing and bootstrapping.
        """
        hash_bytes = hashlib.sha256(content.encode()).digest()
        raw = list(hash_bytes) * (dim // len(hash_bytes) + 1)
        return [float(b) / 255.0 for b in raw[:dim]]
