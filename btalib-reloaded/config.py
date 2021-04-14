#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################

__all__ = []


# Standard ordering of OHLCV_OI fields
OHLC_INDICES = {
    'open': 0,
    'high': 1,
    'low': 2,
    'close': 3,
    'volume': 4,
    'openinterest': 5,
}

OHLC_FIRST = False


def set_use_ohlc_indices_first(onoff=True):
    global OHLC_FIRST
    OHLC_FIRST = onoff


def set_input_indices(**kwargs):
    OHLC_INDICES.update(kwargs)


def get_input_indices():
    return OHLC_INDICES.copy()


RETVAL = ''  # can be 'dataframe', 'df'


def set_return(val):
    global RETVAL
    RETVAL = val


def set_return_dataframe():
    global RETVAL
    RETVAL = 'df'


def get_return():
    return RETVAL


def get_return_dataframe():
    return RETVAL in ['df', 'dataframe']


TALIB_COMPAT = False  # global flag for ta-lib compatibility


def set_talib_compat(onoff=True):
    global TALIB_COMPAT
    TALIB_COMPAT = onoff


def get_talib_compat():
    return TALIB_COMPAT
