#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, SumN, smma


class cmo(Indicator):
    '''

    Formula:
      - sum_updays = Sum(max(close - close(-1), 0.0), period)
      - sum_downdays = Sum(abs(min(close - close(-1)), 0.0), period)

      - cmo = 100 * (sum_updays - sum_downdays) / (sum_updays + sum_downdays)

    See also:
      - https://www.investopedia.com/terms/c/chandemomentumoscillator.asp
      - https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/chande-momentum-oscillator-cmo/
    '''
    groups = 'momentum'
    alias = 'CMO', 'ChandeMomentumOscillator'
    outputs = 'cmo'

    params = (
        ('period', 14, 'Period to consider',),
        ('_sum', SumN, 'Summation used to accumulate updays/downdays'),
    )

    def __init__(self):
        cdiff = self.i0.diff(periods=1)
        updays = self.p._sum(cdiff.clip(lower=0.0), period=self.p.period)
        dodays = self.p._sum(cdiff.clip(upper=0.0).abs(), period=self.p.period)
        self.o.cmo = 100.0 * (updays - dodays) / (updays + dodays)

    def _talib(self, kwdict):
        '''Against what the book by Chande states, ta-lib smooths the values before
        performing the RSI like calculation using the `smma`, whereas Chande
        clearly states that the advantage of his oscillator is the fact that
        unsmoothed values are being used
        '''
        kwdict.setdefault('_sum', smma)
