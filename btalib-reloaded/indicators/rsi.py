#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, smma


class rsi(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    It measures momentum by calculating the ration of higher closes and
    lower closes after having been smoothed by an average, normalizing
    the result between 0 and 100

    Formula:
      - up = upday(data)  # max(close - close(-1), 0.0)
      - down = downday(data)  # abs( min(close - close(-1), 0.0) )
      - maup = movingaverage(up, period)
      - madown = movingaverage(down, period)
      - rs = maup / madown
      - rsi = 100 - 100 / (1 + rs)

    The moving average used is the one originally defined by Wilder,
    the SmoothedMovingAverage

    See:
      - http://en.wikipedia.org/wiki/Relative_strength_index
    '''
    group = 'momentum'
    alias = 'RSI', 'RelativeStrengthIndex'
    outputs = 'rsi'
    params = (
        ('period', 14, 'Period to consider'),
        ('lookback', 1, 'Lookback for up/down days'),
        ('_ma', smma, 'Smoothing moving average'),
    )

    def __init__(self):
        upday = self.i0.diff(periods=self.p.lookback).clip(lower=0.0)
        downday = self.i0.diff(periods=self.p.lookback).clip(upper=0.0).abs()
        maup = self.p._ma(upday, period=self.p.period)
        madown = self.p._ma(downday, period=self.p.period)
        rs = maup / madown
        self.o.rsi = 100.0 - 100.0 / (1.0 + rs)
