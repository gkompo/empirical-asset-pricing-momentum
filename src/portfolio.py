import numpy as np

def long_short_portfolio(signal, top_q=0.1, bottom_q=0.1, long_only=False, sectors=None):
    if sectors is not None:
        # Sector neutralization: subtract the cross-sectional mean of each sector
        aligned_sectors = sectors.reindex(signal.columns).fillna("Unknown")
        sector_means = signal.T.groupby(aligned_sectors).transform('mean').T
        signal = signal - sector_means

    ranks = signal.rank(axis=1, pct=True)

    long = (ranks >= 1 - top_q).astype(int)
    
    if long_only:
        weights = long
    else:
        short = (ranks <= bottom_q).astype(int)
        weights = long - short
        
    weights = weights.div(weights.abs().sum(axis=1), axis=0).fillna(0.0)

    return weights