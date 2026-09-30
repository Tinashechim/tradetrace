"""Authorized OHLC candle CSV import and conservative trade-to-candle grounding."""
from dataclasses import dataclass
from datetime import datetime
import csv
from pathlib import Path

def _time(value):
    for fmt in (None, "%Y.%m.%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"):
        try: return datetime.fromisoformat(value) if fmt is None else datetime.strptime(value, fmt)
        except ValueError: pass
    raise ValueError(f"Unsupported timestamp: {value}")

@dataclass(frozen=True)
class Candle:
    time: datetime; open: float; high: float; low: float; close: float; volume: float | None = None

def import_ohlc_csv(path):
    with Path(path).open("r", encoding="utf-8-sig", newline="") as handle:
        rows=[]
        for number,row in enumerate(csv.DictReader(handle),2):
            row={(key or "").strip().lower():value for key,value in row.items()}
            try: rows.append(Candle(_time(row.get("time") or row.get("date")),float(row["open"]),float(row["high"]),float(row["low"]),float(row["close"]),float(row["volume"]) if row.get("volume") else None))
            except (KeyError,TypeError,ValueError) as exc: raise ValueError(f"Invalid OHLC row {number}") from exc
    if not rows: raise ValueError("OHLC CSV contains no candles")
    return sorted(rows,key=lambda candle:candle.time)

def ground_trade_entries(trades,candles):
    """Attach only the latest available candle at/before a parseable trade entry."""
    grounded=[]
    for trade in trades:
        if not trade.open_time: grounded.append({"trade":trade,"status":"abstained_missing_open_time"});continue
        entry=_time(trade.open_time);matches=[c for c in candles if c.time<=entry]
        grounded.append({"trade":trade,"status":"grounded" if matches else "abstained_no_prior_candle","candle":matches[-1] if matches else None})
    return grounded
