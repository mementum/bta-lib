#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import sys

__all__ = []


def _generate(cls, bases, dct, name='alias', autoexport=True, **kwargs):
    # Ensure exporting itself and the alias is done
    clsmod = sys.modules[cls.__module__]  # keep handy ref to mod

    if autoexport:
        if not hasattr(clsmod, '__all__'):
            setattr(clsmod, '__all__', [])  # add exports section if not there

        clsmod.__all__.append(cls.__name__)  # add itelf to exports

    # Add aliases as needed and autoexport aliases and main class
    aliases = dct.get(name, ())
    if isinstance(aliases, str):
        aliases = (aliases,)

    if aliases:
        cls.alias = aliases  # re-set as tuple even if string was passed

        for alias in aliases:  # add and export aliases
            setattr(clsmod, alias, cls)
            if autoexport:
                clsmod.__all__.append(alias)
