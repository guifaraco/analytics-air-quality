import pandas as pd

def get_stations(filters=[], cols=None):
    if not cols:
        cols = [
            'Nome do Município', 'Estado', 'Nome da Estação', 'Código IBGE do Município',
            'Latitude', 'Longitude'
        ]

    df = pd.read_csv("../data/monitor_ar/EstacoesMonitorAr-Nov-2022.csv", sep=";", usecols=cols)

    if filters:
        df = apply_filters(df, filters)

    return df

def get_monitors(filters=[], cols=None):
    jan_mar_df = pd.read_csv("../data/monitor_ar/Dados_monitorar_jan_mar.csv", encoding="latin", sep=";", usecols=cols)
    abr_jun_df = pd.read_csv("../data/monitor_ar/Dados_monitorar_abr_jun.csv", encoding="latin", sep=";", usecols=cols)
    jul_nov_df = pd.read_csv("../data/monitor_ar/Dados_monitorar_jul_nov.csv", encoding="latin", sep=";", usecols=cols)

    # Junta as três tabelas de monitores
    df = pd.concat([jan_mar_df, abr_jun_df, jul_nov_df], axis=0)

    df = apply_filters(df, filters)

    return df


def apply_filters(df, filters):
    if filters['uf']:
        df = df[df['Estado'] == filters['uf']]
        if filters['city']:
            df = df[df['Nome do Município'] == filters['city']]

    return df
