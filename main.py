from src.data_loader import load_prices, load_universe, align_universe, clean_prices
from src.returns import compute_returns
from src.factors import momentum_factor
from src.portfolio import long_short_portfolio
from src.backtest import backtest, apply_monthly_rebalancing
from src.costs import apply_transaction_costs
from src.risk import volatility_targeting
from src.statistics import sharpe_ratio
from config import LOOKBACK, TARGET_VOL

import os
import json
import matplotlib.pyplot as plt

# =========================
# CREATE OUTPUT FOLDERS
# =========================
os.makedirs("results/figures", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# =========================
# LOAD DATA
# =========================
prices = load_prices(r"data/close.parquet")
universe = load_universe(r"data/IWV_holdings.csv")

prices = align_universe(prices, universe)
prices = clean_prices(prices)

# =========================
# RETURNS
# =========================
returns = compute_returns(prices)

# =========================
# MOMENTUM SIGNAL
# =========================
signal = momentum_factor(returns, lookback=LOOKBACK)

# =========================
# PORTFOLIO
# =========================
weights = long_short_portfolio(signal)

# =========================
# REBALANCE (MONTHLY)
# =========================
weights = apply_monthly_rebalancing(weights)

# =========================
# GROSS RETURNS
# =========================
gross_returns = (weights.shift(1) * returns).sum(axis=1)

# =========================
# NET RETURNS (COSTS)
# =========================
net_returns = apply_transaction_costs(weights, returns)

# =========================
# VOL TARGETING
# =========================
vol_scaled = volatility_targeting(net_returns, TARGET_VOL)
final_returns = net_returns * vol_scaled

# =========================
# EQUITY CURVE
# =========================
equity = (1 + final_returns).cumprod()

# =========================
# METRICS
# =========================
raw_sharpe = sharpe_ratio(gross_returns)
net_sharpe = sharpe_ratio(net_returns)
final_sharpe = sharpe_ratio(final_returns)

print("\n====================")
print("RESULTS")
print("====================")
print(f"Raw Sharpe:   {raw_sharpe:.3f}")
print(f"Net Sharpe:   {net_sharpe:.3f}")
print(f"Vol Adjusted: {final_sharpe:.3f}")

# =========================
# SAVE METRICS
# =========================
results = {
    "raw_sharpe": float(raw_sharpe),
    "net_sharpe": float(net_sharpe),
    "vol_adjusted_sharpe": float(final_sharpe)
}

with open("results/metrics.json", "w") as f:
    json.dump(results, f, indent=4)

# =========================
# SAVE EQUITY CURVE
# =========================
equity.to_frame("equity").to_csv("results/equity_curve.csv")

plt.figure()
equity.plot()
plt.title("Equity Curve")
plt.savefig("results/figures/equity_curve.png")
plt.close()

# =========================
# REPORT
# =========================
from src.report import summary_text

report = summary_text(raw_sharpe)

with open("reports/report.txt", "w") as f:
    f.write(report)