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
    sig2 = 2.*pars[1]**2
    norm = pars[1]*np.sqrt(2.0*np.pi)
    return pars[0]*np.exp(-(x-pars[2])**2/sig2)/norm


class Model:

    def __init__(self, x, y_map):
        self.x = x
        self.y_map = y_map
        self.functions = []
        self.par_names = []
        self.pars_init = []
        self.num_pars = []
        self.lskws = {
            'ftol': 1.49012e-08,
            'xtol': 1.49012e-08,
            'gtol': 0.0,
            'maxfev': 64000,
        }

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

    def residual(self, pars, x, y):
        res = np.zeros((x.size))
        n_par = 0
        for func, num_par in zip(self.functions, self.num_pars):
            res += func(x, pars[n_par:n_par+num_par])
            n_par += num_par
        return res - y

    def fit(self, method='trf'):
        num_fev = []
#        i = 0
        for y in self.y_map:
            y = y/y.max()
#            print(f'\nself.pars_init:\n\t{self.pars_init}')
#            print(f'y.max: {y.max()}')
            result = leastsq(
                self.residual, self.pars_init, args=(x, y), full_output=True,
                **self.lskws)
#            self.pars_init = result[0]
            num_fev.append(result[2]['nfev'])
#            print(f'nfev: {result[2]["nfev"]}')
#            quick_plot(
#                (self.x, y, '.'), (self.x, y + result[2]['fvec'], 'k'),
#                block=True)
#            i += 1
#            if i == 2:
#                break
        print(f'\nnum_fev:\n{num_fev}')
        print(f'\ntotal num_fev:\n{sum(num_fev)}')


if __name__ == '__main__':

    # Read data
    with np.load('edd_data.npz') as f:
        x = f['x']
        y_map = f['y']
        centers = f['centers']

#    print(f'x: {x.shape}')
#    print(f'y_map: {y_map.shape}')
#    print(f'centers: {centers.shape}')

    model = Model(x, y_map)
    background = ['quadratic']
    model.create_multipeak_model(centers, background=background)

    t0 = time()
    model.fit()
    t1 = time()
    print(f'\nRunning the fit with leastsq took {t1-t0:.6f} seconds\n')

