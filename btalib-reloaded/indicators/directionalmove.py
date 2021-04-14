#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, smma, truerange, SEED_SUM


class smacc(Indicator):
    '''Smoothed (Exponential-like) Accumulation (`smacc`) as defined by J. Welles
    Wilder, Jr. in 1978 in his book *"New Concepts in Technical Trading
    Systems"*. The accumuation technique is used in defining the Directional
    Indicator (+DI/-DI), to create an smoothed accumulation of the Directional
    Move (+DM/-DM) and the TrueRange over a period of time.

    Although the technique is similar to the Smoothed Moving Average (SMMA),
    this is not an average.

    Formula:
      - smacc = Sum(data, period)  # seed
      - smacc = samacc(-1) - smacc(-1)/period + data

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx

    Note:
      - Welles Wilder states in the book that the seed value is the sum of
        the 1st n periods (n = 14 in the narrative), but the sample worksheet
        in the book sums 13 (n - 1), with the 1st day not having a value
        because, for example, the TrueRange does not have a value.

        The implementation uses the exact period as seed, which can be
        overridden with the `_pearly` parameter (setting it to `True`) to
        advance the seed calculation by 1 period (i.e.: n-1) Modern sources
        like stockcharts are also conflicting, showing a picture with a step by
        step reproduction of Wilders' worksheet, but offering a sample Excel
        sheet which calculates the seed with the 1st n periods and not n-1
    '''
    groups = 'overlap'
    alias = 'WildersSmoothedAccmulation', 'SmoothedAccumulation'
    outputs = 'smacc'
    params = (
        ('period', 14, 'Period to consider'),
        ('_pearly', False, '`False`: use period - 1 as seed, keeping period'),
        ('_seed', SEED_SUM, 'Default to use sum of period vals as seed'),
    )

    def __init__(self):
        p = self.p.period
        _ewm = self.i0._ewm(span=p, _pearly=self.p._pearly, _seed=self.p._seed)
        self.o.smacc = _ewm._lfilter(alpha=1.0, beta=(p - 1) / p)

    def _talib(self, kwdict):
        '''Seed with 1 value less than the period and accumulate afterwards'''
        kwdict.setdefault('_pearly', True)


class _dm(Indicator):
    '''
    This class serves as the root base class for all "Directional Movement
    System" related indicators, given that the calculations are first common
    and then derived from the common calculations.

    It can calculate the +DM and -DM values over a period of time as the hint
    as to what to calculate) but doesn't assign them to lines. This is left for
    subclases of this class using the class attributes `_plus` and `_minus`
    '''
    group = 'momentum'  # common for all sub-classes
    inputs = 'high', 'low'  # common for all sub-classes
    params = (
        ('period', 14, 'Period to consider'),
        ('_period', 1, 'Lookback period for upmove/downmove calculations'),
        ('_pearly', False, 'If `False` use period - 1 as seed'),
        ('_alt', False, 'Use the SMMA instead of Smoothed Accmulation'),
        ('_accum', smacc, 'Accumulation to use if not in `_alt`` mode'),
        ('_ma', smma, 'Moving Average to use in `_alt` mode'),
    )

    _plus = False  # if True, calculate the +xx elements
    _minus = False  # if True, calculate the -xx elements

    def __init__(self):
        # Determine smoother and args (also for subclasses)
        self._smoothargs = smoothargs = dict(period=self.p.period)
        if not self.p._alt:
            smoothargs['_pearly'] = self.p._pearly  # only for accum

        self._smoother = self.p._accum if not self.p._alt else self.p._ma

        # Calculate
        upmove = self.i.high.diff(periods=self.p._period)  # can apply diff
        downmove = self.i.low(-self.p._period) - self.i.low   # no diff

        if self._plus:  # upvmoe > 0 and where upmove > downmove
            pdm = upmove.clip(lower=0.0) * (upmove > downmove)
            self._pdm = self._smoother(pdm, **smoothargs)

        if self._minus:  # downmove > 0 and where downmove > upmove
            mdm = downmove.clip(lower=0.0) * (downmove > upmove)
            self._mdm = self._smoother(mdm, **smoothargs)

    def _talib(self, kwdict):
        '''Calculate seed 1-period too early and therefore deliver one period
        too early'''
        kwdict.setdefault('_pearly', True)


class plus_dm(_dm):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - upmove = high - high(-1)
      - downmove = low(-1) - low
      - +dm1 = upmove if upmove > downmove and upmove > 0 else 0
      - +dm = SmoothAccum(+dm1, period)

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
      - https://en.wikipedia.org/wiki/Average_directional_movement_index

    Note:
      - Although the original definition from Welles Wilder for DirectionalMove
        does not imply a period, `ta-lib` defines `plus_dm` (+dm) and
        `minus_dm` (-dm) with a period over which they are accumulted. The
        accumulation was defined within the scope of the `DirectionalIndicator`
        (+di, -di) definition.
    '''
    alias = 'PLUS_DM', 'PlusDirectionalMovement'
    outputs = 'plusdm'

    _plus = True

    def __init__(self):
        self.o.plusdm = self._pdm


class minus_dm(_dm):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - upmove = high - high(-1)
      - downmove = low(-1) - low
      - -dm1 = downmove if downmove > upmove and downmove > 0 else 0
      - -dm = SmoothAccum(-dm1, period)

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
      - https://en.wikipedia.org/wiki/Average_directional_movement_index

    Note:
      - Although the original definition from Welles Wilder for DirectionalMove
        does not imply a period, `ta-lib` defines `plus_dm` (+dm) and
        `minus_dm` (-dm) with a period over which they are accumulted. The
        accumulation was defined within the scope of the `DirectionalIndicator`
        (+di, -di) definition.

    '''
    alias = 'MINUS_DM', 'MinusDirectionalMovement'
    outputs = 'minusdm'

    _minus = True

    def __init__(self):
        self.o.minusdm = self._mdm


class dm(_dm):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - upmove = high - high(-1)
      - downmove = low(-1) - low
      - +dm1 = upmove if upmove > downmove and upmove > 0 else 0
      - -dm1 = downmove if downmove > upmove and downmove > 0 else 0
      - +dm = SmoothAccum(+dm1, period)
      - -dm = SmoothAccum(-dm1, period)

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
      - https://en.wikipedia.org/wiki/Average_directional_movement_index

    Note:
      - Although the original definition from Welles Wilder for DirectionalMove
        does not imply a period, `ta-lib` defines `plus_dm` (+dm) and
        `minus_dm` (-dm) with a period over which they are accumulted. The
        accumulation was defined within the scope of the `DirectionalIndicator`
        (+di, -di) definition.
    '''
    alias = 'DM', 'DirectionalMovement'
    outputs = 'plusdm', 'minusdm'

    _plus = True
    _minus = True

    def __init__(self):
        self.o.plusdm = self._pdm
        self.o.minusdm = self._mdm


# NOTE: Usage of INCPERIOD. ta-lib does something incredible, which can only
# mean that +dm/-dm and +di/-di were written by different people.  The +dm/-dm
# are calculated using the step-by-step worksheet approach seen in Wilder's
# book, in which the seed uses 13 values after 14 days, because the 1st day
# cannot produce a value due to the constraint imposed by truerange. Even if
# wilders says in the book that the seed is the sum of the 1st 14 days (which
# one can only strictly understand as the 1st 14 days with a value).  Accepted:
# the `_pearly` parameter takes care of offering compatibility with `ta-lib` if
# that behavior has to be.  But `ta-lib` discards then the seed when
# calculating `+di/-di` overruling the strict step-by-step following of the
# worksheet. The incredible thing is that the 1st value is discarded and the
# preiod changes but the calculation continues with the other values from the
# original period - 1 (_pearly) calculation, which is then wrong, because the
# period in `+dm/-dm` was kept untouched to respect the `+dm/-dm` calculations.
# This can only be corrected by increasing the period (_period) by 1 if
# `ta-lib` compatibility is enabled, which discards the 1st value for
# calculations by increasing the period

class _di(_dm):
    '''
    This class serves as the root base class for all "Directional Indicator"
    subclasses given that the calculations are first common and then derived
    from the common calculations.

    It builds upon `_dm` to use the `+dm/-dm` calculations and the pre-set
    smoother and smoothing args.

    It can calculate the `+di` and `-di` values over a period of time as the
    hint as to what to calculate) but doesn't assign them to lines. This is
    left for subclases of this class using the class attributes `_plus` and
    `_minus`
    '''
    inputs_extend = 'close'  # high and low from bas, add close for truerange

    _plus = False  # reset to false, let +di/-di/di decide what to calc
    _minus = False  # reset to false, let +di/-di/di decide what to calc

    def __init__(self):
        tr = truerange(*self.i, _period=self.p._period)  # same inputs order
        trp = self._smoother(tr, **self._smoothargs)  # smoother/args from base

        trp._period(self._talib_)  # increase period by 1 for ta-lib compat

        if self._plus:
            self._pdi = 100.0 * self._pdm / trp

        if self._minus:
            self._mdi = 100.0 * self._mdm / trp

    def _talib(self, kwdict):
        '''Increase period by 1, but keep 1-period early calculation from dm
        intact'''


class plus_di(_di):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - upmove = high - high(-1)
      - downmove = low(-1) - low
      - +dm = upmove if upmove > downmove and upmove > 0 else 0
      - +di = 100 * SmoothedAccum(+dm, period) / SmoothAccum(truerange, period)

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
      - https://en.wikipedia.org/wiki/Average_directional_movement_index

    Note:
      - The `_alt` parameter changes the formula to use the
        SmoothedMovingAverage in place of `SmoothAccum` as is interpreted by
        several alternative sources (which also effectively implies that
        `SmoothAccum(truerange, period) = ATR(high, low, close, period)`
    '''
    alias = 'PLUS_DI', 'PlusDirectionalIndicator'
    outputs = 'plusdi'

    _plus = True

    def __init__(self):
        self.o.plusdi = self._pdi


class minus_di(_di):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - upmove = high - high(-1)
      - downmove = low(-1) - low
      - -dm = downmove if downmove > upmove and downmove > 0 else 0
      - -di = 100 * SmoothedAccum(-dm, period) / SmoothAccum(truerange, period)

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
      - https://en.wikipedia.org/wiki/Average_directional_movement_index

    Note:
      - The `_alt` parameter changes the formula to use the
        SmoothedMovingAverage in place of `SmoothAccum` as is interpreted by
        several alternative sources (which also effectively implies that
        `SmoothAccum(truerange, period) = ATR(high, low, close, period)`
    '''
    alias = 'MINUS_DI', 'MinusDirectionalIndicator'
    outputs = 'minusdi'

    _minus = True

    def __init__(self):
        self.o.minusdi = self._mdi


class di(_di):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - upmove = high - high(-1)
      - downmove = low(-1) - low
      - +dm = upmove if upmove > downmove and upmove > 0 else 0
      - -dm = downmove if downmove > upmove and downmove > 0 else 0
      - +di = 100 * SmoothedAccum(+dm, period) / SmoothAccum(truerange, period)
      - -di = 100 * SmoothedAccum(-dm, period) / SmoothAccum(truerange, period)

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
      - https://en.wikipedia.org/wiki/Average_directional_movement_index

    Note:
      - The `_alt` parameter changes the formula to use the
        SmoothedMovingAverage in place of `SmoothAccum` as is interpreted by
        several alternative sources (which also effectively implies that
        `SmoothAccum(truerange, period) = ATR(high, low, close, period)`
    '''
    alias = 'DI', 'DirectionalIndicator', 'DIRECTIONALINDICATOR'
    outputs = 'plusdi', 'minusdi'

    _plus = True
    _minus = True

    def __init__(self):
        self.o.plusdi = self._pdi
        self.o.minusdi = self._mdi


class dx(_di):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - upmove = high - high(-1)
      - downmove = low(-1) - low
      - +dm = upmove if upmove > downmove and upmove > 0 else 0
      - -dm = downmove if downmove > upmove and downmove > 0 else 0
      - +di = 100 * SmoothedAccum(+dm, period) / SmoothAccum(truerange, period)
      - -di = 100 * SmoothedAccum(-dm, period) / SmoothAccum(truerange, period)
      - dx = 100 * abs(+di - -di) / (+di + -di)

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
      - https://en.wikipedia.org/wiki/Average_directional_movement_index

    Note:
      - The `_alt` parameter changes the formula to use the
        SmoothedMovingAverage in place of `SmoothAccum` as is interpreted by
        several alternative sources (which also effectively implies that
        `SmoothAccum(truerange, period) = ATR(high, low, close, period)`
    '''
    alias = 'DX', 'DirectionalIndex', 'DIRECTIONALINDEX'
    outputs = 'dx'

    _plus = True
    _minus = True

    def __init__(self):
        self.o.dx = 100.0 * abs(self._pdi - self._mdi)/(self._pdi + self._mdi)


class adx(dx):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - upmove = high - high(-1)
      - downmove = low(-1) - low
      - +dm = upmove if upmove > downmove and upmove > 0 else 0
      - -dm = downmove if downmove > upmove and downmove > 0 else 0
      - +di = 100 * SmoothedAccum(+dm, period) / SmoothAccum(truerange, period)
      - -di = 100 * SmoothedAccum(-dm, period) / SmoothAccum(truerange, period)
      - dx = 100 * abs(+di - -di) / (+di + -di)
      - adx = MovingAverage(dx, period)

    The moving average used is the one originally defined by Wilder,
    the SmoothedMovingAverage

    See also:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:average_directional_index_adx
      - https://en.wikipedia.org/wiki/Average_directional_movement_index

    Note:
      - The `_alt` parameter changes the formula to use the
        SmoothedMovingAverage in place of `SmoothAccum` as is interpreted by
        several alternative sources (which also effectively implies that
        `SmoothAccum(truerange, period) = ATR(high, low, close, period)`
    '''
    alias = 'ADX', 'AverageDirectionalIndex', 'AVERAGEDIRECTIONALINDEX'
    outputs = 'adx'

    def __init__(self):
        self.o.adx = self.p._ma(self.o.dx, period=self.p.period)


class adxr(adx):
    '''
    Defined by J. Welles Wilder, Jr. in 1978 in his book *"New Concepts in
    Technical Trading Systems"*.

    Intended to measure trend strength and directionality

    Formula:
      - adxr = (adx - adx(-period)) / 2.0

    See also:
      -
    '''
    alias = 'ADXR', 'AverageDirectionalIndexRating'
    outputs = 'adxr'

    params = (
        ('_prating', None, 'Use as rating period instead of default period'),
    )

    def __init__(self):
        period = (self.p._prating or self.p.period) - self._talib_  # from base
        self.o.adxr = (self.o.adx + self.o.adx(-period)) / 2.0

    def _talib(self, kwdict):
        '''ta-lib uses period - 1 for the adxr formula when summing the current
        adx and the adx from `period` ago'''
        # nop for documentation purposes
        # base clases have already set _talib_ to True, which is used to
        # decrement the period if ta-lib compatibility is active
