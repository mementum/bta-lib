#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class donchian(Indicator):
    '''
    The Donchian channel is an indicator used in market trading developed by Richard Donchian. 

    It is formed by taking the highest high and the lowest low of the last n periods. The area between the high and the low is the channel for the period chosen. 

    Formula: 
      - top = max(high)
      - bottom = min(low)
      - mid = bottom + (top - bottom)/2

    See: 
      - https://en.wikipedia.org/wiki/Donchian_channel
    '''

    group = 'volatility'

    inputs = ('high', 'low',)

    alias = 'DONCHIAN', 'DonchianChannel', 'DONCHIANCHANNEL'

    outputs = 'top', 'bot', 'mid'

    params = (
            ('period', 20, 'Period to consider'),
            )

    def __init__(self):

        self.o.top = top = self.i.high.rolling(window=self.p.period).max()
        self.o.bot = bot = self.i.low.rolling(window=self.p.period).min()
        self.o.mid = bot + (top - bot)/2
