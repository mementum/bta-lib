#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
__all__ = ['TaPyError', 'InputsError', ]


class TaPyError(Exception):
    pass


class InputsError(TaPyError):
    pass


def OneInputNeededZeroProvided():
    errmsg = 'One (1) input is at least needed and 0 were provided'
    raise InputsError(errmsg)


def MultiDimSmall():
    errmsg = (
        'The multidimensional input size is smaller than the number of needed '
        'inputs'
    )
    raise InputsError(errmsg)


def MultiDimType():
    errmsg = (
        'Only DataFrames or library/user indicators are accepted as '
        'multi-dimensional inputs'
    )
    raise InputsError(errmsg)


def PandasNotTopStack():
    errmsg = (
        'Pandas DataFrames only valid as input from outside of the library'
    )
    raise InputsError(errmsg)


def ColdIndexStrNotFound(name, rename):
    errmsg = (
        'OHLC Column Name "{}" remapped to "{}", but this cannot be found'
    )
    raise InputsError(errmsg.format(name, rename))
