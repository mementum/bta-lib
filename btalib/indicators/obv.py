#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, _DECPERIOD, _MINIDX

import numpy as np


class obv(Indicator):
    '''
    Originally called "continuous volume" by Woods and Vignola, it was later
    named "on-balance volume" by Joseph Granville in his 1963 book Granville's
    New Key to Stock Market Profits.

    On Balance Volume (OBV) measures buying and selling pressure as a
    cumulative indicator, adding volume on up days and subtracting it on down
    days.

    Formula:
      - close > close(-1) => vol_pressure = +volume
      - close < close(-1) => vol_pressure = -volume
      - close == close(-1) => vol_pressure = 0

      - obv = obv(-1) + vol_pressure

    See also:
      - https://en.wikipedia.org/wiki/On-balance_volume
      - https://www.investopedia.com/terms/o/onbalancevolume.asp
      - https://school.stockcharts.com/doku.php?id=technical_indicators:on_balance_volume_obv
    '''
    group = 'volume'
    alias = 'OBV', 'OnBalanceVolume'
    inputs = 'close', 'volume'  # close was in base class, no issue repeating
    outputs = 'obv'
    params = (
        ('_period', 1, 'Period for `close` comparison'),
    )

    def __init__(self):
        close1 = self.i.close.diff(periods=self.p._period)

        if self._talib_:  # ## black voodoo to overcome ta-lib errors
            _DECPERIOD(close1)  # force period reduction to propagate use
            close1[_MINIDX(close1)] = 1.0  # force use 1st value POSITIVE

        self.o.obv = (self.i.volume * close1.apply(np.sign)).cumsum()

        # non-numpy alternative also one-line vectorized formulation
        # self.o.obv = (self.i.volume * (close1 / close1.abs())).cumsum()

    _talib_ = False

    def _talib(self, kwdict):
        '''Use first day volume as *positive* seed value'''
        self._talib_ = True
