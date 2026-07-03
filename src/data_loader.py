import pandas as pd


def load_prices(path: str) -> pd.DataFrame:
    """
    Load OHLCV price data (parquet).
    """
    df = pd.read_parquet(path)

    # fix date index if needed
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index("date")

    df.index = pd.to_datetime(df.index)
    df = df.sort_index()

    return df


def load_universe(path: str):
    """
    Robust loader for iShares-style holdings files.
    Automatically finds the header row containing 'Ticker'.
    """

    # read raw file lines first
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # find the line where the real table starts
    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("Ticker,"):
            header_idx = i
            break

    if header_idx is None:
        raise ValueError("Could not find Ticker header row in file")

    # now read properly from header row
    df = pd.read_csv(path, skiprows=header_idx)

    # clean tickers
    tickers = (
        df["Ticker"]
        .dropna()
        .astype(str)
        .str.strip()
        .tolist()
    )

    return tickers


def align_universe(prices, universe):
    """
    Keep only tickers that exist in universe
    """
    common = [c for c in prices.columns if c in universe]
    return prices[common]


def clean_prices(prices):
    """
    Basic cleaning
    """
    prices = prices.dropna(axis=1, how="all")
    prices = prices.ffill()
    return prices


def load_sectors(path: str) -> pd.Series:
    """
    Load mapping from Ticker to Sector from iShares-style holdings file.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    header_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith("Ticker,"):
            header_idx = i
            break

    if header_idx is None:
        raise ValueError("Could not find Ticker header row in holdings file")

    df = pd.read_csv(path, skiprows=header_idx)
    df = df.dropna(subset=["Ticker", "Sector"])
    df["Ticker"] = df["Ticker"].astype(str).str.strip()
    df["Sector"] = df["Sector"].astype(str).str.strip()
    df = df.drop_duplicates(subset=["Ticker"])
    
    return pd.Series(df["Sector"].values, index=df["Ticker"])


def load_volumes(path: str) -> pd.DataFrame:
    """
    Load volume data (parquet).
    """
    df = pd.read_parquet(path)
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    return df