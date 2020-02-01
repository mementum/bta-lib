#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, sma, highest, lowest


class stochastic(Indicator):
    '''
    By Dr. George Lane in the 50s. It compares a closing price to the price
    range and tries to show convergence if the closing prices are close to the
    extremes

      - It will go up if closing prices are close to the highs
      - It will go down if closing prices are close to the lows

    It shows divergence if the extremes keep on growing/decreasing but closing
    prices do not in the same manner (distance to the extremes increases)

    Formula:
      - hh = highest(high, period)
      - ll = lowest(low, period)
      - kfast = 100 * (close - ll) / (hh - ll)
      - k = MovingAverage(kfast, pfast)
      - d = MovingAverage(k, pslow)

    See:
      - http://en.wikipedia.org/wiki/Stochastic_oscillator
    '''
    group = 'momentum'
    alias = 'stoch', 'Stochastic', 'STOCHASTIC', 'STOCH'
    inputs = 'high', 'low', 'close'
    outputs = 'k', 'd'
    params = (
        ('period', 14, 'Period to consider'),
        ('pfast', 3, 'Fast smoothing period'),
        ('pslow', 3, 'Slow moving average period'),
        ('_ma', sma, 'Moving average to use'),
        ('_maslow', None, 'Slow moving average (if `None`, use same as fast)'),
    )

    def __init__(self):
        hh = highest(self.i.high, period=self.p.period)
        ll = lowest(self.i.low, period=self.p.period)
        kfast = 100.0 * (self.i.close - ll) / (hh - ll)

        self.o.k = k = self.p._ma(kfast, period=self.p.pfast)
        self.o.d = (self.p._maslow or self.p._ma)(k, period=self.p.pslow)

    def _talib(self, kwdict):
        '''Change period to 5'''
        kwdict.setdefault('period', 5)
