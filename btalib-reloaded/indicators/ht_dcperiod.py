#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator

import collections
from math import atan

import numpy as np

RAD2DEG = 180.0 / (4.0 * atan(1))


class ht_dcperiod(Indicator):
    '''
    Ehlers': Hilber Transform Dominant Cycle Period

    Formula:
      - From *"Rocket Science for Traders: Digital Signal Processing Applications"*

    See:
      - https://www.amazon.com/Rocket-Science-Traders-Processing-Applications/dp/0471405671
    '''
    group = 'cycle'
    alias = 'HT_DCPERIOD', 'HilberTransform_DominantCyclePeriod'
    inputs = 'high', 'low'
    allowinputs = 1  # allow only 1 input if only 1 passed for ta-lib compat
    outputs = 'dcperiod'

    LOOKBACK_TOTAL = 33
    LOOKBACK_SMOOTH = 4
    LOOKBACK_HT = 7
    LOOKBACK_HT_SKIP = 0  # skip before applying ht
    LOOKBACK_SMOOTH_EXTRA = LOOKBACK_HT - LOOKBACK_SMOOTH
    LOOKBACK_REST = LOOKBACK_TOTAL - LOOKBACK_HT

    def __init__(self):
        # Choose p0, depending on passed number o inputs
        p0 = (self.i.high + self.i.low) / 2.0 if len(self.i) > 1 else self.i0

        # smooth p0
        p0smooth = (4.0*p0 + 3.0*p0(-1) + 2.0*p0(-2) + p0(-3)) / 10.0
        # Add the needed lookback for HT, not yet offered by the smoothing
        p0smooth._period(self.LOOKBACK_SMOOTH_EXTRA)

        dcbuffer = p0smooth(val=0.0)  # copy p0smooth index, fill with 0.0
        dcperiod = p0smooth._apply(self._periodize, dcbuffer, raw=True)  # calc

        # _periodize - no auto period. Add non-count period, filled with nan
        self.o.dcperiod = dcperiod._period(self.LOOKBACK_REST, val=np.nan)

    def _ht(self, x, adjperiod, i):
        ht0 = 0.0962*x[i] + 0.5769*x[i - 2] - 0.5769*x[i - 4] - 0.0962*x[i - 6]
        return ht0 * adjperiod

    def _periodize(self, price, dcperiod):
        # period 7 needed in _periodize for hilbert transform
        # p0smooth has: 4 and needs additional 3 before applying  _periodize
        # actual "return" values to be used in __init__ for phase calculations
        LOOKBACK = self.LOOKBACK_HT
        LOOKIDX = LOOKBACK - 1
        LOOKSTART = LOOKIDX + self.LOOKBACK_HT_SKIP

        # circular buffers for ht calcs
        detrender = collections.deque([0.0] * LOOKBACK, maxlen=LOOKBACK)
        i1 = collections.deque([0.0] * LOOKBACK, maxlen=LOOKBACK)
        q1 = collections.deque([0.0] * LOOKBACK, maxlen=LOOKBACK)

        # the first LOOKBACK elements of the input are ignored in the ta-lib
        # calculations for the detrender. Nullify them.
        price[0:LOOKSTART] = 0.0

        # Variables for the running calculations
        i2, q2, re, im, period, smoothperiod = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0

        for i in range(LOOKSTART, len(price)):
            adjperiod = 0.075*period + 0.54  # adj period_1 for ht transformx

            detrender.append(self._ht(price, adjperiod, i))

            # New detrender val pushed, append to the right -1 is actual value
            i10 = detrender[-4]  # 3 periods ago: -2, -3, -4
            q10 = self._ht(detrender, adjperiod, LOOKIDX)

            i1.append(i10), q1.append(q10)

            ji = self._ht(i1, adjperiod, LOOKIDX)  # looback up to -6
            jq = self._ht(q1, adjperiod, LOOKIDX)

            i21, q21 = i2, q2  # need them for re/im before recalc

            i2 = i10 - jq
            q2 = q10 + ji

            i2 = 0.2*i2 + 0.8*i21  # smooth
            q2 = 0.2*q2 + 0.8*q21  # smooth

            re0 = i2*i21 + q2*q21
            im0 = i2*q21 - q2*i21

            re = 0.2*re0 + 0.8*re  # smooth
            im = 0.2*im0 + 0.8*im  # smooth

            period1 = period
            period = 360 / (RAD2DEG*atan(im / re)) if re and im else period1
            period = min(period, period1 * 1.5)
            period = max(period, period1 * 0.67)
            period = max(period, 6)
            period = min(period, 50)
            period = 0.2*period + 0.8*period1  # smooth

            smoothperiod = 0.33*period + 0.67*smoothperiod
            dcperiod[i] = smoothperiod

        return dcperiod
