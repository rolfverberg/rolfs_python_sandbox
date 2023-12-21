"""
Created on We Dec 20 16:35:00 2023

@author: rv43
"""
from time import time

from get_primes import (
    get_primes,
    get_num_primes,
)

if __name__ == '__main__':

#    num_primes = 5
#    print(f'\nThe first {num_primes} prime numbers are:\n\t'
#          f'{get_primes(num_primes)}\n')
    
    num = 1000000
    t0 = time()
    n, primes = get_num_primes(num)
    print(f'\nThe number of primes in [0:{num}] is {n}')
#    print(f'These {n} prime numbers are:\n\t{primes}')
    print(f'\nIt took {time()-t0:.2f} seconds\n')
