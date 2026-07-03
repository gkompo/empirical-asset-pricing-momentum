import pandas as pd
df = pd.read_parquet("data/close.parquet")
if "^GSPC" in df.columns:
    print("S&P 500 (^GSPC) is in the close.parquet columns!")
    sp500 = df["^GSPC"]
    print(f"S&P 500 head:\n{sp500.head()}")
    print(f"S&P 500 tail:\n{sp500.tail()}")
else:
    print("S&P 500 (^GSPC) is NOT in the columns!")
