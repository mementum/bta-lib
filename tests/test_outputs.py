#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import testcommon

import btalib


def run(main=False):
    IND = btalib.stochastic
    INDOUTS = IND.outputs
    TYPE = btalib.meta.lines.Line

    df = testcommon.df
    outputs = IND(df).outputs

    assert all(hasattr(outputs, x) for x in INDOUTS)
    assert all(type(getattr(outputs, x)) == TYPE for x in INDOUTS)

    assert len(outputs) == len(INDOUTS)

    slist = list(outputs)
    assert len(slist) == len(INDOUTS)
    assert all(type(x) == TYPE for x in slist)

    slist = list(iter(outputs))
    assert len(slist) == len(INDOUTS)
    assert all(type(x) == TYPE for x in slist)

    sdict = dict(outputs)
    assert len(sdict) == len(INDOUTS)
    assert all(type(x) == TYPE for x in sdict.values())
    assert all(x == y for x, y in zip(sdict, INDOUTS))

    sdict = dict(**outputs)
    assert len(sdict) == len(INDOUTS)
    assert all(type(x) == TYPE for x in sdict.values())
    assert all(x == y for x, y in zip(sdict, INDOUTS))

    assert all(x in sdict for x in INDOUTS)

    def xargs(*args):
        assert len(args) == len(INDOUTS)
        assert all(type(x) == TYPE for x in args)

    xargs(*outputs)

    return True


if __name__ == '__main__':
    run(main=True)
