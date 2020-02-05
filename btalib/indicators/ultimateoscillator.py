#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, SumN, truelow, truerange


class ultimateoscillator(Indicator):
    '''
    Developed by Larry Williams. It is based on notion of buying or selling
    pressure by considering where where a the closing price is within the true
    range.

    Formula (default values):
      - bp = close - truelow(low, close)  # buying pressure
      - tr = truerange(high, low, close)
      - av7 = Sum(bp, 7) / Sum(tr, 7)
      - av14 = Sum(bp, 14) / Sum(tr, 14)
      - av28= Sum(bp, 28) / Sum(tr, 28)
      - uo = 100 * (4*av7 + 2*av14 + av18) / (4 + 2 + 1)

    See:
      - https://en.wikipedia.org/wiki/Ultimate_oscillator
      - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:ultimate_oscillator
    '''
    group = 'momentum'
    alias = 'ultosc', 'UltimateOscillator', 'ULTOSC'
    inputs = 'high', 'low', 'close'
    outputs = 'uo'
    params = (
        ('period1', 7, 'Faster oscillating period'),
        ('period2', 14, 'Medium oscillating period'),
        ('period3', 28, 'Slower oscillating period'),
        ('factor1', 4.0, 'Factor weight for the faster oscillation'),
        ('factor2', 2.0, 'Factor weight for the medium oscillation'),
        ('factor3', 1.0, 'Factor weight for the slower oscillation'),
    )

    def __init__(self):
        bp = self.i.close - truelow(self.i.low, self.i.close)
        tr = truerange(self.i.high, self.i.low, self.i.close)

        av1 = SumN(bp, period=self.p.period1) / SumN(tr, period=self.p.period1)
        av2 = SumN(bp, period=self.p.period2) / SumN(tr, period=self.p.period2)
        av3 = SumN(bp, period=self.p.period3) / SumN(tr, period=self.p.period3)

        factor = 100.0 / (self.p.factor1 + self.p.factor2 + self.p.factor3)
        uo1 = (self.p.factor1 * factor) * av1
        uo2 = (self.p.factor2 * factor) * av2
        uo3 = (self.p.factor3 * factor) * av3

        self.o.uo = uo1 + uo2 + uo3
