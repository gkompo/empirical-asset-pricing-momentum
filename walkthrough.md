# Walkthrough - Institutional Systematic Asset Pricing Platform

We have successfully rebuilt the systematic platform to use **Inverse Volatility Weighting** for portfolio stock weights, removed the volatility targeting scaling mechanism, disabled sector neutralization, set the portfolio selection (concentration vs. diversification) comparison AUM scale to **$1M**, removed all sector concentration (HHI) calculations, and re-run all backtests to output updated figures and metrics.

---

## 1. Performance Summary (Sub-Periods & Futures Hedging)

Using Fama-French daily benchmarks to ensure statistical and economic alignment, we evaluated the **Long-Only Inverse Volatility Weighted Raw Momentum Strategy** across four macro market windows, comparing unhedged vs. futures-hedged versions for Gross, Net, and Tranche-Rebalanced portfolios at a **$1M AUM scale**:

| Period / Window | CAGR (Gross) | CAGR (Gross Hedged) | CAGR (Net) | CAGR (Net Hedged) | CAGR (Tranche) | Sharpe (Net Hedged) | Sharpe (Tranche) | MaxDD (Net Hedged) | DSR | S&P500 Sharpe |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **US Expansion (2012-2015)** | 29.09% | 24.35% | 27.50% | 22.81% | **28.44%** | 1.053 | **1.271** | -15.63% | 87.7% | 0.843 |
| **Rate Hikes (2016-2019)** | 18.46% | 14.27% | 17.19% | 13.05% | **18.75%** | 0.604 | **0.832** | -24.46% | 63.4% | 0.791 |
| **COVID & AI (2020-2026)** | 31.67% | 25.42% | 30.92% | 24.71% | **30.87%** | 0.847 | **0.909** | -31.37% | 85.1% | 0.614 |
| **Full Horizon (2012-2026)** | 27.16% | 21.93% | 26.03% | 20.85% | **26.73%** | 0.824 | **0.937** | -33.97% | 92.3% | 0.684 |

### Quantitative Highlights:
* **No Volatility Targeting**: Strategy returns are determined directly by the Inverse Volatility Weighted stock selection, without artificial leverage scaling.
* **Inverse Volatility Weighting**: Controls stock-specific risk concentrations directly in weights:
  $$w_{i,t} = \frac{1/\sigma_{i,t}}{\sum_{j} 1/\sigma_{j,t}}$$
  An institutional daily volatility floor of **0.005** (8% annualized) and filter are applied to completely isolate the portfolio from illiquid, zero-volume shell companies.
* **Trend-Following Futures Hedging**: shorts S&P 500 Index Futures when the index is below its 200-day simple moving average (SMA), in proportion to the rolling 60-day portfolio beta, successfully minimizing market-wide drawdowns.

#### Multi-Period PnL Growth Charts
````carousel
![Full Horizon General PnL](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/equity_curve_general_full_horizon_2012-2026.png)
<!-- slide -->
![Recent COVID & AI General PnL](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/equity_curve_general_recent_covid__ai_era_2020-2026.png)
<!-- slide -->
![Rate Hikes General PnL](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/equity_curve_general_rate_hikes__pre-covid_boom_2016-2019.png)
<!-- slide -->
![US Expansion General PnL](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/equity_curve_general_us_expansion__tech_growth_2012-2015.png)
````

#### Futures Hedging Impact Analysis Charts
````carousel
![Full Horizon Hedging PnL](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/equity_curve_hedging_full_horizon_2012-2026.png)
<!-- slide -->
![Recent COVID & AI Hedging PnL](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/equity_curve_hedging_recent_covid__ai_era_2020-2026.png)
<!-- slide -->
![Rate Hikes Hedging PnL](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/equity_curve_hedging_rate_hikes__pre-covid_boom_2016-2019.png)
<!-- slide -->
![US Expansion Hedging PnL](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/equity_curve_hedging_us_expansion__tech_growth_2012-2015.png)
````

---

## 2. Selection Quantiles (1%, 3%, 5%, 10%, 20%)

We simulated different selection thresholds for the raw momentum basket at a **$1M AUM scale** as requested. Within all compared portfolio selections, we use the exact same **Inverse Volatility Weighting** algorithm ($w_i \propto 1/\sigma_i$) as defined in Section 1. If $N$ stocks are selected in the Top $Q\%$ rank on date $t$, their cross-sectional weights are allocated inversely to their rolling 20-day daily standard deviation (clipped to the 0.005 risk floor and filtered) and normalized to sum to 1.0. This holds the weighting methodology constant to isolate only the effect of portfolio concentration vs. diversification:

| Portfolio Selection | Annualized Return (CAGR) | Annualized Volatility | Sharpe Ratio (4% RF) | Max Drawdown |
| :--- | :---: | :---: | :---: | :---: |
| **Top 1% (Concentrated)** | **47.25%** | 64.23% | 0.814 | -72.92% |
| **Top 3% (Optimal Sharpe)** | **37.76%** | **33.29%** | **1.007** | **-41.56%** |
| **Top 5%** | 31.16% | 28.81% | 0.947 | -41.08% |
| **Top 10%** | 26.04% | 24.46% | 0.906 | -42.55% |
| **Top 20% (Diversified)** | 21.41% | 21.46% | 0.825 | -40.27% |

* **Optimal Balanced Selection**: At $1M AUM, the **Top 3%** selection achieves the highest Sharpe ratio (**1.007**) and a stellar CAGR of **37.76%**. At this AUM scale, execution costs are low enough to make the highly concentrated factor premium viable.

#### Selection Quantiles PnL Comparison
![Quantile Comparison](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/quantile_comparison.png)

---

## 3. Slippage Capacity Curve: Standard vs. Tranche Rebalancing

We compared the execution decay of standard month-end block rebalancing against daily rolling tranche rebalancing across portfolio sizes from **$100K AUM up to $1B AUM** (deleting $10B and $50B AUM levels):

| AUM Size | CAGR (Standard) | Sharpe (Standard) | CAGR (Tranche) | Sharpe (Tranche) |
| :--- | :---: | :---: | :---: | :---: |
| **$100K** | 26.51% | 0.921 | **26.85%** | **0.941** |
| **$500K** | 26.24% | 0.913 | **26.78%** | **0.939** |
| **$1M** | 26.04% | 0.906 | **26.73%** | **0.937** |
| **$5M** | 25.20% | 0.878 | **26.51%** | **0.930** |
| **$10M** | 24.57% | 0.857 | **26.34%** | **0.924** |
| **$50M** | 21.94% | 0.768 | **25.64%** | **0.901** |
| **$100M** | 19.99% | 0.700 | **25.11%** | **0.884** |
| **$500M** | 11.91% | 0.413 | **22.92%** | **0.811** |
| **$1.0B** | 6.01% | 0.209 | **21.30%** | **0.756** |

* **Tranche Capacity Edge**: Tranche rebalancing mitigates market impact decay, preserving a **0.756 Sharpe ratio** and **21.30% CAGR** at $1B AUM, whereas standard monthly block rebalancing collapses to **0.209 Sharpe** (6.01% CAGR) due to execution slippage.

#### Slippage Capacity Curve Comparison
![Capacity Decay](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/capacity_decay.png)

---

## 4. Institutional Routing Strategies to Minimize Slippage (AUM $100M - $50B)

Executing block-size momentum trades directly onto lit exchanges (such as NYSE or NASDAQ) triggers massive adverse selection and market impact, particularly at scales between **$100M and $50B AUM**. To mitigate this decay, the execution pipeline should be routed via a Smart Order Router (SOR) utilizing the following institutional mechanisms:
* **Dark Pool Crossing & Block Networks ($100M - $1B AUM)**: Orders should be routed to dark crossing networks (e.g., Liquidnet, Instinet BlockMatch, or ITG Posit) to match blocks internally. This prints trades to the tape only after execution, bypassing the public limit order books and preventing front-running.
* **Volume/Time-Scheduled Algorithmic Routing ($1B - $10B AUM)**: Order slicing must be scheduled using Time-Weighted Average Price (TWAP) or Volume-Weighted Average Price (VWAP) algorithms. The execution rate should be dynamically throttled to keep the Participation Rate (POV) strictly under **5% of the security's rolling 20-day Average Daily Volume (ADV)**, minimizing market signature.
* **Internalization & OTC Liquidity Desks ($10B - $50B AUM)**: At mega-cap scale, the portfolio's rebalancing flow should be crossed internally against secondary strategies (such as mean-reversion or value portfolios). Any residual flow is negotiated directly with institutional market makers via bilateral over-the-counter (OTC) block desks, avoiding public exchange books completely.
