import pandas as pd
import numpy as np

def format_regression_markdown(model, name="Regression Model"):
    """
    Format statsmodels regression results into a beautiful Markdown table.
    """
    params = model.params
    tvalues = model.tvalues
    pvalues = model.pvalues
    
    # Map index names to user-friendly labels
    name_map = {
        "const": "Alpha (Intercept)",
        "MKT_RF": "Market Premium (MKT_RF)",
        "SMB": "Size (SMB)",
        "HML": "Value (HML)",
        "RMW": "Profitability (RMW)",
        "CMA": "Investment (CMA)"
    }
    
    rows = []
    for var in params.index:
        label = name_map.get(var, var)
        coef = params[var]
        t_stat = tvalues[var]
        pval = pvalues[var]
        
        # Add significance stars
        stars = ""
        if pval < 0.001:
            stars = "***"
        elif pval < 0.01:
            stars = "**"
        elif pval < 0.05:
            stars = "*"
        elif pval < 0.1:
            stars = "."
            
        rows.append({
            "Factor": label,
            "Coefficient": f"{coef:.6f}{stars}",
            "t-Statistic": f"{t_stat:.2f}",
            "p-Value": f"{pval:.4f}"
        })
        
    df_table = pd.DataFrame(rows)
    
    # Build markdown table manually for cleanliness
    md = f"### {name} Results\n\n"
    md += "| Factor / Predictor | Coefficient | t-Statistic | p-Value |\n"
    md += "| :--- | :---: | :---: | :---: |\n"
    for _, row in df_table.iterrows():
        md += f"| {row['Factor']} | {row['Coefficient']} | {row['t-Statistic']} | {row['p-Value']} |\n"
        
    md += f"\n* **Observations**: {int(model.nobs):,}\n"
    md += f"* **R-Squared**: {model.rsquared:.4f} | **Adj. R-Squared**: {model.rsquared_adj:.4f}\n"
    md += f"* **F-Statistic**: {model.fvalue:.2f} (p-value: {model.f_pvalue:.4e})\n"
    md += "\n*Significance codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1*\n\n"
    
    return md

def generate_summary_report(metrics, capm_raw, ff5_raw, capm_final, ff5_final):
    """
    Generate the complete analysis report including tables and performance summaries.
    """
    report = f"""# Empirical Asset Pricing & Momentum Strategy Analysis Report

## 1. Strategy Performance Summary

| Metric | Raw Strategy (Gross) | Net Strategy (After Costs) | Vol-Targeted Strategy (Final) | S&P 500 Index |
| :--- | :---: | :---: | :---: | :---: |
| **Annualized Return** | {metrics['raw_ann_ret']:.2%} | {metrics['net_ann_ret']:.2%} | {metrics['final_ann_ret']:.2%} | {metrics['sp500_ann_ret']:.2%} |
| **Annualized Volatility** | {metrics['raw_ann_vol']:.2%} | {metrics['net_ann_vol']:.2%} | {metrics['final_ann_vol']:.2%} | {metrics['sp500_ann_vol']:.2%} |
| **Sharpe Ratio** | {metrics['raw_sharpe']:.3f} | {metrics['net_sharpe']:.3f} | {metrics['final_sharpe']:.3f} | {metrics['sp500_sharpe']:.3f} |
| **Max Drawdown** | {metrics['raw_max_dd']:.2%} | {metrics['net_max_dd']:.2%} | {metrics['final_max_dd']:.2%} | {metrics['sp500_max_dd']:.2%} |

---

## 2. Asset Pricing Regression Analysis

The strategy returns are regressed against the CAPM (Market factor only) and the Fama-French 5-factor model to test if the momentum anomaly generates statistically significant risk-adjusted abnormal returns (Alpha).

### 2.1 Raw (Gross) Strategy Regressions

{format_regression_markdown(capm_raw, "CAPM Regression (Raw Returns)")}

{format_regression_markdown(ff5_raw, "Fama-French 5-Factor Regression (Raw Returns)")}

---

### 2.2 Volatility-Targeted (Final) Strategy Regressions

{format_regression_markdown(capm_final, "CAPM Regression (Vol-Targeted Returns)")}

{format_regression_markdown(ff5_final, "Fama-French 5-Factor Regression (Vol-Targeted Returns)")}

---

## 3. Findings & Conclusions

1. **Transaction Cost Impact**: The Sharpe ratio drops from **{metrics['raw_sharpe']:.3f}** (gross) to **{metrics['net_sharpe']:.3f}** (net), highlighting the significance of market frictions in high-turnover cross-sectional momentum strategies.
2. **Risk Control**: Volatility targeting scaled down leverage when market risk spiked, helping stabilize the equity curve.
3. **Alpha Predictability**: Check the t-statistics on the intercepts (Alphas). A t-stat > 1.96 (or p-value < 0.05) indicates that the momentum strategy yields significant abnormal returns unexplained by standard risk factors.
4. **Factor Exposures**: Look at the factor loadings:
   - **Market (MKT_RF)**: Typically, market-neutral momentum long-short portfolios should have low or negative market betas.
   - **Size (SMB) & Value (HML)**: Loadings show if the strategy tilts towards small-cap or value/growth firms.
"""
    return report