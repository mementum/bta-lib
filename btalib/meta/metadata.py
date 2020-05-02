#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import threading

__all__ = ['metadata']


class Metadata(object):

    def __init__(self):
        self._metadata = threading.local()

    @classmethod
    def register(cls, name, default=None):

        def get_or_default(self):
            if not hasattr(self._metadata, name):
                setattr(self._metadata, name, default())
            return getattr(self._metadata, name)

        setattr(cls, name, property(get_or_default))


metadata = Metadata()
