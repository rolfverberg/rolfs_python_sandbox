import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from time import time

def gaussian(x, amp, sig, cen):
    sig2 = 2.*sig**2
    norm = sig*np.sqrt(2.0*np.pi)
    return amp*np.exp(-(x-cen)**2/sig2)/norm

def func(x, c, amp, sig, cen):
    return c + gaussian(x, amp, sig, cen)

def myDfun(x, c, amp, sig, cen):
    dummy = (x-cen)/sig**2
    g = gaussian(x, amp, sig, cen)
    return np.vstack(
        (np.ones(x.size), g/amp, g*((x-cen)*dummy - 1.)/sig, g*dummy)).T

num = 101
sigma_noise = 0.1

c = 1.5
amp = 2.
sig = 0.35
cen = -0.25

x = np.array(np.linspace(-1, 1, num))
y = func(x, c, amp, sig, cen)

np.random.seed(0)
sigma = np.random.normal(size=x.size, scale=sigma_noise)
y += sigma

print(f'\nInput parameters:\n{c} {amp} {sig} {cen}')

plt.plot(x, y, 'b-', label='data')

t0 = time()
#def func(x, c, amp, sig, cen):
popt, pcov, infodict, mesg, ier = curve_fit(func, x, y, full_output=True,
    method='trf', ftol=1e-05, xtol=1e-05, gtol=1e-05, maxfev=20000)
t1 = time()
print(f'\nFinal parameters:\n{popt}')
print(f'Number of function evals with trf: {infodict["nfev"]}')
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(x, func(x, *popt), 'k', label='least_squares')

t0 = time()
popt, pcov, infodict, mesg, ier = curve_fit(func, x, y, full_output=True,
    method='trf', jac=myDfun, ftol=1e-05, xtol=1e-05, gtol=1e-05, maxfev=20000)
t1 = time()
print(f'\nFinal parameters:\n{popt}')
print(f'Number of function evals with trf and Jac: {infodict["nfev"]}')
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(x, func(x, *popt), 'k.', label='least_squares')

t0 = time()
popt, pcov, infodict, mesg, ier = curve_fit(func, x, y, full_output=True,
    method='lm', ftol=1e-05, xtol=1e-05, gtol=1e-05, maxfev=20000)
t1 = time()
print(f'\nFinal parameters:\n{popt}')
print(f'Number of function evals with lm: {infodict["nfev"]}')
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(x, func(x, *popt), 'k', label='least_squares')

t0 = time()
popt, pcov, infodict, mesg, ier = curve_fit(func, x, y, full_output=True,
    method='lm', jac=myDfun, ftol=1e-05, xtol=1e-05, gtol=1e-05, maxfev=20000)
t1 = time()
print(f'\nFinal parameters:\n{popt}')
print(f'Number of function evals with lm and Jac: {infodict["nfev"]}')
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(x, func(x, *popt), 'k.', label='least_squares')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
