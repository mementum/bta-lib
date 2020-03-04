#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, arctan, SEED_ZERO

import collections
from math import atan, pi as PI

import numpy as np


RAD2DEG = 180.0 / (4.0 * atan(1))
INVRAD2DEG = 360 / RAD2DEG


class mama(Indicator):
    '''Quoting Ehlers: "The MESA Adaptive Moving Average (MAMA) adapts to price
    movement in an entirely new and unique way. The adapation is based on the
    rate change of phase as measured by the Hilbert Transform Discriminator"
    '''
    group = 'overlap'
    alias = 'MAMA', 'MesaAdaptiveMovingAverage'
    inputs = 'high', 'low'
    outputs = 'mama', 'fama'
    params = (
        ('period', 5, 'Period to consider'),
        ('fastlimit', 0.5, 'Fast Limit'),
        ('slowlimit', 0.05, 'Fast Limit'),
        ('_early', False, 'Deliver as soon as possible'),
    )

    def _ht(self, x, aperiod1, i):
        ht0 = 0.0962*x[i] + 0.5769*x[i - 2] - 0.5769*x[i - 4] - 0.0962*x[i - 6]
        return ht0 * aperiod1

    def _periodize(self, price, i1, q1):
        # period 7 needed in _periodize for hilbert transform
        # p0smooth has: 4 and needs additional 3 before applying  _periodize
        # actual "return" values to be used in __init__ for phase calculations

        # Running calculations
        i2_1, q2_1 = 0.0, 0.0
        re_1, im_1 = 0.0, 0.0
        period1 = 0.0

        LOOKBACK = 7  # to have up to lookback [-6] in _ht for the price
        LOOKIDX = LOOKBACK - 1
        detrender = collections.deque([0.0] * LOOKBACK, maxlen=LOOKBACK)

        # talib ignores the first batch of existing prices and considers them 0
        price[0:LOOKIDX] = 0.0

        i2, q2, re, im, period = 0.0, 0.0, 0.0, 0.0, 0.0

        for i in range(LOOKIDX, len(price)):
            # For next round
            i2_1, q2_1 = i2, q2  # keep for next round
            re_1, im_1 = re, im  # keep for next round
            period1 = period

            aperiod1 = 0.075*period1 + 0.54  # adj period1 for ht transformx

            detrender.append(self._ht(price, aperiod1, i))

            # New detrender val pushed, append to the right -1 is actual value
            i1[i] = i1_0 = detrender[-4]  # 3 periods ago: -2, -3, -4
            q1[i] = q1_0 = self._ht(detrender, aperiod1, LOOKIDX)

            ji = self._ht(i1, aperiod1, i)  # looback up to -6
            jq = self._ht(q1, aperiod1, i)

            i2 = i1_0 - jq
            q2 = q1_0 + ji

            i2 = 0.2*i2 + 0.8*i2_1  # smooth
            q2 = 0.2*q2 + 0.8*q2_1  # smooth

            re = i2*i2_1 + q2*q2_1
            im = i2*q2_1 - q2*i2_1

            re = 0.2*re + 0.8*re_1  # smooth
            im = 0.2*im + 0.8*im_1  # smooth

            period = INVRAD2DEG / atan(im / re) if re and im else period1
            period = min(period, period1 * 1.5)
            period = max(period, period1 * 0.67)
            period = max(period, 6)
            period = min(period, 50)
            period = 0.2*period + 0.8*period1  # smooth

        # Store the i1, q1 calculated values in the i1/q1 objects, starting at
        # the minimum period (mpseries => minimum period series)
        self.i1.mpseries[:] = i1
        self.q1.mpseries[:] = q1

        # Calculations for mama/fama start as soon as the detrender has a
        # value, even if not really valid, because p0smooth has not yet met the
        # minimum -6 lookback period, and that is +6 after p0smooth. Because q1
        # is part of the phase calculation, add the period to it. i1 can remain
        # unchanged, the dominant period of q1 will take over.
        self.q1._period(6)  # from ht (-6), 7 - 1 overlap

    def __init__(self):
        if not self._talib_:
            p0 = (self.i.high + self.i.low) / 2.0
        else:
            p0 = p0 = self.i0

        p0smooth = (4.0*p0 + 3.0*p0(-1) + 2.0*p0(-2) + 1.0*p0(-3)) / 10.0

        # the ta-lib calculations can be delivered 3 bars earlier. Unknown why
        # it was chosen not to. The play-with parameter allows to do it.
        if not self.p._early:
            p0smooth._period(3)

        # _periodize calcs i1, q1. Prep buffers. Filled 0.0 for talib compat
        self.i1 = p0smooth(val=0.0)  # copy index, fill zeros, from mp
        self.q1 = p0smooth(val=0.0)  # copy index, fill zeros, from mp

        # passing i1, q1 ensures same array type as p0smooth in _periodize
        p0smooth._apply(self._periodize, self.i1, self.q1, raw=True)

        # where i1 == 0 fore arctan to return also 0, with Ehlers formula
        atanq1num = self.q1.mask(self.i1 == 0.0, 0.0)
        phase = (180 / PI) * arctan(atanq1num / self.i1).fillna(0.0)

        # ta-lib cals deltaphase starting as soon as phase has 1 value in spite
        # of using phase(-1) which would be void, but it is considered as
        # 0.0. Reduce the phase period by 1 and set the initial value to 0.
        # This behavior matches all other calculations in _speriodize
        phase._period(-1, val=0.0)  # at minper rel idx 0 => 0.0

        deltaphase = (phase(-1) - phase).clip(lower=1.0)
        alpha = (self.p.fastlimit / deltaphase).clip(lower=self.p.slowlimit)

        # span determines the period, but "alpha" already carries a dominant
        # period, so span can be a simple nop (hence 1)
        _mama = p0._ewm(alpha=alpha, span=1, _seed=SEED_ZERO)._mean()
        # Add no span, to let the fama calculation use the entire _mama range
        _fama = _mama._ewm(alpha=alpha*0.5, _seed=SEED_ZERO)._mean()

        # _speriodize is a manual loop to handle the Ehlers recursion, which
        # adds period constraints not automatically accounted for. To add
        # detrender: +6, q1:+6 ji/jq:+6, re/im:+1, deltaphase:+1
        # smoothings against [-1] don't add a period, because the original
        # implementation always has a valid valud for them (0)
        # Total: 6 + 6  + 6 + 1 + 1 = 20
        # Adding these periods allows removing the initial "unstable" values
        # because the initial calculation uses no seed (0 is the seed)
        _mama._period(20, val=np.nan)  # inc period, fill region with nan
        _fama._period(20, val=np.nan)  # inc period, fill region with nan

        self.o.mama = _mama
        self.o.fama = _fama

    def _talib(self, kwdict):
        '''ta-lib uses only 1 value for the calculation, there where the formula from
            Ehlers uses the average of the high and the low. If ta-lib
            compatibility is activated, the indicator default to use only 1
            input (with the default name `close`. Else `high` and `low` will be
            expected (or two series)
        '''
        pass

    @classmethod
    def _talib_class(cls, kwdict):
        # Regenerate inputs to be only close in 'ta-lib' compatible mode
        cls._regenerate_inputs('close')
