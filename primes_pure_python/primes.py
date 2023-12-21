"""
Created on We Dec 20 16:35:00 2023

@author: rv43
"""
import numpy as np
from time import time

def get_primes(num_primes):

    primes = np.zeros((num_primes), dtype=np.int64)

    i = 2    # The current integer to test
    num = 0  # The current number of primes
    while num < num_primes:
        # Is i prime?
        for j in primes[:num]:
            if not i%j:
                # No
                break
        else:
            # Yes
            primes[num] = i
            num += 1
        i += 1
    return [prime for prime in primes[:num]]

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
    return n, [prime for prime in primes[:n]]


if __name__ == '__main__':

    num_primes = 100
    t0 = time()
    primes = get_primes(num_primes)
    t1 = time()
    print(f'\nThe first {num_primes} prime numbers are:\n\t{primes}\n')
    print(f'\nRunning get_primes({num_primes}) took {t1-t0:.6f} seconds\n')
    
    num = 1000000
    t0 = time()
    n, primes = get_num_primes(num)
    t1 = time()
    print(f'\nThe number of primes in [0:{num}] is {n}')
#    print(f'These {n} prime numbers are:\n\t{primes}')
    print(f'\nRunning get_num_primes({num}) took {t1-t0:.6f} seconds\n')
