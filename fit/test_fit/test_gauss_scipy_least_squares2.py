import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as optimize
from time import time

def constant(x, pars):
    return [pars[0]]*len(x)

def gaussian(x, pars):
    sig2 = 2.*pars[1]**2
    norm = pars[1]*np.sqrt(2.0*np.pi)
    return pars[0]*np.exp(-(x-pars[2])**2/sig2)/norm

def myDfun(pars, x, y, functions, num_pars):
    n_par = 0
    jac = None
    for func, num_par in zip(functions, num_pars):
        if func == constant:
            dfunc = np.ones(x.size)
        elif func == gaussian:
            dummy = (x-pars[n_par+2])/pars[n_par+1]**2
            g = func(x, pars[n_par:n_par+num_par])
            dfunc = np.asarray([
                g/pars[n_par],
                g*((x-pars[n_par+2])*dummy - 1.)/pars[n_par+1],
                g*dummy])
        else:
            raise ValueError(f'Invalid function ({func})\n\n({dir(func)})')
        if jac is None:
            jac = dfunc
        else:
            jac = np.vstack((jac, dfunc))
        n_par += num_par
    return jac.T

def residual(pars, x, y, functions, num_pars):
    res = np.zeros((x.size))
    n_par = 0
    for func, num_par in zip(functions, num_pars):
        res += func(x, pars[n_par:n_par+num_par])
        n_par += num_par
    return res - y

num = 101
sigma_noise = 0.1

c = 1.5
amp = 2.0
sig = 0.35
cen = -0.25

x = np.array(np.linspace(-1, 1, num))
y = c + gaussian(x, (amp, sig, cen))

np.random.seed(0)
sigma = np.random.normal(size=x.size, scale=sigma_noise)
y += sigma

print(f'\nInput parameters:\n{c} {amp} {sig} {cen}')

plt.plot(x, y, 'b-', label='data')

pars_init = np.asarray([1., 1., 0.1, 0.])

t0 = time()
result = optimize.least_squares(
    residual, pars_init,
    ftol=1e-05, xtol=1e-05, gtol=1e-05, max_nfev=20000,
    args=(x, y, [constant, gaussian], [1, 3]))
#def residual(pars, x, y, functions, num_pars):
t1 = time()
print(f'\nFinal parameters:\n{result["x"]}')
print(f'Number of function evals with trf: {result["nfev"]}')
print(f'Running least_squares took {t1-t0:.6f} seconds\n')
y_fit = y + result['fun']
plt.plot(x, y_fit, 'k', label='least_squares trf')

t0 = time()
result = optimize.least_squares(
    residual, pars_init, myDfun,
    ftol=1e-05, xtol=1e-05, gtol=1e-05, max_nfev=20000,
    args=(x, y, [constant, gaussian], [1, 3]))
t1 = time()
print(f'\nFinal parameters:\n{result["x"]}')
print(f'Number of function evals with trf and Jac: {result["nfev"]}')
print(f'Running least_squares took {t1-t0:.6f} seconds\n')
y_fit = y + result['fun']
plt.plot(x, y_fit, 'k.', label='least_squares trf')

t0 = time()
result = optimize.least_squares(
    residual, pars_init, method='lm',
    ftol=1e-05, xtol=1e-05, gtol=1e-05, max_nfev=20000,
    args=(x, y, [constant, gaussian], [1, 3]))
t1 = time()
print(f'\nFinal parameters:\n{result["x"]}')
print(f'Number of function evals with lm: {result["nfev"]}')
print(f'Running least_squares took {t1-t0:.6f} seconds\n')
y_fit = y + result['fun']
plt.plot(x, y_fit, 'k', label='least_squares lm')

t0 = time()
result = optimize.least_squares(
    residual, pars_init, myDfun, method='lm',
    ftol=1e-05, xtol=1e-05, gtol=1e-05, max_nfev=20000,
    args=(x, y, [constant, gaussian], [1, 3]))
t1 = time()
print(f'\nFinal parameters:\n{result["x"]}')
print(f'Number of function evals with lm and Jac: {result["nfev"]}')
print(f'Running least_squares took {t1-t0:.6f} seconds\n')
y_fit = y + result['fun']
plt.plot(x, y_fit, 'k.', label='least_squares lm')

plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.show()
