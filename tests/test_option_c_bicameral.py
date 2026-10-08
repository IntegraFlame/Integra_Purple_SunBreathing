"""
INTEGRA O/S: Option C Bicameral Architecture Tests
Tests that the hemispheres receive genuinely different inputs and lenses.

Verifies:
1. Per-eye routing gives each Eye different lenses when using defaults
2. Shikamaru analyzes K (structured dict), not raw data
3. DST finds real contradictions when hemispheres see different data
4. Full pipeline with 0930 defaults produces differentiated outputs
"""
import pytest
from evolution.shiva_action.orchestrator import ShivaActionSuite, DEFAULT_EYE_LENS_BINDINGS
from evolution.shiva_action.lenses import LensLibrary


@pytest.fixture
def suite():
    return ShivaActionSuite()


@pytest.fixture
def test_code():
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


# --- Test 1: Per-eye defaults give DIFFERENT lenses ---
@pytest.mark.asyncio
async def test_per_eye_routing_activates_on_defaults(suite, test_code):
    """When no lens_names provided, each Eye gets its 0930 canonical lenses."""
    report = await suite.execute(test_code, passes=3)
    
    assert report["per_eye_routing"] is True
    assert report["lens_bindings"] is not None
    assert report["lens_bindings"]["neji"] == ["Eagle", "Chameleon", "Byakugan"]
    assert report["lens_bindings"]["shikamaru"] == ["Spider", "Snake", "ShadowJutsu"]
    assert report["lens_bindings"]["itachi"] == ["Owl", "Sharingan", "CelestialSpacetime"]


# --- Test 2: Neji and Shikamaru apply DIFFERENT lenses ---
@pytest.mark.asyncio
async def test_neji_and_shikamaru_have_different_lenses(suite, test_code):
    """With 0930 defaults, Neji and Shikamaru must have zero lens overlap."""
    report = await suite.execute(test_code, passes=2)
    
    neji_lenses = set(report["results"]["neji"]["lenses_applied"])
    shikamaru_lenses = set(report["results"]["shikamaru"]["lenses_applied"])
    
    # Zero overlap — each hemisphere has its own tools
    assert neji_lenses & shikamaru_lenses == set()
    assert neji_lenses == {"Eagle", "Chameleon", "Byakugan"}
    assert shikamaru_lenses == {"Spider", "Snake", "ShadowJutsu"}


# --- Test 3: Shikamaru processes K (dict), not raw data (string) ---
@pytest.mark.asyncio
async def test_shikamaru_analyzes_structured_knowledge(suite, test_code):
    """Shikamaru's lenses must receive K (a dict), producing dict-analysis outputs."""
    report = await suite.execute(test_code, passes=2)
    
    shikamaru_synthesis = report["results"]["shikamaru"]["synthesis"]
    
    # Spider lens on a dict produces "key_connections" (not "import_dependencies")
    spider_output = shikamaru_synthesis.get("Spider", {})
    assert "key_connections" in spider_output or "connection_count" in spider_output
    # Import dependencies would only appear if Spider analyzed raw string data
    assert "import_dependencies" not in spider_output
    
    # Snake lens on a dict produces "tracked_flows" (not "flow_control_lines")
    snake_output = shikamaru_synthesis.get("Snake", {})
    assert "tracked_flows" in snake_output or "circulation_status" in snake_output
    assert "flow_control_lines" not in snake_output


# --- Test 4: DST detects genuine contradictions with per-eye routing ---
@pytest.mark.asyncio
async def test_dst_with_per_eye_routing(suite, test_code):
    """With 0930 defaults, DST should find DISJOINT analytical surfaces
    (no shared lenses) and report COMPLEMENTARY coverage."""
    report = await suite.execute(test_code, passes=2)
    dst = report["results"]["deep_systems_thinking"]
    
    # No shared lenses between hemispheres
    assert len(dst["shared_analytical_surface"]) == 0
    
    # Each hemisphere contributes unique coverage
    assert set(dst["neji_unique_coverage"]) == {"Eagle", "Chameleon", "Byakugan"}
    assert set(dst["shikamaru_unique_coverage"]) == {"Spider", "Snake", "ShadowJutsu"}
    
    # Systems map reflects disjoint topology
    assert dst["systems_map"]["integration_quality"] == "DISJOINT"
    assert dst["systems_map"]["cross_hemispheric_surface"] == 0


# --- Test 5: Explicit lens_names override per-eye routing ---
@pytest.mark.asyncio
async def test_explicit_lenses_disable_per_eye_routing(suite, test_code):
    """When explicit lens_names are provided, all Eyes share the same set."""
    report = await suite.execute(test_code, ["Eagle", "Spider"], passes=2)
    
    assert report["per_eye_routing"] is False
    assert report["lens_bindings"] is None
    
    neji_lenses = set(report["results"]["neji"]["lenses_applied"])
    shikamaru_lenses = set(report["results"]["shikamaru"]["lenses_applied"])
    
    # Both eyes get the same explicit set
    assert neji_lenses == {"Eagle", "Spider"}
    assert shikamaru_lenses == {"Eagle", "Spider"}


# --- Test 6: Full 3-pass with 0930 defaults ---
@pytest.mark.asyncio
async def test_full_pipeline_with_0930_defaults(suite, test_code):
    """Full K→DST→U→W pipeline with per-eye routing produces all outputs."""
    report = await suite.execute(test_code, passes=3)
    
    assert report["per_eye_routing"] is True
    assert "neji" in report["results"]
    assert "shikamaru" in report["results"]
    assert "deep_systems_thinking" in report["results"]
    assert "itachi" in report["results"]
    
    # All 9 canonical lenses should appear in lenses_active
    assert len(report["lenses_active"]) == 9
    
    # Itachi gets its own lenses
    itachi_lenses = set(report["results"]["itachi"]["lenses_applied"])
    assert itachi_lenses == {"Owl", "Sharingan", "CelestialSpacetime"}
