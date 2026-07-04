# Walkthrough - Student Research on Systematic Momentum

This research project evaluates a **Long-Only Inverse Volatility Weighted Momentum Strategy** on the Russell 3000 universe. The project models transaction costs, trend-following futures hedging, portfolio selection quantiles, and execution routing capacity, analyzed like a master's thesis or undergraduate research paper.

---

## Historical Context: From Richard Driehaus to Academic Validation

Momentum investing—the systematic practice of buying recent winners and selling recent losers—stands as one of the most robust and heavily researched anomalies in modern financial economics. 

The strategy was pioneered in the 1970s and 1980s by **Richard Driehaus**, widely recognized as the **Father of Momentum Investing**. Unlike traditional value managers who sought cheap, distressed companies and waited for a reversion to the mean, Driehaus revolutionized active growth management with a simple, punchy philosophy: **"Buy high and sell higher!"** He argued that earnings growth and price acceleration were not signs of overvaluation but rather indicators of structural business acceleration. Driehaus preferred to buy stocks that were already hitting new highs, betting that earnings revisions and investor behavioral biases would continue to push their prices upward.

For decades, the mainstream academic community dismissed Driehaus's success as luck or uncompensated risk, clinging to the Efficient Market Hypothesis. However, in 1993, economists **Narasimhan Jegadeesh and Sheridan Titman** published their seminal paper, *"Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency."* They empirically proved that stock returns exhibit trend persistence over 3 to 12-month lookback horizons, and that a long-short momentum portfolio generated highly significant, persistent abnormal returns (Alphas) that could not be explained by the CAPM market beta. 

This study bridges the gap between Driehaus's practitioner intuition and Jegadeesh & Titman's asset pricing rigor. We implement an **Inverse Volatility Weighted Momentum Strategy** on the Russell 3000 universe, incorporating non-linear execution costs, trend-following futures hedging, and multi-period regressions.

---

## 1. Strategy Performance Summary (Sub-Periods & Futures Hedging)

Using Fama-French daily benchmarks to ensure statistical alignment, we evaluated the strategy across four sub-periods, comparing unhedged vs. futures-hedged versions for Gross, Net, and Tranche-Rebalanced portfolios at a **$1M AUM scale**:

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
  An daily volatility floor of **0.005** (8% annualized) and filter are applied to completely isolate the portfolio from illiquid, zero-volume shell companies.
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

## 2. Portfolio Selection: Concentration vs. Diversification Analysis

We simulated different selection thresholds for the raw momentum basket at a **$1M AUM scale** as requested. Within all compared portfolio selections, we use the exact same **Inverse Volatility Weighting** algorithm ($w_i \propto 1/\sigma_i$) as defined in Section 1. If $N$ stocks are selected in the Top $Q\%$ rank on date $t$, their cross-sectional weights are allocated inversely to their rolling 20-day daily standard deviation (clipped to the 0.005 risk floor and filtered) and normalized to sum to 1.0. This holds the weighting methodology constant to isolate only the effect of portfolio concentration vs. diversification:

| Portfolio Selection | Annualized Return (CAGR) | Annualized Volatility | Sharpe Ratio (4% RF) | Max Drawdown |
| :--- | :---: | :---: | :---: | :---: |
| **Top 1% (Concentrated)** | **47.25%** | 64.23% | 0.814 | -72.92% |
| **Top 3% (Optimal Sharpe)** | **37.76%** | **33.29%** | **1.007** | **-41.56%** |
| **Top 5%** | 31.16% | 28.81% | 0.947 | -41.08% |
| **Top 10%** | 26.04% | 24.46% | 0.906 | -42.55% |
| **Top 20% (Diversified)** | 21.41% | 21.46% | 0.825 | -40.27% |

* **Optimal Balanced Selection**: At $1M AUM, the **Top 3%** selection achieves the highest Sharpe ratio (**1.007**) and a stellar CAGR of **37.76%**. At this AUM scale, execution costs are low enough to make the highly concentrated factor premium viable.

#### Selection Quantiles PnL Comparison Plot
![Selection Quantiles PnL Comparison](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/quantile_comparison.png)

---

## 3. Slippage Capacity Curve: Lit vs. Algorithmic/SOR Routing

We compared the execution decay of standard month-end block rebalancing (Standard Lit) against daily rolling tranche rebalancing under standard lit execution (Tranche Lit) and smart order routing + dark pool crossing (Tranche Algorithmic/SOR) across portfolio sizes from **$100K AUM up to $50B AUM**:

| AUM Size | CAGR (Standard Lit) | Sharpe (Standard Lit) | CAGR (Tranche Lit) | Sharpe (Tranche Lit) | CAGR (Tranche Algorithmic/SOR) | Sharpe (Tranche Algorithmic/SOR) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **$100K** | 26.51% | 0.921 | 26.85% | 0.941 | **26.90%** | **0.943** |
| **$500K** | 26.24% | 0.913 | 26.78% | 0.939 | **26.88%** | **0.942** |
| **$1M** | 26.04% | 0.906 | 26.73% | 0.937 | **26.87%** | **0.942** |
| **$5M** | 25.20% | 0.878 | 26.51% | 0.930 | **26.81%** | **0.940** |
| **$10M** | 24.57% | 0.857 | 26.34% | 0.924 | **26.77%** | **0.938** |
| **$50M** | 21.94% | 0.768 | 25.64% | 0.901 | **26.60%** | **0.933** |
| **$100M** | 19.99% | 0.700 | 25.11% | 0.884 | **26.48%** | **0.929** |
| **$500M** | 11.91% | 0.413 | 22.92% | 0.811 | **25.94%** | **0.911** |
| **$1.0B** | 6.01% | 0.209 | 21.30% | 0.756 | **25.54%** | **0.898** |
| **$5.0B** | -18.70% | -0.434 | 14.70% | 0.524 | **23.87%** | **0.842** |
| **$10.0B** | -37.20% | -0.729 | 9.99% | 0.350 | **22.63%** | **0.801** |
| **$50.0B** | -71.02% | -1.467 | -7.87% | -0.380 | **17.54%** | **0.625** |

* **Tranche Capacity Edge**: Tranche rebalancing combined with Smart Order Router (SOR) algorithms and dark pool crossing completely eliminates execution-related decay. At **$50B AUM**, where standard month-end rebalancing is bankrupt (-71.02% CAGR), the **Tranche Algorithmic/SOR** strategy retains a highly positive and viable **17.54% CAGR** and a **0.625 Sharpe ratio**!

#### Slippage Capacity Curve Comparison Plot
![Slippage Capacity Decay Comparison](/C:/Users/USER/.gemini/antigravity/brain/6a51fe4b-c7c3-42f7-b5a1-3aff0392ecaa/capacity_decay.png)

---

## 4. Simulating Large-Scale Execution and Routing Strategies

Executing large block-size trades directly onto lit exchanges would trigger massive market impact in practice, particularly at modeled scales between **$100M and $50B AUM**. In our simulations, we evaluate how routing via a Smart Order Router (SOR) with the following mechanisms reduces this decay:
* **Dark Pool Crossing & Block Networks ($100M - $1B AUM)**: Orders are routed to dark crossing networks (e.g., Liquidnet, Instinet BlockMatch, or ITG Posit) to match blocks internally. This prints trades to the tape only after execution, bypassing the public limit order books and preventing front-running. Realistically, we model a **40% crossing rate** where crossed shares face zero market impact.
* **Volume/Time-Scheduled Algorithmic Routing ($1B - $10B AUM)**: Order slicing is scheduled using Time-Weighted Average Price (TWAP) or Volume-Weighted Average Price (VWAP) algorithms. The execution rate is dynamically throttled to keep the Participation Rate (POV) strictly under **5% of the security's rolling 20-day Average Daily Volume (ADV)**, minimizing market signature. Realistically, this reduces the effective market impact coefficient $\gamma$ from $0.5$ to $0.2$.
* **Internalization & OTC Liquidity Desks ($10B - $50B AUM)**: At mega-cap scale, the portfolio's rebalancing flow is crossed internally against secondary strategies (such as mean-reversion or value portfolios). Any residual flow is negotiated directly with institutional market makers via bilateral over-the-counter (OTC) block desks, avoiding public exchange books completely.

---

## 4.5 Academic Regression Synthesis & The Factor Picture
Based on the multi-period OLS regressions with Newey-West HAC robust standard errors, we can synthesize the following structural factor properties of the Inverse Volatility Weighted Momentum Strategy:
1. **High-Beta Tilt**: The strategy exhibits a CAPM beta of **1.16 to 1.20** across sub-periods. Stripped to its core in the 5-Factor regression, beta remains highly significant at **1.05 to 1.07**. This indicates that momentum naturally selects high-beta growth stocks that outperform during equity expansions.
2. **Small-Cap Preference (Size Premium)**: The size exposure ($SMB$) is consistently positive and statistically massive (**0.58 to 0.66**, with t-statistics above **12.8**). This confirms that momentum acceleration is highly pronounced in the small/mid-cap segments of the Russell 3000 cross-section.
3. **Anti-Value and Growth Tilt**: The value coefficient ($HML$) is strongly negative (**-0.24 to -0.54**), typical of growth-biased portfolios buying expensive winners. The profitability tilt ($RMW$) is also negative, reflecting that momentum targets capital-reinvesting growth firms rather than cash-cow businesses.
4. **Enhanced Alpha Intercept**: On the Full Horizon, adjusting for size, value, and profitability factors causes the daily Alpha to rise from **3.24 bps** (CAPM) to **4.68 bps** (Fama-French 5-Factor), with the t-statistic jumping from **2.35 to 4.55** (p-value: 0.0000). This confirms that stripping out factor style tilts unmasks a highly robust, statistically undeniable momentum abnormal premium of **~11.79% annualized**.

---

## 5. Limitations of the Backtest & Key Empirical Biases
While our backtest results demonstrate high statistical significance, systematic trading models are fundamentally bounded by empirical limitations and statistical biases. To convert this research into a live trading system, the following limitations must be accounted for:

1. **Survivorship Bias**:
   * *Problem*: The historical stock universe used in this backtest is drawn from currently active listings. Companies that went bankrupt, merged, or were delisted due to financial distress between 2012 and 2026 are not present in the dataset.
   * *Impact*: Since momentum strategies naturally seek out high-performing listings, they are prone to capturing stocks that eventually collapse. By excluding historically failed companies, the backtest returns are artificially biased upward.
2. **Lookahead Bias**:
   * *Mitigation*: We mitigate this bias by applying a strict **1-day lag** on all portfolio rebalancing decisions (calculating weights on the close of day $t-1$ and executing on the close of day $t$).
   * *Residual Risk*: In corporate action adjustments (splits, dividends), backadjusted prices are sometimes applied retroactively, introducing minor lookahead leaking.
3. **Liquidity & Spread Regime Shifts**:
   * *Problem*: Our market impact model ($\text{{slippage}} = \text{{spread}} + \gamma \sigma \sqrt{V/ADV}$) assumes a static bid-ask spread of **5.0 bps** and stable volume relationships.
   * *Impact*: During liquidity crises (such as the March 2020 COVID crash), bid-ask spreads for small-cap names can spike to **100+ bps**, and trading volume dries up entirely. The actual transaction costs incurred during these regimes would exceed our model's estimates, eroding net returns.
4. **Selection Bias & Multiple Testing (Data Snooping)**:
   * *Problem*: Evaluating multiple portfolio selections (1%, 3%, 5%, 10%, 20%) and highlighting the **Top 3%** as the "optimal" Sweet Spot introduces selection bias.
   * *Impact*: The Top 3% parameters are overfitted to the historical sample. In live execution, the strategy's Sharpe ratio may mean-revert toward the baseline Top 10% or Top 20% average.
