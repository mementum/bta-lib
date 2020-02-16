#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class mom(Indicator):
    '''
    Measures the change in price by calculating the difference between the
    current price and the price from a given period ago


    Formula:
      - momentum = data - data(-period)

    See:
      - http://en.wikipedia.org/wiki/Momentum_(technical_analysis)
    '''
    groups = 'momentum'
    alias = 'momentum', 'MOM', 'Momentum'
    outputs = 'mom'

    params = (
        ('period', 10, 'Period to consider',),
    )

    def __init__(self):
        self.l.mom = self.i0.diff(periods=self.p.period)
