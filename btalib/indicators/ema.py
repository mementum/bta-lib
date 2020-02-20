#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, SEED_AVG

# named argument poffset in __init__ below is for compatibility with ta-lib
# broken MACD. When poffset > period, the delivery of the 1st valid value
# happens at poffset instead of at period
# The start of the calculation is accordingly delayed: poffset - period


class ema(Indicator):
    '''
    A Moving Average that smoothes data exponentially over time.

      - Exponential Smotthing factor: alpha = 2 / (1 + period)

    Formula
      - prev = mean(data, period)
      - movav = prev * (1.0 - alpha) + newdata * alpha
      - (or alternatively #  movav = prev + alpha(new - prev))

    See also:
      - http://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    '''
    group = 'overlap'
    alias = 'EMA', 'ExponentialMovingAverage'
    outputs = 'ema'
    params = (
        ('period', 30, 'Period for the moving average calculation'),
        ('_seed', SEED_AVG, 'Default to use average of periods as seed'),
    )

    def __init__(self, poffset=0):  # see above for poffset
        span, seed, poff = self.p.period, self.p._seed, poffset
        self.o.ema = self.i0._ewm(span=span, _seed=seed, _poffset=poff).mean()
