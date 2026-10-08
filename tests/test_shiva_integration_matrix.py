import pytest
import asyncio
from evolution.shiva_action.neji_eye import NejiEye
from evolution.shiva_action.shikamaru_eye import ShikamaruEye
from evolution.shiva_action.itachi_eye import ItachiEye
from evolution.shiva_action.lenses import LensLibrary
from evolution.shiva_action.orchestrator import ShivaActionSuite

@pytest.fixture
def mock_data():
    return """
def process_cognitive_cycle(self):
    assert self.state is not None
    if self.h_smooth > self.threshold:
        raise ValueError("Entropy breach")
    # TODO: fix
    return self.state
"""

@pytest.fixture
def lib():
    return LensLibrary()

@pytest.fixture
def all_lenses(lib):
    return lib.list_available()

@pytest.fixture
def new_lenses():
    return ["Byakugan", "ShadowJutsu", "Sharingan", "CelestialSpacetime"]


@pytest.mark.asyncio
async def test_eye_new_lens_coupling(mock_data, lib, new_lenses):
    """Test 1: Eye + New Lens coupling (running the 4 new lenses through each Eye)"""
    neji = NejiEye()
    shikamaru = ShikamaruEye()
    itachi = ItachiEye()
    
    lenses = lib.get_lenses(new_lenses)
    
    # Neji Pass
    k = await neji.analyze_data(mock_data, lenses)
    assert k["eye"] == "NEJI"
    assert "facts" in k
    assert set(k["lenses_applied"]) == set(new_lenses)
    
    # Shikamaru Pass
    u = await shikamaru.analyze_data(mock_data, k, lenses)
    assert u["eye"] == "SHIKAMARU"
    assert "synthesis" in u
    
    # Itachi Pass
    w = await itachi.analyze_data(u, lenses)
    assert w["eye"] == "ITACHI"
    assert "tpsl_evaluation" in w
    assert "lens_insights" in w


@pytest.mark.asyncio
async def test_eye_full_library_coupling(mock_data, lib, all_lenses):
    """Test 2: Eye + Full Library coupling (running ALL 10 lenses through Neji Eye)"""
    neji = NejiEye()
    lenses = lib.get_lenses(all_lenses)
    
    k = await neji.analyze_data(mock_data, lenses)
    assert k["lens_count"] == 10
    assert set(k["lenses_applied"]) == set(all_lenses)
    for lens_name in all_lenses:
        assert lens_name in k["facts"]


@pytest.mark.asyncio
async def test_orchestrator_pipeline_new_lenses(mock_data, new_lenses):
    """Test 3: Orchestrator pipeline with new lenses only"""
    suite = ShivaActionSuite()
    report = await suite.execute(mock_data, new_lenses, passes=3)
    
    assert report["passes_executed"] == 3
    assert set(report["lenses_active"]) == set(new_lenses)
    assert "neji" in report["results"]
    assert "shikamaru" in report["results"]
    assert "itachi" in report["results"]
    
    # Check that Sharingan specifically generated its drift risk in Neji pass
    neji_facts = report["results"]["neji"]["facts"]
    assert "Sharingan" in neji_facts
    assert "drift_risk" in neji_facts["Sharingan"]


@pytest.mark.asyncio
async def test_orchestrator_pipeline_full_library(mock_data, all_lenses):
    """Test 4: Orchestrator pipeline with full library (all 10 lenses)"""
    suite = ShivaActionSuite()
    report = await suite.execute(mock_data, all_lenses, passes=3)
    
    assert report["passes_executed"] == 3
    assert len(report["lenses_active"]) == 10
    assert "composite_cra" in report
    
    # The composite CRA should be calculated for all 10 lenses
    assert report["composite_cra"]["composite_cra_score"] > 0


def test_composite_cra_calculations(lib, new_lenses, all_lenses):
    """Test 5 & 6: Composite CRA with new lenses vs full library"""
    # 4 new lenses
    neji_cra_new = lib.compute_composite_cra(NejiEye.W_Y, NejiEye.C_C, new_lenses)
    
    # All 10 lenses
    neji_cra_all = lib.compute_composite_cra(NejiEye.W_Y, NejiEye.C_C, all_lenses)
    
    assert neji_cra_new["composite_cra_score"] > 0.0
    assert neji_cra_all["composite_cra_score"] > 0.0
    # 10 lenses vs 4 lenses will have different ratios based on average efficiency
    assert neji_cra_all["composite_cra_score"] > 0.0


def test_celestial_spacetime_lens_kernel_context(lib):
    """Test 7: CelestialSpacetimeLens with real Clock Context"""
    lens = lib.get_lens("CelestialSpacetime")
    result = lens.apply("dummy_data")
    
    # The lens should verify sync isolation when the clock is available
    assert result["sync_isolation_verified"] is True
    assert "celestial_timestamp" in result
    assert result["celestial_timestamp"] is not None
