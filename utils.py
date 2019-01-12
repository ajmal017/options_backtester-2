#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 15:21:09 2019
useful functions for an options backtester
@author: jacobsolawetz
"""

import math
from scipy.stats import norm
import pandas as pd
from datetime import date
import numpy as np

def strike_from_delta(S0, T, r, sigma, delta, right):
    if right == 'C':
        strike = S0 * math.exp(-norm.ppf(delta * math.exp ((r)*T) ) * sigma * math.sqrt(T) + ((math.pow(sigma,2.0))/2.0)* T)
    if right == 'P':
        strike = S0 * math.exp(norm.ppf(delta * math.exp ((r)*T) ) * sigma * math.sqrt(T) + ((math.pow(sigma,2.0))/2.0)* T)
    return strike

def get_implied_vol(option_type, k, s, vix, skew):
    #assumptions - these were empirically based on "Fitting the Smile.xlx" and the idea that implied volatility 
    #increases mostly linearly with some none linearity defined by the skewness of the underlying distribution
    #measured by CBOE skew
    #Assumed Parameters
    
    skew = (skew - 100) / (-10)
    vix_multiplier = .85
    otm_multiplier = 75
    skew_multiplier = 2
    skew_power = 4
    otm = abs((s - k)) / s
    #starts at a base of the VIX, linear in %otm, nonlinear in skew
    if option_type == 'P':
        implied_vol = vix_multiplier*vix + otm_multiplier*otm #+ skew_multiplier*math.pow((1 + otm),(skew_power)) * (-1) * skew \
                                                                                        #+ skew_multiplier * skew
    if option_type == 'C':
        #calls decrease in implied vol and then increase again
        #again we could improve the model
        otm_shift = abs(.08 - otm) - .08
        implied_vol = vix_multiplier*vix + otm_multiplier*otm_shift
        
    return implied_vol


#given market conditions, calculate how far OTM to place your strike
#Per Josh - FLOOR(EXP(D3/100*SQRT(1/12)*-Inputs!$B$4)*C3,1)
#what is the z-score that holds the most consistency 
#30 delta on a 10 vol? 30 delta on on a 30 vol?  - your mindset is going to change 
#vix is at record lows maybe we turn it off
#if vix is at a given range you can be more aggressive 

def calculate_strike(option_type, SPY, VIX, Z_SCORE):
    if option_type == 'P':
        return math.exp((VIX/100) * (math.pow(1/12, 1/2))*-Z_SCORE)*SPY
    if option_type == 'C': 
        return math.exp((VIX/100) * (math.pow(1/12, 1/2))*Z_SCORE)*SPY

from datetime import datetime
def is_third_friday(d):
    #d = datetime.strptime(s, '%b %d, %Y')
    return (d.weekday() == 4 and 15 <= d.day <= 21) or d in \
            [datetime.strptime('20Apr2000', '%d%b%Y'), datetime.strptime('16Apr1992', '%d%b%Y') \
             , datetime.strptime('17Apr2014', '%d%b%Y'), datetime.strptime('20Mar2008', '%d%b%Y') \
            ,datetime.strptime('17Apr2003', '%d%b%Y')]#scrub CME data '2000-4-20' '1992-4-16' '2003-4-17' '2008-03-20' '2014-4-17'





