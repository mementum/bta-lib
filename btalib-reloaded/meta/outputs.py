#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import lines

__all__ = ['Output', 'Outputs']


_CLSOUTPUTS = {}  # holds auto-generated Lines clases


class Output(lines.Line):
    pass


class Outputs(lines.Lines):
    pass


def _generate(cls, bases, dct, name='outputs', klass=Outputs, **kwargs):
    _CLSOUTPUTS[cls] = lines._generate(
        cls, bases, dct, name=name, klass=klass, **kwargs,
    )


def _from_class(cls):
    return _CLSOUTPUTS[cls]()  # defvals params in dict format
