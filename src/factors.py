import pandas as pd

def momentum_factor(returns, lookback=252):
    return returns.rolling(lookback).mean()

def lagged_excess_returns(returns, rf=0.0):
    return returns - rf