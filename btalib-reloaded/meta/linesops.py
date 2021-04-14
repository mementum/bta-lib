#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import sys


__all__ = []


def install_cls(startlevel=2, name=None, attr=None, propertize=False):
    # Go up the frames until __module__ is found (present in class declaration)
    while True:
        try:
            frame = sys._getframe(startlevel)
        except ValueError:
            return  # went to far up the chain of frames

        if '__module__' in frame.f_locals:  # found class in definition
            break  # found ... time to

        startlevel += 1  # one up ...

    if propertize:
        attr = property(attr)

    frame.f_locals[name] = attr  # install in locals => add to class def


_BINOPS = (
    # BINary OPerationS: operate on self and other, returning a length-wise
    # equal series with the result of the self-other element-wise operation

    # comparison
    '__eq__', 'eq',
    '__le__', 'le',
    '__lt__', 'lt',
    '__ge__', 'ge',
    '__gt__', 'gt',
    '__ne__', 'ne',

    # arithmetic
    '__add__', '__radd__', 'add', 'radd',
    '__div__', '__rdiv__', 'div', 'divide', 'rdiv',
    '__floordiv__', '__rfloordiv__', 'floordiv', 'rfloordiv',
    '__mod__', '__rmod__', 'mod', 'rmod',
    '__mul__', '__rmul__', 'mul', 'multiply', 'rmul',
    '__pow__', '__rpow__', 'pow', 'rpow',
    '__sub__', '__rsub__', 'sub', 'subtract', 'rsub',
    '__truediv__', '__rtruediv__', 'truediv', 'rtruediv',

    # logic
    '__and__', '__or__', '__xor__',
)

_STDOPS = {
    # STandarD OPerationS: do something with the series
    # the period may be changed and a copy may or ma not be returned

    # sargs: True => *args may contain other series (Line => Series)
    # skwargs: True => **kwargs may contain other series (Line => Series)

    # change period
    'diff': dict(parg='periods'),
    'shift': dict(parg='periods'),
    'pct_change': dict(parg='periods'),

    # operate on existing values
    'abs': {}, '__abs__': {},
    'append': {'sargs': True},
    'apply': {'skwargs': True},
    'astype': {},
    'between': {'sargs': True},
    'bfill': {},
    'clip': {'skwargs': True},
    'combine': {'sargs': True},  # other => potential binop
    'combine_first': {'sargs': True},  # other => potential binop
    'concat': {'sargs': True},
    'copy': {},
    'cummax': {},
    'cummin': {},
    'cumprod': {},
    'cumsum': {},
    'drop': {},
    'drop_duplicates': {},
    'dropna': {},
    'duplicated': {},
    'ffill': {},
    'fillna': {},
    'filter': {},
    'first': {},
    'head': {},
    'last': {},
    'interpolate': {},
    'isin': {'sargs': True},
    'isna': {},
    'isnull': {},
    'nlargest': {},
    'mask': {'sargs': True, 'skwargs': True},
    'notna': {},
    'notnull': {},
    'nsmallest': {},
    'replace': {},
    'rank': {},
    'round': {},
    # 'update': {'sargs': True},
    'tail': {},
    'where': {'sargs': True, 'skwargs': True},
}

_REDOPS = {
    # REDuction OPerationS: convert the series to a single value
    'all': {},
    'any': {},
    'autocorr': {},
    'corr': {'sargs': True},
    'count': {},
    'cov': {'sargs': True},
    'dot': {'sargs': True},  # other => potential binop
    'equals': {'sargs': True},  # other => potential binop
    'factorize': {},  # returns a tuple
    'first_valid_index': {},
    'idxmax': {},
    'idxmin': {},
    'item': {},
    'items': {},
    'iteritems': {},
    'keys': {},
    'kurt': {},
    'kurtosis': {},
    'last_valid_index': {},
    'mad': {},
    'max': {},
    'mean': {},
    'median': {},
    'memory_usage': {},
    'min': {},
    'mode': {},
    'nunique': {},
    'prod': {},
    'product': {},
    'quantile': {},
    'sem': {},
    'skew': {},
    'std': {},
    'sum': {},
    'unique': {},
}


_MULTIFUNCOPS = dict(
    # MULTIFUNCtion OPerations
    # Provide an object which can later provide any (of many) operations like
    # in a series: rolling(window=10).mean()

    # provide a set of oprations
    expanding=dict(parg='min_periods'),
    ewm=dict(),
    _ewm=dict(),
    rolling=dict(parg='window'),

    # accessors
    iloc=dict(propertize=True),
    loc=dict(propertize=True),
)
