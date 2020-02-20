#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class avgprice(Indicator):
    '''
    Returns the average of the 4 OHLC price components

    Formula:
      - avg = (open + high + low + close) / 3

    See:
      - (None)
    '''
    group = 'price'
    alias = 'AvgPrice', 'AveragePrice', 'AVGPrice', 'AVGPRICE'
    inputs = 'open', 'high', 'low', 'close'
    outputs = 'avg'
    params = (
        ('divisor', 4.0, 'Factor to use in the division'),
    )

    def __init__(self):
        prices_sum = self.i.open + self.i.high + self.i.low + self.i.close
        self.o.avg = prices_sum / self.p.divisor


class typprice(Indicator):
    '''
    Delivers the typical price

    Formula:
      - tp = (high + low + close) / 3

    See:
      - https://en.wikipedia.org/wiki/Typical_price
    '''
    group = 'price'
    alias = 'typicalprice', 'TypicalPrice', 'TypPrice', 'TYPPRICE'
    inputs = 'high', 'low', 'close'
    outputs = 'tp'
    params = (
        ('divisor', 3.0, 'Factor to use in the division'),
    )

    def __init__(self):
        self.o.tp = (self.i.high + self.i.low + self.i.close) / self.p.divisor


class wclprice(Indicator):
    '''
    Delivers the Weighted Close Price

    Formula:
      - wcl = (high + low + close * 2) / 4

    See:
      - https://www.metastock.com/customer/resources/taaz/?p=124
      - http://www.ta-guru.com/Book/TechnicalAnalysis/TechnicalIndicators/WeightedClose.php5
    '''
    group = 'price'
    alias = 'WCLPrice', 'WeightedClosePrice', 'WCLPRICE', 'weightedcloseprice'
    inputs = 'high', 'low', 'close'
    outputs = 'wcl'
    params = (
        ('weight', 2.0, 'Weight Factor for close'),
        ('divisor', 4.0, 'Factor to use in the division'),
    )

    def __init__(self):
        wclose = self.i.close * self.p.weight
        self.o.wcl = (self.i.high + self.i.low + wclose) / self.p.divisor


class medprice(Indicator, inputs_override=True):
    '''
    Delivers the Median Price

    Formula:
      - med = (high + low) / 2.0

    See:
      - https://www.metastock.com/customer/resources/taaz/?p=70
    '''
    group = 'price'
    alias = 'WCLPrice', 'WeightedClosePrice', 'WCLPRICE', 'weightedcloseprice'
    # inputs = {'high': 'close'}, 'low'  # map "high" in place of default close
    inputs = 'high', 'low'  # inputs have been overriden in class def
    outputs = 'med'
    params = (
        ('divisor', 2.0, 'Factor to use in the division'),
    )

    def __init__(self):
        self.o.med = (self.i.high + self.i.low) / self.p.divisor
