#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, atan

import numpy as np

# THEORY
# From ta-lib
# Linear Regression is a concept also known as the "least squares method" or
# "best fit." Linear Regression attempts to fit a straight line between several
# data points in such a way that distance between each data point and the line
# is minimized.
#
# For each point, a straight line over the specified previous bar period is
# determined in terms of y = b + m*x:
#
# TA_LINEARREG          : Returns b+m*(period-1)
# TA_LINEARREG_SLOPE    : Returns 'm'
# TA_LINEARREG_ANGLE    : Returns 'm' in degree.
# TA_LINEARREG_INTERCEPT: Returns 'b'
# TA_TSF                : Returns b+m*(period)
#

# REALITY
# If a end user gets 'm' and 'b' independently and tries for example to
# reconstruct "tsf" with
#   - y = b + m * period
# IT WILL FAIL.
# The reason is that the calculation for m and "b" (which depends on "m") are
# different.
#
# In the case of 'b' (intercept) the internal calculated 'm' uses the range [0,
# period] instead of [1, period + 1], which means that the 1st term of the "x"
# calculations is nullified and in the x*y dot product ... too.


class _linreg_base(Indicator):
    '''Base class for linear regression calculations which does all the work

    It will always calculate 'm' (slope) and if _intercept == True, it will
    also calculate 'b' (intercept)

    'pminus1' is there for compatibility with the broken ta-lib behavior
    described above and will be activated by sub-classes with the method _talib

    If active, "p1" will be p - 1 and calculations will diverge by having "0"
    as the 1st item of "x" ([0, period] instead of [1, period + 1])
    '''
    params = (
        ('period', 14, 'Period to consider'),
    )

    _pminus1 = False  # use period - 1 for x calculations

    _intercept = False  # calculate not only slope but also intercept

    def __init__(self):
        # x is the temporal axis, i.e.: period, y is the amplitude, asset val
        p = self.p.period
        p0, p1 = 1 - self._pminus1, p - self._pminus1

        s_x = p1 * (p1 + 1) / 2  # Gauss instead of  - self._s_x = sum(prange)
        s_y = s_y = self.i0.rolling(window=p).sum()

        # Triangle formula below, else: s_xx = sum(pow(x, 2) for x in prange)
        s_xx = p1 * (p1 + 1) * (2*p1 + 1) / 6

        pxdot = list(range(p0, p1 + 1))
        s_xy = self.i0.rolling(window=p).apply(lambda x: x.dot(pxdot))

        self._m = m = (p * s_xy - s_x * s_y) / (p * s_xx - s_x * s_x)

        if self._intercept:
            self._b = (s_y - m * s_x) / p


class linearreg_slope(_linreg_base):
    '''
    Linear Regression of the values of an asset (y-axis) along the "x" (period
    window, x-axix) using the least squares method to find the best fit.

    Formula:
      - y = b + m * x

    **This indicator returns: "m" or (slope)**

    See:
      - https://en.wikipedia.org/wiki/Ordinary_least_squares#Simple_linear_regression_model
      - https://devarea.com/linear-regression-with-numpy/
    '''
    group = 'statistic'
    alias = 'LINEARREG_SLOPE', 'LinearReg_Slope', 'linreg_slope'
    outputs = 'slope'

    def __init__(self):
        self.o.slope = self._m


class linearreg_angle(_linreg_base):
    '''
    Linear Regression of the values of an asset (y-axis) along the "x" (period
    window, x-axix) using the least squares method to find the best fit.

    Formula:
      - y = b + m * x

    **This indicator returns: "m" or (slope)** (expressed in degrees)

    See:
      - https://en.wikipedia.org/wiki/Ordinary_least_squares#Simple_linear_regression_model
      - https://devarea.com/linear-regression-with-numpy/
    '''
    group = 'statistic'
    alias = 'LINEARREG_ANGLE', 'LinearReg_Angle', 'linreg_angle'
    outputs = 'slope'

    def __init__(self):
        self.o.slope = atan(self._m) * (180.0 / np.pi)


class linearreg_intercept(_linreg_base):
    '''
    Linear Regression of the values of an asset (y-axis) along the "x" (period
    window, x-axix) using the least squares method to find the best fit.

    Formula:
      - y = b + m * x

    **This indicator returns: "b" or (intercept)**

    See:
      - https://en.wikipedia.org/wiki/Ordinary_least_squares#Simple_linear_regression_model
      - https://devarea.com/linear-regression-with-numpy/
    '''
    group = 'statistic'
    alias = 'LINEARREG_INTERCEPT', 'LinearReg_Intercept', 'linreg_intercept'
    outputs = 'intercept'

    _intercept = True

    def __init__(self):
        self.o.intercept = self._b

    def _talib(self, kwdict):
        '''`pminus1` is there for compatibility with the broken ta-lib behavior

        If active, "p1" will be p - 1 and calculations will diverge by having
        "0" as the 1st item of "x" ([0, period] instead of [1, period + 1])

        The 1st behavior is used by ta-lib for `linearreg`,
        `linearreg_intercept` and `tsf`.

        The 2nd behavior is used by ta-lib for `linearreg_slope` and
        `linearreg_angle`.

        Intercept can be calculated as follows b = (Sum(y) - m * Sum(x)) / n.

        In the default `ta-lib` behavior (and in the compatible one with this
        method) this equation isn't true due to the
        different period ranges used for the calculations.
        '''
        self._pminus1 = True


class linearreg(_linreg_base):
    '''
    Linear Regression of the values of an asset (y-axis) along the "x" (period
    window, x-axix) using the least squares method to find the best fit.

    Formula:
      - y = b + m * x

    **This indicator returns: "b + m * x" (using x = period - 1)**

    See:
      - https://en.wikipedia.org/wiki/Ordinary_least_squares#Simple_linear_regression_model
      - https://devarea.com/linear-regression-with-numpy/
    '''
    group = 'statistic'
    alias = 'LINEARREG', 'LinearReg', 'linreg'
    outputs = 'linreg'

    _pminus1 = True
    _intercept = True

    def __init__(self):
        self.o.linreg = self._b + self._m * (self.p.period - 1)

    def _talib(self, kwdict):
        '''`pminus1` is there for compatibility with the broken ta-lib behavior

        If active, "p1" will be p - 1 and calculations will diverge by having
        "0" as the 1st item of "x" ([0, period] instead of [1, period + 1])

        The 1st behavior is used by ta-lib for `linearreg`,
        `linearreg_intercept` and `tsf`.

        The 2nd behavior is used by ta-lib for `linearreg_slope` and
        `linearreg_angle`.

        Intercept can be calculated as follows b = (Sum(y) - m * Sum(x)) / n.

        In the default `ta-lib` behavior (and in the compatible one with this
        method) this equation isn't true due to the
        different period ranges used for the calculations.
        '''
        self._pminus1 = True


class tsf(_linreg_base):
    '''
    Linear Regression of the values of an asset (y-axis) along the "x" (period
    window, x-axix) using the least squares method to find the best fit.

    Formula:
      - y = b + m * x

    **This indicator returns: "b + m * x" (using x = period)**

    See:
      - https://en.wikipedia.org/wiki/Ordinary_least_squares#Simple_linear_regression_model
      - https://devarea.com/linear-regression-with-numpy/
    '''
    group = 'statistic'
    alias = 'TSF', 'TimeSeriesForecast'
    outputs = 'tsf'

    _pminus1 = True
    _intercept = True

    def __init__(self):
        self.o.tsf = self._b + self._m * self.p.period

    def _talib(self, kwdict):
        '''`pminus1` is there for compatibility with the broken ta-lib behavior

        If active, "p1" will be p - 1 and calculations will diverge by having
        "0" as the 1st item of "x" ([0, period] instead of [1, period + 1])

        The 1st behavior is used by ta-lib for `linearreg`,
        `linearreg_intercept` and `tsf`.

        The 2nd behavior is used by ta-lib for `linearreg_slope` and
        `linearreg_angle`.

        Intercept can be calculated as follows b = (Sum(y) - m * Sum(x)) / n.

        In the default `ta-lib` behavior (and in the compatible one with this
        method) this equation isn't true due to the
        different period ranges used for the calculations.
        '''
        self._pminus1 = True
