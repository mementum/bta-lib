#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import pandas as pd

from . import linesops

__all__ = ['LinesHolder']


class SeriesFetcher:
    def __init__(self, outputs):
        self._o = outputs

    def __getattr__(self, attr):
        if not hasattr(self._o, attr):
            return super().__getattr__(attr)

        return getattr(self._o, attr).series

    def __contains__(self, item):
        return self._o.__contains__(item)

    def __len__(self):
        return len(self._o)

    def __iter__(self):
        yield from (x.series for x in self._o)

    def __getitem__(self, item):
        return self._o[item].series

    def keys(self):
        return self._o.keys()


def binary_op(name):
    def real_binary_op(self, other, *args, **kwargs):
        return getattr(self.outputs[0], name)(other, *args, **kwargs)

    linesops.install_cls(name=name, attr=real_binary_op)


class LinesHolder:
    # base class for any object holding lines
    _df = None
    _sf = None

    # Install the different proxy operations
    for name in linesops._BINOPS:
        binary_op(name)

    def __call__(self, *args, **kwargs):
        return self.outputs[0](*args, **kwargs)

    def __getattr__(self, attr):
        if hasattr(self.outputs, attr):
            return getattr(self.outputs, attr)

        try:
            return getattr(self.outputs[0], attr)
        except AttributeError:
            pass

        # retrieval was impossible, signal real culprit
        raise AttributeError(attr)

    def __contains__(self, item):
        return hasattr(self.outputs, item)

    def __len__(self):
        return len(self.outputs)

    def __iter__(self):
        return iter(self.outputs)

    def __getitem__(self, item):
        return self.outputs[item]

    def keys(self):
        return self.outputs.keys()

    @property
    def size(self):
        return self.outputs.size

    @property
    def df(self):
        if self._df is None:
            self._df = pd.DataFrame(dict(self.series))

        return self._df

    @property
    def series(self):
        if self._sf is None:
            self._sf = SeriesFetcher(self.outputs)

        return self._sf

    def _period(self, p):
        self._minperiod += 1
        return self
