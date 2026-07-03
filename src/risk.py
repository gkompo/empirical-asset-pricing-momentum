import pandas as pd
import numpy as np

def volatility_targeting(returns, target_vol=0.10):
    vol = returns.rolling(20).std() * (252 ** 0.5)
    scaling = target_vol / vol
    return scaling.clip(0, 3)