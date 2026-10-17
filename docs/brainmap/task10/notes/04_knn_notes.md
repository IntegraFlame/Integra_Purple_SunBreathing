# 04 — `BluprintArchitecture/K NN algorithm Modifications.md`

**Read:** 2026-10-16, the whole file (1,736 lines, 6,447 words). It is a chain of assistant answers (Gemini-style, citing "MASTERv8.2 … p. N") that redesign Rodin Route Retrieval around k-nearest neighbours, then extend the change to the Hoard schema, Phoenix's SWDS duties, Zenitsu 3.0 and Alexandria.

## What it says (isolated read)
- **Rodin's 3-phase pre-action review:** (1) activation: Y789 extracts keywords, the Hoard activates a subgraph by CCID; (2) quantification: M_route = 2E ⁄ (V(V−1)) (density of the activated subgraph), M_sem = cosine(prompt, centroid of the cluster), M_stale = (now − node time > T_stale); (3) decision tree: low cohesion → `Nexus.RequestClarification()`; stale or weak → Alexandria "VERIFY" (loop 2); pass "Gate III" (≥ 0.95) → commit to the Hoard and act.
- **MRL coarse-to-fine search:** filter on the first 64 dimensions (top ~50 candidates), re-rank on the full 768; files > 5 MB stay as `gcs_uri` pointers.
- **The KNN change:** replace the centroid test with a vote of the K (5 or 7) nearest past nodes, each labelled success or failure. Three different formulas are given for the same M_knn:
  1. (1⁄K) Σ (1 − d_i)·I(success_i), threshold 0.95;
  2. (1⁄K) Σ I(success_i)·exp(−d_i²⁄σ²), threshold 0.85;
  3. Σ I(success_i)·w_i ⁄ Σ w_i with w_i = exp(−d_i²⁄σ²), σ = 0.5 (the Python version), threshold 0.85.
- **Hoard schema (pgvector):** `embedding_64d`, `embedding_768d`, `outcome_label` (default 0.5), `importance_score`, `is_stale`, `created_at`, `last_accessed`, `causal_parent_id`; an ivfflat index on the 64-d column.
- **Phoenix in SWDS gets five duties:** LABEL (set outcome labels from the user's words: "proceed/correct" = 1, "stop/wrong/clarify/verify" = 0; veto after 3 negatives); MODIFY (refresh stale nodes through Alexandria, keep `node_id`); TRACK (Lamport/vector-clock lineage, 5 levels); ORGANIZE (HDBSCAN clustering, merge clusters < 5 nodes, prune orphans); BLUEPRINT (promote a node used ≥ 50 times at 100 % success into the Dragon prompt).
- **Zenitsu 3.0 as a system loop:** Neji = 64-d feature extraction; Shikamaru = KNN neighbourhood + M_knn; Itachi = Gate III judge; 13th Form = output plus Phoenix tags (context id, parent id, vector clock). Ω gains a sigmoid of M_knn and a "previous night's" Phoenix term.
- **Alexandria "Amaterasu":** on a failed gate, search the web, write a report, insert it into the Hoard **with `outcome_label = 1.0`**, and re-run, expecting M_knn = 1.0 "because this exact node is now the nearest neighbour".

## Problems found in this read
- **Three incompatible M_knn formulas** under one name; only formula 3 is a bounded weighted vote that can reach a high threshold honestly. Formula 1 can reach 0.95 only if all neighbours are near-duplicates.
- **Self-confirming loop:** Amaterasu writes its own evidence at full trust and then votes with it. The gate becomes a rubber stamp.
- **Unbounded recursion:** `ZenitsuSystem.run_system_loop` calls itself after Amaterasu with no depth limit, and Amaterasu's `depth` is never incremented.
- **"O(1)" nearest-neighbour search** is not O(1) (ivfflat is sub-linear, approximate).
- **Label noise:** outcome labels inferred from words like "verify" or "thank you" are weak; "verify" as a failure signal punishes caution.
- **Deletion in SWDS** ("auto_prune_orphans") conflicts with the To-Do's gates (Chroma deletion needs approval; R1 keeps cold nodes).
- **One staleness horizon (7 days) for everything** ignores the kind of node.

## Links to the earlier documents (compounding)
- **Tufte / Anscombe:** the centroid test (M_sem) is a summary statistic; Anscombe's quartet shows identical summaries over different data. The KNN vote "looks at the data" instead — the right direction.
- **Buzsáki:** semantic nodes are invariant to time and place, episodic ones are not, so staleness should depend on the node's kind (episode vs semantic junction), not one global T_stale.
- **Tufte's galaxy map / apophenia:** a node the system wrote about itself is not independent evidence; external or held-out confirmation is required before it counts in a vote.
- **Purple3's matrix clock:** the safe-pruning test it proposed is exactly what "prune orphans" lacks; nothing is deleted without proof that every reader has absorbed it, plus the Architect's approval.
