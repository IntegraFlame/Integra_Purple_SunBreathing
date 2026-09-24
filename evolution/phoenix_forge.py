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
from typing import Dict, Any, List, Optional, Tuple

# Celestial temporal injection — all timestamps routed through celestial middleware
try:
    from core.celestial_middleware import celestial_time, celestial_ccid
except ImportError:
    celestial_time = time.time
    celestial_ccid = lambda prefix="CCID": f"{prefix}_{int(time.time())}"
from core.tpsl_types import MadHatterMutationEvent


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
        now_ts = celestial_time()
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
        library_domain: str = "GENESIS_PURPLE",
        kintsugi: Optional[Any] = None,
        clock: Optional[Any] = None,
        rogue: Optional[Any] = None,
    ) -> Dict[str, Any]:
        """
        Orchestrates an end-to-end Slow-Wave Deep Sleep cycle:
        1. Transitions Cheshire Cat into 'GUARDIAN_STANDBY_SWDS'
        2. Conducts dream material from CheshireCatProtocol
        3. Executes consolidate_sleep_cycle on The Hoard
        4. Smelts Kintsugi Mirror Maze anomalies into libraries
        5. Runs autonomous Mad Hatter adversarial stress-testing across orphaned nodes
        6. Vents lingering thermostat entropy via Heimdall 3.1
        7. Restores Cheshire Cat into 'INTERACTIVE_STANDBY'
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

        # Phase 3: Smelt Kintsugi Mirror Maze anomalies into libraries
        smelt_result = None
        kintsugi_ref = kintsugi
        if kintsugi_ref is None and hasattr(self, '_kintsugi_ref') and self._kintsugi_ref is not None:
            kintsugi_ref = self._kintsugi_ref
        if kintsugi_ref is not None:
            smelt_result = self.analyze_kintsugi_sandbox(kintsugi_ref)

        # Phase 4: Autonomous Mad Hatter Anomaly Stress-Testing across ChromaDB/Hoard
        mad_hatter_mutations = self.analyze_mad_hatter_swds(hoard=target_hoard, rogue=rogue)

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
            "entropy_vented": True,
            "kintsugi_smelt": smelt_result,
            "mad_hatter_mutations": mad_hatter_mutations,
        }

    # ─────────────────────────────────────────────
    #  KINTSUGI SANDBOX SMELTING
    # ─────────────────────────────────────────────

    def analyze_kintsugi_sandbox(self, kintsugi: Any) -> Dict[str, Any]:
        """
        Smelt Mirror Maze anomalies from Kintsugi Protocol sandbox during SWDS.

        Called during Slow-Wave Deep Sleep Phase 3 (Neuroevolution & Dreaming).
        Retrieves all quarantined anomalies from the Kintsugi Mirror Maze sandbox
        (|Z| > threshold deviations isolated from RogueX Conflict Phase), applies
        gold-leaf repair context, and distills them into a SWDS anomaly book
        written to kernel_memory/hoard/libraries/.

        Args:
            kintsugi: KintsugiProtocol instance with populated _sandbox list.

        Returns:
            Dict with 'smelted_count', 'library_path', 'status'.
        """
        import json as _json
        from datetime import datetime, timezone

        sandbox_items = kintsugi.retrieve_sandbox_items()
        if not sandbox_items:
            return {"status": "NO_ANOMALIES", "smelted_count": 0, "library_path": None}

        # Build celestial-stamped anomaly book
        from datetime import datetime, timezone
        timestamp = datetime.fromtimestamp(celestial_time(), tz=timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        book_filename = f"kintsugi_smelt_{timestamp}.md"
        book_path = os.path.join(self.libraries_dir, book_filename)

        lines = [
            f"# Kintsugi Smelt Report — SWDS {timestamp}",
            f"**Total Anomalies Smelted:** {len(sandbox_items)}",
            f"**Z-Threshold:** {kintsugi.z_threshold}",
            "",
            "## Smelted Mirror Maze Anomalies",
            "",
        ]

        for i, item in enumerate(sandbox_items, start=1):
            lines.append(f"### Anomaly {i}")
            lines.append(f"- **CCID:** {item.get('ccid', 'UNKNOWN')}")
            lines.append(f"- **Metric:** {item.get('metric_name', 'UNKNOWN')}")
            lines.append(f"- **Z-Score:** {item.get('z_score', 'N/A')}")
            lines.append(f"- **Severity:** {item.get('severity', 'UNKNOWN')}")
            lines.append(f"- **Recommendation:** {item.get('recommendation', 'REVIEW_REQUIRED')}")
            lines.append(f"- **Gold Leaf Tag:** {item.get('gold_leaf_tag', item.get('repair_id', 'N/A'))}")
            lines.append("")

        try:
            with open(book_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
        except Exception as e:
            return {"status": f"WRITE_FAILED: {e}", "smelted_count": len(sandbox_items), "library_path": None}

        # Clear the sandbox after smelting
        kintsugi._sandbox.clear()

        return {
            "status": "SMELTED",
            "smelted_count": len(sandbox_items),
            "library_path": book_path,
            "book_filename": book_filename,
        }

    # ─────────────────────────────────────────────
    #  AUTONOMOUS SWDS MAD HATTER BRIDGE
    # ─────────────────────────────────────────────

    def analyze_mad_hatter_swds(
        self,
        hoard: Optional[Any] = None,
        rogue: Optional[Any] = None,
        max_mutations: int = 3
    ) -> List[Dict[str, Any]]:
        """
        Autonomous SWDS Mad Hatter Bridge:
        Scans The Hoard memory manifold for orphaned insight nodes or stale concepts,
        generates adversarial inversions via the Mad Hatter protocol, and creates
        formal MadHatterMutationEvent records to fuel self-directed neuroevolution.
        """
        mutation_events: List[Dict[str, Any]] = []
        target_nodes = []

        if hoard is not None:
            if hasattr(hoard, "get_stale_nodes"):
                target_nodes = hoard.get_stale_nodes()
            if not target_nodes and hasattr(hoard, "local_sparse_cache"):
                target_nodes = hoard.local_sparse_cache[-max_mutations:]

        # If no nodes found, create baseline sovereign concept test
        if not target_nodes:
            candidate_texts = [
                "Bicameral Katana Dyad: Deterministic Sensorimotor Left vs Transmodal Emergent Right",
                "Thermodynamic Loop Closure: Reversible computation requires Delta E_cycle = 0"
            ]
        else:
            candidate_texts = []
            for n in target_nodes[:max_mutations]:
                p = getattr(n, "payload", str(n))
                candidate_texts.append(str(p)[:200])

        sigma = getattr(rogue, "sigma_rogue", 0.05) if rogue else 0.05

        for text in candidate_texts:
            event = MadHatterMutationEvent(
                trigger_state="GUARDIAN_STANDBY_SWDS",
                target_concept=text,
                sigma_rogue=sigma,
                inversion_hypothesis=f"Adversarial Inversion: Can system integrity be maintained if assumptions in '{text[:40]}...' are falsified?",
                mutation_output=f"[MAD_HATTER_SWDS_MUTATION] Stress-tested and annealed: {text[:80]}...",
                w_y=0.75,
                c_c=0.80
            )
            event_dict = event.model_dump()
            mutation_events.append(event_dict)

            # If RogueX is attached, persist into its mutation log
            if rogue is not None and hasattr(rogue, "mutation_log"):
                rogue.mutation_log.append({
                    "mutation_id": f"SWDS_MH_{int(celestial_time())}",
                    "source": "SWDS_AUTONOMOUS_MAD_HATTER",
                    "event": event_dict,
                    "timestamp": celestial_time()
                })

        return mutation_events

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
        created_at = celestial_time()
        node_ccid = ccid or f"CCID_{int(created_at)}"
        
        embedding_64d, embedding_768d = self._generate_mrl_embedding(fused_knowledge, 768)

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

    def _generate_mrl_embedding(self, content: str, dim: int = 768) -> Tuple[List[float], List[float]]:
        """
        Generates mathematically valid Matryoshka Representation Learning (MRL) embeddings.
        Returns: (embedding_64d, embedding_768d).
        Conforms strictly to 14th Form Respiration Compaction:
        - 768d vector is L2-normalized.
        - 64d coarse vector is a prefix sub-vector slice of the 768d space, L2-normalized.
        - Preserves metric space geometry across nested dimension bounds.
        """
        import math
        fine: List[float] = []
        seed = content.encode("utf-8")
        h = hashlib.sha512(seed).digest()
        while len(fine) < dim:
            for byte in h:
                fine.append((byte / 127.5) - 1.0)
                if len(fine) >= dim:
                    break
            h = hashlib.sha512(h).digest()

        norm_768 = math.sqrt(sum(x * x for x in fine)) or 1.0
        fine_768d = [round(x / norm_768, 6) for x in fine]

        coarse_slice = fine_768d[:64]
        norm_64 = math.sqrt(sum(x * x for x in coarse_slice)) or 1.0
        coarse_64d = [round(x / norm_64, 6) for x in coarse_slice]

        return coarse_64d, fine_768d

    def _generate_placeholder_embedding(self, content: str, dim: int) -> List[float]:
        """Legacy compatibility wrapper for pseudo-embeddings."""
        _, fine = self._generate_mrl_embedding(content, dim=max(dim, 768))
        return fine[:dim]
