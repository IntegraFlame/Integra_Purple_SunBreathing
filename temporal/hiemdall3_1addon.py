"""
INTEGRA O/S: HEIMDALL 3.1 DEFERRED INTERACTION TELEMETRY ADDON
Module: temporal/hiemdall3_1addon.py
Layer: 4/7 (Sensory & Temporal Surveillance)

Provides structured polling and terminal-state surveillance for deferred
Gemini Interactions API executions, attached to Heimdall31.
"""

import time
from typing import Any, Dict, Optional

TERMINAL_STATES = ("completed", "failed", "cancelled")
POLL_INTERVAL_SECONDS = 15
TIMEOUT_MINUTES = 60


def poll_deferred_interaction(
    client: Any,
    interaction_id: str,
    poll_interval_seconds: float = POLL_INTERVAL_SECONDS,
    timeout_minutes: float = TIMEOUT_MINUTES,
    verbose: bool = False,
) -> Dict[str, Any]:
    """
    Polls a deferred interaction until it reaches one of TERMINAL_STATES
    ('completed', 'failed', 'cancelled') or exceeds `timeout_minutes`.
    When `client` is None (offline/local mode), returns a simulated telemetry snapshot.
    """
    started = time.time()
    deadline = started + timeout_minutes * 60.0

    if client is None or not hasattr(client, "interactions"):
        return {
            "interaction_id": interaction_id,
            "status": "completed",
            "steps_count": 1,
            "elapsed_seconds": 0,
            "mode": "LOCAL_OFFLINE_TELEMETRY",
        }

    while True:
        current = client.interactions.get(interaction_id)
        elapsed = int(time.time() - started)
        steps = getattr(current, "steps", None) or []
        status = getattr(current, "status", "completed")
        if verbose:
            print(f"[{elapsed:>4}s] status={status} steps={len(steps)}")

        if status in TERMINAL_STATES:
            return {
                "interaction_id": interaction_id,
                "status": status,
                "steps_count": len(steps),
                "elapsed_seconds": int(time.time() - started),
                "interaction": current,
                "mode": "LIVE_INTERACTIONS_API",
            }
        if time.time() >= deadline:
            raise TimeoutError(
                f"Still {status} after {timeout_minutes} min. The interaction "
                "continues running server-side; re-run the check to resume polling."
            )
        time.sleep(poll_interval_seconds)