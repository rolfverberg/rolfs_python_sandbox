from math import ceil
from multiprocessing import Pool
import numpy as np
import os
import random
from time import time

def get_num_primes(num):

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

def coro_func(value):
    num = 10000*value
    t0 = time()
    n = get_num_primes(num)
    t1 = time()
    print(f'Process {os.getpid()} done in {t1-t0:.2f} s (found {n} primes in [0, {num}])')
    return n


if __name__ == "__main__":
    num_procs = 3
    num_samples = 20
#    random.seed(0)
#    values = [random.randint(2,8) for _ in range(16)]
#    values = [i for i in reversed(range(num_samples))]
    values = [1]*num_samples
    values[0] = 10
    values[2] = 10
    values[num_samples-1] = 10
    t0 = time()
    with Pool(processes=num_procs) as pool:
        results = [result for result in pool.imap_unordered(coro_func, values)]
        print(f'unordered results: {results}')
    t1 = time()
    print(f'Done in {t1-t0:.2f} s')
    t0 = time()
    with Pool(processes=num_procs) as pool:
        results = [result for result in pool.imap_unordered(coro_func, values, ceil(num_samples/num_procs))]
        print(f'unordered results: {results}')
    t1 = time()
    print(f'With chunksize of {ceil(num_samples/num_procs)}: Done in {t1-t0:.2f} s')
