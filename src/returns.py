import pandas as pd

def compute_returns(prices: pd.DataFrame):
    return prices.pct_change().dropna()