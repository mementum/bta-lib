#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, rsi, sma, highest, lowest


class stochrsi(Indicator):
    '''
    Presented by Chande and Kroll the 1990 book: "The New Technical Trader".
    The RSI is fed into a atochastic-like calculation to increase its
    sensitivity.

    The recommendation is to keep the period for looking for highest highes and
    lowest lows the same as the for the RSI, but it can be played with for
    experimentation.

    Scaling to 100 is also suggested as a possiblity (the range is 0.0 => 1.0)

    Formula:

      - rsi = RSI(data, period)
      - maxrsi = Highest(rsi, period)
      - minrsi = Lowest(rsi, period)

      - stochrsi = (rsi - minrsi) / (maxrsi - minrsi)

    See
      - https://school.stockcharts.com/doku.php?id=technical_indicators:stochrsi
    '''
    group = 'momentum'
    alias = 'StochRsi', 'STOCHRSI'
    outputs = 'stochrsi'
    params = (
        ('period', 14, 'Period to consider'),
        ('_philo', None, 'Period for highest/lowest (None => period)'),
        ('_scale', 1.0, 'Scale the result by this factor'),
    )

    def __init__(self, _pfast=None, _ma=None):
        philo = self.p._philo or self.p.period  # set highest/lowest period

        r = rsi(self.i0, period=self.p.period)  # rsi
        maxrsi = highest(r, period=philo)  # max in period
        minrsi = lowest(r, period=philo)  # min in period
        self.o.stochrsi = (r - minrsi) / (maxrsi - minrsi) * self.p._scale

        if _pfast:  # set by _talib. A 2nd output d will have been defined
            self.o.d = _ma(self.o.stochrsi, period=_pfast)

    def _talib(self, kwdict):
        '''
        ta-lib uses internally the fast stochastic to calculate the stochrsi,
        with these side-effects

          - The scale changes from 0.0-1.0 to 0.0-100.0

          - A 2nd output is returned (stochrsi as defined by its authors has
            only 1 output)

          - The highest/lowest period is no longer symmetric with the rsi
            period

        Compatibility does this
          - Change the scale to 0.0-100.0
          - Change the highest/lowest period 5
          - Add a 2nd output named 'd' (as the 2nd output of the stochastic)
          - Run a simple moving average on it of period 3
        '''
        # Change regular play-with parameters to match ta-lib expectations
        kwdict.setdefault('_philo', 5)
        kwdict.setdefault('_scale', 100.0)

        # 2nd output - ta-lib extra parameters defined as kwargs to __init__
        self.o.__slots__.append('d')  # add real-time second output
        kwdict.setdefault('_pfast', 3)  # defined in kwargs
        kwdict.setdefault('_ma', sma)  # defined in kwargs
