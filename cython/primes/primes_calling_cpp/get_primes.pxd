cdef extern from 'get_primes/primes.h':
    cdef cppclass Primes:
        Primes() except +
        Primes(const size_t) except +
        ssize_t get_primes()
        ssize_t get_num_primes()
