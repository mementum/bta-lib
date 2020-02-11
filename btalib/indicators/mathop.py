#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator




# ## over a period

class max(Indicator):
    '''
    Rolling maximum over `period` of the input

    Formula:
      - highest = max(data, period)
    '''
    group = 'mathop'
    alias = 'highest', 'Highest', 'maxn', 'MaxN', 'MAX'
    outputs = 'highest'
    params = (
        ('period', 30, 'Period to consider'),
    )

    def __init__(self):
        self.o.highest = self.i0.rolling(window=self.p.period).max()


class min(Indicator):
    '''
    Rolling minimum over `period` of the input

    Formula:
      - lowest = min(data, period)
    '''
    group = 'mathop'
    alias = 'lowest', 'Lowest', 'minn', 'MinN', 'MIN'
    outputs = 'lowest'
    params = (
        ('period', 30, 'Period to consider'),
    )

    def __init__(self):
        self.o.lowest = self.i0.rolling(window=self.p.period).min()


class sum(Indicator):
    '''
    Rolling sum over `period` of the input

    Formula:
      - sum = sum(data, period)
    '''
    group = 'mathop'
    alias = 'sumn', 'Sum', 'SumN', 'SUM'
    outputs = 'sum'
    params = (
        ('period', 30, 'Period to consider'),
    )

    def __init__(self):
        self.o.sum = self.i0.rolling(window=self.p.period).sum()
