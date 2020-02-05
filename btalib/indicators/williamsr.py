#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, highest, lowest


class williamsr(Indicator):
    '''
    Developed by Larry Williams to show the relation of closing prices to
    the highest-lowest range of a given period.

    Known as Williams %R (but % is not allowed in Python identifiers)

    Formula:
      - num = highest(high, period) - close
      - den = highest(high, period) - lowest(low, period)
      -  %R = -100.0 * (num / den)

    See:
      - http://en.wikipedia.org/wiki/Williams_%25R
      - https://school.stockcharts.com/doku.php?id=technical_indicators:williams_r
    '''
    group = 'momentum'
    alias = 'willr', 'WilliamsR', 'WILLIAMSR', 'WILLR'
    inputs = 'high', 'low', 'close'
    outputs = 'r'
    params = (
        ('period', 14, 'Period to consider'),
    )

    def __init__(self):
        hh = highest(self.i.high, period=self.p.period)
        ll = lowest(self.i.low, period=self.p.period)
        self.o.r = -100.0 * (hh - self.i.close) / (hh - ll)
