import numpy as np

def long_short_portfolio(signal, top_q=0.1, bottom_q=0.1, long_only=False, sectors=None, vols=None):
    if sectors is not None:
        # Sector neutralization: subtract the cross-sectional mean of each sector
        aligned_sectors = sectors.reindex(signal.columns).fillna("Unknown")
        sector_means = signal.T.groupby(aligned_sectors).transform('mean').T
        signal = signal - sector_means

    ranks = signal.rank(axis=1, pct=True)

    long = (ranks >= 1 - top_q).astype(float)
    
    if vols is not None:
        # Inverse Volatility Weighting with risk floors to avoid penny/flatline stock cost spikes
        vols_clipped = vols.clip(lower=0.005)
        vols_valid = (vols >= 0.005).astype(float)
        inv_vol = 1.0 / (vols_clipped + 1e-8)
        weights = long * inv_vol * vols_valid
    else:
        weights = long
        
    if not long_only:
        short = (ranks <= bottom_q).astype(float)
        if vols is not None:
            weights = weights - (short * inv_vol * vols_valid)
        else:
            weights = weights - short
        
    weights = weights.div(weights.abs().sum(axis=1), axis=0).fillna(0.0)

    return weights