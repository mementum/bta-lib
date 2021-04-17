#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import pandas as pd

from . import config
from . import errors
from . import lines
from . import linesholder
from . import metadata


__all__ = ['Inputs', 'Input']


_CLSINPUTS = {}  # holds auto-generated inputs clases
_CLSINAME = {}  # holds naming used for the class


class Input(lines.Line):
    pass


class Inputs(lines.Lines):
    pass


def _generate(cls, bases, dct, name='inputs', klass=Inputs, **kwargs):
    inputscls = lines._generate(
        cls, bases, dct, name=name, klass=klass, **kwargs,
    )
    _CLSINPUTS[cls] = inputscls
    _CLSINAME[cls] = name


def _from_args(cls, *args):
    if not args:  # this must break ... no inputs ... no fun
        errors.OneInputNeededZeroProvided()

    clsinputs = getattr(cls, _CLSINAME[cls])  # Get input definitions
    linputs, largs = len(clsinputs), len(args)  # different logic with lengths

    allowinputs = 0  # control at the end if inputs length has to be capped

    if largs >= linputs:
        argsinputs, args = args[:linputs], args[linputs:]  # split inputs/args

        # map actual inputs to expected input. Let constructor do conversions
        inputargs = {clsinput: Input(arginput, clsinput)
                     for arginput, clsinput in zip(argsinputs, clsinputs)}

    else:  # largs < linputs
        # less arguments, the 1st argument must then be multidimensional
        arginput, args = args[0], args[1:]  # take only 1-elem, rest is args

        if isinstance(arginput, pd.DataFrame):  # check input validity
            inputargs = _from_arg_dataframe(arginput, clsinputs)
        elif isinstance(arginput, linesholder.LinesHolder):
            inputargs = _from_arg_linesholder(arginput, clsinputs)
        else:
            allowinputs = linputs = getattr(cls, 'allowinputs', 0)
            if not linputs:
                errors.MultiDimType()  # raise error, non-acceptable type

            # reconstruct args
            args = (arginput,) + args

            # repeat as above for single inputs but with less inputs
            # less inputs are allowed ... let's go fot it - split inputs/args
            argsinputs, args = args[:linputs], args[linputs:]

            # map inputs to expected input. Let constructor do conversions
            inputargs = {clsinput: Input(arginput, clsinput)
                         for arginput, clsinput in zip(argsinputs, clsinputs)}

    # Create instance of inputs and adjust if needed
    inpret = _CLSINPUTS[cls](**inputargs)  # return instance / rem. args
    if allowinputs:
        inpret.__slots__[:] = inpret.__slots__[:linputs]  # cap the inputs length

    return inpret, args  # return the instance and remaining args


def _from_arg_dataframe(arginput, clsinputs):
    if metadata.callstack:  # top-of the stack, pandas cannot be used
        errors.PandasNotTopStack()

    cols = [x.lower() for x in arginput.columns]

    if len(cols) < len(clsinputs):  # check input validity
        errors.MultiDimSmall()  # raise error

    # create colindices reversed to have 0 atthe end (use list.pop def -1)
    colindices = list(range(len(cols) - 1, -1, -1))

    # try to find the input
    # 0. Use OHLC indices first if dictated by config
    # 1. By columnn name (case insensitive) (if OHLC_index and not helpful)
    # 2. By using the col index from the configuration settings
    # 3. Else, get the next free column
    inputargs = {}
    for i, clsinput in enumerate(clsinputs):
        inputidx = -1
        if config.OHLC_FIRST:
            inputidx = inputidxstr = config.OHLC_INDICES.get(clsinput, -1)

            if isinstance(inputidx, str):  # index set specifically to colname
                try:
                    inputidx = cols.index(inputidxstr)
                except ValueError:
                    inputidx = -1

                if inputidx == -1:
                    errors.ColdIndexStrNotFound(clsinput, inputidxstr)  # raise

        try:
            if inputidx not in colindices:  # not found yet, try names
                inputidx = cols.index(clsinput)  # try first by name
        except ValueError:  # else pre-def index ... or default to 0
            inputidx = inputidxstr = config.OHLC_INDICES.get(clsinput, -1)
            if isinstance(inputidx, str):
                try:
                    inputidx = cols.index(inputidxstr)
                except ValueError:
                    inputidx = -1

                if inputidx == -1:
                    errors.ColdIndexStrNotFound(clsinput, inputidxstr)  # raise

        try:
            colindices.remove(inputidx)  # see if index is valid
        except ValueError:
            inputidx = colindices.pop()  # wasn't there, get next free

        inputargs[clsinput] = arginput.iloc[:, inputidx]  # store input

    return inputargs


def _from_arg_linesholder(arginput, clsinputs):
    if arginput.size < len(clsinputs):  # check input validity
        errors.MultiDimSmall()  # raise error

    # Simple first come first served, no name checking for internal objects
    return {clsinp: out for clsinp, out in zip(clsinputs, arginput.outputs)}
