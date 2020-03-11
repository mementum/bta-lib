#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import sys

__all__ = ['__version__', '__version_info__']

__version__ = '1.0.0'

__version_info__ = tuple(int(x) for x in __version__.split('.'))


_min_py_error = 'Python version >=3.6 is needed. The interpreter rerports {}'

assert sys.version_info >= (3, 6), _min_py_error.format(sys.version)
