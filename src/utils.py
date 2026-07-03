import numpy as np

def clean_data(df):
    return df.dropna(how='all')

def normalize(df):
    return df / df.std()