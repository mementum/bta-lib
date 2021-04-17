#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class correl(Indicator):
    '''
    Rolling Pearson correlation of the two inputs `asset1` and `asset2`

    Note: the default inputs are named `high` and `low` to ensure an easy match
    with a multiple input (dataframe). But they can be anything

    See:
      - https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    '''
    group = 'statistic'
    alias = 'CORREL', 'Correl'
    inputs = 'high', 'low'
    outputs = 'correl'
    params = (
        ('period', 30, 'Period to consider'),
        ('_prets', 1, 'Lookback period to calculate the returns'),
        ('_rets', True, 'Calculate beta on returns'),
    )

    def __init__(self):
        self.o.correl = self.i0.rolling(window=self.p.period).corr(self.i1)
