#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class bop(Indicator):
    '''
    Bop tries to determine the power of buyers vs sellers, by calculating the
    power of being able to take the price to the extremes.

    Igor Livshin introduced in August 2001 in the Stocks and Commodities
    Magazine

    Formula:
      - bop = (close - open) / (high - low)

    See also:
      - https://www.interactivebrokers.com/en/software/tws/usersguidebook/technicalanalytics/balancePower.htm
      - https://www.marketvolume.com/technicalanalysis/balanceofpower.asp
    '''
    group = 'momentum'
    alias = 'BOP', 'BalanceOfPower'
    inputs = 'open', 'high', 'low', 'close'
    outputs = 'bop'
    params = ()

    def __init__(self):
        self.o.bop = (self.i.close - self.i.open) / (self.i.high - self.i.low)
