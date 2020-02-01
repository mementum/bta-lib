#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
__all__ = ['_DS', '_LS']


def _DS(df):
    # reduce dataframes to 1 column series, regardless of col ount
    return df.iloc[:, 0]


def _LS(line):
    # reduce dataframes to 1 column series, regardless of col ount
    return line._series
