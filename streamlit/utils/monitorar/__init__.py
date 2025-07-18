import numpy as np
import pandas as pd

from utils.execute_query import select

def get_stations(cols='*', filters=[]):
    df = select('silver_stations', cols, filters)

    if 'city_ibge_code' in df.columns:
        df['city_ibge_code'] = (df['city_ibge_code'] / 10).astype(int)

    return df

