#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class _crossbase(Indicator, inputs_override=True):
    '''Base crossover class doing the calculations depending on the attribute
    _updown, set by subclasses
    '''
    _updown = 0  # -1 crossdown, 0 both, 1 crossup

    inputs = 'crosser', 'crossed'  # overrides (see above) and add an input
    params = (
        ('_strict', False,
         'If `True`, Consider cross only with two consecutive bars. Else the '
         'default method will take into account that a cross up/down can '
         'happen along several bars with the extremes being above/below and '
         'below/above respectively, and the middle bars having a zero '
         'difference between the crosser and crossed inputs'),
    )

    def __init__(self):
        i0, i1 = self.i0, self.i1

        idiff = (i0 - i1).shift(periods=1)  # inputs (io crosser, i1 crossed)
        if not self.p._strict:  # fill 0.0 intervening bars with previous vals
            # replace consecutive zeros with the value before the first zero
            # this accounts for crossovers which happen over several bars, with
            # the middle bars having both inputs equal (0.0 diff between them)
            idiff = idiff.replace(to_replace=0.0, method='ffill')

        if self._updown >= 0:  # cross upwards
            self._cup = (idiff < 0.0) & (i0 > i1)  # i0(-1) < i1(-1) & ...

        if self._updown <= 0:  # cross downwards
            self._cdown = (idiff > 0.0) & (i0 < i1)    # i0(-1) > i1(-1) & ...


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
        self.o.crossup = 1.0 * self._cup


class crossdown(_crossbase):
    '''
    This indicator gives a signal if the 1st provided data crosses over the 2nd
    indicator upwards

    It does need to look into the current time index (0) and the previous time
    index (-1) of both the 1st and 2nd data

    Formula:
      - crossdown = data0(-1) > data1(-1) and data0 < data1
    '''
    group = 'utils'
    alias = 'CrossDown'
    outputs = 'crossdown'

    _updown = -1

    def __init__(self):
        self.o.crossdown = -1.0 * self._cdown


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
