"""
INTEGRA O/S: DAILY PLANET PROTOCOL LIFECYCLE & INTEGRATION TESTS
Module: tests/test_daily_planet_lifecycle.py
Layer: 5 (Analytical Toolkit & External Intelligence)

Tests:
    1. Pydantic Schemas: SourceProvenance, ContradictionVector, MetacognitiveBinding, DailyPlanetReport
    2. FirecrawlClient: multi-modal domain searches (news, academic, financial) and resilient sovereign fallback
    3. DailyPlanetProtocol 6-Stage Lifecycle execution
    4. MRL Embedding Generation (64d prefix slice of 768d space)
    5. TheHoard v2.0 Commit Verification
    6. Subsystem Integration: AlexandriaProtocol Loop 2, ShivaActionToolkit CRA Simplex, RogueXProtocol live_data
"""

import pytest
import asyncio
import time
import os
import sys

# Ensure integra-homebase is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from tools.daily_planet import (
    DailyPlanetProtocol,
    DailyPlanetReport,
    SourceProvenance,
    ContradictionVector,
    MetacognitiveBinding,
    FirecrawlClient,
)
from memory.alexandria_protocol import AlexandriaProtocol
from tools.shiva_toolkit import ShivaActionToolkit
from evolution.rogue_x import RogueXProtocol
from memory.the_hoard import TheHoard


# ─── 1. PYDANTIC SCHEMAS VERIFICATION ────────────────────────────────────────

def test_source_provenance_schema():
    prov = SourceProvenance(
        url="https://nature.com/articles/s41586-026-001",
        title="Emergent Non-Linearity in Dual-Engine Cognition",
        publishing_entity="Nature Portfolio",
        publication_date="2026-09-21",
        declared_funding="National Science Foundation",
        bias_vector={"political": 0.0, "commercial": 0.1, "epistemic_rigor": 0.98},
        credibility_score=0.96,
        extracted_entities=["Neural Dynamics", "Tensegrity", "Bicameral"]
    )
    assert prov.publishing_entity == "Nature Portfolio"
    assert prov.credibility_score == 0.96
    assert prov.bias_vector["epistemic_rigor"] == 0.98
    assert "Neural Dynamics" in prov.extracted_entities


def test_contradiction_vector_schema():
    cv = ContradictionVector(
        thesis="Monolithic dense LLMs are computationally optimal.",
        antithesis="Biological neuroanatomy requires sparse, bicameral transmodal hubs.",
        synthesis="Hybrid bicameral architecture balances deterministic execution with transmodal emergence.",
        semantic_tension=0.78,
        opposing_sources=["https://arxiv.org/abs/1", "https://arxiv.org/abs/2"],
        counter_arguments=["Autoregressive error compounding in monolithic stacks."]
    )
    assert cv.semantic_tension == 0.78
    assert len(cv.opposing_sources) == 2
    assert "Hybrid bicameral architecture" in cv.synthesis


def test_metacognitive_binding_schema():
    binding = MetacognitiveBinding(
        project_id="INTEGRA_V8_2",
        active_task="Daily Planet Intelligence Verification",
        conversation_goal="Lossless External Truth Ingestion",
        historical_precedents=["LeCun SAI Hypothesis", "Tolstoy Principle TPSL"],
        future_implications=["Proactive UGL Lookback avoidance"],
        ideological_alignment_score=0.95,
        metacognitive_reflection="Bound to active sovereign memory manifold."
    )
    assert binding.project_id == "INTEGRA_V8_2"
    assert binding.ideological_alignment_score == 0.95
    assert len(binding.historical_precedents) == 2


def test_daily_planet_report_schema():
    binding = MetacognitiveBinding(
        active_task="Audit",
        conversation_goal="Truth"
    )
    report = DailyPlanetReport(
        report_id="DP_TEST_001",
        query="Quantum Topological Order",
        domain_focus="academic",
        timestamp=time.time(),
        celestial_vector=[0.7071, -0.7071, 0.0, 500.0],
        summary="# Quantum Topological Order Brief",
        provenance_audit=[],
        dialectic_contradictions=[],
        metacognitive_bindings=binding,
        cra_simplex_score=1.1667
    )
    assert report.report_id == "DP_TEST_001"
    assert report.cra_simplex_score == 1.1667
    assert report.domain_focus == "academic"
    assert report.status == "COMPLETED"


# ─── 2. FIRECRAWL CLIENT & SOVEREIGN FALLBACK ────────────────────────────────

def test_firecrawl_client_fallback_news():
    client = FirecrawlClient(api_key="your_firecrawl_api_key")
    results = client.search("Federal Reserve interest rates", domain_focus="news", limit=2)
    assert len(results) >= 1
    assert "title" in results[0]
    assert "url" in results[0]
    assert "markdown" in results[0]


def test_firecrawl_client_fallback_academic():
    client = FirecrawlClient(force_fallback=True)
    results = client.search("Superhuman Adaptable Intelligence", domain_focus="academic", limit=2)
    assert len(results) >= 1
    assert results[0]["epistemic_rigor"] >= 0.90
    assert "arxiv.org" in results[0]["url"] or "journal" in results[0]["url"]


def test_firecrawl_client_fallback_financial():
    client = FirecrawlClient(force_fallback=True)
    results = client.search("Consumer Credit Loss Provisions", domain_focus="financial", limit=2)
    assert len(results) >= 1
    assert results[0]["commercial_bias"] >= 0.70
    assert "sec.gov" in results[0]["url"] or "macro-liquidity" in results[0]["url"]


def test_firecrawl_client_scrape_fallback():
    client = FirecrawlClient(force_fallback=True)
    res = client.scrape("https://example.com/test-article")
    assert "markdown" in res
    assert "Extracted Content" in res["markdown"]


# ─── 3. DAILY PLANET PROTOCOL 6-STAGE LIFECYCLE ──────────────────────────────

def test_daily_planet_6_stage_lifecycle_synchronous():
    hoard = TheHoard()
    dp = DailyPlanetProtocol(hoard=hoard)

    # Execute full brief
    report = dp.execute_daily_planet_brief(
        query="Subprime Consumer Credit Spreads and Liquidity",
        domain_focus="financial",
        task_context={"task_name": "Credit Plumbing Audit", "goal": "Systemic Risk Monitoring"},
        commit=True
    )

    # Stage 1 Verification (Ingestion)
    assert len(report.raw_content_samples) >= 1

    # Stage 2 Verification (Provenance & Bias Audit - Neji Eye / Chameleon)
    assert len(report.provenance_audit) >= 1
    for p in report.provenance_audit:
        assert p.credibility_score > 0.0
        assert "political" in p.bias_vector
        assert "commercial" in p.bias_vector
        assert "epistemic_rigor" in p.bias_vector

    # Stage 3 Verification (Dialectic Opposition - Shikamaru Eye / Spider + Snake)
    assert len(report.dialectic_contradictions) >= 1
    cv = report.dialectic_contradictions[0]
    assert cv.semantic_tension >= 0.2
    assert len(cv.thesis) > 0
    assert len(cv.antithesis) > 0
    assert len(cv.synthesis) > 0

    # Stage 4 Verification (Metacognitive Binding - Itachi Eye / Dragon Engine)
    assert report.metacognitive_bindings.active_task == "Credit Plumbing Audit"
    assert report.metacognitive_bindings.ideological_alignment_score >= 0.90
    assert len(report.metacognitive_bindings.historical_precedents) >= 1

    # Stage 5 Verification (Lossless MTCW Synthesis Brief)
    assert "DAILY PLANET INTELLIGENCE REPORT" in report.summary
    assert report.cra_simplex_score == 1.1667

    # Stage 6 Verification (Hoard Commitment)
    assert report.hoard_ccid is not None
    assert report.hoard_ccid.startswith("CCID_DAILY_PLANET_")


@pytest.mark.asyncio
async def test_daily_planet_async_execution():
    dp = DailyPlanetProtocol()
    report = await dp.execute_daily_planet_brief_async(
        query="Neurobiological Connectomics in Dual LLMs",
        domain_focus="academic",
        commit=False
    )
    assert isinstance(report, DailyPlanetReport)
    assert report.domain_focus == "academic"
    assert report.cra_simplex_score == 1.1667


# ─── 4. MRL EMBEDDING SUB-VECTOR COMPACTION ──────────────────────────────────

def test_mrl_embedding_subset_preservation():
    dp = DailyPlanetProtocol()
    coarse_64d, fine_768d = dp._generate_mrl_embeddings("Test MRL Embedding String")
    
    assert len(coarse_64d) == 64
    assert len(fine_768d) == 768

    # Coarse vector should be normalized
    norm_64 = sum(x*x for x in coarse_64d)
    assert abs(norm_64 - 1.0) < 1e-4

    # Fine vector should be normalized
    norm_768 = sum(x*x for x in fine_768d)
    assert abs(norm_768 - 1.0) < 1e-4


# ─── 5. SUBSYSTEM INTEGRATION TESTS ──────────────────────────────────────────

def test_alexandria_protocol_loop_2_wires_daily_planet():
    alexandria = AlexandriaProtocol()
    res = alexandria.execute_loop_2_learning(query="Global Supply Chain Realignment")
    
    assert res["status"] == "ALEXANDRIA_LEARNING_COMPLETE"
    assert res["report_generated"] is True
    assert "new_node_id" in res
    assert res["new_node_id"].startswith("CCID_DAILY_PLANET_") or res["new_node_id"].startswith("DP_")
    assert "daily_planet_report" in res


def test_shiva_toolkit_executes_daily_planet():
    toolkit = ShivaActionToolkit()
    # Check CRA simplex evaluation
    cra = toolkit.evaluate_cra_simplex("daily_planet")
    assert cra["wisdom_yield"] == 0.70
    assert cra["cognitive_cost"] == 0.60
    assert cra["simplex_score"] == 1.1667
    assert cra["approved"] is True

    # Check execution method
    res = toolkit.execute_daily_planet(query="Autonomous Economic Agents", domain_focus="news", commit=False)
    assert res["status"] == "DAILY_PLANET_COMPLETE"
    assert res["cra_simplex_score"] == 1.1667
    assert res["provenance_count"] >= 1


@pytest.mark.asyncio
async def test_rogue_x_live_data_accepts_daily_planet_report():
    dp = DailyPlanetProtocol()
    report = dp.execute_daily_planet_brief(query="High Frequency Market Volatility", domain_focus="financial", commit=False)
    
    rogue = RogueXProtocol(shiva_action=None)
    touch_result = await rogue._phase_touch(target_data=report, target_type="live_data")
    
    assert touch_result["target_type"] == "live_data"
    assert touch_result["lenses"] == ["Eagle", "Spider", "Hawk"]
    assert touch_result["passes"] == 2
    # Verify content was extracted from report.summary
    assert "DAILY PLANET INTELLIGENCE REPORT" in touch_result["results"]["neji"]["raw"]
