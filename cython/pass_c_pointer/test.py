import numpy as np

from memview_to_c import multiply_by_10

a = np.ones(5, dtype=np.double)
print(a)
print(id(a))
c = multiply_by_10(a)
print(c)
print(a)
print(id(a))
print(id(c))

b = np.ones(10, dtype=np.double)
b = b[::2]  # b is not contiguous.

print()
print(b)
print(id(b))
c = multiply_by_10(b)
print(c)  # but our function still works as expected.
print(b)
print(id(b))
print(id(c))
