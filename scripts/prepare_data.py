import os
import shutil
import urllib.request
import zipfile
import io
import pandas as pd
import numpy as np

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

    # 2. Convert historical prices to parquet
    src_prices = r"C:\Users\USER\.gemini\antigravity\scratch\momentumlab\data\historical_prices.csv"
    dest_prices = r"data/close.parquet"
    if os.path.exists(src_prices):
        print(f"Reading historical prices from {src_prices}...")
        prices_df = pd.read_csv(src_prices, index_col=0, parse_dates=True)
        # Sort index and ensure it's named 'date'
        prices_df = prices_df.sort_index()
        prices_df.index.name = "date"
        
        # Save to parquet
        print(f"Saving prices to {dest_prices}...")
        prices_df.to_parquet(dest_prices)
    else:
        raise FileNotFoundError(f"Source historical prices not found at {src_prices}")

    # 2b. Convert historical volumes to parquet
    src_volumes = r"C:\Users\USER\.gemini\antigravity\scratch\momentumlab\data\historical_volumes.csv"
    dest_volumes = r"data/volume.parquet"
    if os.path.exists(src_volumes):
        print(f"Reading historical volumes from {src_volumes}...")
        volumes_df = pd.read_csv(src_volumes, index_col=0, parse_dates=True)
        volumes_df = volumes_df.sort_index()
        volumes_df.index.name = "date"
        print(f"Saving volumes to {dest_volumes}...")
        volumes_df.to_parquet(dest_volumes)
    else:
        raise FileNotFoundError(f"Source historical volumes not found at {src_volumes}")

    # 3. Download Kenneth French 5 Factors Daily
    ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip"
    print(f"Downloading Fama-French 5 Factors from: {ff_url}")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    req = urllib.request.Request(ff_url, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            zip_data = response.read()
        
        print("Extracting ZIP contents...")
        with zipfile.ZipFile(io.BytesIO(zip_data)) as z:
            # find csv file in zip
            csv_filenames = [name for name in z.namelist() if name.lower().endswith(".csv")]
            if not csv_filenames:
                raise ValueError("No CSV file found in the Fama-French ZIP archive")
            
            csv_name = csv_filenames[0]
            print(f"Parsing {csv_name}...")
            with z.open(csv_name) as f:
                content = f.read().decode("utf-8")
        
        # Parse Fama-French CSV lines
        lines = content.splitlines()
        
        # Find start of data
        header_idx = None
        for idx, line in enumerate(lines):
            # Kenneth French daily file headers contain "Mkt-RF"
            if "mkt-rf" in line.lower() and "smb" in line.lower():
                header_idx = idx
                break
        
        if header_idx is None:
            raise ValueError("Could not find the header row in the Fama-French CSV")
            
        print(f"Found headers on line {header_idx}: {lines[header_idx]}")
        
        # Clean lines to read into pandas
        # Kenneth French daily files sometimes have a copyright/footnote section at the end.
        # We parse only lines that have a valid date prefix (e.g. YYYYMMDD like 20200102)
        data_rows = []
        col_names = [c.strip() for c in lines[header_idx].split(",") if c.strip()]
        # Prepend 'Date' to column names if missing
        if len(col_names) == 6:
            col_names = ["Date"] + col_names
        
        for line in lines[header_idx + 1:]:
            parts = [p.strip() for p in line.split(",") if p.strip()]
            if not parts:
                continue
            # First element must be an 8-digit date
            if len(parts[0]) == 8 and parts[0].isdigit():
                data_rows.append(parts)
            elif len(data_rows) > 0:
                # Once we reach non-numeric lines after starting, we are done
                break
                
        df_ff = pd.DataFrame(data_rows, columns=col_names)
        df_ff["Date"] = pd.to_datetime(df_ff["Date"], format="%Y%m%d")
        df_ff = df_ff.set_index("Date")
        
        # Convert numeric columns to float and divide by 100 (Ken French is in %, we want decimal)
        for col in df_ff.columns:
            df_ff[col] = pd.to_numeric(df_ff[col]) / 100.0
            
        # Rename columns to standard names used in statistics and models
        # e.g., 'Mkt-RF' -> 'MKT_RF'
        df_ff = df_ff.rename(columns={"Mkt-RF": "MKT_RF"})
        
        # Ensure index sorting
        df_ff = df_ff.sort_index()
        df_ff.index.name = "date"
        
        # Save to parquet
        dest_ff = r"data/fama_french_factors.parquet"
        print(f"Saving Fama-French factors to {dest_ff}...")
        df_ff.to_parquet(dest_ff)
        print("Data preparation completed successfully!")
        
    except Exception as e:
        print(f"Error preparing Fama-French factors: {e}")
        raise

if __name__ == "__main__":
    prepare_data()
