#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, highest, lowest


class midprice(Indicator, inputs_override=True):
    '''
    Calculates the middle price of the highest high/lowest low across a period

    Formula:
      - midprice = (Highest(high, period) + Lowest(low, period)) / 2.0

    See:
      - https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/midprice-midpri/
    '''
    group = 'overlap'
    alias = 'MIDPRICE', 'MidPrice'
    inputs = 'high', 'low'  # notice inputs_override in class def
    outputs = 'midprice'
    params = (
        ('period', 14, 'Period to consider'),
    )

    def __init__(self):
        hh = highest(self.i.high, period=self.p.period)
        ll = lowest(self.i.low, period=self.p.period)
        self.o.midprice = (hh + ll) / 2.0


class midpoint(Indicator):
    '''
    Calculates the middle price of the highest/lowest price across a period

    Formula:
      - midpoint = (Highest(close, period) + Lowest(close, period)) / 2.0

    See:
      - https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/midpoint-midpnt/
    '''
    group = 'overlap'
    alias = 'MIDPOINT', 'MidPoint'
    outputs = 'midpoint'
    params = (
        ('period', 14, 'Period to consider'),
    )

    def __init__(self):
        self.o.midpoint = midprice(self.i0, self.i0, period=self.p.period)
