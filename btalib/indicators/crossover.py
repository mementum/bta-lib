#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class _crossbase(Indicator, inputs_override=True):
    _updown = 0  # -1 crossdown, 0 both, 1 crossup

    inputs = 'crosser', 'crossed'  # overrides (see above) and add an input
    prams = (
        ('_type', float, 'final type of the output. ex<: int, bool, float',)
    )

    def __init__(self):
        nzd = (self.i0 - self.i1).shift(periods=1)
        nzd = nzd.replace(to_replace=0.0, method='ffill')

        if self._updown >= 0:  # cross upwards
            nzd = nzd.clip(upper=0.0).astype(bool)  # below
            self._cup = (nzd & (self.i0 > self.i1)).astype(self.p._type)

        if self._updown <= 0:  # cross downwards
            nzd = nzd.clip(lower=0.0).astype(bool)  # above
            self._cdown = (nzd & (self.i0 < self.i1)).astype(self.p._type)


class crossup(_crossbase):
    '''
    This indicator gives a signal if the 1st provided data crosses over the 2nd
    indicator upwards

    It does need to look into the current time index (0) and the previous time
    index (-1) of both the 1st and 2nd data

    Formula:
      - crossup = data0(-1) < data1(-1) and data0 > data1
    '''
    group = 'utils'
    alias = 'CrossUp'
    outputs = 'crossup'

    _updown = 1

    def __init__(self):
        self.o.crossup = self._cup


class crossdown(_crossbase):
    '''
    This indicator gives a signal if the 1st provided data crosses over the 2nd
    indicator upwards

    It does need to look into the current time index (0) and the previous time
    index (-1) of both the 1st and 2nd data

    Formula:
      - crossup = data0(-1) < data1(-1) and data0 > data1
      - crossdown = data0(-1) > data1(-1) and data0 < data1
      - crossdown = data0(-1) > data1(-1) and data0 < data1
    '''
    group = 'utils'
    alias = 'CrossDown'
    outputs = 'crossdown'

    _updown = -1

    def __init__(self):
        self.o.crossdown = self._cdown


class crossover(_crossbase):
    '''
    This indicator gives a signal if the provided datas (2) cross up or down.

      - `1.0` if the 1st data crosses the 2nd data upwards
      - `-1.0` if the 1st data crosses the 2nd data downwards

    It does need to look into the current time index (0) and the previous time
    index (-1) of both the 1st and 2nd data

    Formula:
      - crossup = data0(-1) < data1(-1) and data0 > data1
      - crossdown = data0(-1) > data1(-1) and data0 < data1
      - crossover = crossup - crossdown
    '''
    group = 'utils'
    alias = 'CrossOver'
    outputs = 'crossover'

    _updown = 0

    def __init__(self):
        self.o.crossover = self._cup - self._cdown
