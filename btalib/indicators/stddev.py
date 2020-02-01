#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
from . import Indicator


class stddev(Indicator):
    '''
    Calculates the standard deviation of the passed data for a given period,
    considering the data to be the entire population

    See:
      - http://en.wikipedia.org/wiki/Standard_deviation
    '''
    group = 'statistic'
    alias = 'StdDev', 'STDDEV', 'StandardDeviation', 'stddev_p', 'STDDEV_P'
    outputs = 'std'
    params = (
        ('period', 20, 'Period to consider'),
        ('ddof', 0, 'Degree of Freedom: 0 = population, > 0 sample'),
    )

    def __init__(self):
        self.o.std = (
            self.i0.rolling(window=self.p.period).std(ddof=self.p.ddof))

    def _talib(self, kwdict):
        '''Change period to 5'''
        kwdict.setdefault('period', 5)


class stddev_s(stddev):
    '''
    Calculates the standard deviation of the passed data for a given period,
    considering the data to be a sample

    See:
      - http://en.wikipedia.org/wiki/Standard_deviation
    '''
    '''
    Calculates the standard deviation of the passed data for a given period,
    considering the data to be the entire population and not a sample

    See:
      - http://en.wikipedia.org/wiki/Standard_deviation
    '''
    group = 'statistic'
    alias = 'stddev_sample', 'STDDEV_S', 'StandardDeviationSample'
    params = (
        ('ddof', 1, 'Degree of Freedom: 0 = population, > 0 sample'),
    )
