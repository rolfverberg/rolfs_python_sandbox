# distutils: sources = get_primes/get_primes.c
# distutils: include_dirs = get_primes/

cimport get_primes

cdef class Primes:
    cdef int _num_primes
    cdef int* _primes

    def __cinit__(self, num_primes):
        self._num_primes = num_primes
        self._primes = get_primes.alloc_primes(num_primes)
        if self._primes is NULL:
            raise MemoryError()

    def __dealloc__(self):
        if self._primes is not NULL:
            get_primes.free_primes(self._primes)

    cpdef get_primes(self):
        num_primes = get_primes.get_primes(self._num_primes, self._primes)    
        assert num_primes == self._num_primes

    cpdef get_num_primes(self):
        num_primes = get_primes.get_num_primes(self._num_primes, self._primes)
        return num_primes, [self._primes[i] for i in range(num_primes)]

    @property
    def primes(self):
        return [self._primes[i] for i in range(self._num_primes)]
