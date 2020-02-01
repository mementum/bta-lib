#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import testcommon

import btalib
import pandas as pd


def run(main=False):
    IND = btalib.stochastic
    INDOUTS = IND.outputs
    TYPE = pd.Series

    df = testcommon.df
    series = IND(df).series

    assert all(hasattr(series, x) for x in INDOUTS)
    assert all(type(getattr(series, x)) == TYPE for x in INDOUTS)

    assert len(series) == len(INDOUTS)

    slist = list(series)
    assert len(slist) == len(INDOUTS)
    assert all(type(x) == TYPE for x in slist)

    slist = list(iter(series))
    assert len(slist) == len(INDOUTS)
    assert all(type(x) == TYPE for x in slist)

    sdict = dict(series)
    assert len(sdict) == len(INDOUTS)
    assert all(type(x) == TYPE for x in sdict.values())
    assert all(x == y for x, y in zip(sdict, INDOUTS))

    sdict = dict(**series)
    assert len(sdict) == len(INDOUTS)
    assert all(type(x) == TYPE for x in sdict.values())
    assert all(x == y for x, y in zip(sdict, INDOUTS))

    assert all(x in sdict for x in INDOUTS)

    def xargs(*args):
        assert len(args) == len(INDOUTS)
        assert all(type(x) == TYPE for x in args)

    xargs(*series)

    return True


if __name__ == '__main__':
    run(main=True)
