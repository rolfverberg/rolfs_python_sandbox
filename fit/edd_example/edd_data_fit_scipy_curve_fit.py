#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tu Apr 26 13:22:35 2022

@author: rv43
"""

import numpy as np
from scipy.optimize import curve_fit
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

class Model:

    def __init__(self):
        self.functions = []
        self.par_names = []
        self. pars_init = []
        self. num_pars = []

    def create_multipeak_model(self, centers, background=[]):
        assert isinstance(centers, (tuple, list, np.ndarray))
        assert is_str_series(background)

        # Add background models
        for model in background:
            if model == 'constant':
                self.functions += [constant]
                self.par_names += ['c']
                self.pars_init += [1.0]
                self.num_pars += [1]
            elif model == 'linear':
                self.functions += [linear]
                self.par_names += ['b', 'c']
                self.pars_init += [1.0, 1.0]
                self.num_pars += [2]
            elif model == 'quadratic':
                self.functions += [quadratic]
                self.par_names += ['a', 'b', 'c']
                self.pars_init += [1.0, 1.0, 1.0]
                self.num_pars += [3]
            else:
                raise ValueError('Invalid background model ({model})')

        # Add peak models (for now Gaussians)
        for n, cen in enumerate(centers):
            self.functions += [gaussian]
            self.par_names += [f'amp_{n}', f'sig_{n}', f'cen_{n}']
            self.pars_init += [1.0, 1.0, cen]
            self.num_pars += [3]

    def func(self, x, *args):
        f = np.zeros((x.size))
        n_par = 0
        for func, num_par in zip(self.functions, self.num_pars):
            f += func(x, args[n_par:n_par+num_par])
            n_par += num_par
        return f

    def fit(self, x, y, method='trf'):
        popt, pcov, infodict, mesg, ier = curve_fit(
            self.func, x, y, self.pars_init, full_output=True, method=method,
            ftol=1e-05, xtol=1e-05, gtol=1e-05, maxfev=20000)
        return popt, pcov, infodict, mesg, ier

if __name__ == '__main__':

    # Read data
    with np.load('edd_data.npz') as f:
        x = f['x']
        y_map = f['y']
        centers = f['centers']

#    print(f'x: {x.shape}')
#    print(f'y_map: {y_map.shape}')
#    print(f'centers: {centers.shape}')

    model = Model()
    background = ['quadratic']
    model.create_multipeak_model(centers, background=background)

    t = 0.
    for y in y_map:
        y = y/y.max()
        t0 = time()
        popt, pcov, infodict, mesg, ier = model.fit(x, y)
        t1 = time()
        t += t1-t0
#        quick_plot(
#            (x, y, '.'), (x, model.func(x, *popt), 'k'), block=True)
    print(f'\nRunning the fit with trf took {t:.6f} seconds\n')

    t = 0.
    for y in y_map:
        y = y/y.max()
        t0 = time()
        popt, pcov, infodict, mesg, ier = model.fit(x, y, method='lm')
        t1 = time()
        t += t1-t0
#        quick_plot(
#            (x, y, '.'), (x, model.func(x, *popt), 'k'), block=True)
    print(f'\nRunning the fit with lm took {t:.6f} seconds\n')

    t = 0.
    for y in y_map:
        y = y/y.max()
        t0 = time()
        popt, pcov, infodict, mesg, ier = model.fit(x, y, method='dogbox')
        t1 = time()
        t += t1-t0
#        quick_plot(
#            (x, y, '.'), (x, model.func(x, *popt), 'k'), block=True)
    print(f'\nRunning the fit with dogbox took {t:.6f} seconds\n')

