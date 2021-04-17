#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
__all__ = []


def _generate(cls, bases, dct, **kwargs):
    # Try to find a group definition in the directory of the class and it not
    # possible, get the attribute which will have been inherited from the class
    # Add the final attribute in tuple form, to support many
    grps = dct.get('group', ()) or getattr(cls, 'group', ())
    if isinstance(grps, str):
        grps = (grps,)  # if only str, simulate iterable

    cls.group = grps  # set it in the instance, let others process
