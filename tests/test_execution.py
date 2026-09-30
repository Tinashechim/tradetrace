import unittest
from trading_strategy_lab.execution import ExecutionConfiguration, ExecutionMode, RiskLimits

class ExecutionSafetyTests(unittest.TestCase):
    def test_live_requires_all_gates(self):
        self.assertFalse(ExecutionConfiguration(mode=ExecutionMode.LIVE).permits_order_submission())
        limits = RiskLimits(1.0, 100.0, 5)
        self.assertFalse(ExecutionConfiguration(mode=ExecutionMode.LIVE, risk_limits=limits, broker_authorized=True).permits_order_submission())
        self.assertTrue(ExecutionConfiguration(mode=ExecutionMode.LIVE, risk_limits=limits, broker_authorized=True, explicit_live_confirmation=True).permits_order_submission())
        self.assertFalse(ExecutionConfiguration(mode=ExecutionMode.LIVE, risk_limits=RiskLimits(1.0, 100.0, 5, emergency_stop=True), broker_authorized=True, explicit_live_confirmation=True).permits_order_submission())
