import matplotlib.pyplot as plt

def plot_equity(equity):
    plt.figure()
    equity.plot()
    plt.title("Equity Curve")
    plt.show()

def summary_text(sharpe, alpha=None, beta=None):
    return f"""
    =========================
    STRATEGY PERFORMANCE
    =========================
    Sharpe Ratio: {sharpe:.2f}
    Alpha: {alpha}
    Beta: {beta}
    """