#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import testcommon

import test_linesholder
import test_outputs
import test_series_fetcher


def test_run(main=False):
    return testcommon.run_indicators(main=main, **metatests)


metatests = dict(
    atr=dict(
        minperiods=[15],
        decimals=11,  # round limit for equality
    ),
    bbands=dict(
        btkwargs=dict(_talib=True),
        minperiods=[5],
        decimals=6,
        swapouts={0: 1},  # ta-lib order top/mid/bot, swap outputs 0:1 to match
    ),
    cci=dict(
        btkwargs=dict(_talib=True),
        minperiods=[14],
        decimals=9,
    ),
    dema=dict(
        minperiods=[59],
        decimals=9,
    ),
    ema=dict(
        minperiods=[30],
        decimals=9,
    ),
    macd=dict(
        btkwargs=dict(_talib=True),
        minperiods=[26, 34, 34],
        decimals=9,  # round limit for equality
    ),
    midpoint=dict(
        minperiods=[14],
    ),
    max=dict(
        minperiods=[30],
    ),
    min=dict(
        minperiods=[30],
    ),
    midprice=dict(
        inputs=('high', 'low'),
        minperiods=[14],
    ),
    rsi=dict(
        minperiods=[15],
        decimals=11,
    ),
    cos=dict(
        minperiods=[1],
    ),
    cosh=dict(
        minperiods=[1],
    ),
    sin=dict(
        minperiods=[1],
    ),

    sinh=dict(
        minperiods=[1],
    ),
    tan=dict(
        minperiods=[1],
    ),
    tanh=dict(
        minperiods=[1],
    ),
    asin=dict(
        minperiods=[1],
    ),
    acos=dict(
        minperiods=[1],
    ),
    atan=dict(
        minperiods=[1],
    ),

    smma='rsi',  # tested by RSI, no direct comparison with ta-lib possible

    sma=dict(
        minperiods=[30],
    ),
    stddev=dict(
        btkwargs=dict(_talib=True),
        minperiods=[5],
        decimals=6,
    ),
    stochastic=dict(
        btkwargs=dict(_talib=True),
        minperiods=[16, 18],
        decimals=11,  # round limit for equality
    ),
    t3=dict(
        minperiods=[25],
    ),

    gdema='t3',  # tested with T3

    tema=dict(
        minperiods=[88],
        decimals=10,
    ),
    trix=dict(
        minperiods=[89],
        decimals=12,
    ),
    truerange=dict(
        btind='truerange',
        minperiods=[2],
    ),

    # OTHER TESTS
    series_fetcher=test_series_fetcher.run,
    linesholder=test_linesholder.run,
    outputs=test_outputs.run,
)

if __name__ == '__main__':
    test_run(main=True)
