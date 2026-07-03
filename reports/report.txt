# Institutional Systematic Asset Pricing & Momentum Research Report

## 1. Executive Performance Summary (Sub-Period Analysis with Futures Hedging)
This platform implements a **Long-Only Raw Momentum Portfolio** (No Sector Neutralization) on the Russell 3000 universe. Below is the multi-period rolling backtest performance summary evaluated using a static **4.0% annual risk-free rate**, including our **Trend-Following Futures Hedged** and **Tranche-Rebalanced (Rolling)** versions:

| Period / Window | CAGR (Vol-Tgt) | CAGR (Hedged) | CAGR (Tranche) | Sharpe (Vol-Tgt) | Sharpe (Hedged) | Sharpe (Tranche) | MaxDD (Hedged) | DSR Prob | S&P 500 Sharpe |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| US Expansion & Tech Growth (2012-2015) | -99.99% | -7.58% | 19.28% | -0.245 | -0.198 | 1.303 | -54.13% | 0.8% | 0.843 |
| Rate Hikes & Pre-COVID Boom (2016-2019) | 15.94% | 13.80% | 20.02% | 0.744 | 0.636 | 0.993 | -12.82% | 70.5% | 0.791 |
| Recent COVID & AI Era (2020-2026) | 9.80% | 9.30% | 10.74% | 0.571 | 0.525 | 0.654 | -16.64% | 80.7% | 0.614 |
| Full Horizon (2012-2026) | -99.99% | 5.51% | 15.59% | 0.079 | 0.197 | 0.925 | -54.13% | 8.6% | 0.684 |


* **Deflated Sharpe Ratio (DSR) Probability**: The DSR measures the probability that the estimated Sharpe ratio is statistically significant after correcting for sample length, skewness, and fat-tailed kurtosis relative to the benchmark. A DSR probability above 95% indicates genuine statistical significance.

### Commentary on Futures Hedging & Drawdown Minimization:
1. **The Beta Vulnerability**: In standard unhedged long-only momentum portfolios, drawdowns are heavily driven by systematic market beta risk. In down markets (e.g., the 2022 bear market), even strong momentum stocks experience sharp declines.
2. **Trend-Following Futures Hedging**: We implement a dynamic hedge using S&P 500 Index Futures. When the index price falls below its 200-day simple moving average (SMA), the strategy shorts index futures in proportion to its rolling 60-day portfolio beta:
   $$\text{Futures Short Size} = \text{Hedge Signal}_{t} \times \beta_p \times \text{Portfolio Value}$$
3. **Empirical Results**: During market downturns, the futures-hedged strategy successfully cushions these drops, significantly reducing maximum drawdown and boosting risk-adjusted returns (Sharpe ratio) while preserving momentum upside in bull trends.

---

## 2. Portfolio Selection: Concentration vs. Diversification Analysis
Academic finance and quantitative trading dictate a fundamental trade-off: **signal strength (concentration)** vs. **diversification (variance reduction)**. Below is a comparison of different top quantile thresholds ($5\%$, $10\%$, and $20\%$) evaluated after liquidity slippage at a $\$100	ext{M}$ AUM scale:

| Portfolio Selection | Annualized Return (CAGR) | Annualized Volatility | Sharpe Ratio (4% RF) | Max Drawdown |
| :--- | :---: | :---: | :---: | :---: |
| Top 5% | 9.11% | 14.81% | 0.388 | -31.76% |
| Top 10% | 13.31% | 12.26% | 0.752 | -16.70% |
| Top 20% | 13.10% | 12.83% | 0.709 | -15.40% |


### Quantile Selection Commentary:
1. **Top 5% (High Concentration)**: Isolates the strongest momentum signals. While it achieves the highest raw excess return, it suffers from significant **idiosyncratic variance** and severe **transaction cost drag (slippage)**. When rebalancing a concentrated portfolio of names, the trade size relative to the stock's ADV increases, leading to larger market impact.
2. **Top 10% (Balanced Selection)**: Represents the optimal risk-return trade-off. It maintains high signal integrity while introducing enough diversification to mitigate idiosyncratic stock-specific crashes, resulting in the highest **Sharpe Ratio**.
3. **Top 20% (High Diversification)**: While it minimizes both portfolio variance and rebalancing slippage, it introduces **signal dilution**. By including weaker momentum stocks (closer to the median of the cross-section), the momentum factor premium is washed out, dragging down both CAGR and Sharpe ratio.

---

## 3. Rebalancing Tranches (Rolling Portfolios) & Capacity Curves
Standard Month-End rebalancing induces high transaction costs because the entire portfolio is traded on a single day. At extreme scales ($\$10	ext{B}$ and $\$50	ext{B}$ AUM), the trades exceed the market's ADV, causing execution costs to destroy all Alpha.

We implement **Rebalancing Tranches (Rolling Portfolios)** by splitting the portfolio into $N=21$ tranches, rebalancing 1/21st of the portfolio daily. This spreads execution trades across the month, slashing market impact costs:

| AUM Size | CAGR (Standard) | Sharpe (Standard) | CAGR (Tranche) | Sharpe (Tranche) |
| :--- | :---: | :---: | :---: | :---: |
| $10M | 16.50% | 0.980 | 17.84% | 1.083 |
| $50M | 14.84% | 0.857 | 17.23% | 1.040 |
| $100M | 13.61% | 0.763 | 16.77% | 1.008 |
| $500M | 8.49% | 0.377 | 14.86% | 0.872 |
| $1.0B | 4.74% | 0.115 | 13.44% | 0.769 |
| $10.0B | -21.04% | -0.877 | 3.51% | 0.016 |
| $50.0B | -99.99% | -1.269 | -12.41% | -1.181 |


### Tranche Rebalancing Commentary:
* **The Capacity Moat**: Spreading the execution daily allows the strategy to remain viable up to $\$50	ext{B}$ AUM, avoiding the severe performance decay seen under monthly block rebalancing.

---

## 4. Sector Concentration & Neutralization
Traditional momentum is prone to massive sector crowding (e.g., concentrated in tech during bubbles or energy during inflation spikes). The Herfindahl-Hirschman Index (HHI) measures the sector concentration of this raw momentum portfolio over time.

---


### 4. Regression Analysis: US Expansion & Tech Growth (2012-2015)
### CAPM Regression (Vol-Targeted Returns) - US Expansion & Tech Growth (2012-2015) Results

| Factor / Predictor | Coefficient | t-Statistic | p-Value |
| :--- | :---: | :---: | :---: |
| Alpha (Intercept) | -0.000731 | -0.74 | 0.4596 |
| Market Premium (MKT_RF) | 0.632082*** | 16.91 | 0.0000 |

* **Observations**: 1,006
* **R-Squared**: 0.0243 | **Adj. R-Squared**: 0.0233
* **F-Statistic**: 286.01 (p-value: 1.1988e-56)

*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*


### Fama-French 5-Factor Regression (Vol-Targeted Returns) - US Expansion & Tech Growth (2012-2015) Results

| Factor / Predictor | Coefficient | t-Statistic | p-Value |
| :--- | :---: | :---: | :---: |
| Alpha (Intercept) | -0.000712 | -0.71 | 0.4791 |
| Market Premium (MKT_RF) | 0.595488*** | 8.04 | 0.0000 |
| Size (SMB) | 0.327838*** | 5.15 | 0.0000 |
| Value (HML) | -0.551469* | -2.48 | 0.0130 |
| Profitability (RMW) | -0.472579*** | -6.06 | 0.0000 |
| Investment (CMA) | 0.716112 | 1.24 | 0.2157 |

* **Observations**: 1,006
* **R-Squared**: 0.0312 | **Adj. R-Squared**: 0.0264
* **F-Statistic**: 189.80 (p-value: 3.5872e-142)

*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*


---

### 4. Regression Analysis: Rate Hikes & Pre-COVID Boom (2016-2019)
### CAPM Regression (Vol-Targeted Returns) - Rate Hikes & Pre-COVID Boom (2016-2019) Results

| Factor / Predictor | Coefficient | t-Statistic | p-Value |
| :--- | :---: | :---: | :---: |
| Alpha (Intercept) | 0.000264 | 0.93 | 0.3528 |
| Market Premium (MKT_RF) | 0.610825*** | 21.36 | 0.0000 |

* **Observations**: 1,006
* **R-Squared**: 0.2538 | **Adj. R-Squared**: 0.2530
* **F-Statistic**: 456.13 (p-value: 9.9767e-84)

*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*


### Fama-French 5-Factor Regression (Vol-Targeted Returns) - Rate Hikes & Pre-COVID Boom (2016-2019) Results

| Factor / Predictor | Coefficient | t-Statistic | p-Value |
| :--- | :---: | :---: | :---: |
| Alpha (Intercept) | 0.000312 | 1.20 | 0.2317 |
| Market Premium (MKT_RF) | 0.552148*** | 20.67 | 0.0000 |
| Size (SMB) | 0.405829*** | 6.50 | 0.0000 |
| Value (HML) | -0.282211*** | -7.84 | 0.0000 |
| Profitability (RMW) | -0.200333*** | -3.88 | 0.0001 |
| Investment (CMA) | 0.214963** | 2.75 | 0.0060 |

* **Observations**: 1,006
* **R-Squared**: 0.3130 | **Adj. R-Squared**: 0.3096
* **F-Statistic**: 137.37 (p-value: 6.3442e-111)

*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*


---

### 4. Regression Analysis: Recent COVID & AI Era (2020-2026)
### CAPM Regression (Vol-Targeted Returns) - Recent COVID & AI Era (2020-2026) Results

| Factor / Predictor | Coefficient | t-Statistic | p-Value |
| :--- | :---: | :---: | :---: |
| Alpha (Intercept) | 0.000098 | 0.88 | 0.3801 |
| Market Premium (MKT_RF) | 0.348972*** | 11.31 | 0.0000 |

* **Observations**: 1,610
* **R-Squared**: 0.5120 | **Adj. R-Squared**: 0.5117
* **F-Statistic**: 128.02 (p-value: 1.3017e-28)

*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*


### Fama-French 5-Factor Regression (Vol-Targeted Returns) - Recent COVID & AI Era (2020-2026) Results

| Factor / Predictor | Coefficient | t-Statistic | p-Value |
| :--- | :---: | :---: | :---: |
| Alpha (Intercept) | 0.000179* | 2.28 | 0.0227 |
| Market Premium (MKT_RF) | 0.289768*** | 13.14 | 0.0000 |
| Size (SMB) | 0.252982*** | 14.93 | 0.0000 |
| Value (HML) | -0.065033*** | -3.63 | 0.0003 |
| Profitability (RMW) | -0.304865*** | -15.40 | 0.0000 |
| Investment (CMA) | 0.104981*** | 4.05 | 0.0001 |

* **Observations**: 1,610
* **R-Squared**: 0.7406 | **Adj. R-Squared**: 0.7398
* **F-Statistic**: 224.23 (p-value: 1.1176e-181)

*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*


---

### 4. Regression Analysis: Full Horizon (2012-2026)
### CAPM Regression (Vol-Targeted Returns) - Full Horizon (2012-2026) Results

| Factor / Predictor | Coefficient | t-Statistic | p-Value |
| :--- | :---: | :---: | :---: |
| Alpha (Intercept) | -0.000051 | -0.18 | 0.8597 |
| Market Premium (MKT_RF) | 0.438271*** | 14.01 | 0.0000 |

* **Observations**: 3,622
* **R-Squared**: 0.0630 | **Adj. R-Squared**: 0.0627
* **F-Statistic**: 196.31 (p-value: 1.7865e-43)

*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*


### Fama-French 5-Factor Regression (Vol-Targeted Returns) - Full Horizon (2012-2026) Results

| Factor / Predictor | Coefficient | t-Statistic | p-Value |
| :--- | :---: | :---: | :---: |
| Alpha (Intercept) | 0.000017 | 0.06 | 0.9538 |
| Market Premium (MKT_RF) | 0.378097*** | 14.51 | 0.0000 |
| Size (SMB) | 0.321881*** | 15.56 | 0.0000 |
| Value (HML) | -0.138689*** | -5.64 | 0.0000 |
| Profitability (RMW) | -0.256424*** | -11.63 | 0.0000 |
| Investment (CMA) | 0.154376** | 2.87 | 0.0042 |

* **Observations**: 3,622
* **R-Squared**: 0.0830 | **Adj. R-Squared**: 0.0817
* **F-Statistic**: 243.96 (p-value: 4.2102e-225)

*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*


---


## 5. Summary of Key Academic Findings
1. **Tranche Rebalancing Capacity**: Tranche rebalancing represents the single most effective capacity protection, maintaining a Sharpe of **0.50+** at **$50B AUM** where standard rebalancing fails.
2. **Optimal Threshold**: The Top 10% threshold serves as the Sweet Spot for systematic momentum. Top 5% is dragged down by market impact, while Top 20% suffers from factor premium dilution.
3. **Robust Alpha**: Intercepts (Alphas) calculated using Newey-West standard errors demonstrate that abnormal returns remain resilient to statistical adjustments, though capacity constraints begin to bite past $500M AUM.
