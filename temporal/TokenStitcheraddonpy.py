"""
INTEGRA O/S: TOKEN STITCHER INTERACTION EXTRACTION ADDON
Module: temporal/TokenStitcheraddonpy.py
Layer: 4/7 (Temporal & Token Stitcher)

Extracts final text and token usage telemetry from completed deferred interactions,
attached to TokenStitcher (temporal/token_stitcher.py).
"""

from typing import Any, Dict


def get_final_text(completed_interaction: Any) -> str:
    """Returns the text of the last step that produced output."""
    if isinstance(completed_interaction, dict):
        steps = completed_interaction.get("steps") or []
        for step in reversed(steps):
            content = step.get("content") or []
            text = "".join(p.get("text", "") for p in content if isinstance(p, dict) and p.get("text"))
            if text:
                return text
        return str(completed_interaction.get("text", ""))

    for step in reversed(getattr(completed_interaction, "steps", None) or []):
        text = "".join(
            part.text
            for part in (getattr(step, "content", None) or [])
            if getattr(part, "text", None)
        )
        if text:
            return text
    return ""


def inspect_completed_interaction(client: Any, interaction_id: str) -> Dict[str, Any]:
    """Retrieves final status, output text, and token usage from a completed interaction."""
    if client is None or not hasattr(client, "interactions"):
        return {
            "interaction_id": interaction_id,
            "status": "completed",
            "final_text": "(Local TokenStitcher addon ready)",
            "usage": {"total_input_tokens": 0, "total_output_tokens": 0, "total_tokens": 0},
            "mode": "LOCAL_OFFLINE_STITCHER",
        }

    final = client.interactions.get(interaction_id)
    usage_obj = getattr(final, "usage", None)
    usage = {
        "total_input_tokens": getattr(usage_obj, "total_input_tokens", 0) if usage_obj else 0,
        "total_output_tokens": getattr(usage_obj, "total_output_tokens", 0) if usage_obj else 0,
        "total_tokens": getattr(usage_obj, "total_tokens", 0) if usage_obj else 0,
    }
    return {
        "interaction_id": interaction_id,
        "status": getattr(final, "status", "completed"),
        "final_text": get_final_text(final) or "(No text output)",
        "usage": usage,
        "mode": "LIVE_INTERACTIONS_API",
    }