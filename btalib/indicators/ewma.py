#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator
from . import SEED_AVG


class ewma(Indicator):
    '''
    This is **NOT** the `ema` or `ExponentialMovingAverage`. This is a wrap
    around pandas.Series.ewm where `ewma` stands for `ExponentialWeigthedMean`
    ... to which later a function like `mean` is applied

    Applying `mean` doesn't make it the `ExponentialMovingAverage` (aka `EMA`
    or `ema`) because `ewma` in `pandas.Series` or `pandas.DataFrames` does not
    support using a seed of the first n periods of an `ewm` of `span=n`

    The purpose of this, is to be able to use this in place of the real `ema`
    with parameters like `period` and `_seed` for compatibility.
    '''
    group = 'overlap'
    alias = 'EWMA'
    outputs = 'ewma'
    params = (
        ('period', 30, 'Default Period for the ewm calculation'),
        ('adjust', False, 'Default calc individual terms like in `ema`'),
        ('_seed', SEED_AVG, '(nop) for compatibility with `ema`'),
    )

    def __init__(self, **kwargs):
        kwargs.setdefault('span', self.p.period)  # translate period to span
        self.o.ewma = self.i0.ewm(adjust=self.p.adjust, **kwargs).mean()
