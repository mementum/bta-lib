#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator

import itertools

import numpy as np


# ## over the entire series

class add(Indicator):
    '''
    Calculates the summation of the two inputs

    Formula:
      - add = data0 + data1
    '''
    group = 'mathop'
    alias = 'ADD'
    inputs = 'input1', 'input2'
    outputs = 'add'

    def __init__(self):
        self.o.add = self.i.input1 + self.i.input2


class div(Indicator):
    '''
    Calculates the division of the two inputs

    Formula:
      - div = data0 / data1
    '''
    group = 'mathop'
    alias = 'DIV'
    inputs = 'input1', 'input2'
    outputs = 'div'

    def __init__(self):
        self.o.div = self.i.input1 / self.i.input2


class mult(Indicator):
    '''
    Calculates the multiplication of the two inputs

    Formula:
      - mult = data0 * data1
    '''
    group = 'mathop'
    alias = 'MULT'
    inputs = 'input1', 'input2'
    outputs = 'mult'

    def __init__(self):
        self.o.mult = self.i.input1 * self.i.input2


class sub(Indicator):
    '''
    Calculates the subtraction of the two inputs

    Formula:
      - sub = data0 - data1
    '''
    group = 'mathop'
    alias = 'SUB'
    inputs = 'input1', 'input2'
    outputs = 'sub'

    def __init__(self):
        self.o.sub = self.i.input1 - self.i.input2


# ## over a period

class max(Indicator):
    '''
    Rolling maximum over `period` of the input

    Formula:
      - max = max(data, period)
    '''
    group = 'mathop'
    alias = 'highest', 'Highest', 'maxn', 'MaxN', 'MAX'
    outputs = 'max'
    params = (
        ('period', 30, 'Period to consider'),
    )

    def __init__(self):
        self.o.max = self.i0.rolling(window=self.p.period).max()


class min(Indicator):
    '''
    Rolling minimum over `period` of the input

    Formula:
      - min = min(data, period)
    '''
    group = 'mathop'
    alias = 'lowest', 'Lowest', 'minn', 'MinN', 'MIN'
    outputs = 'min'
    params = (
        ('period', 30, 'Period to consider'),
    )

    def __init__(self):
        self.o.min = self.i0.rolling(window=self.p.period).min()


class minmax(Indicator):
    '''
    Rolling the minimum and maximo over `period` of the input

    Formula:
      - min = min(data, period)
      - min = max(data, period)
    '''
    group = 'mathop'
    alias = 'MINMAX'
    outputs = 'min', 'max'
    params = (
        ('period', 30, 'Period to consider'),
    )

    def __init__(self):
        self.o.min = min(self.i0, period=self.p.period)
        self.o.max = max(self.i0, period=self.p.period)


class maxindex(Indicator):
    '''
    Rolling index of the max value over a period

    Formula:
      - maxindex = data.index(max(data, period))
    '''
    group = 'mathop'
    alias = 'MAXINDEX'
    outputs = 'maxindex'
    params = (
        ('period', 30, 'Period to consider'),
        ('_absidx', False, 'Return maxindex over the entire period'),
    )

    def _argmax(self, x):
        return np.argmax(x) + (next(self._count) * self.p._absidx)

    def __init__(self):
        i0rolling = self.i0.rolling(window=self.p.period)  # prep rolling win

        if not self.p._absidx:  # maxindex relative to window period
            self.o.maxindex = i0rolling.apply(np.argmax)
        else:
            # maxindex is absolute with respect to all previous vals in array
            self._count = itertools.count()  # help win rel-index => absolute
            self.o.maxindex = i0rolling.apply(self._argmax)._series.fillna(0)
            # using the raw _series resets period to 1, fillna fills as ta-lib

    def _talib(self, kwdict):
        '''ta-lib returns 0 as index during the warm-up period and then returns the
        absolute index over the entire series and not over the window period
        '''
        kwdict.setdefault('_absidx', True)


class minindex(Indicator):
    '''
    Rolling index of the max value over a period

    Formula:
      - maxindex = data.index(max(data, period))
    '''
    group = 'mathop'
    alias = 'MININDEX'
    outputs = 'minindex'
    params = (
        ('period', 30, 'Period to consider'),
        ('_absidx', False, 'Return maxindex over the entire period'),
    )

    def _argmin(self, x):
        return np.argmin(x) + (next(self._count) * self.p._absidx)

    def __init__(self):
        i0rolling = self.i0.rolling(window=self.p.period)  # prep rolling win

        if not self.p._absidx:  # maxindex relative to window period
            self.o.minindex = i0rolling.apply(np.argmin)
        else:
            # maxindex is absolute with respect to all previous vals in array
            self._count = itertools.count()  # help win rel-index => absolute
            self.o.minindex = i0rolling.apply(self._argmin)._series.fillna(0)
            # using the raw _series resets period to 1, fillna fills as ta-lib

    def _talib(self, kwdict):
        '''ta-lib returns 0 as index during the warm-up period and then returns the
        absolute index over the entire series and not over the window period
        '''
        kwdict.setdefault('_absidx', True)


class minmaxindex(Indicator):
    '''
    Rolling index of the max value over a period

    Formula:
      - maxindex = data.index(max(data, period))
    '''
    group = 'mathop'
    alias = 'MINMAXINDEX'
    outputs = 'minindex', 'maxindex'
    params = (
        ('period', 30, 'Period to consider'),
        ('_absidx', False, 'Return maxindex over the entire period'),
    )

    def __init__(self, **kwargs):
        kwargs.update(**self.params)
        self.o.minindex = minindex(self.i0, **kwargs)
        self.o.maxindex = maxindex(self.i0, **kwargs)

    def _talib(self, kwdict):
        '''ta-lib returns 0 as index during the warm-up period and then returns
        the absolute index over the entire series and not over the window
        period
        '''
        kwdict.setdefault('_absidx', True)
        kwdict.setdefault('_talib', True)  # re-set value for sub-indicators


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
