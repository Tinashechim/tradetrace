import tempfile,unittest
from pathlib import Path
from trading_strategy_lab.history import import_csv,summarize
from trading_strategy_lab.market import import_ohlc_csv,ground_trade_entries
from trading_strategy_lab.backtest import replay_sl_tp
from trading_strategy_lab.history import Trade
from trading_strategy_lab.market import Candle
from datetime import datetime
class HistoryTests(unittest.TestCase):
 def test_import(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/"h.csv";p.write_text("Symbol,Type,Volume,Profit\nEURUSD,buy,0.1,12.5\nEURUSD,sell,0.1,-4\n",encoding="utf-8");x=summarize(import_csv(p));self.assertEqual((x["trade_count"],x["symbols"]["EURUSD"]["wins"]),(2,1))
 def test_conservative_sl_tp_replay(self):
  t=Trade("EURUSD","buy",.1,0,entry_price=1.0,stop_loss=.9,take_profit=1.1);c=Candle(datetime(2026,1,1),1,1.11,.95,1.05);self.assertEqual(replay_sl_tp(t,[c])["status"],"take_profit")
 def test_ohlc_and_trade_grounding(self):
  with tempfile.TemporaryDirectory() as d:
   h=Path(d)/"h.csv";h.write_text("Symbol,Type,Volume,Profit,Open Time\nEURUSD,buy,0.1,1,2026.01.01 10:05:00\n",encoding="utf-8");c=Path(d)/"c.csv";c.write_text("Time,Open,High,Low,Close\n2026.01.01 10:00:00,1,2,0.5,1.5\n",encoding="utf-8");g=ground_trade_entries(import_csv(h),import_ohlc_csv(c));self.assertEqual((g[0]["status"],g[0]["candle"].close),("grounded",1.5))
