"""
INTEGRA O/S: DAILY PLANET STAGE 6 WRITES NO INVENTED VECTOR (offline)

Measured 2026-10-15: 41 of the 307 live shards carried a unit-length pseudo-vector; 40 of the 307 are Daily Planet
reports, and this stage builds its vectors from SHA-512. It looked like an embedding and meant nothing. Stage 6 now
commits the report without a vector and marks it PENDING.
"""

import json
from types import SimpleNamespace

from memory.the_hoard import TheHoard
from tools.daily_planet import DailyPlanetProtocol


def test_stage_6_commits_the_report_without_a_vector_and_marks_it_pending(tmp_path):
    hoard = TheHoard(base_dir=str(tmp_path))
    dp = DailyPlanetProtocol(hoard=hoard, shiva_suite=SimpleNamespace(), firecrawl_client=SimpleNamespace())
    report = SimpleNamespace(
        report_id="R1", query="q", domain_focus="general", timestamp=1.0, celestial_vector=[0.1, 0.2, 0.3, 4.0],
        summary="a short research summary", provenance_audit=[], dialectic_contradictions=[],
        cra_simplex_score=1.1667, hoard_ccid=None)

    ccid = dp.stage_6_commit_to_hoard(report)

    assert ccid == "CCID_DAILY_PLANET_R1" and report.hoard_ccid == ccid
    node = hoard.local_sparse_cache[-1]
    assert node.embed_space is None and not any(node.embedding_768d) and not any(node.embedding_64d)
    assert node.metadata["embedding_status"] == "PENDING"
    with open(hoard._shard_path(ccid), encoding="utf-8") as fh:
        shard = json.load(fh)
    assert not any(shard["embedding_768d"]) and shard["embed_space"] is None
    assert hoard.count() == 0
    assert hoard.get_telemetry()["unembedded_nodes"] == 1 and hoard.get_telemetry()["untrusted_vector_nodes"] == 0
