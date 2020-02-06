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
    return testcommon.run_indicators(metatests, main=main)


metatests = dict(
    # Price Transform
    avgprice=dict(
        minperiods=[1],
        decimals=12,
    ),
    medprice=dict(
        minperiods=[1],
        decimals=12,
    ),
    typprice=dict(
        minperiods=[1],
        decimals=12,
    ),
    wclprice=dict(
        minperiods=[1],
        decimals=12,
    ),

    # Math Operators
    max=dict(
        minperiods=[30],
    ),
    min=dict(
        minperiods=[30],
    ),
    sum=dict(
        minperiods=[30],
    ),

    # Math Transform
    acos=dict(
        minperiods=[1],
    ),
    asin=dict(
        minperiods=[1],
    ),
    atan=dict(
        minperiods=[1],
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

    # Statistic Functions
    mad='cci',  # mean sbsolute deviation is tested by cci, not in ta-lib
    stddev=dict(
        btkwargs=dict(_talib=True),
        minperiods=[5],
        decimals=6,
    ),

    # Overlap
    sma=dict(
        minperiods=[30],
    ),
    smma='rsi',  # tested by RSI, no direct comparison with ta-lib possible
    ema=dict(
        minperiods=[30],
        decimals=9,
    ),
    dema=dict(
        minperiods=[59],
        decimals=9,
    ),
    gdema='t3',  # tested with T3
    t3=dict(
        minperiods=[25],
    ),
    tema=dict(
        minperiods=[88],
        decimals=10,
    ),
    trix=dict(
        minperiods=[89],
        decimals=12,
    ),
    bbands=dict(
        btkwargs=dict(_talib=True),
        minperiods=[5],
        decimals=6,
        swapouts={0: 1},  # ta-lib order top/mid/bot, swap outputs 0:1 to match
    ),
    midpoint=dict(
        minperiods=[14],
    ),
    midprice=dict(
        minperiods=[14],
    ),

    # Momentum
    cci=dict(
        btkwargs=dict(_talib=True),
        minperiods=[14],
        decimals=8,  # only 1 value forces the cut at 8 instead of 9
    ),
    macd=dict(
        btkwargs=dict(_talib=True),
        minperiods=[26, 34, 34],
        decimals=9,  # round limit for equality
    ),
    mfi=dict(
        minperiods=[15],
        decimals=11,
    ),
    rsi=dict(
        minperiods=[15],
        decimals=11,
    ),
    stochastic=dict(
        btkwargs=dict(_talib=True),
        minperiods=[16, 18],
        decimals=11,  # round limit for equality
    ),
    stochf=dict(
        btkwargs=dict(_talib=True),
        minperiods=[5, 7],
        decimals=11,  # round limit for equality
    ),
    stochrsi=dict(
        btkwargs=dict(_talib=True),
        minperiods=[19, 21],
        decimals=9,  # round limit for equality
    ),
    williamsr=dict(
        minperiods=[14],
        decimals=12,  # round limit for equality
    ),
    ultimateoscillator=dict(
        minperiods=[29],
        decimals=11,  # round limit for equality
    ),
    # Volatility
    truerange=dict(
        minperiods=[2],
    ),
    truehigh='truerange',
    truelow='truerange',
    atr=dict(
        minperiods=[15],
        decimals=11,  # round limit for equality
    ),

    # OTHER TESTS - Internal functionality
    series_fetcher=test_series_fetcher.run,
    linesholder=test_linesholder.run,
    outputs=test_outputs.run,
)

if __name__ == '__main__':
    test_run(main=True)
