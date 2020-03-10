#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator

import numpy as np


class sarext(Indicator):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"* for the RSI

    SAR stands for *Stop and Reverse* and the indicator was meant as a signal
    for entry (and reverse)

    How to select the 1st signal is left unspecified in the book. Because the
    inputs are "high" and "low", a 1-bar MinusDM is calculated, which accounts
    for both downmove and upmove of high/low. This is also done by ta-lib

    Compared to the standard `sar`, one can define the initial trend, the value
    of the initial `sar`, different acceleration factors for long and short,
    and an offset to be applied to the sar when the trend is reversed

    See:
      - https://en.wikipedia.org/wiki/Parabolic_SAR
      - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:parabolic_sar
    '''
    group = 'momentum'
    alias = 'SAR', 'psar', 'ParabolicStopAndReverse'
    inputs = 'high', 'low'
    outputs = 'sar'
    params = (
        ('startval', 0, 'Start trend (0 auto, 1 long, -1 short)'),
        ('aflong', 0.02, 'Acceleration Factor (Long)'),
        ('afmaxlong', 0.20, 'Maximum Acceleration Factor (Long)'),
        ('afshort', 0.02, 'Acceleration Factor (Long)'),
        ('afmaxshort', 0.20, 'Maximum Acceleration Factor (Long)'),
        ('offsetonreverse', 0.0, 'Offset to apply when reversing position'),
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
        if not self.p.startval:
            upmove, downmove = hi - hi1, lo1 - lo
            minusdm = max(downmove, 0.0) * (downmove > upmove)
            trend = not (minusdm > 0)  # initial trend, long if not downmove

            # use the trend to set the first ep, sar values
            ep, sar = (hi, lo1) if trend else (lo, hi1)
        else:
            if self.p.startval > 0:
                trend = 1
                ep, sar = hi, self.p.startval
            else:
                trend = 0
                ep, sar = lo, abs(self.p.startval)

        AFLONG, AFMAXLONG = self.p.aflong, self.p.afmaxlong
        AFSHORT, AFMAXSHORT = self.p.afshort, self.p.afmaxshort
        OFFSETONREVERSE = self.p.offsetonreverse

        aflong, afshort = AFLONG, AFSHORT

        for i in range(1, len(high)):  # loop over
            hi1, lo1 = hi, lo
            hi, lo = high[i], low[i]

            if trend:
                if lo <= sar:  # trend reversal
                    trend = 0
                    sar = ep + sar * OFFSETONREVERSE
                    sarbuf[i] = -sar
                    ep, afshort = lo, AFSHORT  # kickstart ep and af
                    sar = max(sar + afshort * (ep - sar), hi, hi1)  # new sar
                else:
                    sarbuf[i] = sar  # no change, annotate current sar
                    if hi > ep:  # if extreme breached
                        ep, aflong = hi, min(aflong + AFLONG, AFMAXLONG)
                    sar = min(sar + aflong * (ep - sar), lo, lo1)  # recalc sar
            else:  # trend is 0
                if hi >= sar:  # trend reversal
                    trend = 1
                    sarbuf[i] = sar = ep - sar * OFFSETONREVERSE

                    ep, aflong = hi, AFLONG  # kickstart ep and af
                    sar = min(sar + aflong * (ep - sar), lo, lo1)
                else:
                    sarbuf[i] = -sar
                    if lo < ep:  # if extreme breached
                        ep, afshort = lo, min(afshort + AFSHORT, AFMAXSHORT)
                    sar = max(sar + afshort * (ep - sar), hi, hi1)

        return sarbuf
