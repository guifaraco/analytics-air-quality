import pandas as pd

def get_stations(filters=[], cols=None):
    if not cols:
        cols = [
            'Nome do Município', 'Estado', 'Nome da Estação', 'Código IBGE do Município',
            'Latitude', 'Longitude'
        ]

    df = pd.read_csv("data/monitor_ar/EstacoesMonitorAr-Nov-2022.csv", sep=";", usecols=cols)

    if 'Código IBGE do Município' in cols:
        df['Código IBGE do Município'] = (df['Código IBGE do Município'] / 10).astype(int)


    if filters:
        df = apply_filters(df, filters)

    return df

def get_monitors(filters=[], cols=None):
    if cols:
        cols = cols + ['iqar']

    jan_mar_df = pd.read_csv("data/monitor_ar/Dados_monitorar_jan_mar.csv", encoding="latin", sep=";", usecols=cols)
    abr_jun_df = pd.read_csv("data/monitor_ar/Dados_monitorar_abr_jun.csv", encoding="latin", sep=";", usecols=cols)
    jul_nov_df = pd.read_csv("data/monitor_ar/Dados_monitorar_jul_nov.csv", encoding="latin", sep=";", usecols=cols)


    # Junta as três tabelas de monitores
    df = pd.concat([jan_mar_df, abr_jun_df, jul_nov_df], axis=0)

    df = apply_filters(df, filters)

    df['iqar'] = pd.to_numeric(df['iqar'], errors='coerce')

    df = df.dropna(subset=['iqar'])
    df = df[df['iqar'] >= 0]

    return df

def apply_filters(df, filters):
    if filters['uf']:
        df = df[df['Estado'] == filters['uf']]
        if filters['city']:
            df = df[df['Nome do Município'] == filters['city']]

    return df

def get_valid_ibge(filters):
    cols=[
        'Nome do Município', 'Estado', 'Nome da Estação'
    ]
    monitors_df = get_monitors(filters=filters, cols=cols)


    station_cols = [
        'Código IBGE do Município', 'Nome do Município', 'Estado', 'Nome da Estação'
    ]

    stations_df = get_stations(filters=filters, cols=station_cols)

    stations_df.dropna(subset=['Código IBGE do Município'], inplace=True)

    filter_df = stations_df[
        stations_df['Nome do Município'].isin(list(monitors_df['Nome do Município'])) &
        stations_df['Estado'].isin(list(monitors_df['Estado'])) &
        stations_df['Nome da Estação'].isin(list(monitors_df['Nome da Estação']))
    ]

    ibge_codes = filter_df["Código IBGE do Município"].astype(int)
    ibge_codes = ibge_codes.unique()

    return ibge_codes

