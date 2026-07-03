import numpy as np
import pandas as pd


# =========================
# PERFORMANCE METRICS
# =========================

def sharpe_ratio(returns: pd.Series):
    """
    Annualized Sharpe Ratio
    """
    returns = returns.dropna()

    if len(returns) < 2:
        return 0.0

    std = returns.std()

    if std == 0 or np.isnan(std):
        return 0.0

    return np.sqrt(252) * returns.mean() / std


def volatility(returns: pd.Series):
    """
    Annualized volatility
    """
    returns = returns.dropna()

    if len(returns) < 2:
        return 0.0

    return np.sqrt(252) * returns.std()


# =========================
# REGRESSION OUTPUTS
# =========================

def regression_summary_table(model, name="Strategy"):
    """
    Extract alpha, betas, t-stats, p-values (CAPM / FF models)
    """

    summary = pd.DataFrame({
        "coef": model.params,
        "t_stat": model.tvalues,
        "p_value": model.pvalues
    })

    summary["strategy"] = name

    return summary