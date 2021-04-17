#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, sma, stddev


class bbands(Indicator):
    '''
    Defined by John Bollinger in the 80s. It measures volatility by defining
    upper and lower bands at distance x standard deviations

    Formula:
      - midband = SimpleMovingAverage(close, period)
      - topband = midband + devfactor * StandardDeviation(data, period)
      - botband = midband - devfactor * StandardDeviation(data, period)

    See:
      - http://en.wikipedia.org/wiki/Bollinger_Bands
    '''
    group = 'overlap'
    alias = 'BBANDS', 'BollingerBands', 'BOLLINGERBANDS'
    outputs = 'mid', 'top', 'bot'
    params = (
        ('period', 20, 'Period to consider'),
        ('devs', 2.0, 'Standard Deviations of Top/Bottom Bands'),
        ('_ma', sma, 'Moving average to use'),
        ('_stdev', stddev, 'Standard Deviation Calculation to use'),
    )

    def __init__(self):
        self.o.mid = mid = self.p._ma(self.i0, period=self.p.period)

        devdist = self.p.devs * stddev(self.i0, period=self.p.period)
        self.o.top = mid + devdist
        self.o.bot = mid - devdist

    def _talib(self, kwdict):
        '''Change period to 5'''
        kwdict.setdefault('period', 5)
