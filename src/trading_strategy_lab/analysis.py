"""Transparent candidate descriptions; never claims an unknown strategy is recovered."""
from collections import Counter
def candidate_report(trades, grounded):
 symbols=Counter(t.symbol for t in trades);sides=Counter(t.side for t in trades);volumes=Counter(t.volume for t in trades)
 sltp=[t for t in trades if t.entry_price is not None and t.stop_loss is not None and t.take_profit is not None]
 ratios=[]
 for t in sltp:
  risk=abs(t.entry_price-t.stop_loss);reward=abs(t.take_profit-t.entry_price)
  if risk:ratios.append(reward/risk)
 return {"candidate_patterns":{"symbols":dict(symbols),"directions":dict(sides),"common_volumes":dict(volumes),"mean_declared_reward_risk":sum(ratios)/len(ratios) if ratios else None,"grounded_entries":sum(x["status"]=="grounded" for x in grounded)},"limitations":["Trade history does not reveal unrecorded entry signals.","Candidate patterns are hypotheses, not recovered truth.","No pair is assumed transferable without separate testing."]}
