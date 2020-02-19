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
    testcommon.run_indicators(metatests, main=main)


metatests = dict(
    # Price Transform
    avgprice=dict(minperiod=1, decimals=12),
    medprice=dict(minperiod=1, decimals=12),
    typprice=dict(minperiod=1, decimals=12),
    wclprice=dict(minperiod=1, decimals=12),

    # Math Operators
    # ## over the entire series
    add=dict(inputs=['high', 'low']),
    div=dict(inputs=['high', 'low']),
    mult=dict(inputs=['high', 'low']),
    sub=dict(inputs=['high', 'low']),

    # ## over a period
    max=dict(minperiod=30),
    min=dict(minperiod=30),
    minmax=dict(minperiod=30),
    maxindex=dict(minperiod=1, talib=True),
    minindex=dict(minperiod=1, talib=True),
    minmaxindex=dict(minperiod=1, talib=True),
    sum=dict(minperiod=30),

    # Math Transform
    acos=dict(minperiod=1, inputop=lambda *a: [x / 4000.0 for x in a]),
    asin=dict(minperiod=1, inputop=lambda *a: [x / 4000.0 for x in a]),
    atan=dict(minperiod=1),
    cos=dict(minperiod=1),
    cosh=dict(minperiod=1, inputop=lambda *a: [x / 4000.0 for x in a]),
    sin=dict(minperiod=1),
    sinh=dict(minperiod=1, inputop=lambda *a: [x / 4000.0 for x in a]),
    tan=dict(minperiod=1),
    tanh=dict(minperiod=1),

    ceil=dict(minperiod=1),
    exp=dict(minperiod=1, inputop=lambda *a: [x / 1000.0 for x in a]),
    floor=dict(minperiod=1),
    ln=dict(minperiod=1),
    log10=dict(minperiod=1),
    sqrt=dict(minperiod=1),

    # Statistic Functions
    mad='cci',  # mean asbsolute deviation is tested by cci, not in ta-lib
    stddev=dict(minperiod=5, decimals=6, talib=True),

    # Overlap
    sma=dict(minperiod=30),
    smma='rsi',  # tested by RSI, no direct comparison with ta-lib possible
    wma=dict(minperiod=30, decimals=9),
    ema=dict(minperiod=30, decimals=9),
    ewm='adosc',
    dema=dict(minperiod=59, decimals=9),
    gdema='t3',  # tested with T3
    kama=dict(minperiod=31, talib=True),
    t3=dict(minperiod=25),
    tema=dict(minperiod=88, decimals=10),
    trima=dict(minperiod=30, decimals=10),
    trix=dict(minperiod=89, decimals=12),
    # ta-lib order top/mid/bot, swap outputs 0:1 to match
    bbands=dict(minperiod=5, decimals=6, talib=True, swapouts={0: 1}),
    midpoint=dict(minperiod=14),
    midprice=dict(minperiod=14),

    # ## acumulation (also inside the overlap group)
    smacc='plus_dm',  # tested with the directoinal movement indicators

    # Momentum
    apo=dict(minperiod=26, decimals=9, talib=True),
    aroon=dict(minperiod=15, decimals=13),
    aroonosc=dict(minperiod=15, decimals=12),
    bop=dict(minperiod=1),
    cci=dict(minperiod=14, decimals=8, talib=True),
    cmo=dict(minperiod=15, decimals=11, talib=True),
    macd=dict(minperiods=[26, 34, 34], decimals=9, talib=True),
    mfi=dict(minperiod=15, decimals=11),
    mom=dict(minperiod=11),
    ppo=dict(minperiods=[26, 34, 34], decimals=10, talib=True),
    ppofast='ppo',
    roc=dict(minperiod=11, talib=True),
    rocp=dict(minperiod=11, decimals=14, talib=True),
    rocr=dict(minperiod=11, talib=True),
    rocr100=dict(minperiod=11, talib=True),
    rsi=dict(minperiod=15, decimals=11),
    stoch=dict(minperiods=[7, 9], decimals=11, talib=True),
    stochf=dict(minperiods=[5, 7], decimals=11, talib=True),
    stochrsi=dict(minperiods=[19, 21], decimals=9, talib=True),
    williamsr=dict(minperiod=14, decimals=12),
    ultimateoscillator=dict(minperiod=29, decimals=11),

    # ## also momentum: Directional Movement/Indicators/Index from Wilders
    # ## In the order in which they are defined due to the dependencies
    plus_dm=dict(minperiods=14, decimals=10, talib=True),
    minus_dm=dict(minperiods=14, decimals=11, talib=True),
    dm='plus_dm',
    plus_di=dict(minperiods=15, decimals=11, talib=True),
    minus_di=dict(minperiods=15, decimals=11, talib=True),
    di='plus_di',
    dx=dict(minperiods=15, decimals=11, talib=True),
    adx=dict(minperiods=28, decimals=11, talib=True),
    adxr=dict(minperiods=41, decimals=11, talib=True),

    # Volatility
    atr=dict(minperiod=15, decimals=11),
    natr=dict(minperiod=15, decimals=13),
    truerange=dict(minperiod=2),
    truehigh='truerange',
    truelow='truerange',

    # Volume
    ad=dict(minperiod=1),
    adosc=dict(minperiod=10, talib=True),
    obv=dict(minperiod=1, talib=True),

    # OTHER TESTS - Internal functionality
    series_fetcher=test_series_fetcher.run,
    linesholder=test_linesholder.run,
    outputs=test_outputs.run,
)


if __name__ == '__main__':
    test_run(main=True)
