# TradeTrace

## By Tinashe Chimanikire

Authorized MT4/MT5 trading-history analysis, strategy reconstruction,
per-symbol backtesting, paper trading, and deliberately gated live execution.

Read [USER_GUIDE.md](USER_GUIDE.md) for the step-by-step workflow.

## Desktop interface

From PowerShell in this folder:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m trading_strategy_lab.ui
```

## Safety boundary

Live execution is disabled by default. Importing history never enables it.
Every strategy candidate is evaluated per symbol and timeframe; it is never
assumed to transfer safely to another pair. The application records an audit
trail and requires explicit broker authorization, risk limits, and a live-mode
confirmation before an order adapter may be used.

## Planned modules

- MT4/MT5 CSV or report importer for authorized exports.
- Candidate-rule analysis with uncertainty and reproducible backtests.
- Paper broker simulator.
- MT5 live adapter behind an explicit configuration gate.
- MT4 export-first support; no hidden terminal automation.

## Use it now

1. Export only account history you are authorized to use from MT4 or MT5 as a
   CSV file. The first importer expects headers equivalent to `Symbol`, `Type`,
   `Volume`, and `Profit`; optional open/close time columns are retained.
2. From this project folder, run:

   ```powershell
   $env:PYTHONPATH = "$PWD\src"
   python -m trading_strategy_lab.cli analyze-history C:\path\to\history.csv
   ```

3. Review the per-symbol trade count, profit, win/loss count, and side count.
   This does **not** claim to have reconstructed a strategy or predict future
  profitability.

4. To include candle grounding and candidate-pattern reporting:

   ```powershell
   $env:PYTHONPATH = "$PWD\src"
   python -m trading_strategy_lab.cli analyze-history C:\path\to\trades.csv --ohlc-csv C:\path\to\EURUSD_H1.csv
   ```

The report covers observable direction, sizing, SL/TP reward-risk placement,
and candle-grounding coverage. It explicitly lists what cannot be inferred.

## Modes

`analysis` and `backtest` never submit orders. `paper` writes simulated orders
only. `live` requires explicit confirmation, broker authorization, risk limits,
and a separate MT5 terminal adapter; that adapter is intentionally not yet
installed or connected.

Paper and live execution commands are intentionally not implemented yet. The
live safety gate exists but no broker connection or order submission exists.

For candle analysis, also export an OHLC CSV with `Time, Open, High, Low,
Close` columns. The importer grounds each trade only to the latest available
candle at or before its recorded entry time; missing or incompatible times
remain abstentions.
