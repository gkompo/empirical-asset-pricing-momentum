import pandas as pd
import numpy as np


def backtest(returns: pd.DataFrame, weights: pd.DataFrame):
    """
    Vectorized backtest:
    - weights assumed aligned with returns index
    - uses lagged weights to avoid look-ahead bias
    """

    # ensure alignment
    weights = weights.reindex(returns.index).fillna(0)

    # shift weights (VERY IMPORTANT → no look-ahead bias)
    lagged_weights = weights.shift(1)

    # portfolio returns
    strat_returns = (lagged_weights * returns).sum(axis=1)

    equity_curve = (1 + strat_returns).cumprod()

    return strat_returns, equity_curve


def apply_monthly_rebalancing(weights: pd.DataFrame):
    """
    Forces weights to update only at month-end.
    Everything in between is held constant.
    """

    # take last available weight each month
    monthly_weights = weights.resample("ME").last()

    # forward-fill daily weights until next rebalance
    daily_weights = monthly_weights.reindex(weights.index).ffill()

    return daily_weights


def sharpe(returns):
    returns = returns.dropna()

    if len(returns) < 2:
        return 0.0

    std = returns.std()

    if std == 0 or np.isnan(std):
        return 0.0

    return np.sqrt(252) * returns.mean() / std