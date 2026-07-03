import os
import shutil
import urllib.request
import zipfile
import io
import time
import pandas as pd
import numpy as np
import yfinance as yf
import requests
import urllib3

# Disable SSL verification warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def prepare_data():
    print("Creating data directory...")
    os.makedirs("data", exist_ok=True)

    # 1. Copy IWV holdings
    src_holdings = r"C:\Users\USER\Desktop\IWV_holdings.csv"
    dest_holdings = r"data/IWV_holdings.csv"
    if os.path.exists(src_holdings):
        print(f"Copying holdings from {src_holdings} to {dest_holdings}...")
        shutil.copy(src_holdings, dest_holdings)
    else:
        raise FileNotFoundError(f"Source holdings file not found at {src_holdings}")

    # Curate a list of 50 major US stocks with history back to 1999 that exist in Russell 3000
    curated_tickers = [
        "MSFT", "AAPL", "AMZN", "CSCO", "WMT", "PG", "JNJ", "XOM", "JPM", "GE",
        "KO", "MCD", "DIS", "CAT", "IBM", "INTC", "PFE", "MRK", "BAC", "VZ",
        "T", "CVX", "WFC", "PEP", "HD", "LOW", "HON", "DE", "MMM", "LLY",
        "ORCL", "LMT", "RTX", "UNH", "COST", "SLB", "CVS", "MS", "AXP", "SCHW",
        "UPS", "F", "BMY", "GS", "MET", "USB", "TGT", "ADBE", "AXP", "CI"
    ]
    # Remove duplicates and ensure ^GSPC is included
    curated_tickers = list(set(curated_tickers))
    if "^GSPC" not in curated_tickers:
        curated_tickers.append("^GSPC")
        
    print(f"Selected {len(curated_tickers)} liquid tickers spanning from 1999 to today...")

    # 2. Download historical prices & volumes from yfinance
    print("Downloading 1999-2026 daily price & volume data from Yahoo Finance...")
    start_date = "1999-01-01"
    end_date = "2026-07-03"
    
    session = requests.Session()
    session.verify = False
    
    try:
        # Download in a single request to avoid rate limits
        data = yf.download(curated_tickers, start=start_date, end=end_date, session=session, progress=False, timeout=30)
        
        close_df = data["Close"] if "Close" in data.columns else pd.DataFrame()
        volume_df = data["Volume"] if "Volume" in data.columns else pd.DataFrame()
        
        if close_df.empty or close_df.shape[1] < 5:
            raise ValueError("Downloaded data is empty or missing columns (rate limit / connection issue)")
            
        close_df = close_df.dropna(how="all", axis=1)
        volume_df = volume_df.dropna(how="all", axis=1)
        
        close_df = close_df.sort_index()
        close_df.index.name = "date"
        
        volume_df = volume_df.sort_index()
        volume_df.index.name = "date"
        
        dest_prices = r"data/close.parquet"
        dest_volumes = r"data/volume.parquet"
        
        print(f"Saving prices to {dest_prices} (Shape: {close_df.shape})...")
        close_df.to_parquet(dest_prices)
        
        print(f"Saving volumes to {dest_volumes} (Shape: {volume_df.shape})...")
        volume_df.to_parquet(dest_volumes)
        
    except Exception as e:
        print(f"\n[WARNING] yfinance download failed: {e}")
        print("Falling back to local 2020-2025 CSV files...")
        
        src_prices = r"C:\Users\USER\.gemini\antigravity\scratch\momentumlab\data\historical_prices.csv"
        src_volumes = r"C:\Users\USER\.gemini\antigravity\scratch\momentumlab\data\historical_volumes.csv"
        
        if os.path.exists(src_prices) and os.path.exists(src_volumes):
            prices_df = pd.read_csv(src_prices, index_col=0, parse_dates=True)
            prices_df = prices_df.sort_index()
            prices_df.index.name = "date"
            
            volumes_df = pd.read_csv(src_volumes, index_col=0, parse_dates=True)
            volumes_df = volumes_df.sort_index()
            volumes_df.index.name = "date"
            
            dest_prices = r"data/close.parquet"
            dest_volumes = r"data/volume.parquet"
            
            prices_df.to_parquet(dest_prices)
            volumes_df.to_parquet(dest_volumes)
            print("Fallback local files saved successfully!")
        else:
            raise FileNotFoundError("Could not find local fallback CSV files.")

    # 3. Download Kenneth French 5 Factors Daily
    ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip"
    print(f"Downloading Fama-French 5 Factors from: {ff_url}")
    
    try:
        response = session.get(ff_url, timeout=20)
        response.raise_for_status()
        zip_data = response.content
        
        print("Extracting ZIP contents...")
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            csv_filenames = [name for name in z.namelist() if name.lower().endswith(".csv")]
            if not csv_filenames:
                raise ValueError("No CSV file found in the Fama-French ZIP archive")
            
            csv_name = csv_filenames[0]
            print(f"Parsing {csv_name}...")
            with z.open(csv_name) as f:
                content = f.read().decode("utf-8")
        
        lines = content.splitlines()
        header_idx = None
        for idx, line in enumerate(lines):
            if "mkt-rf" in line.lower() and "smb" in line.lower():
                header_idx = idx
                break
        
        if header_idx is None:
            raise ValueError("Could not find the header row in the Fama-French CSV")
            
        print(f"Found headers on line {header_idx}: {lines[header_idx]}")
        
        data_rows = []
        col_names = [c.strip() for c in lines[header_idx].split(",") if c.strip()]
        if len(col_names) == 6:
            col_names = ["Date"] + col_names
        
        for line in lines[header_idx + 1:]:
            parts = [p.strip() for p in line.split(",") if p.strip()]
            if not parts:
                continue
            if len(parts[0]) == 8 and parts[0].isdigit():
                data_rows.append(parts)
            elif len(data_rows) > 0:
                break
                
        df_ff = pd.DataFrame(data_rows, columns=col_names)
        df_ff["Date"] = pd.to_datetime(df_ff["Date"], format="%Y%m%d")
        df_ff = df_ff.set_index("Date")
        
        for col in df_ff.columns:
            df_ff[col] = pd.to_numeric(df_ff[col]) / 100.0
            
        df_ff = df_ff.rename(columns={"Mkt-RF": "MKT_RF"})
        df_ff = df_ff.sort_index()
        df_ff.index.name = "date"
        
        dest_ff = r"data/fama_french_factors.parquet"
        print(f"Saving Fama-French factors to {dest_ff}...")
        df_ff.to_parquet(dest_ff)
        print("Data preparation completed successfully!")
        
    except Exception as e:
        print(f"Error preparing Fama-French factors: {e}")
        raise

if __name__ == "__main__":
    prepare_data()
