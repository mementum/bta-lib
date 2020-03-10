#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import config
from .metadata import metadata
from . import linesholder
from . import linesops
from .. import SEED_AVG, SEED_LAST, SEED_SUM, SEED_NONE, SEED_ZERO, SEED_ZFILL

import numpy as np
import pandas as pd

__all__ = ['Line', 'Lines']


def _generate(cls, bases, dct, name='', klass=None, **kwargs):
    # If "name" is defined (inputs, outputs) it overrides any previous
    # definition from the base clases.
    # An extension can be done by using "name_extend" (inputs_extend) in which
    # case the definition will be appended to that of the base classes
    # In case of a redefinition, automatic mappings to the existing definitions
    # (by index) will be done to ensure "instances" do still work in base
    # classes when going the super route
    # Manual mappings can also be defined if a definition is a dictionary like
    # in:
    #   outputs = {'atr': 'tr'}
    # In this case 'atr' is the new output and the base class had a 'tr' output
    # and now whenenver 'tr' is referenced it will point to 'atr'

    # Get actual lines definition and that of the bases
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

    # After having parsed mappings in dict form, create the actual definition
    clsdefs = tuple(cdefs)

    # Gather base definitions - needed here to do mappings
    lbases = (getattr(base, name, ()) for base in bases)
    lbdefs = tuple(ldef for lbase in lbases for ldef in lbase)

    if clsdefs:  # a new definition was made
        final_defs = clsdefs

        for clsdef, lbdef in zip(clsdefs, lbdefs):  # create automappings
            if lbdef in clsdefs:  # cannot remap if exists in current defs
                continue
            defmappings.setdefault(clsdef, lbdef)
    else:
        # no new definition, see if _extend has been put in place
        clsdefs = dct.get(name + '_extend', ())  # new defs
        if isinstance(clsdefs, str):
            clsdefs = (clsdefs,)  # unpacked below
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
        result[minidx:] = r = binop(other, *args, **kwargs)  # exec / store
        result = result.astype(r.dtype, copy=False)

        return self._clone(result, period=minperiod)  # ret new obj w minperiod

    linesops.install_cls(name=name, attr=real_binary_op)


def standard_op(name, parg=None, sargs=False, skwargs=False):
    def real_standard_op(self, *args, **kwargs):
        # Prepare a result filled with 'Nan'
        result = pd.Series(np.nan, index=self._series.index)

        # get the series capped to actual period to consider
        a = args if sargs else tuple()
        kw = kwargs if skwargs else {}
        minperiod, minidx, a, kw = self._minperiodize(*a, **kw)
        if sargs:
            args = a
        if skwargs:
            kwargs = kw

        # get the operation from a view capped to the max minperiod
        stdop = getattr(self._series[minidx:], name)
        result[minidx:] = r = stdop(*args, **kwargs)  # execute and assign
        result = result.astype(r.dtype, copy=False)  # keep dtype intact

        line = self._clone(result, period=minperiod)  # create resulting line
        if parg:  # consider if the operation increases the minperiod
            line._minperiod += kwargs.get(parg)

        return line

    linesops.install_cls(name=name, attr=real_standard_op)


def reduction_op(name, sargs=False, *args, **kwargs):
    def real_reduction_op(self, *args, **kwargs):
        if sargs:
            _, minidx, args, _ = self._minperiodize(*args)
        else:
            minidx = self._minperiod - 1

        red_op = getattr(self._series[minidx:], name)
        return red_op(*args, **kwargs)

    linesops.install_cls(name=name, attr=real_reduction_op)


# Below if _ewm is called
#
#   - Calculating the p1:p2 range which will be used to calculate the
#     single seed value with an arithmetic average (i.e.: "mean")
#     The following are true for p1 and p2
#       - p1 >= 0
#       - p2 >= (p1 + self.p.preiod)

#   - Creating a [0:p2] long seed array filled with NaN
#   - Calculating the mean of input[p1:p2] and putting it a p2
#   - Concatenating seed array + rest data and  storing it at outputs[0],
#     (output name is unknown but: subclasses will have an output)

# The parameter "poffset" allows to start the calulation at an offset. This
# is used to replicate the internal ta-lib behavior with ema when
# calculating the fast ema of the macd, where the start of the delivery of
# data is offset to the period of the slow ema.

# For regular usage, poffset is always 0 and plays no role. If poffset
# didn't exist, the calculation of p1 and p2 would simpler
#   - p1 = self._minperiod - 1
#   - p2 = p1 + self.p.period
#
# but due to poffset the calculation is made backwards
#   - poffset = (poffset or period)  # assume here poffset > period
#   - p2 = self._minperiod - 1 + poffset # seed end calc
#   - p1 = p2 - period  # beginning of seed calculation


def multifunc_op(name, parg=None, propertize=False):

    class _MultiFunc_Op:
        def __init__(self, line, *args, **kwargs):
            # plethora of vals needed later in __getattr__/__getitem__
            self._is_seeded = False
            self._line = line
            self._series = series = line._series
            self._minperiod = line._minperiod

            # if the end user passes alpha=None, it means that the alpha
            # calculation for an ewm will be done directy by the caller using
            # apply. This can only be achieved if instead of delivering ewm,
            # rolling(window=2) is returned (the end user should not do that,
            # because the minperiod calculations would be off)
            self._alpha_ = None

            lsname = name.lstrip('_')  # left stripped name (lsname)
            # get/pop period related parameter ... as needed for multi-ewm
            if lsname == 'ewm':
                if 'alpha' in kwargs:  # all bets are on 'alpha'
                    # period cannot be recovered, force the user to specify it
                    # use a default value of 0 to indicate that the period of
                    # the calling line has to be used even if alphas carry a
                    # period. See below the alpha period check against offset
                    self._pval = kwargs.pop('span', 0)
                    alpha = kwargs['alpha']  # it is there ...
                    if isinstance(alpha, (int, float)):
                        pass  # regular behavior
                    else:  # dynamic alpha which can be calc'ed by _mean_
                        self._alpha_ = alpha
                        kwargs['alpha'] = 1.0
                elif 'halflife' in kwargs:
                    # period cannot be recovered, force the user to specify it
                    self._pval = kwargs.pop('span')  # exception if not there
                elif 'com' in kwargs:
                    self._pval = kwargs.get('com') + 1  # alpha = 1 / (com + 1)
                elif 'span' in kwargs:
                    # must be, period cannot be infered from alpha/halflife
                    self._pval = kwargs.get('span')  # alpha = 2 / (alpha + 1)
            else:
                self._pval = kwargs.get(parg)

            # set alphaperiod which is needed in the future
            self._alpha_p = getattr(self._alpha_, '_minperiod', 1)

            # Extra processing if special _ewm
            if name == '_ewm':  # specific behavior for custom _ewm
                # exp smoothing in tech analysis uses 'adjust=False'
                kwargs.setdefault('adjust', False)  # set if not given

                # collect special parameters
                self._pearly = _pearly = kwargs.pop('_pearly', 0)
                self._poffset = kwargs.pop('_poffset', 0)
                self._seed = _seed = kwargs.pop('_seed', SEED_AVG)

                # Determine where the actual calculation is offset to. _poffset
                # is there to support the failure made by ta-lib when offseting
                # the fast ema in the macd. _pofffset > _pval
                poffset = self._poffset or self._pval

                # For a dynamic alpha like in KAMA, the period of the dynamic
                # alpha can exceed that of the calculated offset. But ta-lib
                # makes a mistake an calculates that without taking that period
                # into account if _seed is activated

                # If no pval has been provided (span), don't take the alpha
                # period, the period of the calling line will be used
                if self._pval and self._alpha_p > poffset:
                    poffset += self._alpha_p - poffset - 1

                p2 = self._minperiod - 1 + poffset - _pearly  # seed end calc
                p1 = p2 - self._pval  # beginning of seed calculation
                # beginning of result calculation. Includes the calculated seed
                # value which is the 1st value to be returned. Except in KAMA,
                # where ta-lib uses the value before that as seed for the
                # exponential smoothing calculation
                self._minidx = pidx = p2 - 1  # beginning of result calculation

                trailprefix = pd.Series(np.nan, index=series.index[pidx:p2])
                # Determine the actul seed value to use
                if _seed == SEED_AVG:
                    trailprefix[-1] = series[p1:p2].mean()
                elif _seed == SEED_LAST:
                    trailprefix[-1] = series[pidx]
                elif _seed == SEED_SUM:
                    trailprefix[-1] = series[p1:p2].sum()
                elif _seed == SEED_NONE:
                    pass  # no seed wished ... do nothing
                elif _seed == SEED_ZERO:
                    trailprefix[-1] = 0.0
                elif _seed == SEED_ZFILL:
                    trailprefix[:] = 0.0

                # complete trailer: prefix (seed at end) + series vals to calc
                trailer = trailprefix.append(series[p2:])
            else:
                self._pearly = 0  # it will be checked in getattr
                self._minidx = self._minperiod - 1
                trailer = series[self._minidx:]

            self._multifunc = getattr(trailer, lsname)(*args, **kwargs)

        def _mean_exp(self, alpha, beta=None):  # recurisive definition
            # alpha => new data, beta => old data (similar to 1-alpha)
            if not beta:
                beta = 1.0 - alpha

            def _sm_acc(x):
                prev = x[0]
                for i in range(1, len(x)):
                    x[i] = prev = beta * prev + alpha * x[i]

                return x

            return self._apply(_sm_acc)  # trigger __getattr__ for _apply

        def _lfilter(self, alpha, beta=None):  # recurisive definition
            try:
                import scipy.signal
            except ImportError:  # if not available use tight loop
                return self._mean_exp(alpha, beta)

            # alpha => new data, beta => old data (similar to 1-alpha)
            if not beta:
                beta = 1.0 - alpha

            def _sp_lfilter(x):
                # Initial conditions "ic" can be used for the calculation, the
                # next two lines detail that. A simple scaling of x[0] achieves
                # the same in the 1-d case
                # zi = lfiltic([alpha], [1.0, -beta], y=[x[0]])
                # x[1:], _ = lfilter([alpha], [1.0, -beta], x[1:], zi=zi)
                x[0] /= alpha  # scale start val, descaled in 1st op by alpha
                return scipy.signal.lfilter([alpha], [1.0, -beta], x)

            return self._apply(_sp_lfilter)  # trigger __getattr__ for _apply

        def _mean(self):  # meant for ewm with dynamic alpha
            def _dynalpha(vals):
                # reuse vals: not the original series, it's the trailer abvoe
                alphas = self._alpha_[self._alpha_p - 1:]  # -1: get array idx

                prev = vals[0]  # seed value, which isn't part of the result
                vals[0] = np.nan  # made 1 tick longer to carry seed, nan it
                for i, alphai in enumerate(alphas, 1):  # tight-loop-calc
                    vals[i] = prev = prev + alphai * (vals[i] - prev)

                return vals  # can return vals, made Series via __getattr__

            return self._apply(_dynalpha)  # triggers __getattr__ for _apply

        def __getattr__(self, attr):
            if self._pval is not None and not self._is_seeded:
                # window operation overlap with the 1st calc point ... -1
                self._minperiod += self._pval - self._pearly - 1

                # for a dynamic alpha, the period of the alpha can exceed minp
                self._minperiod = max(self._minperiod, self._alpha_p)

            op = getattr(self._multifunc, attr)  # get real op/let exp propag

            def call_op(*args, **kwargs):  # actual op executor
                result = pd.Series(np.nan, index=self._series.index)  # prep

                sargs = []  # cov takes an "other" parameter for example
                for arg in args:
                    if isinstance(arg, Line):
                        arg = arg._series[self._minidx:]

                    sargs.append(arg)

                result[self._minidx:] = r = op(*sargs, **kwargs)  # run/store
                result = result.astype(r.dtype, copy=False)
                return self._line._clone(result, period=self._minperiod)

            return call_op

        def __getitem__(self, item):
            return self._line._clone(self._series.iloc[item])

        @property
        def _seeded(self):
            self._is_seeded = True  # call if applied after a seed
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

    def __call__(self, ago=0, val=np.nan):
        if ago:
            return self.shift(periods=-ago)

        if ago is None:
            val = None  # called as in (None, ...) ago wasn't meant

        if val is None:
            val = self._series.copy()

        return self._clone(val, index=self._series.index)

    def __iter__(self):
        return iter(self._series)

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
    def mpseries(self):
        return self._series[self._minperiod - 1:]

    @property
    def series(self):
        return self._series.rename(self._name, inplace=True)

    @property
    def index(self):
        return self._series.index

    def _period(self, period, rolling=False, val=None):
        # return the line with the period increased by period
        inc = period - rolling
        if not inc:
            return self

        if val is not None:  # set entire changed period to val
            idx0 = self._minperiod - 1
            idx1 = idx0 + (inc or 1)  # maybe no period inc only setval
            if idx1 < idx0:  # inc is negative ...
                idx0, idx1 = idx1, idx0
            self._series[idx0:idx1] = val

        self._minperiod += inc
        return self

    def _setval(self, i0=0, i1=0, val=np.nan):
        # set a value relative to minperiod as start.
        if not i0 and not i1:
            self._series[self._minperiod - 1:i1] = val
        else:
            i0 = self._minperiod - 1 + i0
            if i1 >= 0:
                i1 = i0 + (i1 or 1)  # i1 rel to i0 or extend i0 by 1 for singl value
            self._series[i0:i1] = val

        return self

    def _minperiodize(self, *args, raw=False, **kwargs):
        # apply func, adding args and kwargs
        minpers = [self._minperiod]
        minpers.extend(getattr(x, '_minperiod', 1) for x in args)
        minpers.extend(getattr(x, '_minperiod', 1) for x in kwargs.values())

        minperiod = max(minpers)  # max of any series involved in op
        minidx = minperiod - 1  # minperiod is 1-based, easier for location

        nargs = []
        for x in args:
            x = getattr(x, '_series', x)
            if isinstance(x, pd.Series):
                x = x[minidx:]
                if raw:
                    x = x.to_numpy()

            nargs.append(x)

        nkwargs = {}
        for k, x in kwargs.items():
            x = getattr(x, '_series', x)
            if isinstance(x, pd.Series):
                x = x[minidx:]
                if raw:
                    x = x.to_numpy()

            nkwargs[k] = x

        return minperiod, minidx, nargs, nkwargs

    def _apply(self, func, *args, raw=False, **kwargs):
        minperiod, minidx, a, kw = self._minperiodize(*args, raw=raw, **kwargs)

        sarray = self._series[minidx:]
        if raw:
            sarray = sarray.to_numpy(copy=True)  # let caller modify the buffer

        result = pd.Series(np.nan, index=self._series.index)
        result[minidx:] = func(sarray, *a, **kw)

        return self._clone(result, period=minperiod)  # create resulting line

    def _applymulti(self, func, *args, raw=False, **kwargs):
        minperiod, minidx, a, kw = self._minperiodize(*args, raw=raw, **kwargs)

        sarray = self._series[minidx:]
        if raw:
            sarray = sarray.to_numpy(copy=True)  # let caller modify the buffer

        results = func(sarray, *a, **kw)
        lines = []
        for r in results:
            result = pd.Series(np.nan, index=self._series.index)
            result[minidx:] = r
            lines.append(self._clone(result, period=minperiod))  # result/store

        return lines


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
