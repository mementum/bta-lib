#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, SumN
from . import SEED_AVG, SEED_LAST


class kama(Indicator):
    '''
    Defined by Perry Kaufman in his book `"Smarter Trading"`.

    It is A Moving Average with a continuously scaled smoothing factor by
    taking into account market direction and volatility. The smoothing factor
    is calculated from 2 ExponetialMovingAverage smoothing factors, a fast one
    and slow one.

    If the market trends the value will tend to the fast ema smoothing
    period. If the market doesn't trend it will move towards the slow EMA
    smoothing period.

    It is a subclass of SmoothingMovingAverage, overriding once to account for
    the live nature of the smoothing factor

    Formula:
      - direction = close - close_period
      - volatility = sumN(abs(close - close_n), period)
      - effiency_ratio = abs(direction / volatility)
      - smoothing constant fast = 2 / (fast_period + 1)
      - smoothing constant slow = 2 / (slow_period + 1)

      - smoothing factor = pow(efficienty_ratio * (fast - slow) + slow), 2)
      - kama = ewm(data, alpha=smoothing factor, period=period)

    Notice that "smoothing factor" isn't a single value, hence the
    exponentially weighted moving average uses a value which changes for each
    step of the calculation.

    The standard seed is the simple moving average, use _seed=btalib.SEED_LAST
    to apply the "last" known value of the input as the seed (for compatibility
    this can be simply `True` or `1`)

    Because the dynamic smoothing constant has a larger period (+1) than the
    actual moving average, this average has alrady a seed value when the
    calculation can start. Hence the seed value (eithre the simple moving
    average or the last known value, is not seen because it can be calculated
    before the actual period comes in effect)

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:kaufman_s_adaptive_moving_average
      - http://fxcodebase.com/wiki/index.php/Kaufman's_Adaptive_Moving_Average_(KAMA)
      - http://www.metatrader5.com/en/terminal/help/analytics/indicators/trend_indicators/ama
      - http://help.cqg.com/cqgic/default.htm#!Documents/adaptivemovingaverag2.htm
    '''
    group = 'overlap'
    alias = 'KAMA', 'KaufmanAdaptiveMovingAverage'
    outputs = 'kama'
    params = (
        ('period', 30, 'Period to consider'),
        ('fast', 2, 'Fast exponential smoothing factor'),
        ('slow', 30, 'Slow exponential smoothing factor'),
        ('_seed', SEED_AVG, 'Default to use average of n periods as seed'),
        ('_pvol', 1, 'Lookback period for volatility calculation'),
    )

    def __init__(self):
        # Calculate components of effratio and the ratio itself
        direction = self.i0.diff(periods=self.p.period)
        volseries = self.i0.diff(periods=self.p._pvol)
        volatility = SumN(volseries.abs(), period=self.p.period)

        effratio = (direction / volatility).abs()  # efficiency ratio

        # smoothing constast alpha values for fast and slow ema behaviors
        scfast = 2.0 / (self.p.fast + 1.0)
        scslow = 2.0 / (self.p.slow + 1.0)

        # Calculate the "smoothing constant": alpha input for exp smoothing
        sc = (effratio * (scfast - scslow) + scslow).pow(2)

        # Get the _ewm window function and calculate the dynamic mean on it
        self.o.kama = self.i0._ewm(
            span=self.p.period, alpha=sc, _seed=self.p._seed)._mean()

    def _talib(self, kwdict):
        '''Apply las value as seed, instead of average of period values'''
        kwdict.setdefault('_seed', SEED_LAST)
