"""Deterministic paper-order ledger; no broker connection."""
from dataclasses import dataclass,field
@dataclass
class PaperBroker:
 balance:float=10000.0;orders:list=field(default_factory=list)
 def submit(self,symbol,side,volume,price,reason="strategy_candidate"):
  if volume<=0 or price<=0:raise ValueError("Paper order needs positive volume and price")
  order={"order_id":f"paper_{len(self.orders)+1:06d}","symbol":symbol,"side":side,"volume":volume,"price":price,"reason":reason,"status":"simulated"};self.orders.append(order);return order
