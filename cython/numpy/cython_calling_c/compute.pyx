# cython: infer_types=True
cimport cython
import numpy as np

@cython.boundscheck(False)  # Deactivate bounds checking
@cython.wraparound(False)   # Deactivate negative indexing
def compute(int[:, ::1] array_1, int[:, ::1] array_2, int a, int b, int c):

    dim = (array_1.shape[0], array_1.shape[1])

    assert tuple(array_1.shape) == tuple(array_2.shape)
    cdef int[:, ::1] array_1_memview = array_1
    cdef int[:, ::1] array_2_memview = array_2

    result = np.empty(dim, dtype=np.intc)
    cdef int[:, ::1] result_memview = result

    compute_in_c(
        &array_1_memview[0,0], &array_2_memview[0,0], &result_memview[0,0],
        result_memview.size, a, b, c)

    return result
