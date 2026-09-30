"""Placeholder for a separately configured MT5 adapter; cannot submit orders."""
from .execution import ExecutionConfiguration
def submit_order(configuration:ExecutionConfiguration, order:dict):
 if not configuration.permits_order_submission():raise PermissionError("Live submission is disabled until all explicit gates are satisfied")
 raise NotImplementedError("MT5 live adapter requires separate broker/terminal configuration and is not installed")
