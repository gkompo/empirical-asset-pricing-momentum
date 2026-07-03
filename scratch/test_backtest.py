from src.data_loader import load_prices, load_universe, align_universe, clean_prices
from src.returns import compute_returns
from src.factors import momentum_factor
from src.portfolio import long_short_portfolio
from src.backtest import backtest, apply_monthly_rebalancing

prices = load_prices("data/close.parquet")
universe = load_universe("data/IWV_holdings.csv")

prices = align_universe(prices, universe)
prices = clean_prices(prices)

returns = compute_returns(prices)
print(f"Returns shape: {returns.shape}")
print(f"Returns head:\n{returns.head(3)}")

signal = momentum_factor(returns, lookback=252)
print(f"Signal shape: {signal.shape}")
print(f"Signal non-nan values in first rows: {signal.notna().sum(axis=1).head(260)}")

weights = long_short_portfolio(signal)
print(f"Weights shape: {weights.shape}")
print(f"Weights non-zero values count per day: {(weights != 0).sum(axis=1).head(270)}")
print(f"Weights sum per day: {weights.sum(axis=1).head(270)}")

weights_rebalanced = apply_monthly_rebalancing(weights)
print(f"Weights rebalanced shape: {weights_rebalanced.shape}")
print(f"Weights rebalanced non-zero: {(weights_rebalanced != 0).sum(axis=1).head(270)}")

gross_returns = (weights_rebalanced.shift(1) * returns).sum(axis=1)
print(f"Gross returns non-zero count: {(gross_returns != 0).sum()}")
print(f"Gross returns head:\n{gross_returns.head(270)}")
