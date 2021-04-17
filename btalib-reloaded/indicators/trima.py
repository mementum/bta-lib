#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, sma


class trima(Indicator):
    '''
    The Triangular Moving Average (TRIMA) is an average of an average, similar
    to the `sma` but placing more weight on the middle values due to the second
    smoothing.

    Formula:
      - if period is odd: p1 = p2 = (period + 1) // 2
      - if period is even: p1, p2 = (p // 2) + 1, p //2
      - trima = sma(sma(data, p2), p1)

    See also:
      - https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/triangular-moving-average-trima/
    '''
    group = 'overlap'
    alias = 'TRIMA', 'TriangularMovingAverage'
    outputs = 'trima'
    params = (
        ('period', 30, 'Period for the moving average calculation'),
        ('_ma', sma, 'Moving average to use'),
    )

    def __init__(self):
        p = self.p.period
        if p % 2:  # odd
            p1 = p2 = (p + 1) // 2
        else:
            p1, p2 = (p // 2) + 1, p // 2

        self.o.trima = sma(sma(self.i0, period=p2), period=p1)
