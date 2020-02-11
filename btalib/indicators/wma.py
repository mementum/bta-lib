#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator

import numpy as np


class wma(Indicator):
    '''
    A Moving Average which gives an arithmetic weighting to values with the
    newest having the more weight

    Formula:
      - weights = range(1, period + 1)
      - coef = 2 / (period * (period + 1))
      - movav = coef * Sum(weight[i] * data[period - i] for i in range(period))

    See also:
      - http://en.wikipedia.org/wiki/Moving_average#Weighted_moving_average
    '''
    group = 'overlap'
    alias = 'WMA', 'WeightedMovingAverage'
    outputs = 'wma'
    params = (
        ('period', 30, 'Period for the moving average calculation'),
        ('coef', 1.0),
    )

    def __init__(self):
        # pre-calculate coe
        # weights = np.array([x for x in range(1, self.p.period + 1)])  # weights
        weights = np.array(list(range(1, self.p.period + 1)))  # weights
        _wma = lambda x: np.dot(x, weights)  # closure  # noqa: E731

        coef = 2.0 / (self.p.period * (self.p.period + 1))  # calc coef &
        self.o.wma = coef * self.i0.rolling(window=self.p.period).apply(_wma)
