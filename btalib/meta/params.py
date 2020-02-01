#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
__all__ = ['Params']


_CLSPARAMS = {}  # holds auto-generated Params classes
_CLSPINFO = {}  # holds auto-generated Params information


def get_pinfo(cls):
    return _CLSPINFO.get(cls, {})


class Params:
    # Base slotted class to hold output lines (results) of indicators, which
    # cannot have any member attribute which has not been declared by
    # indicators using the "lines = ('line1', 'line2', ...) syntax

    # It does implemente a Mapping-like interface using __slots__ contents as
    # keys to be able to treat it like a dict for handy usage like "**"
    # expansion and iteration (general and of keys/values)

    __slots__ = []

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __contains__(self, item):
        return hasattr(self, item)

    def __len__(self):
        return len(self.__slots__)

    def __iter__(self):
        yield from self.__slots__

    def __getitem__(self, item):
        try:
            return getattr(self, item)
        except AttributeError:
            pass  # doe not raise inside another exception

        # Raise proper KeyError instead of AttributeError
        raise KeyError('Key not found: {}'.format(item))

    def keys(self):
        yield from self.__slots__

    def _values(self):
        yield from (getattr(self, x) for x in self.__slots__)

    def _items(self):
        yield from ((x, getattr(self, x)) for x in self.__slots__)

    def _get(self, item, default=None):
        try:
            return getattr(self, item)
        except AttributeError:
            pass

        return default

    def _update(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __str__(self):
        return str(dict(self))


def _generate(cls, bases, dct, **kwargs):
    # Get the params, join them and update to final definition
    params = {}  # to keep declared default values
    _CLSPINFO[cls] = pinfo = {}  # to keep rest of info (doc, req'ed, ...)

    # Gather all params from bases and the newly updated/defined
    pbases = [getattr(base, 'params', {}) for base in bases]
    pbases.append(dct.get('params', {}))

    # Gather previous doc definition from bases
    pibases = [_CLSPINFO.get(base, {}) for base in bases]
    pbdocs = {k: v for pibase in pibases for k, v in pibase.items()}

    # Scan and set as dict, support dict/list/tuple formats
    # Examples (component name, default value, docstring, required)
    # docstring and required can be ommited and actually swapped
    # required must always be True/False if present
    # params = (('p1', 30, 'Doc1'), ('p2', None, 'Doc2', True), ('p3', 5),)
    # params = dict(p1=(30, 'My 1'), p2=(None, 'My2', True), p3=20)
    for pbase in pbases:
        if isinstance(pbase, (list, tuple)):
            pbase = dict((pname, tuple(pval)) for pname, *pval in pbase)
        # else:  # ... it was already a dict

        for pname, pval in pbase.items():
            if not isinstance(pval, tuple):  # dict with only def val
                pval = (pval,)  # tuple

            pdefault, *pothers = pval
            pdoc = pothers[0] if pothers else ''
            prequired = pothers[1] if len(pothers) > 1 else False
            if pdoc is True or pdoc is False:  # required set before doc
                # prequired then set to real docstring or default 'False'
                pdoc, prequired = (prequired or ''), pdoc  # swap

            if pname in params:   # param set by previous base class
                pdoc = pdoc or pbdocs.get('doc', '')  # update doc or keep

            params[pname] = pdefault  # update rest
            pinfo[pname] = {'doc': pdoc, 'required': prequired}

    cls.params = params

    # Create a specific slotted Params class and install it
    clsdct = dict(__module__=cls.__module__, __slots__=list(params))
    clsname = 'params'.capitalize() + cls.__name__
    _CLSPARAMS[cls] = type(clsname, (Params,), clsdct)


def _from_kwargs(cls, **kwargs):
    # separate instance params from other kwargs
    params = {k: kwargs.pop(k) for k in list(kwargs) if k in cls.params}

    # Params
    self = _CLSPARAMS[cls](**cls.params)  # defvals params in dict format
    self._update(**params)  # update with instance params
    return self, kwargs   # rest of kwargs and params
