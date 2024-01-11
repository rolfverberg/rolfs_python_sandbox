#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tu Apr 26 13:22:35 2022

@author: rv43
"""

import numpy as np
from time import time

from fit import FitMap
from general import quick_plot

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

    # Create conventional Python model
    fit_python = FitMap(y_map, x=x)
    background = ['quadratic']
    fit_python.create_multipeak_model(centers, background=background)
    t0 = time()
    #fit_python.fit(method='leastsq', num_proc=1)
    fit_python.fit(num_proc=1)
    t1 = time()
    print(f'\nnum_fev:\n{fit_python.num_func_eval}')
    print(f'\ntotal num_fev:\n{sum(fit_python.num_func_eval)}')
    print(f'\nRunning the fit with leastsq took {t1-t0:.6f} seconds\n')

    # Create conventional Python model
#    fit_python = FitMap(y_map, x=x)
#    background = ['quadratic']
#    fit_python.create_multipeak_model(centers, background=background)
#    t0 = time()
#    fit_python.fit(method='least_squares', num_proc=1)
#    t1 = time()
#    print(f'\nRunning the fit with least_squares took {t1-t0:.6f} seconds\n')
