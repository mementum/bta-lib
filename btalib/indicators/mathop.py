#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class max(Indicator):
    '''
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
