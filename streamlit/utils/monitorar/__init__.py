import streamlit as st
import pandas as pd
from .map import render_map

def render_monitorar():
    st.header("MonitorAr")
    stations_df, monitors_df, joined_df = get_df(
        stations_cols=[
            'Código IBGE do Município', 'Nome do Município', 'Estado', 'Nome da Estação', 
            'Latitude', 'Longitude'
        ],
        monitors_cols=[
            'Nome do Município', 'Estado', 'Nome da Estação', 'Sigla', 'Concentracao', 'iqar', 'Data'
        ]
    )

    st.subheader("Estações")
    st.dataframe(stations_df.head(10))
    render_map(stations_df)

    st.subheader("Monitoramentos")
    st.dataframe(monitors_df.head(10))
    st.write(f"Total Encontrados: {len(monitors_df)}")

    st.subheader("Relacionados")
    st.dataframe(joined_df)
    st.write(f"Total Encontrados: {len(joined_df)}")

    return stations_df

def get_df(stations_cols=None, monitors_cols=None):
    stations_df = pd.read_csv("data/monitor_ar/EstacoesMonitorAr-Nov-2022.csv", sep=";", usecols=stations_cols)
    jan_mar_df = pd.read_csv("data/monitor_ar/Dados_monitorar_jan_mar.csv", encoding="latin", sep=";", usecols=monitors_cols)
    abr_jun_df = pd.read_csv("data/monitor_ar/Dados_monitorar_abr_jun.csv", encoding="latin", sep=";", usecols=monitors_cols)
    jul_nov_df = pd.read_csv("data/monitor_ar/Dados_monitorar_jul_nov.csv", encoding="latin", sep=";", usecols=monitors_cols)

    # Junta as três tabelas de monitores
    monitors_df = pd.concat([jan_mar_df, abr_jun_df, jul_nov_df], axis=0)

    # Junta os datasets com base em seu Nome de Município
    df = pd.merge(
        stations_df[['Nome do Município', 'Estado', 'Nome da Estação']],
        monitors_df,
        on=['Nome do Município', 'Estado', 'Nome da Estação'],
        how='inner'
    )

    return stations_df, monitors_df, df