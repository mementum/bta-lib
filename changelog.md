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
