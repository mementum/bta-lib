#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import collections

from . import config
from . import meta
from .meta import metadata

__all__ = [
    'get_indicators', 'get_ind_names', 'get_ind_by_name',
    'get_ind_by_group', 'get_ind_names_by_group', 'get_groups',
]


metadata.callstack = []  # keep indicators which are currently being executed


_NAMES_IND = {}
_IND_NAMES = {}
_GRP_IND = collections.defaultdict(list)


def get_indicators():
    return [_NAMES_IND[name] for name in sorted(_NAMES_IND)]


def get_ind_names():
    return sorted(_NAMES_IND)


def get_ind_by_name():
    return dict(sorted(_NAMES_IND.items()))


def get_ind_by_group():
    return dict(_GRP_IND)


def get_ind_names_by_group():
    return {c: sorted(_IND_NAMES[i] for i in il) for c, il in _GRP_IND.items()}


def get_groups():
    return list(_GRP_IND)


class MetaIndicator(meta.linesholder.LinesHolder.__class__):
    # The metaclass takes care of parsing the appropriate defintions during
    # class creation (alias, lines, ...) and properly definiing them if needed
    # in the final class (considering the bases)

    def __new__(metacls, name, bases, dct, **kwargs):
        # Creates class, gathers all lines definitions, installs aliases and
        # auto-exports itself and the aliases
        cls = super().__new__(metacls, name, bases, dct)  # create

        meta.aliases._generate(cls, bases, dct, **kwargs)
        meta.inputs._generate(cls, bases, dct, **kwargs)
        meta.outputs._generate(cls, bases, dct, **kwargs)
        meta.params._generate(cls, bases, dct, **kwargs)
        meta.docs._generate(cls, bases, dct, **kwargs)
        meta.groups._generate(cls, bases, dct, **kwargs)

        modsplit = cls.__module__.split('.')
        to_register = modsplit[0] == __package__ and len(modsplit) > 2
        if to_register and not name.startswith('_'):
            _NAMES_IND[name] = cls
            _IND_NAMES[cls] = name

            for grp in cls.group:
                _GRP_IND[grp].append(cls)

        return cls  # return newly created and patched class

    def __call__(cls, *args, **kwargs):
        # In charge of object creation and initialization.
        # Parses and assigns declared parameters
        # Adds auto-magical
        # member attributes before __init__ is given a change to do
        # something. Any subclass with something to do in __init__ will already
        # be able to access the auto-magical attributes
        self = cls.__new__(cls, *args, *kwargs)  # create instance as usual

        # Determine base classes for auto-calling
        # Non-overridden functions will be filtered with list(dict.fromkeys),
        # which removes duplicates and retains order
        bases, bcls = [], cls
        while(bcls != Indicator):
            bcls = bases.append(bcls) or bcls.__bases__[0]  # append rets None

        bases.append(bcls)  # append Indicator which defines neutral methods

        # check if ta-lib compatibility is requestd
        talibflag = kwargs.pop('_talib', False) or config.get_talib_compat()

        # Check if ta-lib compatibility is requested. If so and the indicator
        # defines a _talib function, give it the **ACTUAL** kwargs and use the
        # modified version. Don't let a '_talib' parameter make it to the
        # indicator (hence pop)
        if talibflag:
            talibclass = list(dict.fromkeys(b._talib_class for b in bases))
            for b_ta in reversed(talibclass):
                b_ta(kwargs)

        # Create and install the lines holding instance
        self.outputs = self.o = meta.outputs._from_class(cls)
        self.lines = self.l = self.outputs  # noqa: E741

        # Get inputs and remaining args
        self.inputs, args = meta.inputs._from_args(cls, *args)
        self.i = self.inputs  # shorthand

        # Add array of data feeds ... the s in "datas" to indicate multiple
        self.datas = self.d = list(self.inputs)
        self.data = self.datas[0]  # add main alias to 1st data

        # add direct aliases with numeric index
        for i, _in in enumerate(self.inputs):
            for inalias in ('i{}', 'input{}', 'd{}', 'data{}'):
                setattr(self, inalias.format(i), _in)

        # add direct aliases with naming index
        for i, _in in enumerate(self.inputs.__slots__):
            for inalias in ('i_{}', 'input_{}', 'd_{}', 'data_{}'):
                setattr(self, inalias.format(i), _in)

        # Gather minimum periods and get the dominant mininum period
        self._minperiods = [_in._minperiod for _in in self.inputs]
        self._minperiod = max(self._minperiods)

        # Check if ta-lib compatibility is requested. If so and the indicator
        # defines a _talib function, give it the **ACTUAL** kwargs and use the
        # modified version. Don't let a '_talib' parameter make it to the
        # indicator (hence pop)
        if talibflag:
            for b_ta in reversed(list(dict.fromkeys(b._talib for b in bases))):
                b_ta(self, kwargs)

        # Get params instance and remaining kwargs
        self.params, kwargs = meta.params._from_kwargs(cls, **kwargs)
        self.p = self.params  # shorthand

        # All boilerplate is done, to into execution mode
        metadata.callstack.append(self)  # let ind know hwere in the stack

        # Auto-call base classes
        for b_init in reversed(list(dict.fromkeys(b.__init__ for b in bases))):
            b_init(self, *args, **kwargs)

        # delete old aliases only meant for operational purposes
        for oalias in ('l', 'lines', 'data', 'd', 'datas'):
            delattr(self, oalias)

        # remove direct aliases with numeric index
        for i, _in in enumerate(self.inputs):
            for inalias in ('d{}', 'data{}'):
                delattr(self, inalias.format(i))

        # remove direct aliases with naming index
        for i, _in in enumerate(self.inputs.__slots__):
            for inalias in ('d_{}', 'data_{}'):
                delattr(self, inalias.format(i))

        # update min periods of lines after calculations and replicate
        self.outputs._update_minperiod()
        self._minperiods = self.outputs._minperiods
        self._minperiod = self.outputs._minperiod

        metadata.callstack.pop()  # let ind know hwere in the stack

        # set def return value, but consider stack depth and user pref
        ret = self
        if not metadata.callstack:  # top-of the stack, ret following prefs
            if config.get_return_dataframe():
                ret = self.df

        return ret  # Return itself for now

    def _regenerate_inputs(cls, inputs):
        meta.inputs._generate(cls, cls.__bases__, {'inputs': inputs})


class Indicator(meta.linesholder.LinesHolder, metaclass=MetaIndicator):
    # Base class for any indicator. The heavy lifting to ensure consistency is
    # done by the metaclass.

    _minperiod = 1
    _minperiods = [1]

    inputs = ('close',)  # default input to look for

    def __init__(self, *args, **kwargs):
        # The goal of having an empty __init__ is to avoid passing any
        # arg/kwargs to object.__init__ which would generate an error
        pass

    _talib_ = False

    def _talib(self, kwdict):
        self._talib_ = True  # for subclasses to use if needed

    @classmethod
    def _talib_class(cls, kwdict):
        pass
