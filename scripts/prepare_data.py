import os
import shutil
import urllib.request
import zipfile
import io
import pandas as pd
import numpy as np
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

    # 2. Copy close.parquet & volume.parquet from quant_data
    src_prices = r"C:\Users\USER\Desktop\quant_data\close.parquet"
    src_volumes = r"C:\Users\USER\Desktop\quant_data\volume.parquet"
    
    dest_prices = r"data/close.parquet"
    dest_volumes = r"data/volume.parquet"
    
    if os.path.exists(src_prices) and os.path.exists(src_volumes):
        print(f"Copying price data from {src_prices} to {dest_prices}...")
        shutil.copy(src_prices, dest_prices)
        print(f"Copying volume data from {src_volumes} to {dest_volumes}...")
        shutil.copy(src_volumes, dest_volumes)
    else:
        raise FileNotFoundError(f"Could not find quant_data parquets at {src_prices} or {src_volumes}")

    # 3. Download Kenneth French 5 Factors Daily
    ff_url = "https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_daily_CSV.zip"
    print(f"Downloading Fama-French 5 Factors from: {ff_url}")
    
    session = requests.Session()
    session.verify = False
    
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
