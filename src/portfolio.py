import numpy as np

def long_short_portfolio(signal, top_q=0.1, bottom_q=0.1):
    ranks = signal.rank(axis=1, pct=True)

    long = (ranks >= 1 - top_q).astype(int)
    short = (ranks <= bottom_q).astype(int)

    weights = long - short
    weights = weights.div(weights.abs().sum(axis=1), axis=0)

    return weights