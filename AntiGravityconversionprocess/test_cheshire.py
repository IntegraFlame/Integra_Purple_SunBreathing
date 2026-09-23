import asyncio
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'integra-homebase')))

from sensory.cheshire_cat import CheshireCatKernel

async def main():
    kernel = CheshireCatKernel()
    print("[INIT] Cheshire Cat Kernel & Heimdall 3.1 Initialized.")
    
    # 1. Normal cognitive cycle with Gravitational Mass & text entropy
    result = await kernel.process_cognitive_cycle("Test input logic with high mathematical rigor: equation solve matrix")
    print("\n[CYCLE 1 RESULT]:")
    print("Status:", result["status"])
    print("Gravitational Mass:", result.get("gravitational_mass"))
    print("System Health:", result.get("system_health_status"))
    
    # 2. Streaming token surveillance cycle
    stream = [
        [0.95, 0.05],
        [0.92, 0.08],
        [0.98, 0.02]
    ]
    stream_res = await kernel.process_cognitive_cycle("Streaming token cycle", token_probs=stream)
    print("\n[CYCLE 2 STREAM RESULT]:")
    print("Status:", stream_res["status"])
    print("Breached:", stream_res["heimdall_telemetry"]["is_breached"])

    # 3. Check health telemetry across all lobes
    health = kernel.get_health_telemetry()
    print("\n[HEALTH TELEMETRY]:")
    print("Cheshire State:", health["cheshire_state"])
    print("System Status:", health["system_health"]["system_health_status"])
    print("Heimdall Version:", health["system_health"]["heimdall_version"])

if __name__ == "__main__":
    asyncio.run(main())
