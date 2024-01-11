import numpy as np

def multiply_by_10(arr):  # 'arr' is a one-dimensional numpy array

    if not arr.flags['C_CONTIGUOUS']:
        arr = np.ascontiguousarray(arr)  # Makes a contiguous copy of the numpy array.

    cdef double[::1] arr_memview = arr

    multiply_by_10_in_C(&arr_memview[0], arr_memview.shape[0])

    return arr
