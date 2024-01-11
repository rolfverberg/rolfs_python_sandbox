"""
Created on We Dec 20 16:35:00 2023

@author: rv43
"""
from time import time
import numpy as np

import primes

#num_primes = 100
#P = primes.PyPrimes(num_primes)
#t0 = time()
#P.get_primes()
#t1 = time()
#print(f'\nThe first {num_primes} prime numbers are:\n\t{P.primes}\n')
#print(f'\nRunning get_primes took {t1-t0:.6f} seconds\n')

num = 5000000
P = primes.PyPrimes(num)
t0 = time()
n = P.get_num_primes()
t1 = time()
print(f'\nThe number of primes in [0:{num}] is {n}')
print(f'\nRunning get_num_primes({num}) took {t1-t0:.6f} seconds\n')

