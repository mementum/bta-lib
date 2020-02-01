#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, ema


class trix(Indicator):
    '''
    Defined by Jack Hutson in the 80s and shows the Rate of Change (%) or slope
    of a triple exponentially smoothed moving average

    Formula:
      - ema1 = EMA(data, period)
      - ema2 = EMA(ema1, period)
      - ema3 = EMA(ema2, period)
      - trix = 100 * (ema3 / ema3(1) - 1)
        Where -1 is the lookback period to consider the rate of change

      The final formula can be simplified to: 100 * (ema3 / ema3(-1) - 1)

    The moving average used is the one originally defined by Wilder,
    the SmoothedMovingAverage

    See:
      - https://en.wikipedia.org/wiki/Trix_(technical_analysis)
      - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:trix
    '''
    group = 'momentum'
    alias = 'Trix', 'TRIX'
    outputs = 'trix'
    params = (
        ('period', 30, 'Period to consider'),
        ('_ma', ema, 'Moving average to use'),
    )

    def __init__(self):
        ema1 = self.p._ma(self.i0, period=self.p.period)
        ema2 = self.p._ma(ema1, period=self.p.period)
        ema3 = self.p._ma(ema2, period=self.p.period)
        self.o.trix = 100.0 * (ema3 / ema3(-1) - 1.0)
