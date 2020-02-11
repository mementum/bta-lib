#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator

import numpy as np


def _convert_to_radians(line, convert):
    return np.radians(line._series) if convert else line._series


class _mathrad(Indicator):
    group = 'math'
    params = (
        ('degrees', False, 'Input is in degrees, not radians ... convert it!'),
    )

    def __init__(self):
        self.o[0] = self._func(_convert_to_radians(self.i0, self.p.degrees))


# Trigonometric math transforms

class sin(_mathrad):
    '''
    Calculates the `sine` function of the input

    Formula:
      - sin = sine(data)

    See also:
      - https://en.wikipedia.org/wiki/Trigonometric_functions
    '''
    alias = 'SIN', 'sine'
    outputs = 'sin'

    _func = np.sin


class cos(_mathrad):
    '''
    Calculates the `cosine` function of the input

    Formula:
      - cos = cosine(data)

    See also:
      - https://en.wikipedia.org/wiki/Trigonometric_functions
    '''
    alias = 'COS', 'cosine'
    outputs = 'cos'

    _func = np.cos


class tan(_mathrad):
    '''
    Calculates the `tangent` function of the input

    Formula:
      - tan = tangent(data)

    See also:
      - https://en.wikipedia.org/wiki/Trigonometric_functions
    '''
    alias = 'TAN', 'tangent'
    outputs = 'tan'

    _func = np.tan


# Co-Trigonometric math transforms

class sinh(_mathrad):
    '''
    Calculates the `cosecant` function of the input (1/sine)

    Formula:
      - sinh = cosecant(data)

    See also:
      - https://en.wikipedia.org/wiki/Trigonometric_functions
    '''
    alias = 'SINH', 'cosecant'
    outputs = 'sinh'

    _func = np.sinh


class cosh(_mathrad):
    '''
    Calculates the `secant` function of the input (1/cosine)

    Formula:
      - cosh = secant(data)

    See also:
      - https://en.wikipedia.org/wiki/Trigonometric_functions
    '''
    alias = 'COSH', 'secant'
    outputs = 'cosh'

    _func = np.cosh


class tanh(_mathrad):
    '''
    Calculates the `cotangent` function of the input (1/tangent)

    Formula:
      - tanh = cotangent(data)

    See also:
      - https://en.wikipedia.org/wiki/Trigonometric_functions
    '''
    alias = 'TANH', 'cotangent'
    outputs = 'tanh'

    _func = np.tanh


# Inverse trigonometric math transforms

class asin(_mathrad):
    '''
    Calculates the `arcsin` function of the input, i.e.: the inverse
    trigonometric function of `sin`

    Formula:
      - asin = arcsin(data)

    See also:
      - https://en.wikipedia.org/wiki/Inverse_trigonometric_functions
    '''
    alias = 'ASIN', 'arcsin', 'arcsine'
    outputs = 'asin'

    _func = np.arcsin


class acos(_mathrad):
    '''
    Calculates the `arccos` function of the input, i.e.: the inverse
    trigonometric function of `cos`

    Formula:
      - acos = arccos(data)

    See also:
      - https://en.wikipedia.org/wiki/Inverse_trigonometric_functions
    '''
    alias = 'ACOS', 'arccos', 'arccosine'
    outputs = 'acos'

    _func = np.arccos


class atan(_mathrad):
    '''
    Calculates the `arctan` function of the input, i.e.: the inverse
    trigonometric function of `tan`

    Formula:
      - atan = arctan(data)

    See also:
      - https://en.wikipedia.org/wiki/Inverse_trigonometric_functions
    '''
    alias = 'ATAN', 'arctan', 'arctangent'
    outputs = 'atan'

    _func = np.arctan


# Non-trigonometric math transforms

class ceil(Indicator):
    '''
    Calculates the `ceil` function which maps the input to the least integer
    greater than or equal to the input

    Formula:
      - ceil = ceil(data)

    See also:
      - https://en.wikipedia.org/wiki/Floor_and_ceiling_functions
    '''
    group = 'math'
    alias = 'CEIL'
    outputs = 'ceil'

    def __init__(self):
        self.o.ceil = np.ceil(self.i0.series)


class exp(Indicator):
    '''
    Calculates the natural logarithm of the input, i.e.: the logarithm with
    base `e`

    Formula:
      - exp = exp(data)

    See also:
      - https://en.wikipedia.org/wiki/Exponential_function
    '''
    group = 'math'
    alias = 'EXP'
    outputs = 'exp'

    def __init__(self):
        self.o.exp = np.exp(self.i0.series)


class floor(Indicator):
    '''
    Calculates the `floor` function which maps the input to the greatest
    integer least than or equal to the input

    Formula:
      - floor = floor(data)

    See also:
      - https://en.wikipedia.org/wiki/Floor_and_ceiling_functions
    '''
    group = 'math'
    alias = 'FLOOR'
    outputs = 'floor'

    def __init__(self):
        self.o.floor = np.floor(self.i0.series)


class ln(Indicator):
    '''
    Calculates the natural logarithm of the input, i.e.: the logarithm with
    base `e`

    Formula:
      - ln = ln(data)

    See also:
      - https://en.wikipedia.org/wiki/Natural_logarithm
    '''
    group = 'math'
    alias = 'LN', 'log', 'LOG'
    outputs = 'ln'

    def __init__(self):
        self.o.ln = np.log(self.i0.series)


class log10(Indicator):
    '''
    Calculates the common logarithm, i.e.: the logarithm with base 10, of the
    input

    Formula:
      - log10 = log10(data)

    See also:
      - https://en.wikipedia.org/wiki/Common_logarithm
    '''
    group = 'math'
    alias = 'LOG10'
    outputs = 'log10'

    def __init__(self):
        self.o.log10 = np.log10(self.i0.series)


class sqrt(Indicator):
    '''
    Calculates the square root of the input

    Formula:
      - sqrt = sqrt(data)

    See also:
      - https://en.wikipedia.org/wiki/Square_root
    '''
    group = 'math'
    alias = 'SQRT'
    outputs = 'sqrt'

    def __init__(self):
        self.o.sqrt = self.i0.pow(0.5)
