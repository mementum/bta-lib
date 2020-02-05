#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from .ema import _exp_smoothing


class smma(_exp_smoothing):
    '''
    Smoothed Moving Average used by Wilder in his 1978 book `New Concepts in
    Technical Trading`

    Defined in his book originally as:

      - new_value = (old_value * (period - 1) + new_data) / period

    Which is a moving average that smoothes data exponentially over time.

      - Exponential Smotthing factor: alpha = 1 / period

    Formula
      - prev = mean(data, period)
      - movav = prev * (1.0 - alpha) + newdata * alpha
      - (or alternatively #  movav = prev + alpha(new - prev))

    See also:
      - http://en.wikipedia.org/wiki/Moving_average#Modified_moving_average
    '''
    group = 'overlap'
    alias = 'SMMA', 'SmoothedMovingAverage', 'MMA', 'ModifiedMovingAverage'
    outputs = 'smma'
    params = (
        ('period', 30, 'Period for the moving average calculation'),
    )

    def __init__(self):  # use data prepared by base class
        period, _last = self.p.period, self.p._last
        self.o.smma = self.i0._ewm(com=period - 1, _last=_last).mean()
