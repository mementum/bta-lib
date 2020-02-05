#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import numpy as np
import pandas as pd

from . import config
from .metadata import metadata
from . import linesholder
from . import linesops


__all__ = ['Line', 'Lines']


def _generate(cls, bases, dct, name='', klass=None, **kwargs):
    # Get actual lines definition and that of the bases
    lbases = (getattr(base, name, ()) for base in bases)
    lbdefs = tuple(ldef for lbase in lbases for ldef in lbase)
    clsdefs = dct.get(name, ())  # new defs

    # support remapping lines in subclasses
    cdefs = []  # collect final single new definitions
    defmappings = {}  # collect any mappings

    # one can specify a single input (str) or single remapping (dict)
    if isinstance(clsdefs, (dict, str,)):
        clsdefs = [clsdefs]  # unpacked below

    for clsdef in clsdefs:
        # if a "line" def contains a list or a tuple, it is expected to have 2
        # elements defining a remapping. key=>val where key is the new name and
        # value is the old name, defined in the base class. Make it a dict to
        # support the general case in which it was already a dict
        if isinstance(clsdef, (list, tuple,)):
            clsdef = dict([clsdef])  # and go to dict case

        if isinstance(clsdef, dict):
            cdefs.extend(list(clsdef))

            defmappings.update(clsdef)  # store mapping to genreate properties

        else:  # assume str or else detect and raise exception if not
            cdefs.append(clsdef)

    # clsdefs = tuple(x for x in cdefs if x not in remapped)
    clsdefs = tuple(cdefs)

    # if the class is defined with "name_override", for example
    # inputs_override, the new inputs do simply override the previous
    # ones. This could break base classes, so a remapping following order (if a
    # remapping not in place already, must be done)
    if kwargs.get(name + '_override', False):
        final_defs = clsdefs

        for clsdef, lbdef in zip(clsdefs, lbdefs):  # create automappings
            defmappings.setdefault(clsdef, lbdef)
    else:
        final_defs = lbdefs + clsdefs

    # removed remapped lines from definitions
    remapped = list(defmappings.values())

    # retain last inputs defs - super readable and pythonic one-liner
    lines = tuple(reversed(list(dict.fromkeys(reversed(final_defs)))))
    lines = tuple(x for x in lines if x not in remapped)
    setattr(cls, name, lines)  # install all lines defs

    # Create base dictionary for subclassing via typ
    clsdct = dict(__module__=cls.__module__, __slots__=list(lines))

    # Create properties for attribute retrieval of old line
    propdct = {}
    for name, alias in defmappings.items():
        def get_alias_to_name(self):
            return getattr(self, name)

        def set_alias_to_name(self, value):
            setattr(self, name, value)

        propdct[alias] = property(get_alias_to_name, set_alias_to_name)

    clsdct.update(propdct)  # add properties for alias remapping
    clsname = name.capitalize() + cls.__name__  # decide name
    return type(clsname, (klass,), clsdct)  # subclass and return


def binary_op(name):
    def real_binary_op(self, other, *args, **kwargs):
        # Executes a binary operation where self is guaranteed to have a
        # _series attribute but other isn't. Example > or +
        # The minimum period is taken into account to only apply the operation
        # to the proper range and store in the result in that range. The rest
        # is a bunch of leading 'NaN'

        # See if other has a minperiod, else default to 1
        minperiod = max(self._minperiod, getattr(other, '_minperiod', 1))
        minidx = minperiod - 1  # minperiod is 1-based, easier for location

        # Prepare a result filled with 'Nan'
        result = pd.Series(np.nan, index=self._series.index)

        # Get and prepare the other operand
        other = getattr(other, '_series', other)  # get real other operand
        other = other[minidx:] if isinstance(other, pd.Series) else other

        # Get the operation, exec and store
        binop = getattr(self._series[minidx:], name)  # get op from series
        result[minidx:] = binop(other, *args, **kwargs)  # exec / store

        return self._clone(result, minperiod)  # return new obj with minperiod

    linesops.install_cls(name=name, attr=real_binary_op)


def standard_op(name, period_arg=None, overlap=0, sargs=False, skwargs=False):
    def real_standard_op(self, *args, **kwargs):
        target_method = getattr(self._series, name)

        if sargs:
            args = [getattr(x, '_series', x) for x in args]

        if skwargs:
            kwargs = {k: getattr(v, '_series', v) for k, v in kwargs.items()}

        line = self._clone(target_method(*args, **kwargs))
        if period_arg:
            line._minperiod += kwargs.get(period_arg) - overlap

        return line

    linesops.install_cls(name=name, attr=real_standard_op)


def reduction_op(name, sargs=False, *args, **kwargs):
    def real_reduction_op(self, *args, **kwargs):
        if sargs:
            args = [getattr(x, '_series', x) for x in args]

        red_op = getattr(self._series, name)
        return red_op(*args, **kwargs)

    linesops.install_cls(name=name, attr=real_reduction_op)


def multifunc_op(name, period_arg=None, overlap=1, ewm=False,
                 propertize=False):

    class _MultiFunc_Op:
        def __init__(self, line, *args, **kwargs):
            # get/pop period related parameter ... as needed
            if ewm:
                if 'com' in kwargs:
                    self.pval = kwargs.get('com') + 1
                elif 'span' in kwargs:
                    # must be, period cannot be infered from alpha/halflife
                    self.pval = kwargs.get('span')
                elif 'alpha' in kwargs or 'halflife' in kwargs:
                    # period cannot be recovered, force the user to specify it
                    self.pval = kwargs.pop('period')

                # exp smoothing in tech analysis uses 'adjust=False'
                kwargs.setdefault('adjust', False)  # set if not given
            else:
                self.pval = kwargs.get(period_arg)

            self.multifunc = getattr(line._series, name)(*args, **kwargs)
            self.line = line
            self.seeded = False

        def __getattr__(self, attr):
            op = getattr(self.multifunc, attr)  # let exception propagate

            def call_op(*args, **kwargs):
                line = self.line._clone(op(*args, **kwargs))
                if self.pval is not None and not self.seeded:
                    line._minperiod += self.pval - overlap

                return line

            return call_op

        def __getitem__(self, item):
            return self.line._clone(self.line._series.iloc[item])

        @property
        def _seed(self):
            self.seeded = True  # call if applied after a seed
            return self

    def real_multifunc_op(self, *args, **kwargs):
        return _MultiFunc_Op(self, *args, **kwargs)

    linesops.install_cls(name=name, attr=real_multifunc_op,
                         propertize=propertize)


class MetaLine(type):

    def _line_from_dataframe(cls, self, df, colname):
        # it must be dataframe(-like) with dimensions
        colnames = [x.lower() for x in df.columns]
        try:
            idx = colnames.index(colname)  # try first by name
        except ValueError:  # else pre-def index ... or default to 0
            idx = config.OHLC_INDICES.get(colname, 0)

        # TBD: In this situation the user could be made aware of the invalid
        # inputindex (warning and reset to 0 or exception)
        if idx >= len(colnames):  # sanity check, not beyond possible
            idx = 0  # default mapping if sanity check fails

        # Finally, assign values
        self._minperiod = 1
        self._series = df.iloc[:, idx]

    def __call__(cls, val=None, name='', index=None, *args, **kwargs):
        self = cls.__new__(cls, *args, **kwargs)  # create instance

        # Process input
        if isinstance(val, linesholder.LinesHolder):
            val = val.outputs[0]  # get 1st line and process
            self._minperiod = val._minperiod
            self._series = val._series
        elif isinstance(val, Lines):
            val = val[0]  # get 1st line and process
            self._minperiod = val._minperiod
            self._series = val._series
        elif isinstance(val, Line):
            self._minperiod = val._minperiod
            self._series = val._series
        elif isinstance(val, Line):
            self._minperiod = val._minperiod
            self._series = val._series
        elif isinstance(val, pd.Series):
            self._minperiod = 1
            self._series = val
        elif isinstance(val, pd.DataFrame):
            cls._line_from_dataframe(self, val, name)
        else:
            # Don't know how to convert, store and pray
            self._minperiod = 1
            if index is None:
                self._series = val  # 1st column
            else:
                self._series = pd.Series(val, index=index)

        self._name = name  # fix the name of the data series

        self.__init__(*args, **kwargs)  # init instance
        return self  # return the instance


class Line(metaclass=MetaLine):
    _minperiod = 1
    _series = None
    _name = None

    def __hash__(self):
        return super().__hash__()

    # Install the different proxy operations
    for name in linesops._BINOPS:
        binary_op(name)

    for name, opargs in linesops._REDOPS.items():
        reduction_op(name, **opargs)

    for name, opargs in linesops._STDOPS.items():
        standard_op(name, **opargs)

    for name, opargs in linesops._MULTIFUNCOPS.items():
        multifunc_op(name, **opargs)

    def __call__(self, ago=0, val=None, *args, **kwargs):
        if ago:
            return self.shift(periods=-ago)

        if val is None:
            val = self._series.copy()

        return self._clone(val, index=self._series.index, *args, **kwargs)

    def __len__(self):
        return len(self._series)

    def __getitem__(self, item):
        return self._clone(self._series.iloc[item])

    def __setitem__(self, item, value):
        self._series[item] = value

    def _clone(self, series, period=None, index=None):
        line = self.__class__(series, index=index)
        line._minperiod = period or self._minperiod
        return line

    @property
    def series(self):
        return self._series.rename(self._name, inplace=True)

    @property
    def index(self):
        return self._series.index


# These hold the values for the attributes _minperiods/_minperiod for the
# instances, to avoid having them declared as attributes. Or else __setattr__
# would set them as Line objects (or logic would be needed in __setattr__ to
# avoid assigning an object not the real value
metadata.minperiods = {}
metadata.minperiod = {}


class Lines:
    __slots__ = []

    @property
    def _minperiods(self):
        return metadata.minperiods[self]

    @property
    def _minperiod(self):
        return metadata.minperiod[self]

    def _update_minperiod(self):
        metadata.minperiods[self] = minperiods = [x._minperiod for x in self]
        metadata.minperiod[self] = max(minperiods)

    def __init__(self, *args, **kwargs):
        metadata.minperiods[self] = [1] * len(self)
        metadata.minperiod[self] = 1

        for name, value in zip(self.__slots__, args):
            setattr(self, name, value)  # match slots to args

        for name, value in kwargs.items():
            setattr(self, name, value)  # try with provided name-value pairs

    def __setattr__(self, name, val):
        super().__setattr__(name, Line(val, name))

    def __contains__(self, item):
        return hasattr(self, item)

    @property
    def size(self):
        return len(self[0])

    def __len__(self):
        return len(self.__slots__)

    def __iter__(self):
        yield from (getattr(self, x) for x in self.__slots__)

    def __getitem__(self, item):
        if isinstance(item, str):  # support **unpacking
            # Let an IndexError exception propagate
            return getattr(self, self.__slots__[self.__slots__.index(item)])

        return getattr(self, self.__slots__[item])  # iter with int/slices

    def __setitem__(self, item, val):
        setattr(self, self.__slots__[item], val)

    def keys(self):
        yield from self.__slots__

    def _values(self):
        yield from (getattr(self, x) for x in self.__slots__)

    def _items(self):
        yield from ((x, getattr(self, x)) for x in self.__slots__)

    def _get(self, key, default=None):
        try:
            return getattr(self, key)
        except AttributeError:
            pass

        return default
