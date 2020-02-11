#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


# ## over the entire series

class add(Indicator, inputs_override=True):
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


class div(Indicator, inputs_override=True):
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


class mult(Indicator, inputs_override=True):
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


class sub(Indicator, inputs_override=True):
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
