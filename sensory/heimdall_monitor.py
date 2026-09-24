"""
INTEGRA O/S: HEIMDALL 3.1 — 9-LOBE VISUAL MONITOR
Module: sensory/heimdall_monitor.py
Layer: 4 (Heimdall 3.1: Shannon Entropy Thermostat & Visual Dashboard)
Status: BLOCK 5 / PHASE D — SOVEREIGN VISUAL DASHBOARD

Purpose:
    Replaces the 279-byte stub with a full Rich terminal dashboard displaying
    the 9-Lobe System Health Matrix in real-time. Polls /heimdall/health at 2 Hz.

Launch:
    python -m sensory.heimdall_monitor
"""

import sys
import time
import json

try:
    import urllib.request
    import urllib.error
except ImportError:
    pass

# Lazy import Rich — gracefully degrade if not installed
_RICH_AVAILABLE = False
try:
    from rich.console import Console
    from rich.table import Table
    from rich.live import Live
    from rich.panel import Panel
    from rich.text import Text
    from rich.layout import Layout
    _RICH_AVAILABLE = True
except ImportError:
    pass

# Re-export for backward compatibility
from sensory.heimdall import Heimdall31, HeimdallSensor

try:
    from sensory.heimdall import HeimdallMonitor
except ImportError:
    HeimdallMonitor = None

__all__ = ["HeimdallMonitor", "Heimdall31", "HeimdallSensor"]


# --- 9-Lobe Configuration ---
NINE_LOBES = [
    {"name": "Cheshire Cat", "key": "cheshire_cat", "layer": 4},
    {"name": "Y789NexusDual", "key": "cognitive_engine", "layer": 2},
    {"name": "The Hoard", "key": "the_hoard", "layer": 3},
    {"name": "Rodin Protocol", "key": "rodin", "layer": 3},
    {"name": "Phoenix Forge", "key": "phoenix_forge", "layer": 6},
    {"name": "Celestial Clock", "key": "celestial_clock", "layer": 7},
    {"name": "Friday Fortress Bank", "key": "friday_fortress_bank", "layer": 5},
    {"name": "Antigravity Runner", "key": "antigravity_runner", "layer": "R"},
    {"name": "Thermodynamic Loop", "key": "thermal_core", "layer": 0},
]

HEALTH_URL = "http://localhost:8000/heimdall/health"
METATRON_URL = "http://localhost:8000/metatron/status"
CHESHIRE_URL = "http://localhost:8000/cheshire/status"
POLL_INTERVAL = 0.5  # 2 Hz


def _fetch_json(url: str) -> dict:
    """Fetch JSON from an HTTP endpoint with timeout."""
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as resp:
            return json.loads(resp.read().decode())
    except Exception:
        return {}


def _build_table(health_data: dict, metatron_data: dict, cheshire_data: dict) -> Table:
    """Build the 9-Lobe Health Matrix table."""
    table = Table(
        title="INTEGRA O/S — 9-LOBE SYSTEM HEALTH MATRIX",
        title_style="bold magenta",
        border_style="bright_magenta",
        show_lines=True,
    )
    table.add_column("Layer", style="dim", width=5, justify="center")
    table.add_column("Lobe", style="bold cyan", width=22)
    table.add_column("Status", width=14, justify="center")
    table.add_column("H_smooth", width=10, justify="right")
    table.add_column("Latency (ms)", width=12, justify="right")
    table.add_column("Delta E", width=10, justify="right")
    table.add_column("Last Beat", width=22)

    components = health_data.get("components", {})

    for lobe in NINE_LOBES:
        comp = components.get(lobe["key"], {})
        is_active = comp.get("is_active", comp.get("active", False))
        status_text = "[green]ACTIVE[/green]" if is_active else "[red]OFFLINE[/red]"
        
        h_smooth = health_data.get("h_smooth", 0.0) if lobe["key"] == "cheshire_cat" else "—"
        if isinstance(h_smooth, (int, float)):
            h_smooth = f"{h_smooth:.4f}"
        
        latency = comp.get("latency_ms", "—")
        if isinstance(latency, (int, float)):
            latency = f"{latency:.1f}"
        
        delta_e = "0.0000"
        if lobe["key"] == "thermal_core":
            me_enforcement = metatron_data.get("delta_e_enforcement", "UNKNOWN")
            if me_enforcement == "MECHANICAL":
                delta_e = "[green]0.0000[/green]"
            else:
                delta_e = "[yellow]THEORETICAL[/yellow]"
        
        last_beat = comp.get("last_beat", comp.get("timestamp", "—"))
        if isinstance(last_beat, str) and len(last_beat) > 22:
            last_beat = last_beat[:22]

        table.add_row(
            str(lobe["layer"]),
            lobe["name"],
            status_text,
            str(h_smooth),
            str(latency),
            delta_e,
            str(last_beat),
        )

    return table


def _build_footer(metatron_data: dict, cheshire_data: dict) -> str:
    """Build the footer status line."""
    me_status = metatron_data.get("delta_e_enforcement", "UNKNOWN")
    me_tables = metatron_data.get("tables_count", metatron_data.get("row_counts", {}))
    ch_hz = cheshire_data.get("polling_hz", "?")
    ch_state = cheshire_data.get("state", "UNKNOWN")
    ch_queue = cheshire_data.get("queue_depth", "?")

    anomalies = metatron_data.get("unprocessed_anomalies", 0)
    anomaly_str = f"[green]{anomalies}[/green]" if anomalies == 0 else f"[red]{anomalies}[/red]"

    return (
        f"  Metatron: {me_status} | "
        f"Cheshire: {ch_state} @ {ch_hz}Hz (queue: {ch_queue}) | "
        f"Unprocessed Anomalies: {anomaly_str}"
    )


def run_dashboard():
    """Main entry point for the Heimdall visual dashboard."""
    if not _RICH_AVAILABLE:
        print("ERROR: 'rich' package not installed. Run: pip install rich")
        print("Falling back to basic text mode.")
        _run_basic_mode()
        return

    console = Console()
    console.print(
        Panel(
            "[bold magenta]INTEGRA O/S v8.2.4 — HEIMDALL 3.1 VISUAL MONITOR[/bold magenta]\n"
            "[dim]9-Lobe System Health Matrix | Polling at 2 Hz | Ctrl+C to exit[/dim]",
            border_style="bright_magenta",
        )
    )

    with Live(console=console, refresh_per_second=2, screen=False) as live:
        while True:
            try:
                health = _fetch_json(HEALTH_URL)
                metatron = _fetch_json(METATRON_URL)
                cheshire = _fetch_json(CHESHIRE_URL)

                table = _build_table(health, metatron, cheshire)
                footer = _build_footer(metatron, cheshire)

                panel = Panel(
                    table,
                    subtitle=footer,
                    border_style="bright_magenta",
                )
                live.update(panel)
                time.sleep(POLL_INTERVAL)
            except KeyboardInterrupt:
                console.print("[bold yellow]Heimdall Monitor stopped.[/bold yellow]")
                break
            except Exception as e:
                live.update(Text(f"ERROR: {e}", style="bold red"))
                time.sleep(1.0)


def _run_basic_mode():
    """Fallback text-mode monitor when Rich is not available."""
    print("HEIMDALL 3.1 — BASIC TEXT MODE (install 'rich' for full dashboard)")
    print("=" * 60)
    while True:
        try:
            health = _fetch_json(HEALTH_URL)
            metatron = _fetch_json(METATRON_URL)
            print(f"[{time.strftime('%H:%M:%S')}] "
                  f"Metatron: {metatron.get('delta_e_enforcement', '?')} | "
                  f"Components: {len(health.get('components', {}))} | "
                  f"Anomalies: {metatron.get('unprocessed_anomalies', '?')}")
            time.sleep(2.0)
        except KeyboardInterrupt:
            print("Monitor stopped.")
            break


if __name__ == "__main__":
    run_dashboard()
