import asyncio
import random
from time import time

import aiomultiprocess


async def coro_func(index:int, value:int) -> int:
    sleeptime = random.randint(value, 2*value)
    print(f'sleeptime on {index} for value = {value}: {sleeptime}')
    await asyncio.sleep(sleeptime)
    return sleeptime


async def main():
    tasks = []
    values = [random.randint(2,8) for _ in range(16)]
    t0 = time()
    async with aiomultiprocess.Pool(processes=min(4, len(values))) as pool:
        for args in enumerate(values):
            tasks.append(pool.apply(coro_func, args))

        results = await asyncio.gather(*tasks)
        print(f'results: {results}')
    t1 = time()
    print(f'Done in {t1-t0:.2f} ms')


if __name__ == "__main__":
    asyncio.run(main())
