import numpy as np
import pandas as pd

from utils.execute_query import select

def get_monitorar(cols='*', filters={}):
    df = select('mart_health_vs_air_quality', cols=cols, filters=filters)

    return df


def format_month(df):
    ordem_meses = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 
               'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro']

    df['year_month'] = pd.to_datetime(df['year_month'])
    df['month'] = df['year_month'].dt.month_name(locale='pt_BR')
    df['month'] = pd.Categorical(df['month'], categories=ordem_meses, ordered=True)
    df = df.sort_values('month')

    return df

