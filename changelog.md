## 0.9.7

  - Indicators:
    - `mama`
  - Refactoring internal param names, fixing reduction op and other cosmetics
  - Refactor obv as a function of _period and _setval
  - Re-locate cumXXX and map as standard ops and not as reduction ops
  - Add `_talib_class` classmethod fo ta-lib compatibility actions needed
    before the instance is created
  - API call to regenerate inputs
  - New SEED_ZERO, SEED_ZFILL for _ewm
  - New behavior for `_ewm` in which if alpha is passed but no `span` is
    present, the actual minimum period of the calling lines is applied
  - Added calls `mask` and `where`
  - Correct from 0.9.6 that the dtype of the series was lost, which caused
    problems with wrapped calls which actually check the dtype for example for
    "boolean" like mask and where
  - Internal semantics improved for the `__call__` notation and line `clone`
  - Fix reduction operation minimum period
  - Remove unneeded overlap parameter for standard operations and rolling
    functions
  - Added `_setval` method to set a value/range from the minimum period
  - Extended `_period` to be able to set a value in the period which is
    added/removed
  - Refactor `obv` and others to use `_period`

## 0.9.6

  - Indicators:
    - `mavp`
  - Make scipy.signal an optional requirement with a run-time import and
    default to use _mean_exp if not available
  - Refactor _mean_exp to use prev local variable and let it take an empty beta
    (1-alpha)
  - Report right attribute which was not found in Linesholder
  - Add _minperiodize method which scans and adapts hidden series in args,
    kwargs to minperiod
  - Add line method which allow a dot notation period increase
  - Add generic _apply method to series which mimics hidden _apply in "ewm" but
    with args and kwargs, supporting raw for ndarrays
  - Refactor standard_op to use minperiodize and some renaming
  - Refactor reduction operations to use minperiodize and consider only the
    minperiod
  - Use SEED_AVG (0) enum as default seed instead of non-obvious False
  - Add SEED_NONE logic to multifunc window operations
  - Add reduction operation "unique" and adjust minperiod of series hidden in
    kwargs in apply

## 0.9.5

  - Indicators:
    - `correl`
  - Remove name setting because it may overwrite external inputs and change
    macro-like extraction to fix name, adapting test framework
  - Refactor crossover/up/down family, removing _type, simplifiyng formula and
    adding a _strict parameter to switch between 2 bar crossover (strict) and a
    crossover over multiple bars (non-strict)
  - Macro-like additions: _MPSERIES, _SETVAL and _MPSETVAL to get series
    relative to minperiod and set values (raw and relative to minperiod)
  - Make "series" and "index" properties return only the raw underlying series
    and index, to conform to public API to retrieve series
  - Re-adapt test framework to series macro-like API re-change
  - Remove old pandas macro module and replace with utils
  - Refactor obv to use new _MPSETVAL macro-like function

## 0.9.4

  - Indicators:
    - `linearreg`, `linearreg_angle`, `linearreg_intercept`, `linearreg_slope`,
      `tsf`
  - Changed inputs_override/outputs_override to be the default behavior when
    defining inputs in an indicator
  - Added inputs_extend/outputs_extend to support a partial input definition
    inheriting from the base
  - Refactor all indicators using overrides to new ruling
  - Add superclass _talib_ compat flag and refactor current _talib_ users to
    consume it
  - Add _SERIES macro to work with the underlying series
  - Convert maxindex/minindex to work with _SERIES
  - Convert all math indicators to "apply" instead of using series
  - Make "series" and "index" properties return only the [_minperiod:] slice
    and adapt test framework to change
  - Refactor for logic of indicator auto-registration
  - Use class name for parameterif the parameter is in the indicator hierarchy

## 0.9.3

  - Indicators:
    - `ad`, `add`, `adosc`, `adx`, `adxr`, `apo`, `aroon`, `aroonosc`, `beta`,
      `ceil`, `cmo`, `di`, `div`, `dm`, `dx`, `ewma`, `exp`, `floor`, `ln`,
      `log10`, `maxindex`, `minindex`, `minmaxindex`, `minus_di`, `minus_dm`,
      `mult`, `natr`, `plus_di`, `plus_dm`, `ppo`, `obv`, `ppofast`, `roc`,
      `rocp`, `rocr`, `rocr100`, `smacc`, `sqrt`, `sub`, `trima`, `var`,
      `var_s`

  - Improved autosuper to call all leftmost bases up to Indicator and _talib
    compatibility methods
  - Support of new testcase definition features and refactoring of testcase
    definitions, detection of empty tests sets and improved logging for string
    defined tests, also refactoring their pseudo-execution position
  - Refactoring of _last:_seed, _seed:_seeded and added early (period reducing)
    seed calculations for ta-lib compatibility
  - Add enum SEED_xxx for seed determination
  - Refactor ema, smma, kama for _last:_seed changes
  - Refactor obv to use minperiod "macros"
  - Util Macro-Style Functions to get/set periods/indices for ta-lib
    compatibility

## 0.9.2

  - Indicators:
    - `avgprice`, `cci`, `kama`, `medprice`, `mfi`, `stochf`, `stochrsi`,
      `truelow`, `truehigh`, `typprice`, `ultimateoscillator`, `wclprice`,
      `williamsr`

  - Changes and improvements to the testing framework
  - Internal API changes to streamline indicator development syntax
  - Added custom `_ewm` to use and seed directly instead in the indicators
  - Added support for dynamic alphas in `_ewm`
  - Rewrite of `ewm` based indicators to `_ewm` for simplification

## 0.9.1

  - First initial public release
  - Indicators:
    - `bbands`, `dema`, `ema`, `gdema`, `midpoint`, `midprice`, `sma`, `smma`,
    `t3`, `tema`, `macd`, `stochastic`, `rsi`, `trix`, `atr`, `truerange`,
    `stddev`, `stddev_s`, `acos`, `asin`, `atan`, `cos`, `cosh`, `sin`, `sinh`,
    `tan`, `tanh`, `max`, `min`, `sum`, `crossdown`, `crossover`, `crossup`
  - Utility and Informational methods
  - `ta-lib` compatibility flag/global setting
  - Testing framework in place
  - Documentation, except for indicator development
