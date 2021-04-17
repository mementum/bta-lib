#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator, sumn


class mfi(Indicator):
    '''
    Created by Gene Quong and Avrum Soudack to identify buying/selling
    pressure by combining price and volume in the calculation.

    Pressure is positive if the (typical) price increases and negative if it
    decreases. The volume is the weight factor for how much pressure is being
    exercised on the asset.

    Formula:
      - tp = typical_price = (high + low + close) / 3
      - money_flow_raw = tp * volume
      - flow_positive = Sum(money_flow_raw * (tp > tp(-1)), period)
      - flow_netagive = Sum(money_flow_raw * (tp < tp(-1)), period)
      - money_flow_ratio = flow_positive / flow_negative
      - mfi  100 - 100 / (1 + money_flow_ratio)

    See:
      - https://school.stockcharts.com/doku.php?id=technical_indicators:money_flow_index_mfi
      - https://www.investopedia.com/terms/m/mfi.asp
    '''
    group = 'momentum'
    alias = 'MFI', 'MoneyFlowIndicator'
    inputs = 'high', 'low', 'close', 'volume'
    outputs = 'mfi'
    params = (
        ('period', 14, 'Period to consider'),
    )

    def __init__(self):
        tprice = (self.i.high + self.i.low + self.i.close) / 3.0
        mfraw = tprice * self.i.volume
        flowpos = sumn(mfraw * (tprice > tprice(-1)), period=self.p.period)
        flowneg = sumn(mfraw * (tprice < tprice(-1)), period=self.p.period)
        self.o.mfi = 100.0 - 100.0 / (1.0 + (flowpos / flowneg))
