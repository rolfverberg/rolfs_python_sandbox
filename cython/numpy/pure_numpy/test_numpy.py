import numpy as np
from time import time

def compute_np(array_1, array_2, a, b, c):
    return np.clip(array_1, 2, 10) * a + array_2 * b + c

np.random.seed(0)
array_1 = np.random.uniform(0, 1000, size=(3000, 2000)).astype(np.intc)
array_2 = np.random.uniform(0, 1000, size=(3000, 2000)).astype(np.intc)
a = 4
b = 3
c = 9

n = 100
t = []
for i in range(n):
    t0 = time()
    compute_np(array_1, array_2, a, b, c)
    t1 = time()
    t.append(t1-t0)
t = 1000*np.asarray(t)
print(f'\nRunning compute_np took {t.mean():.6f} +- {t.std():.6f} ms\n')

print(f'sum = {compute_np(array_1, array_2, a, b, c).sum()}\n')

t0 = time()
for i in range(n):
    compute_np(array_1, array_2, a, b, c)
t1 = time()
print(f'\nRunning as one took an average of {1000.0*(t1-t0)/n:.6f} ms per compute_np\n')

