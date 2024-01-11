from compute_fused_types import compute
import numpy as np
from time import time

np.random.seed(0)
array_1 = np.random.uniform(0, 1000, size=(3000, 2000)).astype(np.intc)
array_2 = np.random.uniform(0, 1000, size=(3000, 2000)).astype(np.intc)
a = 4
b = 3
c = 9

n = 50
t = []
for i in range(n):
    t0 = time()
    compute(array_1.astype(np.double), array_2.astype(np.double), a, b, c)
    t1 = time()
    t.append(t1-t0)
t = 1000*np.asarray(t)
print(f'\nRunning compute took {t.mean():.6f} +- {t.std():.6f} ms\n')

result = compute(array_1.astype(np.double), array_2.astype(np.double), a, b, c)
print(f'sum = {result.sum()} {result.dtype}\n')

