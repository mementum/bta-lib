#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, ema


class dema(Indicator):
    '''
    DEMA was first time introduced in 1994, in the article "Smoothing Data with
    Faster Moving Averages" by Patrick G. Mulloy in "Technical Analysis of
    Stocks & Commodities" magazine.

    It attempts to reduce the inherent lag associated to Moving Averages

    Formula:
      - dema = (2.0 * ema(data, period)) - ema(ema(data, period), period)

    See:
      - https://en.wikipedia.org/wiki/Double_exponential_moving_average
    '''
    group = 'overlap'
    alias = 'DEMA', 'DoubleExponentialMovingAverage'
    outputs = 'dema'
    params = (
        ('period', 30, 'Period to consider'),
        ('_ma', ema, 'Moving Average to use'),
    )

    def __init__(self):
        ema1 = self.p._ma(self.i0, period=self.p.period)
        ema2 = self.p._ma(ema1, period=self.p.period)
        self.o.dema = 2.0 * ema1 - ema2
