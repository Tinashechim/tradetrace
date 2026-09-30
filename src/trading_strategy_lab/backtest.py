"""Conservative candle replay for recorded SL/TP; no inferred entries."""
def replay_sl_tp(trade,candles):
 if None in (trade.entry_price,trade.stop_loss,trade.take_profit):return {"status":"abstained_missing_entry_or_sl_tp"}
 hits=[]
 for c in candles:
  if trade.side in {"buy","long"}:
   sl=c.low<=trade.stop_loss;tp=c.high>=trade.take_profit
  else: sl=c.high>=trade.stop_loss;tp=c.low<=trade.take_profit
  if sl and tp:return {"status":"abstained_ambiguous_same_candle","time":c.time}
  if sl:return {"status":"stop_loss","time":c.time,"price":trade.stop_loss}
  if tp:return {"status":"take_profit","time":c.time,"price":trade.take_profit}
 return {"status":"unresolved_end_of_data"}
