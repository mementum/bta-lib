#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from numpy import nan as NaN  # noqa: F401

# Internal objects to work in INdicator development
from .. import Indicator  # noqa: F401
from ..utils import *  # noqa: F401 F403

# Price Transform
from .price import *  # noqa: F401 F403

# Math Operators
from .mathop import *  # noqa: F401 F403

# Math Transform
from .math import *  # noqa: F401 F403

# Utils
from .crossover import *  # noqa: F401 F403

# Overlap
from .ewma import *  # noqa: F401 F403

from .sma import *  # noqa: F401 F403
from .ema import *  # noqa: F401 F403
from .smma import *  # noqa: F401 F403
from .wma import *  # noqa: F401 F403

from .dema import *  # noqa: F401 F403
from .kama import *  # noqa: F401 F403
from .tema import *  # noqa: F401 F403
from .trima import *  # noqa: F401 F403
from .trix import *  # noqa: F401 F403
from .t3 import *  # noqa: F401 F403

from .mavp import *  # noqa: F401 F403

from .mama import *  # noqa: F401 F403
from .ht_trendline import *  # noqa: F401 F403

# ## overlap non-ma
from .midpoint import *  # noqa: F401 F403

# Cycle
from .ht_dcperiod import *  # noqa: F401 F403
from .ht_dcphase import *  # noqa: F401 F403
from .ht_phasor import *  # noqa: F401 F403
from .ht_sine import *  # noqa: F401 F403
from .ht_trendmode import *  # noqa: F401 F403

# Statistics
from .beta import *  # noqa: F401 F403
from .correl import *  # noqa: F401 F403
from .linreg import *  # noqa: F401 F403
from .madev import *  # noqa: F401 F403
from .stddev import *  # noqa: F401 F403
from .var import *  # noqa: F401 F403

# ## Overlap - depends on stddev
from .bbands import *  # noqa: F401 F403

# Volatility
from .atr import *  # noqa: F401 F403

# Momentum
from .aroon import *  # noqa: F401 F403
from .bop import *  # noqa: F401 F403
from .cci import *  # noqa: F401 F403
from .cmo import *  # noqa: F401 F403
from .directionalmove import *  # noqa: F401 F403
from .macd import *  # noqa: F401 F403
from .mfi import *  # noqa: F401 F403
from .mom import *  # noqa: F401 F403
from .ppo import *  # noqa: F401 F403
from .roc import *  # noqa: F401 F403
from .rsi import *  # noqa: F401 F403
from .sar import *  # noqa: F401 F403
from .sarext import *  # noqa: F401 F403
from .stochastic import *  # noqa: F401 F403
from .stochrsi import *  # noqa: F401 F403
from .williamsr import *  # noqa: F401 F403
from .ultimateoscillator import *  # noqa: F401 F403

# Volume
from .ad import *  # noqa: F401 F403
from .obv import *  # noqa: F401 F403
