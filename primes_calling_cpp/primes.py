"""
Created on We Dec 20 16:35:00 2023

@author: rv43
"""
from time import time
import numpy as np

from get_primes import (
    get_primes,
#    get_num_primes,
)

if __name__ == '__main__':

    num_primes = 100
    primes = np.zeros((num_primes), dtype=np.int64)
    t0 = time()
    primes = get_primes(num_primes, primes)
    t1 = time()
    print(f'\nThe first {num_primes} prime numbers are:\n\t{primes}\n')
    print(f'\nRunning get_primes({num_primes}) took {t1-t0:.6f} seconds\n')
    
#    num = 100000
#    t0 = time()
#    n, primes = get_num_primes(num)
#    t1 = time()
#    print(f'\nThe number of primes in [0:{num}] is {n}')
##    print(f'These {n} prime numbers are:\n\t{primes}')
#    print(f'\nRunning get_num_primes({num}) took {t1-t0:.6f} seconds\n')
