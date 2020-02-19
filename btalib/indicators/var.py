#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class var(Indicator):
    '''
    Variance is the expectation of the squared deviation of a random variable
    from its mean

    See:
      - https://en.wikipedia.org/wiki/Variance
    '''
    group = 'statistic'
    alias = 'VAR', 'Var'
    outputs = 'var'
    params = (
        ('period', 5, 'Period to consider'),
        ('ddof', 0, 'Degree of Freedom: 0 = population, > 0 sample'),
    )

    def __init__(self):
        self.o.var = (
            self.i0.rolling(window=self.p.period).var(ddof=self.p.ddof))


class var_s(var):
    '''
    Variance is the expectation of the squared deviation of a random variable
    from its mean

    This version considers the population is a sample (ddof=1)

    See:
      - https://en.wikipedia.org/wiki/Variance
    '''
    group = 'statistic'
    alias = 'varsample', 'VARS', 'VarSample'
    params = (
        ('ddof', 1, 'Degree of Freedom: 0 = population, > 0 sample'),
    )
