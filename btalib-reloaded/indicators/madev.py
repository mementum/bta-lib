#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, sma

import numpy as np


class mad(Indicator):
    '''
    Calculates the Mean Absolute Deviation ('mad') of the input over a given
    period
    See:
      - https://en.wikipedia.org/wiki/Average_absolute_deviation
    '''
    group = 'statistic'
    alias = 'MAD', 'meandev', 'MeanDev', 'MeanDeviation', 'MeanAbsDeviation'
    outputs = 'meandev'
    params = (
        ('period', 20, 'Period to consider'),
        ('_ma', sma, 'Moving Average to use'),
    )

    _mad = lambda self, x: np.fabs(x - x.mean()).mean()  # noqa: E731

    def __init__(self, mean=None):
        r = self.i0.rolling(window=self.p.period)  # get rolling win of period
        self.o.meandev = r.apply(self._mad, raw=False)  # apply mean abs dev
