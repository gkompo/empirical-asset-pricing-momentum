import pandas as pd
import numpy as np

def volatility_targeting(returns, target_vol=0.10, ewma_alpha=0.06):
    if ewma_alpha > 0.0:
        # EWMA conditional volatility forecasting (RiskMetrics standard is alpha=0.06 / lambda=0.94)
        vol = returns.ewm(alpha=ewma_alpha, min_periods=2).std() * (252 ** 0.5)
    else:
        # Simple rolling volatility with min_periods to prevent long flat startup window
        vol = returns.rolling(20, min_periods=2).std() * (252 ** 0.5)
        
    # Backfill startup window NaNs to avoid flat lines in cumulative return charts
    vol = vol.bfill().fillna(target_vol)
    
    scaling = target_vol / vol
    return scaling.shift(1).fillna(1.0).clip(0, 3)