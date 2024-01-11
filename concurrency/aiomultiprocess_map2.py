import asyncio
import numpy as np
import random
from time import time

import aiomultiprocess

async def get_num_primes(num):

    primes = np.zeros((num), dtype=np.int64)

    n = 0  # The current number of primes
    for i in range(2, num):
        # Is i prime?
        for j in primes[:n]:
            if not i%j:
                # No
                break
        else:
            # Yes
            primes[n] = i
            n += 1
        i += 1
    return n

async def coro_func(index, value):
    num = 10000*value
    t0 = time()
    n = await get_num_primes(num)
    t1 = time()
    print(f'Process {index} done in {t1-t0:.2f} s (found {n} primes in [0, {num}])')
    return n


async def main():
    num_procs = 3
    num_samples= 20
#    random.seed(0)
#    values = [random.randint(2,8) for _ in range(16)]
#    values = [i for i in reversed(range(num_samples))]
    values = [1]*num_samples
    values[0] = 10
    values[2] = 10
    values[num_samples-1] = 10
    results = []
    t0 = time()
    async with aiomultiprocess.Pool(processes=num_procs) as pool:
        async for result in pool.starmap(
                coro_func, zip(range(len(values)), values)):
            results.append(result)
        print(f'results: {results}')
    t1 = time()
    print(f'Done in {t1-t0:.2f} s')


if __name__ == "__main__":
    asyncio.run(main())
