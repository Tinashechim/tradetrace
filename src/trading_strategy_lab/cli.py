import argparse,json
from . import APP_NAME, AUTHOR
from .history import import_csv,summarize
from .market import import_ohlc_csv,ground_trade_entries
from .analysis import candidate_report
from .paper import PaperBroker
def main():
 p=argparse.ArgumentParser(prog="tradetrace",description=f"{APP_NAME} — By {AUTHOR}");p.add_argument("--version",action="version",version=f"{APP_NAME} — By {AUTHOR}");s=p.add_subparsers(dest="command",required=True);a=s.add_parser("analyze-history",help="Analyze authorized MT4/MT5 exports");a.add_argument("trades_csv");a.add_argument("--ohlc-csv");x=p.parse_args();trades=import_csv(x.trades_csv);out={"application":APP_NAME,"author":AUTHOR,"history":summarize(trades)}
 if x.ohlc_csv:
  grounded=ground_trade_entries(trades,import_ohlc_csv(x.ohlc_csv));out["candidate_report"]=candidate_report(trades,grounded)
 print(json.dumps(out,indent=2,sort_keys=True,default=str))
if __name__=="__main__":main()
