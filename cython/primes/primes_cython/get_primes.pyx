"""
Created on We Dec 20 16:35:00 2023

@author: rv43
"""
from libc.stdlib cimport malloc, free

def get_primes(int num_primes):
    cdef int i, n, num
    cdef int *primes = NULL

    primes= <int*> malloc(num_primes*sizeof(int))
    if not primes:
        raise MemoryError()

    try:
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
    finally:
        free(primes)

def get_num_primes(int num):
    cdef int i, n
    cdef int *primes = NULL

    primes= <int*> malloc(num*sizeof(int))
    if not primes:
        raise MemoryError()

    try:
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
    finally:
        free(primes)

