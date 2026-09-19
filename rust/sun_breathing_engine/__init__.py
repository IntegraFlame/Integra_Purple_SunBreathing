# INTEGRA O/S: Rust SunBreathingEngine Module
# Python package initializer for the rust/sun_breathing_engine directory.
# Exposes the Python bridge for use within the Genesis Kernel FastAPI ecosystem.

from .python_bridge import (
    SunBreathingEngine,
    SlipstreamResult,
    LoopClosureResult,
    EpiphanyOmegaResult,
    get_engine,
    ANGULAR_MOMENTUM_BASE,
    ULTIMATE_COMPRESSIVE_STRENGTH_MPa,
    PYTHON_BRIDGE_PSI_MPa,
    OPTIMAL_AXIAL_STRESS_MPa,
)

__all__ = [
    "SunBreathingEngine",
    "SlipstreamResult",
    "LoopClosureResult",
    "EpiphanyOmegaResult",
    "get_engine",
    "ANGULAR_MOMENTUM_BASE",
    "ULTIMATE_COMPRESSIVE_STRENGTH_MPa",
    "PYTHON_BRIDGE_PSI_MPa",
    "OPTIMAL_AXIAL_STRESS_MPa",
]
