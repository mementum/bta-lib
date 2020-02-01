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


class _math(Indicator):
    group = 'math'
    params = (
        ('degrees', False, 'Input is in degrees, not radians ... convert it!'),
    )

    def __init__(self):
        self.o[0] = self._func(_convert_to_radians(self.i0, self.p.degrees))


class sin(_math):
    alias = 'SIN'
    outputs = 'sin'

    _func = np.sin


class sinh(_math):
    alias = 'SINH'
    outputs = 'sinh'

    _func = np.sinh


class cos(_math):
    alias = 'COS'
    outputs = 'cos'

    _func = np.cos


class cosh(_math):
    alias = 'COSH'
    outputs = 'cosh'

    _func = np.cosh


class tan(_math):
    alias = 'TAN'
    outputs = 'tan'

    _func = np.tan


class tanh(_math):
    alias = 'TANH'
    outputs = 'tanh'

    _func = np.tanh


class asin(_math):
    alias = 'ASIN'
    outputs = 'asin'

    _func = np.arcsin


class acos(_math):
    alias = 'ACOS'
    outputs = 'acos'

    _func = np.arccos


class atan(_math):
    alias = 'ATAN'
    outputs = 'atan'

    _func = np.arctan
