from src.data_loader import load_prices, load_universe, align_universe, clean_prices
from src.returns import compute_returns
from src.factors import momentum_factor
from src.costs import apply_transaction_costs
from src.risk import volatility_targeting
from src.statistics import sharpe_ratio, volatility

import pandas as pd
import numpy as np

# Load data
prices = load_prices("data/close.parquet")
universe = load_universe("data/IWV_holdings.csv")
prices = align_universe(prices, universe)
prices = clean_prices(prices)
returns = compute_returns(prices)

# Signal
signal = momentum_factor(returns, lookback=252)

# Long-only portfolio weights
ranks = signal.rank(axis=1, pct=True)
long = (ranks >= 0.9).astype(int) # Top 10%
weights_long = long.div(long.abs().sum(axis=1), axis=0).fillna(0.0)

# Rebalance
from src.backtest import apply_monthly_rebalancing
weights_long_rebal = apply_monthly_rebalancing(weights_long)

# Gross Returns
gross_returns_long = (weights_long_rebal.shift(1) * returns).sum(axis=1)

# Net Returns
net_returns_long = apply_transaction_costs(weights_long_rebal, returns)

# Vol Targeting
vol_scaled_long = volatility_targeting(net_returns_long, 0.10)
final_returns_long = net_returns_long * vol_scaled_long

# Helper stats
def stats(ret_series, name):
    ann_ret = (1 + ret_series).cumprod().iloc[-1] ** (252.0 / len(ret_series)) - 1.0
    ann_vol = volatility(ret_series)
    sr = sharpe_ratio(ret_series)
    print(f"{name:15} | Ann. Return: {ann_ret:6.2%} | Ann. Vol: {ann_vol:6.2%} | Sharpe: {sr:5.3f}")

print("--- LONG-ONLY PERFORMANCE ---")
stats(gross_returns_long, "Gross Long-Only")
stats(net_returns_long, "Net Long-Only")
stats(final_returns_long, "Vol-Target Long")

# Let's compare with short-only
short = (ranks <= 0.1).astype(int) # Bottom 10%
weights_short = short.div(short.abs().sum(axis=1), axis=0).fillna(0.0)
weights_short_rebal = apply_monthly_rebalancing(weights_short)
gross_returns_short = (weights_short_rebal.shift(1) * returns).sum(axis=1)

print("\n--- SHORT-ONLY PERFORMANCE ---")
stats(gross_returns_short, "Gross Short-Only")
