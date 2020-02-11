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
