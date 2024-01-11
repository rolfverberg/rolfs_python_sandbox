#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tu Apr 26 13:22:35 2022

@author: rv43
"""

from joblib import (
    Parallel,
    delayed,
)
from lmfit import Parameters
from lmfit.models import (
    ConstantModel,
    LinearModel,
    QuadraticModel,
    GaussianModel,
)
from math import ceil
import numpy as np
from os import (
    mkdir,
    path,
)
import re
from scipy.optimize import leastsq
from shutil import rmtree
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


class FitModel:

    def __init__(self, x, y_map):
        self.x = x
        self.y_map = y_map
        self.memfolder = './joblib_memmap'
        self.model = None
        self.parameters = Parameters()
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
                # Par: c
                newmodel = ConstantModel(prefix='bkgd_')
            elif model == 'linear':
                # Par: slope, intercept
                newmodel = LinearModel(prefix='bkgd_')
            elif model == 'quadratic':
                # Par: a, b, c
                newmodel = QuadraticModel(prefix='bkgd_')
            else:
                raise ValueError('Invalid background model ({model})')
            if self.model is None:
                self.model = newmodel
            else:
                self.model += newmodel
            self.parameters += newmodel.make_params()

        # Add peak models (for now Gaussians)
        for n, cen in enumerate(centers):
            newmodel = GaussianModel(prefix=f'peak{n}_')
            if self.model is None:
                self.model = newmodel
            else:
                self.model += newmodel
            self.parameters += newmodel.make_params()

        # Set initial values:
        for name, par in self.parameters.items():
            par.set(value=1.0)
            if 'center' in name:
                par.set(value=centers[int(re.search('\d', name)[0])])

#        print(f'\n\nself.model:\n{self.model}')
#        print(f'\nself.parameters:')
#        for name, par in self.parameters.items():
#            print(f'{name}: {par.value}')
#        exit('Done')

    def residual(self, pars, x, y):
        res = np.zeros((x.size))
        n_par = 0
        for func, num_par in zip(self.functions, self.num_pars):
            res += func(x, pars[n_par:n_par+num_par])
            n_par += num_par
        return res - y

    def fit(self, num_proc=1, method='trf'):
        num_fit = self.y_map.shape[0]
        if num_proc == 1:
            self.num_func_eval = np.zeros(num_fit, dtype=np.intc)
            for n in range(0, num_fit):
                self._fit(n)
        else:
            try:
                mkdir(self.memfolder)
            except FileExistsError:
                pass
            filename_memmap = path.join(
                self.memfolder, 'num_func_eval_memmap')
            self.num_func_eval = np.memmap(
                filename_memmap, dtype=np.intc, shape=(num_fit, ), mode='w+')
            num_fit_batch = ceil(num_fit/num_proc)
            with Parallel(n_jobs=num_proc) as parallel:
                parallel(
                    delayed(self._fit_parallel)(num_fit_batch, n_start)
                    for n_start in range(0, self.y_map.shape[0], num_fit_batch))
            try:
                rmtree(self.memfolder)
                self.memfolder = None
            except:
                print('\tCould not clean-up automatically.')
        print(f'\nnum_fev:\n{self.num_func_eval}')
        print(f'\ntotal num_fev:\n{sum(self.num_func_eval)}')

    def _fit_parallel(self, num, n_start, **kwargs):
        num = min(num, self.y_map.shape[0]-n_start)
        for n in range(num):
            self._fit(n_start+n, **kwargs)

    def _fit(self, n, method='trf'):
        y = self.y_map[n]/self.y_map[n].max()
        result = self.model.fit(y, self.parameters, x=self.x)#, **self.lskws)
#        quick_plot(
#            (self.x, y, 'b.'), (self.x, result.best_fit, 'k'), block=True)
        self.num_func_eval[n] = result.nfev
        return None


if __name__ == '__main__':

    # Read data
    with np.load('edd_data.npz') as f:
        x = f['x']
        y_map = f['y']
        centers = f['centers']

#    print(f'x: {x.shape}')
#    print(f'y_map: {y_map.shape}')
#    print(f'centers: {centers.shape}')

    model = FitModel(x, y_map)
    background = ['quadratic']
    model.create_multipeak_model(centers, background=background)

    t0 = time()
    num_proc = 1
    model.fit(num_proc=num_proc)
    t1 = time()
    print(f'\nRunning the fit with leastsq took {t1-t0:.6f} seconds\n')

