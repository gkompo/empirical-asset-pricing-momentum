import pandas as pd
from config import TRANSACTION_COST_BPS


def apply_transaction_costs(weights: pd.DataFrame,
                             returns: pd.DataFrame):
    """
    Transaction cost model based on turnover.
    Costs are in basis points from config.
    """

    # align
    weights = weights.reindex(returns.index).fillna(0)

    # turnover (change in portfolio weights)
    turnover = weights.diff().abs().sum(axis=1)

    # convert bps → decimal
    costs = turnover * (TRANSACTION_COST_BPS / 10000)

    # strategy returns (NO lookahead bias)
    strat = (weights.shift(1) * returns).sum(axis=1)

    net_returns = strat - costs

    return net_returns