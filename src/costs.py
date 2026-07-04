import pandas as pd
from config import TRANSACTION_COST_BPS


import numpy as np

def apply_transaction_costs(weights: pd.DataFrame,
                             returns: pd.DataFrame,
                             prices: pd.DataFrame = None,
                             volumes: pd.DataFrame = None,
                             aum: float = 0.0,
                             flat_bps: float = 5.0,
                             gamma: float = 0.5):
    """
    Transaction cost model.
    - If aum > 0 and prices/volumes are provided, uses a non-linear Market Impact model.
    - Otherwise, falls back to a flat turnover-based BPs cost model.
    """
    # align
    weights = weights.reindex(returns.index).fillna(0)

    # Trade weights (turnover)
    trade_weights = weights.diff().abs()

    if aum > 0.0 and prices is not None and volumes is not None:
        # Align prices & volumes
        prices = prices.reindex(returns.index).ffill()
        volumes = volumes.reindex(returns.index).ffill()

        # Lagged rolling metrics to avoid lookahead bias
        daily_vol = returns.rolling(20).std().shift(1)
        adv_shares = volumes.rolling(20).mean().shift(1).clip(lower=1000.0)

        # Estimate trade size in shares (using price floor of $1.00 to prevent penny-stock division spikes)
        trade_shares = trade_weights * aum / (prices.clip(lower=1.0) + 1e-8)

        # Market impact term (gamma * vol * sqrt(trade_shares / ADV))
        ratio = trade_shares / (adv_shares + 1e-8)
        ratio = ratio.fillna(0.0).clip(lower=0.0)
        market_impact = gamma * daily_vol.fillna(0.0) * np.sqrt(ratio)

        # Total cost rate per trade
        total_slippage = (flat_bps / 10000.0) + market_impact

        # Portfolio-level daily costs
        costs = (trade_weights * total_slippage).sum(axis=1)
    else:
        # Flat cost model based on turnover
        turnover = trade_weights.sum(axis=1)
        costs = turnover * (TRANSACTION_COST_BPS / 10000.0)

    # Strategy returns (NO lookahead bias)
    strat = (weights.shift(1) * returns).sum(axis=1)
    net_returns = strat - costs

    return net_returns