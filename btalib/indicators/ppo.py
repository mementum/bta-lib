#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, ema, sma


class _posc(Indicator):
    '''Base clas or po (points) and ppo (percentage)'''

    _fast = False

    params = (
        ('pfast', 12, 'Fast moving average period'),
        ('pslow', 26, 'Slow moving average period'),
        ('_ma', ema, 'Moving average to use'),
    )

    def __init__(self):
        self.ma1 = self.p._ma(self.i0, period=self.p.pfast)
        self.ma2 = self.p._ma(self.i0, period=self.p.pslow)
        if self._fast:  # swap the moving averages for ppofast
            self.ma1, self.ma2 = self.ma2, self.ma1

    def _talib(self, kwdict):
        '''Set moving average to sma instead of ema'''
        kwdict.setdefault('_ma', sma)


class apo(_posc):
    '''
    Shows the difference between a short and long exponential moving
    averages expressed in points, unlike the `ppo` which does in percent values

    Formula:
      - apo = ema(data, pfast) - ema(data, pslow)

    See:
      - http://www.metastock.com/Customer/Resources/TAAZ/?c=3&p=94
      - https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/absolute-price-oscillator-apo/
    '''
    group = 'momentum'
    alias = 'APO', 'AbsolutePriceOscillator', 'PriceOscillator'
    outputs = 'apo'

    def __init__(self):
        self.o.apo = self.ma1 - self.ma2


class ppo(_posc):
    '''
    Shows the difference between a fast and slow exponential moving
    averages expressed in percentage. The MACD does the same but expressed in
    absolute points.

    Expressing the difference in percentage allows to compare the indicator at
    different points in time when the underlying value has significatnly
    different values.

    Formula:
      - ppo = 100.0 * (ema(data, pfast)/ema(data, pslow) - 1.0)

    See:
      - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:price_oscillators_ppo
    '''
    group = 'momentum'
    alias = 'PPO', 'PercentagePriceOscillator'
    outputs = 'ppo', 'signal', 'histogram'
    params = (
        ('psignal', 9, 'Signal smoothing period'),
        ('_masig', None, 'Signal moving average (if `None`, same as others)'),
    )

    def __init__(self):
        self.o.ppo = 100.0 * (self.ma1 / self.ma2 - 1.0)  # base class stored
        masignal = self.p._masig or self.p._ma  # determine movav for signal
        self.o.signal = masignal(self.o.ppo, period=self.p.psignal)
        self.o.histogram = self.o.ppo - self.o.signal


class ppofast(_posc):
    '''
    Shows the difference between a fast and slow exponential moving
    averages expressed in percentage. The MACD does the same but expressed in
    absolute points.

    Expressing the difference in percentage allows to compare the indicator at
    different points in time when the underlying value has significatnly
    different values.

    Most on-line literature shows the percentage calculation having the long
    exponential moving average as the denominator. Some sources like MetaStock
    use the fast one.

    Formula:
      - ppo = 100.0 *  (1.0 - ema(data, pslow) / ema(data, pshort))
      - Alternative = ppo = 100.0 - 100.0 * (ema_slow / ema_fast)

    See:
      - http://www.metastock.com/Customer/Resources/TAAZ/?c=3&p=94
    '''
    group = 'momentum'
    alias = 'PPOFast', 'PercentagePriceOscillatorFast'
    outputs = 'ppo', 'signal', 'histogram'
    params = (
        ('psignal', 9, 'Signal smoothing period'),
        ('_masig', None, 'Signal moving average (if `None`, same as others)'),
    )

    def __init__(self):
        self.o.ppo = 100.0 * (self.ma1 / self.ma2 - 1.0)  # base class stored
        masignal = self.p._masig or self.p._ma  # determine movav for signal
        self.o.signal = masignal(self.o.ppo, period=self.p.psignal)
        self.o.histogram = self.o.ppo - self.o.signal

    _fast = True  # base class will swap fast/slow calculations
