#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, mad, sma


class cci(Indicator):
    '''
    Introduced by Donald Lambert in 1980 to measure variations of the
    "typical price" (see below) from its mean to identify extremes and
    reversals

    Formula:
      - tp = typical_price = (high + low + close) / 3
      - tpmean = MovingAverage(tp, period)
      - deviation = tp - tpmean
      - meandev = MeanDeviation(tp)
      - cci = deviation / (meandeviation * factor)

    See:
      - https://en.wikipedia.org/wiki/Commodity_channel_index
    '''
    group = 'momentum'
    alias = 'CCI', 'CommodityChannelIndex'
    inputs = 'high', 'low', 'close'
    outputs = 'cci'
    params = (
        ('period', 20, 'Period to consider'),
        ('factor', 0.015, 'Channel width factor'),
        ('_ma', sma, 'Moving Average to sue'),
        ('_dev', mad, 'Deviation to use (Def: Mean Abs Dev)'),
    )

    def __init__(self):
        tp = (self.i.high + self.i.low + self.i.close) / 3.0  # typical price
        tpmean = self.p._ma(tp, period=self.p.period)  # mean of tp
        madev = mad(tp, period=self.p.period)  # mean abs deviation of tp
        self.o.cci = (tp - tpmean) / (madev * self.p.factor)  # cci formula

    def _talib(self, kwdict):
        '''Change period to 14'''
        kwdict.setdefault('period', 14)
