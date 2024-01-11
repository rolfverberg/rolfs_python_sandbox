#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tu Apr 26 13:22:35 2022

@author: rv43
"""

import numpy as np
import scipy.optimize as optimize
from time import time

from general import (
    is_str_series,
    quick_plot,
)

def constant(x, pars):
    return [pars[0]]*len(x)

def linear(x, pars):
    return x*pars[0] + pars[1]

def quadratic(x, pars):
    return x * (x*pars[0] + pars[1]) + pars[2]

def gaussian(x, pars):
    sig2 = 2.0*pars[1]**2
    norm = pars[1]*np.sqrt(2.0*np.pi)
    return pars[0]*np.exp(-(x-pars[2])**2/sig2)/norm

def create_multipeak_model(centers, background=[]):
    assert isinstance(centers, (tuple, list, np.ndarray))
    assert is_str_series(background)

    # Add background models
    functions = []
    par_names = []
    pars_init = []
    num_pars = []
    for model in background:
        if model == 'constant':
            functions += [constant]
            par_names += ['c']
            pars_init += [1.0]
            num_pars += [1]
        elif model == 'linear':
            functions += [linear]
            par_names += ['b', 'c']
            pars_init += [1.0, 1.0]
            num_pars += [2]
        elif model == 'quadratic':
            functions += [quadratic]
            par_names += ['a', 'b', 'c']
            pars_init += [1.0, 1.0, 1.0]
            num_pars += [3]
        else:
            raise ValueError('Invalid background model ({model})')

    # Add peak models (for now Gaussians)
    for n, cen in enumerate(centers):
        functions += [gaussian]
        par_names += [f'amp_{n}', f'sig_{n}', f'cen_{n}']
        pars_init += [1.0, 1.0, cen]
        num_pars += [3]

    return functions, par_names, pars_init, num_pars

def residual(pars, x, y, functions, num_pars):
    res = np.zeros((x.size))
    n_par = 0
    for func, num_par in zip(functions, num_pars):
        res += func(x, pars[n_par:n_par+num_par])
        n_par += num_par
    return res - y

if __name__ == '__main__':

    # Read data
    with np.load('edd_data.npz') as f:
        x = f['x']
        y_map = f['y']
        centers = f['centers']

#    print(f'x: {x.shape}')
#    print(f'y_map: {y_map.shape}')
#    print(f'centers: {centers.shape}')

    # Create conventional Python model
    background = ['quadratic']
    functions, par_names, pars_init, num_pars = create_multipeak_model(
        centers, background=background)
    lskws = {
        'ftol': 1.49012e-08,
        'xtol': 1.49012e-08,
        'gtol': 0.0,
        'maxfev': 64000,
    }

    t = 0.
    for y in y_map:
        y = y/y.max()
        t0 = time()
        result = optimize.least_squares(
            residual, pars_init, args=(x, y, functions, num_pars))
# def residual(pars, x, y, functions, num_pars):
        pars_init = result['x']
        t1 = time()
        t += t1-t0
#        y_fit = y + result['fun']
#        quick_plot(
#            (x, y, '.'), (x, y_fit, 'k'), (x, result['fun'], 'r'),
#            block=True)
    print(f'\nRunning the fit with trf took {t:.6f} seconds\n')

    t = 0.
    for y in y_map:
        y = y/y.max()
        t0 = time()
        result = optimize.least_squares(
            residual, pars_init, method='lm', args=(x, y, functions, num_pars))
        pars_init = result['x']
        t1 = time()
        t += t1-t0
#        y_fit = y + result['fun']
#        quick_plot(
#            (x, y, '.'), (x, y_fit, 'k'), (x, result['fun'], 'r'),
#            block=True)
    print(f'\nRunning the fit with lm took {t:.6f} seconds\n')
