"""
INTEGRA O/S: AGENT INTERACTIONS & DEFERRED SCHEDULING MODULE
Module: .agents/AGentinteractionsandeferreddinteractionspy.py
Layer: 4 (Cheshire Cat / Agent Interactions & Deferred Capacity)

Encapsulates Gemini Interactions API and ADK Deferred Scheduling (`ServiceTier.DEFERRED`)
configuration and reference documentation without executing unguarded top-level network calls.
"""

from typing import Any, Callable, Dict, List, Optional

SERVICE_TIERS = ("deferred", "flex", "standard", "priority")

DEFERRED_SCHEDULING_GUIDE_MD = """# Deferred scheduling with Gemini models

Supported in ADKPython v2.10.0Preview

Agent workloads have different latency needs. An interactive assistant must answer immediately,
but a summarization job, a bulk evaluation run, or a document-processing pipeline can wait for capacity.
Deferred scheduling lets ADK agents queue those model calls to run on off-peak capacity instead of
competing for interactive capacity.

You can request deferred scheduling per run, using the `service_tier` setting of `RunConfig`.
The setting is part of the run configuration rather than the model or the agent, so one agent definition
can serve both interactive requests and batch workloads.
"""


def get_current_weather(location: str = "Baker, Louisiana") -> Dict[str, Any]:
    """Default anchor weather tool for interactions_test_agent."""
    return {
        "location": location,
        "coordinates": {"lat": 30.5888, "lon": -91.1673},
        "condition": "Clear / Vacuum Slipstream",
    }


def build_interactions_agent_spec(
    name: str = "interactions_test_agent",
    model_name: str = "gemini-flash-latest",
    use_interactions_api: bool = True,
    extra_tools: Optional[List[Callable[..., Any]]] = None,
) -> Dict[str, Any]:
    """Builds the canonical agent specification for Gemini Interactions API."""
    try:
        from google.adk.agents.llm_agent import Agent  # type: ignore
        from google.adk.models.google_llm import Gemini  # type: ignore
        from google.adk.tools.google_search_tool import GoogleSearchTool  # type: ignore

        agent = Agent(
            model=Gemini(
                model=model_name,
                use_interactions_api=use_interactions_api,
            ),
            name=name,
            tools=[
                GoogleSearchTool(bypass_multi_tools_limit=True),
                get_current_weather,
                *(extra_tools or []),
            ],
        )
        return {"status": "LIVE_ADK_AGENT", "name": name, "agent": agent}
    except ImportError:
        return {
            "status": "SPEC_READY_ADK_OPTIONAL",
            "name": name,
            "model": model_name,
            "use_interactions_api": use_interactions_api,
            "tools": ["GoogleSearchTool", "get_current_weather"],
        }


def build_deferred_run_config(
    service_tier: str = "deferred",
    timeout_seconds: int = 300,
) -> Dict[str, Any]:
    """Builds a deferred scheduling run configuration (`service_tier='deferred'`)."""
    tier_norm = service_tier.lower().strip()
    if tier_norm not in SERVICE_TIERS:
        raise ValueError(f"Unsupported service_tier {service_tier!r}; must be one of {SERVICE_TIERS}")
    return {
        "service_tier": tier_norm,
        "streaming": False,
        "use_interactions_api": True,
        "client_deadline_seconds": timeout_seconds,
    }
