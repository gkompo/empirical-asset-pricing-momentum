from src.data_loader import load_prices, load_universe, align_universe, clean_prices

prices = load_prices("data/close.parquet")
universe = load_universe("data/IWV_holdings.csv")

print(f"Prices shape: {prices.shape}")
print(f"Universe length: {len(universe)}")
print(f"First 10 tickers in universe: {universe[:10]}")
print(f"First 10 columns in prices: {list(prices.columns[:10])}")

common = [c for c in prices.columns if c in universe]
print(f"Common columns count: {len(common)}")

prices_aligned = align_universe(prices, universe)
print(f"Aligned prices shape: {prices_aligned.shape}")
