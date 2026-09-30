# TradeTrace — User Guide

## By Tinashe Chimanikire

## Installation

### Available now: offline analysis

1. Install Python 3.11 or later from [python.org](https://www.python.org/).
   During installation, select **Add Python to PATH**.
2. Keep the TradeTrace folder at:
   `C:\Users\gadcet\Desktop\TradeTrace`
3. Open PowerShell and run:

   ```powershell
   cd C:\Users\gadcet\Desktop\TradeTrace
   $env:PYTHONPATH = "$PWD\src"
   python -m trading_strategy_lab.ui
   ```

No broker login, MT4/MT5 installation, API package, or trading permission is
needed for offline CSV analysis.

### Future MT5 live connector

When the MT5 connector is released, you will install and sign in to your own
MT5 terminal, then install the official `MetaTrader5` Python package. You will
manually enable automated trading in MT5 and explicitly select the terminal and
account in TradeTrace. These steps are not available yet.

### Future MT4 live connector

When the MT4 connector is released, you will manually copy the supplied Expert
Advisor bridge into your own MT4 `Experts` folder, compile it in MetaEditor, and
attach it to a chart. The bridge will show its connection state. These steps are
not available yet.

## Prepare your files

Export authorized MT4/MT5 closed-trade history as CSV. Required columns:
`Symbol, Type, Volume, Profit`. Optional columns: `Open Time`, `Close Time`,
`Price`/`Open Price`, `S/L`/`Stop Loss`, and `T/P`/`Take Profit`.

For candle analysis, export a separate OHLC CSV with:
`Time, Open, High, Low, Close`. Keep one candle file per symbol/timeframe.

## Run analysis

Open PowerShell in `C:\Users\gadcet\Desktop\TradeTrace`, then run:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m trading_strategy_lab.cli analyze-history C:\path\to\trades.csv
```

For candle grounding and candidate-pattern reporting:

```powershell
python -m trading_strategy_lab.cli analyze-history C:\path\to\trades.csv --ohlc-csv C:\path\to\EURUSD_H1.csv
```

## Understand the result

The report describes observable symbol, direction, sizing, declared SL/TP
reward-risk, and candle-grounding patterns. It does not prove the original
strategy, predict profit, or assume a strategy works on another pair. Missing
timestamps/candles remain abstentions rather than guessed matches.

## Paper and live modes

Paper and live commands are not available yet. Importing a CSV never enables
live trading. Future live mode requires explicit confirmation, broker
authorization, positive risk limits, and an emergency stop.

## How platform connection will work

### MT5

TradeTrace will connect to a **locally running MT5 terminal** through the
official MetaTrader 5 Python interface. You will choose the terminal/account
in TradeTrace, and you will manually enable automated trading in MT5. The app
will first verify account, symbol availability, margin, risk limits, and order
parameters. It will never store a password in a CSV or switch itself to live
mode after import.

### MT4

MT4 has no equivalent official Python terminal interface. TradeTrace will use
an explicitly installed **MT4 Expert Advisor bridge** that you place in the
terminal's `Experts` folder and attach to a chart yourself. The bridge will
communicate only with the local TradeTrace app and will show its enabled/disabled
state in MT4. It will not use hidden terminal automation, remote access, or
credential collection.

### Before any live order

1. Select `paper` mode and validate behavior with the same symbol and broker.
2. Set maximum position size, maximum daily loss, maximum orders per day, and
   an emergency stop.
3. Explicitly select `live` and confirm the account in the interface.
4. TradeTrace must pass broker/account/symbol/margin checks before each order.

Live MT4/MT5 connectors are not implemented yet; this section describes the
planned user-controlled connection path, not a currently available feature.
