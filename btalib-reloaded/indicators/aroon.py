#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator

import numpy as np


def _first_idx_highest(x):
    return np.argmax(x[::-1])


def _first_idx_lowest(x):
    return np.argmin(x[::-1])


class _aroon(Indicator):
    '''
    Base class for `aroon` and `aroonosc`. The up and down components are
    calculated and the subclasses can presente them individually or after an
    operation on them.
    '''
    group = 'momentum'
    inputs = 'high', 'low'
    params = (
        ('period', 14, 'Period to consider'),
    )

    def __init__(self):
        p = self.p.period

        hhidx = self.i.high.rolling(window=p + 1).apply(_first_idx_highest)
        self._aup = 100.0 - 100.0 * hhidx / p

        llidx = self.i.low.rolling(window=p + 1).apply(_first_idx_lowest)
        self._adn = 100.0 - 100.0 * llidx / p


class aroon(_aroon):
    '''
    Developed by Tushar Chande in 1995.

    It tries to determine if a trend exists or not by calculating how far away
    within a given period the last highs/lows are (AroonUp/AroonDown)

    Formula:
      - up = 100 * (period - distance to highest high) / period
      - down = 100 * (period - distance to lowest low) / period

    Note:
      The lines oscillate between 0 and 100. That means that the "distance" to
      the last highest or lowest must go from 0 to period so that the formula
      can yield 0 and 100.

      Hence the lookback period is period + 1, because the current bar is also
      taken into account. And therefore this indicator needs an effective
      lookback period of period + 1.

    See:
      - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:aroon
    '''
    alias = 'AROON', 'Aroon'
    outputs = 'aroondn', 'aroonup'

    def __init__(self):
        self.o.aroondn = self._adn
        self.o.aroonup = self._aup


class aroonosc(_aroon):
    '''
    It is a variation of the AroonUpDown indicator which shows the current
    difference between the AroonUp and AroonDown value, trying to present a
    visualization which indicates which is stronger (greater than 0 -> AroonUp
    and less than 0 -> AroonDown)

    Formula:
      - aroonosc = aroonup - aroondn

    See:
      - http://stockcharts.com/school/doku.php?id=chart_school:technical_indicators:aroon
    '''
    alias = 'AROONOSC', 'AroonOscillator'
    outputs = 'aroonosc'

    def __init__(self):
        self.o.aroonosc = self._aup - self._adn
