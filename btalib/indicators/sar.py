#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator

import numpy as np


class sar(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"* for the RSI

    SAR stands for *Stop and Reverse* and the indicator was meant as a signal
    for entry (and reverse)

    How to select the 1st signal is left unspecified in the book. Because the
    inputs are "high" and "low", a 1-bar MinusDM is calculated, which accounts
    for both downmove and upmove of high/low. This is also done by ta-lib

    See:
      - https://en.wikipedia.org/wiki/Parabolic_SAR
      - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:parabolic_sar
    '''
    group = 'momentum'
    alias = 'SAR', 'psar', 'ParabolicStopAndReverse'
    inputs = 'high', 'low'
    outputs = 'sar'
    params = (
        ('af', 0.02, 'Acceleration Factor'),
        ('afmax', 0.20, 'Maximum Acceleration Factor'),
    )

    def __init__(self):
        sarbuf = self.i.high(val=np.nan)  # result buffer
        sar = self.i.high._apply(self._sarize, self.i.low, sarbuf, raw=True)
        self.o.sar = sar._period(1)  # the 1st bar is ignored in _sarize

    def _sarize(self, high, low, sarbuf):
        # kick start values
        hi1, lo1 = high[0], low[0]
        hi, lo = high[1], low[1]

        # Calculate a minusdm of the 1st two values to set the trend
        upmove, downmove = hi - hi1, lo1 - lo
        minusdm = max(downmove, 0.0) * (downmove > upmove)
        trend = not (minusdm > 0)  # initial trend, long if not downmove

        # use the trend to set the first ep, sar values
        ep, sar = (hi, lo1) if trend else (lo, hi1)

        af, AF, AFMAX = self.p.af, self.p.af, self.p.afmax  # acceleration

        for i in range(1, len(high)):  # loop over
            hi1, lo1 = hi, lo
            hi, lo = high[i], low[i]

            if trend:
                if lo <= sar:  # trend reversal
                    trend = 0
                    sarbuf[i] = sar = ep  # update sar and annotate
                    ep, af = lo, AF  # kickstart ep and af
                    sar = max(sar + af * (ep - sar), hi, hi1)  # new sar
                else:
                    sarbuf[i] = sar  # no change, annotate current sar
                    if hi > ep:  # if extreme breached
                        ep, af = hi, min(af + AF, AFMAX)  # annotate, update af
                    sar = min(sar + af * (ep - sar), lo, lo1)  # recalc sar
            else:  # trend is 0
                if hi >= sar:  # trend reversal
                    trend = 1
                    sarbuf[i] = sar = ep  # update sar and annotate
                    ep, af = hi, AF  # kickstart ep and af
                    sar = min(sar + af * (ep - sar), lo, lo1)
                else:
                    sarbuf[i] = sar
                    if lo < ep:  # if extreme breached
                        ep, af = lo, min(af + AF, AFMAX)  # annotate, update af
                    sar = max(sar + af * (ep - sar), hi, hi1)

        return sarbuf
