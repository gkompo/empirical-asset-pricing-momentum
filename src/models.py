import statsmodels.api as sm
import pandas as pd

def capm(stock_ret, market_ret):
    X = sm.add_constant(market_ret)
    # Fit OLS with Newey-West HAC standard errors (5 lags to adjust for daily autocorrelation)
    return sm.OLS(stock_ret, X, missing='drop').fit(cov_type='HAC', cov_kwds={'maxlags': 5})

def fama_french_5(stock_ret, ff5):
    X = sm.add_constant(ff5[['MKT_RF','SMB','HML','RMW','CMA']])
    # Fit OLS with Newey-West HAC standard errors (5 lags to adjust for daily autocorrelation)
    return sm.OLS(stock_ret, X, missing='drop').fit(cov_type='HAC', cov_kwds={'maxlags': 5})