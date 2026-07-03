import pandas as pd
import numpy as np

def volatility_targeting(returns, target_vol=0.10, ewma_alpha=0.06):
    if ewma_alpha > 0.0:
        # EWMA conditional volatility forecasting (RiskMetrics standard is alpha=0.06 / lambda=0.94)
        vol = returns.ewm(alpha=ewma_alpha).std() * (252 ** 0.5)
    else:
        # Simple rolling volatility
        vol = returns.rolling(20).std() * (252 ** 0.5)
        
    scaling = target_vol / vol
    return scaling.shift(1).clip(0, 3)