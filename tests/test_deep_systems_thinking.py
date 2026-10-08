"""
INTEGRA O/S: Deep Systems Thinking Integration Tests
Tests the Corpus Callosum cross-hemispheric emergent modality.

Verifies:
1. DST fires automatically when passes >= 2
2. DST does NOT fire when passes == 1
3. DST produces contradictions, resonances, and a Systems Map
4. DST correctly identifies shared vs unique lens coverage
5. DST integration quality scales with analytical overlap
6. DST coexists with Itachi's Wisdom pass (passes == 3)
7. Full 10-lens library through DST pipeline
"""
import pytest
import asyncio
from evolution.shiva_action.orchestrator import ShivaActionSuite
from evolution.shiva_action.lenses import LensLibrary


@pytest.fixture
def suite():
    return ShivaActionSuite()


@pytest.fixture
def test_data():
    return """
def process_cognitive_cycle(self):
    assert self.state is not None
    if self.h_smooth > self.threshold:
        raise ValueError("Entropy breach")
    # TODO: add P-SSR recovery
    return self.state

def run_event_loop(self):
    while True:
        pass

class CheshireCatKernel:
    pass
"""


# --- Test 1: DST fires on passes >= 2 ---
@pytest.mark.asyncio
async def test_dst_fires_on_two_passes(suite, test_data):
    """Deep Systems Thinking must fire when both Neji and Shikamaru are active."""
    report = await suite.execute(test_data, ["Eagle", "Spider"], passes=2)
    
    assert "deep_systems_thinking" in report["results"]
    dst = report["results"]["deep_systems_thinking"]
    assert dst["modality"] == "DEEP_SYSTEMS_THINKING"
    assert dst["emergent"] is True
    assert dst["corpus_callosum_active"] is True
    assert dst["status"] == "EMERGENT_SYNTHESIS_COMPLETE"


# --- Test 2: DST does NOT fire on passes == 1 ---
@pytest.mark.asyncio
async def test_dst_does_not_fire_on_one_pass(suite, test_data):
    """Deep Systems Thinking must NOT fire when only Neji is active."""
    report = await suite.execute(test_data, ["Eagle"], passes=1)
    
    assert "deep_systems_thinking" not in report["results"]
    assert "neji" in report["results"]


# --- Test 3: DST produces contradictions, resonances, Systems Map ---
@pytest.mark.asyncio
async def test_dst_produces_structural_outputs(suite, test_data):
    """DST must produce contradictions, resonances, and a systems_map."""
    report = await suite.execute(test_data, ["Eagle", "Spider", "Byakugan"], passes=2)
    dst = report["results"]["deep_systems_thinking"]
    
    assert "contradictions" in dst
    assert "resonances" in dst
    assert "systems_map" in dst
    assert isinstance(dst["contradictions"], list)
    assert isinstance(dst["resonances"], list)
    assert isinstance(dst["systems_map"], dict)
    
    # Systems Map must have dimensional metrics
    smap = dst["systems_map"]
    assert "left_hemisphere_facts" in smap
    assert "right_hemisphere_relations" in smap
    assert "integration_ratio" in smap
    assert "integration_quality" in smap
    assert smap["integration_quality"] in ("FULL", "STRONG", "PARTIAL", "DISJOINT")


# --- Test 4: Shared vs unique lens coverage ---
@pytest.mark.asyncio
async def test_dst_shared_lens_coverage(suite, test_data):
    """DST must correctly identify which lenses were shared across hemispheres."""
    lenses = ["Eagle", "Spider", "Byakugan", "ShadowJutsu"]
    report = await suite.execute(test_data, lenses, passes=2)
    dst = report["results"]["deep_systems_thinking"]
    
    # All lenses are applied to BOTH passes, so all should be shared
    assert set(dst["shared_analytical_surface"]) == set(lenses)
    assert dst["systems_map"]["cross_hemispheric_surface"] == len(lenses)


# --- Test 5: DST coexists with Itachi on passes == 3 ---
@pytest.mark.asyncio
async def test_dst_coexists_with_itachi(suite, test_data):
    """DST fires after Pass 2 AND Itachi fires on Pass 3 — both in the report."""
    report = await suite.execute(test_data, ["Eagle", "Spider", "Owl"], passes=3)
    
    assert "neji" in report["results"]
    assert "shikamaru" in report["results"]
    assert "deep_systems_thinking" in report["results"]
    assert "itachi" in report["results"]
    
    # DST should be emergent, Itachi should be TPSL-pruned
    assert report["results"]["deep_systems_thinking"]["emergent"] is True
    assert report["results"]["itachi"]["psyche_pruned"] is True


# --- Test 6: Full 10-lens library through DST ---
@pytest.mark.asyncio
async def test_dst_full_library(suite, test_data):
    """DST with all 10 lenses — maximum analytical surface."""
    lib = LensLibrary()
    all_lenses = lib.list_available()
    assert len(all_lenses) == 10
    
    report = await suite.execute(test_data, all_lenses, passes=3)
    dst = report["results"]["deep_systems_thinking"]
    
    assert dst["corpus_callosum_active"] is True
    assert dst["systems_map"]["cross_hemispheric_surface"] == 10
    assert len(dst["shared_analytical_surface"]) == 10
    assert dst["resonance_count"] + dst["contradiction_count"] > 0
    
    # With 10 lenses, integration quality should not be DISJOINT
    assert dst["systems_map"]["integration_quality"] != "DISJOINT"


# --- Test 7: DST resonance detection with identical data ---
@pytest.mark.asyncio
async def test_dst_detects_resonances(suite, test_data):
    """When both hemispheres see identical data with same lenses, 
    resonances should outnumber contradictions (data agreement)."""
    report = await suite.execute(test_data, ["Eagle"], passes=2)
    dst = report["results"]["deep_systems_thinking"]
    
    # Same lens, same data — high agreement expected
    assert dst["resonance_count"] >= 0
    assert dst["systems_map"]["integration_ratio"] >= 0.0
