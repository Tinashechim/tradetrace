"""Execution-mode boundary. No broker API is called from this module."""
from dataclasses import dataclass
from enum import Enum

class ExecutionMode(str, Enum):
    ANALYSIS = "analysis"
    BACKTEST = "backtest"
    PAPER = "paper"
    LIVE = "live"

@dataclass(frozen=True)
class RiskLimits:
    max_position_size: float
    max_daily_loss: float
    max_orders_per_day: int
    emergency_stop: bool = False

    def validate(self):
        if self.max_position_size <= 0 or self.max_daily_loss <= 0 or self.max_orders_per_day <= 0:
            raise ValueError("Risk limits must be positive")
        return True

@dataclass(frozen=True)
class ExecutionConfiguration:
    mode: ExecutionMode = ExecutionMode.ANALYSIS
    explicit_live_confirmation: bool = False
    broker_authorized: bool = False
    risk_limits: RiskLimits | None = None

    def permits_order_submission(self) -> bool:
        if self.mode is not ExecutionMode.LIVE:
            return False
        if not self.explicit_live_confirmation or not self.broker_authorized or self.risk_limits is None:
            return False
        self.risk_limits.validate()
        return not self.risk_limits.emergency_stop
