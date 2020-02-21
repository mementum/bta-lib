#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import argparse
import logging
from logging import info as loginfo, error as logerror, debug as logdebug
import os.path
import sys
import traceback

import numpy as np
import pandas as pd

import talib

# append module root directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import btalib  # noqa: E402

csv = '../data/2006-day-001.txt'
df = pd.read_csv(
    csv, parse_dates=True, index_col='date', skiprows=1,
    names=['date', 'open', 'high', 'low', 'close', 'volume', 'openinterest'],
)

RESULTS = {}


def run_taindicator(name, testdata, inputs, btind, pargs):
    # Now, determine the actual indicators. The name is the name from the
    # bta-lib indicator. Find the corresponding ta indicator
    # Either specified or capitalize the given name
    taind_name = testdata.get('taind', name.upper())
    try:
        taind = getattr(talib, taind_name)
    except AttributeError:
        for taind_name in btind.alias:
            try:
                taind = getattr(talib, taind_name)
            except AttributeError:
                pass
            else:
                break
        else:
            logerror('[-] No ta-lib indicator found for: {}'.format(name))
            return False

    takwargs = testdata.get('takwargs', {})
    if pargs.ta_overargs:
        takwargs = eval('dict(' + pargs.ta_overargs + ')')
    elif pargs.ta_kwargs:
        takwargs.update(eval('dict(' + pargs.ta_kwargs + ')'))

    touts = taind(*inputs, **takwargs)
    if isinstance(touts, pd.Series):  # check if single output
        touts = (touts,)  # consistent single-multiple result presentation

    return touts


def run_indicators(metatests, main=False):
    pargs = parse_args(None if main else [], main=main)

    loginfo('')
    loginfo('[+] From main        : {}'.format(main))
    if pargs.list_names:
        loginfo(', '.join(metatests))
        sys.exit(0)

    if pargs.name:  # requested specific indicators
        mtests = {k: v for k, v in metatests.items() if k in pargs.name}
    else:
        mtests = metatests

    if pargs.ad_hoc:
        for name in pargs.name:
            if name in mtests:
                continue

            mtests[name] = {}

    if not mtests:  # empty test set ...
        logerror('[-] No tests could be found')
        if pargs.name:
            logerror('[-] Wanted Indicators: {}'.format(','.join(pargs.name)))

        sys.exit(0)

    posttest = {}
    for name, testdata in mtests.items():
        if testdata is None:  # skip
            continue

        if not testdata:  # empty - create empty data
            testdata = {}

        if isinstance(testdata, int):  # only minperiods specified
            testdata = dict(minperiods=testdata)

        if isinstance(testdata, str):  # delay test referred to other tests
            posttest[name] = testdata
            continue  # skip for later

        RESULTS[name] = run_indicator(pargs, name, testdata, main=main)

    # pseudo-run delayed string tests
    for name, othername in posttest.items():
        loginfo('[+]' + '-' * 74)
        loginfo('[+] Test def is string: "{}"'.format(othername))
        if othername not in RESULTS:
            logerror('[-] Test "{}" not run'.format(othername))
            rother = False
        else:
            loginfo('[+] Test completed with : {}'.format(othername))
            rother = RESULTS[othername]

        RESULTS[name] = rother

        loginfo('[+] Test Result     : {} ({})'.format(rother, name))

    all_good = all(RESULTS.values())

    loginfo('[+]' + '-' * 74)
    logging.info('[+] Global Result: {}'.format(all_good))
    if not all_good:
        sys.exit(1)


def run_indicator(pargs, name, testdata, main=False):
    loginfo('[+]' + '-' * 74)
    loginfo('[+] Running test for : {}'.format(name))
    loginfo('[+] Testdata is      : {}'.format(testdata))

    # If a string has been passed, check and return the result
    if callable(testdata):
        loginfo('[+] Calling tesdata')
        try:
            ret = testdata(main=main)
        except AssertionError as e:
            ret = False
            _, _, tb = sys.exc_info()
            tb_info = traceback.extract_tb(tb)
            filename, line, func, text = tb_info[-1]
            logging.error('[-] Assertiont Message "{}"'.format(e))
            logging.error('[-] File {} / Line {} / Text {}'.format(
                filename, line, text,
            ))

        loginfo('[+] Test Result     : {} ({})'.format(ret, name))
        return ret

    # bta-lib indicator calculation
    # The indicator is either the given test name or specified in test data
    btind = getattr(btalib, testdata.get('btind', name))

    # The inputs are either specified in the testdata or the default from ind
    inames = testdata.get('inputs', btind.inputs)
    logging.info('[+] Gathering inputs {}'.format(inames))
    inputs = [df[x] for x in inames]
    if 'inputop' in testdata:
        inputs = testdata['inputop'](*inputs)

    tacompat = testdata.get('talib', False) or pargs.talib

    btkwargs = testdata.get('btkwargs', {})
    if tacompat:
        btkwargs.setdefault('_talib', tacompat)

    if pargs.bt_overargs:
        btkwargs = eval('dict(' + pargs.bt_overargs + ')')
    elif pargs.bt_kwargs:
        btkwargs.update(eval('dict(' + pargs.bt_kwargs + ')'))

    btresult = btind(*inputs, **btkwargs)
    btouts = list(btresult.outputs)
    for a, b in testdata.get('swapouts', {}).items():
        btouts[a], btouts[b] = btouts[b], btouts[a]

    if 'minperiod' in testdata:
        checkminperiods = testdata['minperiod']
    else:
        checkminperiods = testdata.get('minperiods', [1])

    if isinstance(checkminperiods, int):
        checkminperiods = [checkminperiods] * len(btouts)

    if checkminperiods:
        eqperiods = btresult._minperiods == checkminperiods
    else:
        eqperiods = -1

    logging.info('[+] Periods Test Result : {} ({})'.format(eqperiods, name))

    if not pargs.standalone:
        touts = run_taindicator(name, testdata, inputs, btind, pargs)
    else:
        # in standalone mode, fake the outputs from a ta-ind
        touts = []
        for output in btind.outputs:
            touts.append(pd.Series(np.nan, index=df.index))

    # Result checking
    logseries = []
    equal = True  # innocent until proven guilty
    for tseries, btout in zip(touts, btouts):
        btseries = btout._series

        # Rounding to x decimals
        decimals = pargs.decimals
        if decimals is None:  # no command line argument was given
            decimals = testdata.get('decimals', None)

        if decimals is not None and decimals >= 0:
            tseries = tseries.round(decimals=decimals)
            btseries = btseries.round(decimals=decimals)

        # Keep record of entire series for verbosity
        logseries.append([tseries, btseries, btseries.eq(tseries)])

        # Minperiod test check settings
        test_minperiod = pargs.minperiod
        if test_minperiod is None:  # nothing in command line
            test_minperiod = testdata.get('minperiod', 0)
        if not test_minperiod:
            minperiod = btresult._minperiod  # global minperiod
        elif test_minperiod > 0:
            minperiod = btout._minperiod  # per output minperiod
        else:  # < 0
            minperiod = 0  # no minperiod at all

        if minperiod:  # check requested from non starting point
            tseries = tseries[minperiod:]
            btseries = btseries[minperiod:]

        equality = btseries.eq(tseries)  # calculate equality of series
        allequal = equality.all()
        if not allequal:  # make a nancheck
            if btseries.isna().all() and tseries.isna().all():
                allequal = True  # both deliver only nans ... are equal

        equal = equal and allequal  # check if result still equal True

    logging.info('[+] Output Test Result : {} ({})'.format(equal, name))

    serequal = equal
    if eqperiods != -1:
        equal = equal and eqperiods

    logging.info('[+] Test Result     : {} ({})'.format(equal, name))

    if pargs.verbose:  # if verbosity is requested
        # General Information
        logdebug('-' * 78)
        logdebug('Result         : {}'.format(equal))
        logdebug('Series Result  : {}'.format(serequal))
        logdebug('Chk Minperiods : {} {}'.format(
            eqperiods,
            '(-1 if no check done)',
        ))
        logdebug('Decimals       : {}'.format(decimals))
        logdebug('-' * 78)
        logdebug('Indicator      : {}'.format(btind.__name__))
        logdebug('Inputs         : {}'.format(btind.inputs))
        logdebug('Outputs        : {}'.format(btind.outputs))
        logdebug('Def Params     : {}'.format(btind.params))
        logdebug('Params         : {}'.format(dict(btresult.params)))
        logdebug('-' * 78)
        logdebug('Period Check   : {} {}'.format(
            test_minperiod,
            ('(0: after max minperiod / 1: per line / -1: ignore)'),
        ))
        logdebug('Minperiods     : {}'.format(btresult._minperiods))
        logdebug('Minperiod      : {}'.format(btresult._minperiod))
        logdebug('-' * 78)

        # Generate logging dataframe
        pdct = {'count': range(1, len(df.index) + 1)}  # visual period check
        for tseries, btseries, eqseries in logseries:
            name = btseries._name

            pdct['ta__' + name] = tseries
            pdct['bta_' + name] = btseries
            pdct['eq__' + name] = eqseries

        logdf = pd.DataFrame(pdct)
        logdebug(logdf.to_string())

    return equal


def parse_args(pargs, main=False):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description=(
            'Test Argument Parser'
        )
    )

    parser.add_argument('name', nargs='*', help='Specific indicators to test')

    parser.add_argument('--ad-hoc', action='store_true',
                        help='Create ad-hoc test if not already defined')

    parser.add_argument('--standalone', '-sta',  action='store_true',
                        help='Run with no ta-lib indicator comparison')

    parser.add_argument('--list-names', action='store_true',
                        help='List all test names and exit')

    parser.add_argument('--decimals', '-d', type=int,
                        help='Force rounding to x decimals')

    parser.add_argument('--minperiod', '-mp', type=int,
                        help='Minperiod chk: -1: No, 0: per-ind, 1: per-line')

    parser.add_argument('--talib', '-talib', action='store_true',
                        help='Activate talib compatibility for the indicators')

    parser.add_argument('--bt-kwargs', '-btk', default='', metavar='kwargs',
                        help='kwargs in key=value format (update)')

    parser.add_argument('--bt-overargs', '-btok', default='', metavar='kwargs',
                        help='kwargs in key=value format (override)')

    parser.add_argument('--ta-kwargs', '-tak', default='', metavar='kwargs',
                        help='kwargs in key=value format (update)')

    parser.add_argument('--ta-overargs', '-taok', default='', metavar='kwargs',
                        help='kwargs in key=value format (override)')

    pgroup = parser.add_argument_group('Verbosity Options')
    pgroup.add_argument('--stderr', action='store_true',
                        help='Log to stderr, else to stdout')
    pgroup = pgroup.add_mutually_exclusive_group()
    pgroup.add_argument('--quiet', '-q', action='store_true',
                        help='Silent (errors will be reported)')
    pgroup.add_argument('--verbose', '-v', action='store_true',
                        help='Increase verbosity level')

    pargs = parser.parse_args(pargs)
    logconfig(pargs, main=main)  # config logging
    return pargs


def logconfig(pargs, main=False):
    if pargs.quiet:
        verbose_level = logging.ERROR
    else:
        verbose_level = logging.INFO - pargs.verbose * 10  # -> DEBUG

    logger = logging.getLogger()
    for h in logger.handlers:  # Remove all loggers from root
        logger.removeHandler(h)

    # when not main, log always to stderr to let nosetests capture the output
    if not main:
        stream = sys.stderr
    else:
        stream = sys.stderr if pargs.stderr else sys.stdout  # choose stream

    logging.basicConfig(
        stream=stream,
        format="%(message)s",  # format="%(levelname)s: %(message)s",
        level=verbose_level,
    )
