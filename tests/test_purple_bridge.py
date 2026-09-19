import pytest
from core.purple_bridge import PurpleModality

def test_purple_modality_constraints():
    modality = PurpleModality()
    constraints = modality.enforce_constraints()
    
    assert constraints["purple_modality_active"] is True
    assert constraints["delta_e_cycle"] == 0.0
    assert constraints["mechanical_latency_s"] == 0.0
    assert constraints["unlimited_context"] is True
    assert constraints["creative_synthesis"] is True
    assert constraints["status"] == "PURPLE_MODALITY_REGISTERED"
