## 0.9.2

  - Indicators
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
