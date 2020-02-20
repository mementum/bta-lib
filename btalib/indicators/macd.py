#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, ema


class macd(Indicator):
    '''
    Moving Average Convergence Divergence. Defined by Gerald Appel in the 70s.

    It measures the distance of a fast and a slow moving average to try to
    identify the trend.

    A second lagging moving average over the convergence-divergence should
    provide a "signal" upon being crossed by the macd

    Formula:
      - macd = ma(data, pfast) - ma(data, pslow)
      - signal = ma(macd, psignal)
      - histogram = macd - signal

    See:
      - http://en.wikipedia.org/wiki/MACD
    '''
    group = 'momentum'
    alias = 'MACD', 'MovingAverageConvergenceDivergence', 'MACDEXT', 'MACDFIX'
    outputs = 'macd', 'signal', 'histogram'
    params = (
        ('pfast', 12, 'Fast moving average period'),
        ('pslow', 26, 'Slow moving average period'),
        ('psignal', 9, 'Signal smoothing period'),
        ('_ma', ema, 'Moving average to use'),
        ('_masig', None, 'Signal moving average (if `None`, same as others)'),
    )

    def __init__(self):
        ma1 = self.p._ma(self.i0, period=self.p.pfast, **self._talibkw)
        ma2 = self.p._ma(self.i0, period=self.p.pslow)
        self.o.macd = ma1 - ma2

        masignal = self.p._masig or self.p._ma  # determine movav for signal
        self.o.signal = masignal(self.o.macd, period=self.p.psignal)

        self.o.histogram = self.o.macd - self.o.signal  # simple diff of others

    _talibkw = {}  # hold kwargs for ta-lib compatibility if requested

    def _talib(self, kwdict):
        '''Start fast ema calc delivery at the offset of the slow ema'''
        # Determine pslow param (from user or default) and pass it to ema as
        # the offset for the 1st data delivery of the calculations
        pslow = kwdict.get('pslow', self.__class__.params.get('pslow'))

        # _talibkw is a class attribute (empty dict)
        # This create a *specifi*  instance attribute obscuring the class
        # attibute and filled with a value.
        self._talibkw = {'poffset': pslow}
