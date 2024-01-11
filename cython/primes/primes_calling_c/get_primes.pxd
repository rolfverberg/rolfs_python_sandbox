cdef extern from 'get_primes/get_primes.h':
    int get_primes(int num_primes, int *primes)
    int get_num_primes(int num, int *primes)
    int* alloc_primes(int num_primes)
    void free_primes(int *primes)

