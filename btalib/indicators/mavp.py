#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, sma


def _mavp(closes, periods, **ma):
    # kwargs cannot have ints as keys, re-convert them
    ma = {int(k): v for k, v in ma.items()}
    for i, c in enumerate(closes):
        closes[i] = ma[periods[i]][i]

    return closes


class mavp(Indicator):
    '''
    Moving Average Variable Period.

    It takes two inputs of equal length

      - data (usually the "close"
      - periods

    It delivers for each timepoint "i", the value of the moving average
    dictated by period[i], at point it (movingaverage[i])

    Formula:
      - mavp[i] = MovingAverage(data, period[i])[i]

    See also:
      - (None)
    '''
    group = 'overlap'
    alias = 'MAVP', 'MovingAverageVariablePeriod'
    inputs = 'close', 'periods'
    outputs = 'mavp'
    params = (
        ('minperiod', 2, 'Minimum allowed period for the moving averages'),
        ('maxperiod', 30, 'Maximum allowed period for the moving averages'),
        ('_ma', sma, 'Moving Average to use'),
    )

    def __init__(self):
        periods = self.i.periods
        # restrict to min/max period
        periods = periods.clip(lower=self.p.minperiod, upper=self.p.maxperiod)

        # Calculate only the needed mas by getting the unique periods
        uperiods = periods.unique()  # capped and unique now
        # use str(p) to be able to pass it as kwargs in _apply
        ma = {str(p): self.p._ma(self.i.close, period=p) for p in uperiods}

        # ta-lib delivers at param "maxperiod" and not where already possible
        maxp = max(uperiods) if not self._talib_ else self.p.maxperiod

        pclose = self.i.close._period(maxp, rolling=True)
        self.o.mavp = pclose._apply(_mavp, periods, raw=True, **ma)
