cdef extern from 'compute_c.c':
    pass

cdef extern from 'compute_c.h':
    void compute_in_c(const int* const array_1, const int* const array_2, int* const result,
        int a, int b, int c, size_t array_size)

