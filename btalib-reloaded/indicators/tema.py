#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, ema


class tema(Indicator):
    '''
    TEMA was first time introduced in 1994, in the article "Smoothing Data with
    Faster Moving Averages" by Patrick G. Mulloy in "Technical Analysis of
    Stocks & Commodities" magazine.

    It attempts to reduce the inherent lag associated to Moving Averages

    Formula:
      - ema1 = ema(data, period)
      - ema2 = ema(ema1, period)
      - ema3 = ema(ema2, period)
      - tema = 3 * ema1 - 3 * ema2 + ema3

    See:
      - https://en.wikipedia.org/wiki/Triple_exponential_moving_average
    '''
    group = 'overlap'
    alias = 'TEMA', 'TripleExponentialMovingAverage'
    outputs = 'tema'
    params = (
        ('period', 30, 'Period to consider'),
        ('_ma', ema, 'Moving Average to use'),
    )

    def __init__(self):
        ema1 = self.p._ma(self.i0, period=self.p.period)
        ema2 = self.p._ma(ema1, period=self.p.period)
        ema3 = self.p._ma(ema2, period=self.p.period)
        self.o.tema = 3.0 * ema1 - 3.0 * ema2 + ema3
