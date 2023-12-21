#!/usr/bin/env python3

# -*- coding: utf-8 -*-
"""
Created on Tu Apr 26 13:22:35 2022

@author: rv43
"""

import numpy as np
import random

from fit import FitMap
from general import quick_plot
from lmfit.lineshapes import exponential, gaussian

def create_map(
        num_i=2, num_j=2, num_peak=3, num=501, seed=1, add_noise=True,
        add_exp=True):

    def ran_uni():
        return random.random()-0.5

    random.seed(seed)

    x = np.array(np.linspace(0, 20, num))

    amp = 2.0
    cen = 5.0
    sig = 0.5
    a = 0.2
    b = 0.2
    c = 0.5
    exp_amp = 0.2
    exp_decay = 10.0
    if add_noise:
        amp_sig = 1.0
        cen_sig = 1.0
        sig_sig = 0.2
        sigma_noise = 0.02
    else:
        amp_sig = 0.0
        cen_sig = 0.0
        sig_sig = 0.0
        sigma_noise = 0.0

    y_map = []
    sig2 = sig*sig
    norm = sig*np.sqrt(2*np.pi)
    for i in range(num_i):
        for j in range(num_j):
            y = c*np.ones(num)
            if add_exp:
                y += exponential(x, exp_amp, exp_decay)
            for n in range(num_peak):
                y += gaussian(
                    x, amp+amp_sig*ran_uni(), (n+1)*cen+cen_sig*ran_uni(),
                    sig+sig_sig*ran_uni())
            y += np.random.normal(size=x.size, scale=sigma_noise)
            y_map.append(y)
    y_map = np.resize(y_map, (num_i, num_j , num))

    centers = [cen*(i+1) for i in range(num_peak)]

    return x, y_map, centers

if __name__ == '__main__':

    # Create model
    add_exp = True
    x, y_map, centers = create_map(add_exp=add_exp)

    # Create conventional Python model
    fit_python = FitMap(y_map, x=x)
    background = ['constant']
    if add_exp:
        background.append('exponential')
    fit_python.create_multipeak_model(centers, background=background)
    fit_python.fit(plot=True, skip_init=True, print_report=False, num_proc=1)
    #print(f'best_parameters: {fit_python.best_parameters()}')
    #print(f'best_values: {fit_python.best_values}')
    #print(f'redchi: {fit_python.redchi}')
