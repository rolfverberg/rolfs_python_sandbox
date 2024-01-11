# distutils: language = c++

from get_primes cimport Primes

cdef class PyPrimes:
    cdef Primes* c_primes

    def __cinit__(self, const size_t num_primes):
#        print('\nInside PyPrimes:__cinit__ with num_primes = '+str(num_primes))
        self.c_primes = new Primes(num_primes)

    def __dealloc__(self):
#        print('\nInside PyPrimes:__dealoc__ ')
        del self.c_primes

    def get_primes(self):
        return self.c_primes.get_primes()    

    def get_num_primes(self):
        return self.c_primes.get_num_primes()
