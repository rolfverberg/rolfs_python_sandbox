import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from time import time

def func(x, a, b, c):
    return a * np.exp(-b * x) + c

def myDfun(xdata, a, b, c):
    ebx = np.exp(-b * xdata)
    res = np.vstack( ( ebx, a * -xdata * ebx, np.ones(len(xdata)) ) ).T
    return res

xdata = np.linspace(0, 4, 50)
y = func(xdata, 2.5, 1.3, 0.5)
rng = np.random.default_rng()
y_noise = 0.2 * rng.normal(size=xdata.size)
ydata = y + y_noise
plt.plot(xdata, ydata, 'b-', label='data')

t0 = time()
popt, pcov = curve_fit(func, xdata, ydata)
t1 = time()
print(popt)
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(xdata, func(xdata, *popt), 'r-',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

t0 = time()
popt, pcov = curve_fit(func, xdata, ydata, jac=myDfun)
t1 = time()
print(popt)
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(xdata, func(xdata, *popt), 'r.',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

t0 = time()
popt, pcov = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]))
t1 = time()
print(popt)
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(xdata, func(xdata, *popt), 'g--',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

plt.xlabel('x')
t0 = time()
popt, pcov = curve_fit(func, xdata, ydata, bounds=(0, [3., 1., 0.5]), jac=myDfun)
t1 = time()
print(popt)
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(xdata, func(xdata, *popt), 'g.',
         label='fit: a=%5.3f, b=%5.3f, c=%5.3f' % tuple(popt))

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()

#print(np.linalg.cond(pcov))

#def func(x, a, b, c, d):
#    return a * d * np.exp(-b * x) + c  # a and d are redundant
#popt, pcov = curve_fit(func, xdata, ydata)
#print(np.linalg.cond(pcov))

#print(np.diag(pcov))
