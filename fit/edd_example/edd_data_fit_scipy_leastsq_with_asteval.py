#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tu Apr 26 13:22:35 2022

@author: rv43
"""

from asteval import (
    Interpreter,
    get_ast_names,
)
import numpy as np
from scipy.optimize import leastsq
from time import time

from general import (
    is_str_series,
    quick_plot,
)

def constant(x, pars):
    return [pars[0]]*len(x)

def constant_jac(x, pars):
    return np.ones(x.size)

def linear(x, pars):
    return x*pars[0] + pars[1]

def linear_jac(x, pars):
    return x, np.ones(x.size)

def quadratic(x, pars):
    return x * (x*pars[0] + pars[1]) + pars[2]

def quadratic_jac(x, pars):
    return 2.*x*pars[0], pars[1], np.ones(x.size)

def gaussian(x, pars):
    sig2 = 2.*pars[1]**2
    norm = pars[1]*np.sqrt(2.0*np.pi)
    return pars[0]*np.exp(-(x-pars[2])**2/sig2)/norm

def gaussian_jac(x, pars):
    dummy = (x-args[3])/args[2]**2
    g = gaussian(x, args[1:3])
    return g/args[1], g*((x-args[3])*dummy - 1.)/args[2], g*dummy


class Model:

    def __init__(self, x, y_map):
        self.x = x
        self.y_map = y_map
        self.expr = ''
        self.par_names = []
        self.pars_init = []
        self.lskws = {
            'ftol': 1.49012e-08,
            'xtol': 1.49012e-08,
            'gtol': 0.0,
            'maxfev': 64000,
        }
        self.asteval = Interpreter()
        self.astcode = None
        self.asteval.symtable['x'] = x

    def create_multipeak_model(self, centers, background=[]):
        assert isinstance(centers, (tuple, list, np.ndarray))
        assert is_str_series(background)

        # Add background models
        for model in background:
            if model == 'constant':
                if self.expr:
                    self.expr += ' + bkgr_c'
                else:
                    self.expr = 'bkgr_c'
                self.par_names += ['bkgr_c']
                self.pars_init += [1.0]
            elif model == 'linear':
                if self.expr:
                    self.expr += ' + bkgr_b*x + bkgr_c'
                else:
                    self.expr = 'bkgr_b*x + bkgr_c'
                self.par_names += ['bkgr_b', 'bkgr_c']
                self.pars_init += [1.0, 1.0]
            elif model == 'quadratic':
                if self.expr:
                    self.expr += ' + (bkgr_a*x + bkgr_b)*x + bkgr_c'
                else:
                    self.expr = '(bkgr_a*x + bkgr_b)*x + bkgr_c'
                self.par_names += ['bkgr_a', 'bkgr_b', 'bkgr_c']
                self.pars_init += [1.0, 1.0, 1.0]
            else:
                raise ValueError('Invalid background model ({model})')

        # Add peak models (for now Gaussians)
        for n, cen in enumerate(centers):
            if self.expr:
                self.expr += f' + amp_{n}*exp(-0.5*((x-cen_{n})/sig_{n})**2)/'\
                             f'(sig_{n}*sqrt(2*pi))'
            else:
                self.expr = f'amp_{n}*exp(-0.5*((x-cen_{n})/sig_{n})**2)/'\
                             f'(sig_{n}*sqrt(2*pi))'
            self.par_names += [f'amp_{n}', f'sig_{n}', f'cen_{n}']
            self.pars_init += [1.0, 1.0, cen]

        # Check parameter names
        self.astcode = self.asteval.parse(self.expr)
        par_names = []
        for name in get_ast_names(self.astcode):
            if name not in par_names and name not in self.asteval.symtable:
                par_names.append(name)
        assert len(par_names) == len(self.par_names)
        assert all(name in par_names for name in self.par_names)

    def residual(self, pars, x, y):
        for name, val in zip(self.par_names, pars):
            self.asteval.symtable[name] = val
        return self.asteval.run(self.astcode) - y

    def fit(self, method='trf'):
        num_fev = []
        for y in self.y_map:
            y = y/y.max()
            result = leastsq(
                self.residual, self.pars_init, args=(x, y), full_output=True,
                **self.lskws)
#            self.pars_init = result[0]
            num_fev.append(result[2]['nfev'])
#            quick_plot(
#                (self.x, y, '.'), (self.x, y + result[2]['fvec'], 'k'),
#                block=True)
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

