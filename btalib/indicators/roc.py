#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class _rocbase(Indicator):
    params = (
        ('period', 12, 'Period to consider',),
    )

    group = 'momentum'

    def __init__(self):
        self.o[0] = self.i0 / self.i0(-self.p.period)

    def _talib(self, kwdict):
        '''Change period to 10'''
        kwdict.setdefault('period', 10)


class roc(_rocbase):
    '''
    The ROC calculation compares the current price with the price n periods
    ago, to determine momentum the as the percent change in price. This version
    scales the percentage to 100.

      - roc = 100.0 * (data / data(-period) - 1.0)

    See:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum

    '''
    alias = 'rateofchange', 'ROC', 'RateOfChange'
    outputs = 'roc'

    def __init__(self):
        self.o.roc = 100.0 * (self.o.roc - 1.0)


class rocp(_rocbase):
    '''
    The ROC calculation compares the current price with the price n periods
    ago, to determine momentum the as the percent change in price.

    Formula:

      - rocp = data / data(-period) - 1.0

    See:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum
    '''
    alias = 'ROCP', 'RateOfChangePercentage'
    outputs = 'rocp'

    def __init__(self):
        self.o.rocp = self.o.rocp - 1.0


class rocr(_rocbase):
    '''
    The ROCR calculation compares the current price with the price n periods
    ago as a ratio to determine momentum.

    Formula:

      - rocr = data / data(-period)

    See:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum
    '''
    alias = 'ROCR', 'RateOfChangeRatio'
    outputs = 'rocr'


class rocr100(_rocbase):
    '''
    The ROCR calculation compares the current price with the price n periods
    ago as a ratio to determine momentum, scaled to 100.

    Formula:

      - rocr100 = 100.0 * data / data(-period)

    See:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:rate_of_change_roc_and_momentum
    '''
    alias = 'ROCR100', 'RateOfChangeRatio100'
    outputs = 'rocr100'

    def __init__(self):
        self.o.rocr100 = 100.0 * self.o.rocr100
