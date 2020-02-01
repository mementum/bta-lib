#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class sma(Indicator):
    '''
    Non-weighted average of the last n periods

    Formula:
      - movav = Sum(data, period) / period

    See also:
      - http://en.wikipedia.org/wiki/Moving_average#Simple_moving_average
    '''
    group = 'overlap'
    alias = 'SMA', 'SimpleMovingAverage'
    outputs = 'sma'
    params = (
        ('period', 30, 'Period for the moving average calculation'),
    )

    def __init__(self):
        self.o.sma = self.i0.rolling(window=self.p.period).mean()
