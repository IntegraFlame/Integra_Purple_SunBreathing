import asyncio
from sensory.cheshire_cat import CheshireCatKernel

async def main():
    kernel = CheshireCatKernel()
    res = await kernel.process_cognitive_cycle("Compute matrix decomposition and solve Kepler orbit", [0.99, 0.005, 0.005])
    print(res)

asyncio.run(main())
