#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, ema, ewma


class ad(Indicator):
    '''
    Originally the "Cumulative Money Flow Line" by Mark Chaikin, which attempts
    to measure the incoming and outgoing flow of money by using the volume in
    addition the standard price components.

    Formula:
      - mfm = ((close - high) + (close - low)) / (high - low)
        - ergo: mfm = (2*close - high - low) / (high - low)

      - mfv = mf * volume
      - ad = cumulative_sum(mvf)

    See also:
      - https://en.wikipedia.org/wiki/Accumulation/distribution_index
      - https://school.stockcharts.com/doku.php?id=technical_indicators:accumulation_distribution_line
    '''
    group = 'volume'
    alias = 'AD', 'adl', 'ADL', 'ChaikinAD', 'ChaikinADL', 'chaikinad'
    inputs = 'high', 'low', 'close', 'volume'
    outputs = 'ad'

    def __init__(self):
        hilo = self.i.high - self.i.low

        mfm = (2.0 * self.i.close - self.i.high - self.i.low) / hilo
        mfv = mfm * self.i.volume  # money flow volume
        self.o.ad = mfv.cumsum()  # ad line


class adosc(ad):
    '''
    The Chaikin Oscillator applies a `MACD` formula to the
    Accumulation/Distribution Line (`ad`) to calculate the momentum of the
    money flow.

    See also:
      - https://en.wikipedia.org/wiki/Chaikin_Analytics#Chaikin_Oscillator
      - https://school.stockcharts.com/doku.php?id=technical_indicators:chaikin_oscillator
      - https://www.metastock.com/customer/resources/taaz/?p=41
    '''
    alias = 'ADOSC', 'ChaikinADOSC', 'ChaikinOsc', 'ChaikinOscillator'
    outputs = 'adosc'  # automapping output adosc to ad from base class

    params = (
        ('pfast', 3, 'Fast ema period'),
        ('pslow', 10, 'Slow ema period'),
        ('_ma', ema, 'Moving average to use'),
    )

    def __init__(self):
        ma3 = self.p._ma(self.o.ad, period=self.p.pfast)
        ma10 = self.p._ma(self.o.ad, period=self.p.pslow)
        self.o.adosc = ma3 - ma10

    def _talib(self, kwdict):
        '''Switch to `ewma` (i.e.: *exponential weighted moving mean* with no seed
        instead of using a standard `ema` exponential moving average
        '''
        kwdict.setdefault('_ma', ewma)
