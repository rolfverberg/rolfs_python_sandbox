import numpy as np
import matplotlib.pyplot as plt
from time import time

from fit import Fit

def gaussian(x, amp, sig, cen):
    sig2 = 2.*sig**2
    norm = sig*np.sqrt(2.0*np.pi)
    return amp*np.exp(-(x-cen)**2/sig2)/norm

def func(x, c, amp, sig, cen):
    return c + gaussian(x, amp, sig, cen)

def myDfun(pars, *args, **kwargs):
    x = kwargs['x']
    amp = pars['amplitude'].value
    cen = pars['center'].value
    sig = pars['sigma'].value
    dummy = (x-cen)/sig**2
    g = gaussian(x, amp, sig, cen)
    return np.vstack((
        np.ones(x.size), g/amp, g*dummy, g*((x-cen)*dummy - 1.)/sig)).T

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

background = ['constant']
c_init = 1.
amp_init = 1.
sig_init = 0.1
cen_init = 0.

plt.plot(x, y, 'b-', label='data')

fit= Fit(y, x=x)
fit.create_multipeak_model(cen_init, background=background)
t0 = time()
fit.fit()
t1 = time()
print(f'\nFinal parameters:\n{fit.best_values}')
print(f'Number of function evals: {fit.num_func_eval}')
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(x, fit.best_fit, 'k', label='lmfit')

fit= Fit(y, x=x)
fit.create_multipeak_model(cen_init, background=background)
t0 = time()
fit.fit(Dfun=myDfun)
t1 = time()
print(f'\nFinal parameters:\n{fit.best_values}')
print(f'Number of function evals with j: {fit.num_func_eval}')
print(f'Running curve_fit took {t1-t0:.6f} seconds\n')
plt.plot(x, fit.best_fit, 'k.', label='lmfit+Jac')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
