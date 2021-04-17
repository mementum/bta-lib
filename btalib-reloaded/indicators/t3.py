#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, ema


class gdema(Indicator):
    '''
    Described first by Tim Tillson in Stocks & Commodities V16:1, January 1998
    for its use in the T3 indicator.

    It generalizes the DEMA by using a "volume" factor to put weight on
    the 1st or 2nd factor of the DEMA to smooth the output.

    When "vfactor" is 1, the DEMA is the output. When "vfactor" is 0, the
    output is s simple EMA.
    '''
    group = 'overlap'
    alias = 'gd', 'GD', 'GDEMA', 'GeneralizedDEMA'
    outputs = 'gd'
    params = (
        ('period', 5, 'Period to consider'),
        ('vfactor', 0.7, 'volume factor'),
        ('_ma', ema, 'Moving Average to use'),
    )

    def __init__(self, _gd=False):  # _gd may be set by t3. Ingore it.
        ema1 = self.p._ma(self.i0, period=self.p.period)
        ema2 = self.p._ma(ema1, period=self.p.period)

        self.o.gd = (1.0 + self.p.vfactor)*ema1 - self.p.vfactor*ema2


class t3(Indicator):
    '''
    Described first by Tim Tillson in Stocks & Commodities V16:1, January 1998.

    It first generalizes the DEMA by using a "volume" factor to put weight on
    the 1st or 2nd factor of the DEMA to smooth the output.

    And it then passes the input three times (hence T3) through the generalized
    dema to reduce phase lag.

    The default behavir implements the quadractic equation MetaStock version
    presented in the article, which is also ta-lib compatible.

    Using the paramter `_gd` one can enable the GeneralizedDema Triple Filter
    formulation shown in the article (which is expanded to the quadratic
    version) by the auther. The initial results are similar but not the
    same. The results converge aftera number of bars (period dependent) to at
    lest 6 decimals of precision (period 5 => after 71 bars)

    See also:

      - https://www.fmlabs.com/reference/default.htm?url=T3.htm
      - http://www.tradingpedia.com/forex-trading-indicators/t3-moving-average-indicator/
      - https://www.tradingtechnologies.com/xtrader-help/x-study/technical-indicator-definitions/t3-t3/
    '''
    group = 'overlap'
    alias = 'T3', 'TilsonsT3'
    outputs = 't3'
    params = (
        ('period', 5, 'Period to consider'),
        ('vfactor', 0.7, 'Volume factor'),
        ('_ma', ema, 'Moving Average to use'),
        ('_gd', False, '`True` use articl triple gd filter math formulation'),
    )

    def __init__(self):
        if self.p._gd:  # use gd triple filter math formulation
            self.o.t3 = gd(gd(gd(self.i0, **self.p), **self.p), **self.p)  # noqa: F821, E501
            return

        # Else use the expanded quadratic code shown in the article
        a, a2, a3 = self.p.vfactor, self.p.vfactor**2, self.p.vfactor**3

        c1 = -a3
        c2, c3, c4 = (3*a2 + 3*a3), (-6*a2 - 3*a - 3*a3), (1 + 3*a + a3 + 3*a2)

        ema1 = ema(self.i0, period=self.p.period)
        ema2 = ema(ema1, period=self.p.period)
        ema3 = ema(ema2, period=self.p.period)
        ema4 = ema(ema3, period=self.p.period)
        ema5 = ema(ema4, period=self.p.period)
        ema6 = ema(ema5, period=self.p.period)

        self.o.t3 = c1*ema6 + c2*ema5 + c3*ema4 + c4*ema3

    # ALTERANTIVE FORMULATIONS OF THE GDEMA Alternative
    if False:
        # gd has exactly the same parameters signature as t3_gd
        # self.o.t3 = gd(gd(gd(self.i0, **self.p), **self.p), **self.p)

        # Alternatives with the definition of a partial "_gd"
        # _gd = lambda x: gd(x, **self.params)  # noqa: E731

        # p, v, _ma = self.p.period, self.p.vfactor, self.p._ma
        # _gd = lambda x: gd(x, period=p, vfactor=v, _ma=_ma)  # noqa: E731

        # def _gd(x, p=self.p.period, v=self.p.vfactor, _ma=self.p._ma):
            # return gd(x, period=p, vfactor=v, _ma=_ma)  # noqa: E116

        # def _gd(x): return gd(x, **self.params)
        # self.o.t3 = _gd(_gd(_gd(self.i0)))
        pass
