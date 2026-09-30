"""Import authorized MT4/MT5 CSV trade-history exports without broker access."""
from dataclasses import dataclass
import csv
from pathlib import Path
_ALIASES={"symbol":{"symbol","instrument","pair"},"side":{"type","side","action"},"open_time":{"open time","time","open_time"},"close_time":{"close time","close_time"},"volume":{"volume","lots","size"},"profit":{"profit","p/l","pnl"},"entry_price":{"price","open price","entry price"},"stop_loss":{"s/l","sl","stop loss"},"take_profit":{"t/p","tp","take profit"}}
def _field(row,name):
 for key in _ALIASES[name]:
  if key in row and row[key] not in (None,""):return row[key]
 return None
@dataclass(frozen=True)
class Trade: symbol:str;side:str;volume:float;profit:float;open_time:str|None=None;close_time:str|None=None;entry_price:float|None=None;stop_loss:float|None=None;take_profit:float|None=None
def import_csv(path):
 with Path(path).open("r",encoding="utf-8-sig",newline="") as h:
  r=csv.DictReader(h)
  if not r.fieldnames:raise ValueError("CSV has no header row")
  out=[]
  for n,row in enumerate(r,2):
   row={(key or "").strip().lower():value for key,value in row.items()}
   symbol,side,volume,profit=(_field(row,k) for k in ("symbol","side","volume","profit"))
   if None in (symbol,side,volume,profit):raise ValueError(f"Row {n} lacks symbol, side/type, volume, or profit")
   try:
    optional=lambda key:float(str(_field(row,key)).replace(",","")) if _field(row,key) is not None else None
    out.append(Trade(str(symbol).strip(),str(side).strip().lower(),float(str(volume).replace(",","")),float(str(profit).replace(",","")),_field(row,"open_time"),_field(row,"close_time"),optional("entry_price"),optional("stop_loss"),optional("take_profit")))
   except ValueError as e:raise ValueError(f"Row {n} has invalid numeric trade data") from e
 if not out:raise ValueError("CSV contains no trade rows")
 return out
def summarize(trades):
 symbols={}
 for t in trades:
  x=symbols.setdefault(t.symbol,{"trades":0,"profit":0.,"wins":0,"losses":0,"sides":{}});x["trades"]+=1;x["profit"]+=t.profit;x["wins"]+=t.profit>0;x["losses"]+=t.profit<0;x["sides"][t.side]=x["sides"].get(t.side,0)+1
 return {"trade_count":len(trades),"symbols":symbols,"warning":"Descriptive history summary only; not a recovered strategy or profitability prediction."}
