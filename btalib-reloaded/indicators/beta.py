#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class beta(Indicator):
    '''
    The description of the algorithm has been adapted from `ta-lib`

    The Beta 'algorithm' is a measure of a stocks volatility vs from index. The
    stock prices are given as the 1st input and the index prices are given in
    the 2nd input. The size of the inputs should be equal. The algorithm is to
    calculate the change between prices in both inputs and then 'plot' these
    changes are points in the Euclidean plane. The x value of the point is
    market return and the y value is the security return. The beta value is the
    slope of a linear regression through these points. A beta of 1.0 is simple
    the line y=x, so the stock varies precisely with the market. A beta of less
    than 1.0 means the stock varies less thandd the market and a beta of more
    than 1.0 means the stock varies more than market.

    See:
      - http://www.moneychimp.com/articles/risk/regression.htm
    '''
    group = 'statistic'
    alias = 'BETA', 'Beta'
    inputs = 'asset', 'market'
    outputs = 'beta'
    params = (
        ('period', 5, 'Period to consider'),
        ('_prets', 1, 'Lookback period to calculate the returns'),
        ('_rets', True, 'Calculate beta on returns'),
    )

    def __init__(self):
        p, prets = self.p.period, self.p._prets

        if self.p._rets:
            x = self.i.asset.pct_change(periods=prets)  # stock returns
            y = self.i.market.pct_change(periods=prets)  # market returns
        else:
            x, y = self.i.asset, self.i.market

        s_x = x.rolling(window=p).sum()
        s_y = y.rolling(window=p).sum()

        s_xx = x.pow(2).rolling(window=p).sum()
        s_xy = (x * y).rolling(window=p).sum()

        self.o.beta = (p * s_xy - s_x * s_y) / (p * s_xx - s_x.pow(2))
