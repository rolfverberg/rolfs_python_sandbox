#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tu Apr 26 13:22:35 2022

@author: rv43
"""

import numpy as np
from scipy.optimize import leastsq
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
#    y_map = y_map[0:10]
#    print(f'x: {x.shape}')
#    print(f'y_map: {y_map.shape}')
#    print(f'centers: {centers.shape}')

    background = ['quadratic']
    functions, par_names, pars_init, num_pars = create_multipeak_model(
        centers, background=background)
    lskws = {
        'ftol': 1.49012e-08,
        'xtol': 1.49012e-08,
        'gtol': 0.0,
        'maxfev': 64000,
    }
    t0 = time()
    num_fev = []
#    i = 0
    for y in y_map:
        y = y/y.max()
#        print(f'y.max: {y.max()}')
        result = leastsq(
            residual, pars_init, args=(x, y, functions, num_pars),
            full_output=True, **lskws)
#        pars_init = result[0]
        num_fev.append(result[2]['nfev'])
#        print(f'nfev: {result[2]["nfev"]}')
#        quick_plot(
#            (x, y, 'b.'), (x, y+result[2]['fvec'], 'k'),
#            block=True)
#        i += 1
#        if i == 5:
#            break
    t1 = time()
    print(f'\nnum_fev:\n{num_fev}')
    print(f'\ntotal num_fev:\n{sum(num_fev)}')
    print(f'\nRunning the fit took {t1-t0:.6f} seconds\n')
