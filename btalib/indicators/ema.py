#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator
from . import SEED_AVG


# _exp_smoothing acts as a ase class for exponential smoothing averages (ema,
# smma, ...), to prepare the data by
#
#   - Calculating the p1:p2 range which will be used to calculate the
#     single seed value with an arithmetic average (i.e.: "mean")
#     The following are true for p1 and p2
#       - p1 >= 0
#       - p2 >= (p1 + self.p.preiod)

#   - Creating a [0:p2] long seed array filled with NaN
#   - Calculating the mean of input[p1:p2] and putting it a p2
#   - Concatenating seed array + rest data and  storing it at outputs[0],
#     (output name is unknown but: subclasses will have an output)

# The parameter "poffset" allows to start the calulation at an offset. This
# is used to replicate the internal ta-lib behavior with ema when
# calculating the fast ema of the macd, where the start of the delivery of
# data is offset to the period of the slow ema.

# For regular usage, poffset is always 0 and plays no role. If poffset
# didn't exist, the calculation of p1 and p2 would simpler
#   - p1 = self._minperiod - 1
#   - p2 = p1 + self.p.period


class ema(Indicator):
    '''
    A Moving Average that smoothes data exponentially over time.

      - Exponential Smotthing factor: alpha = 2 / (1 + period)

    Formula
      - prev = mean(data, period)
      - movav = prev * (1.0 - alpha) + newdata * alpha
      - (or alternatively #  movav = prev + alpha(new - prev))

    See also:
      - http://en.wikipedia.org/wiki/Moving_average#Exponential_moving_average
    '''
    group = 'overlap'
    alias = 'EMA', 'ExponentialMovingAverage'
    outputs = 'ema'
    params = (
        ('period', 30, 'Period for the moving average calculation'),
        ('_seed', SEED_AVG, 'Default to use average of periods as seed'),
    )

    def __init__(self, poffset=0):  # see above for poffset
        span, seed, poff = self.p.period, self.p._seed, poffset
        self.o.ema = self.i0._ewm(span=span, _seed=seed, _poffset=poff).mean()
