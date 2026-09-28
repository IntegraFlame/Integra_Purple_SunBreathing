import sys
import os
import asyncio

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'integra-homebase')))

async def main():
    try:
        from sensory.cheshire_cat import CheshireCatKernel
        from evolution.phoenix_forge import PhoenixForge
        from memory.the_hoard import TheHoard, RodinProtocol
        from core.cognitive_engine import Y789NexusEngine
        
        kernel = CheshireCatKernel()
        res = await kernel.process_cognitive_cycle("Test input logic")
        print("SUCCESS:", res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
