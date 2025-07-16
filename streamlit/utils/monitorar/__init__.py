import streamlit as st
import pandas as pd
from .map import render_map

def render_monitorar(filters):
    st.header("MonitorAr")
    stations_df = get_stations([
        'Nome do Município', 'Estado', 'Nome da Estação', 'Código IBGE do Município',
        'Latitude', 'Longitude'
        ]
    )

    if filters['uf']:
        stations_df = stations_df[stations_df['Estado'] == filters['uf']]
        if filters['city']:
            stations_df = stations_df[stations_df['Nome do Município'] == filters['city']]

    st.subheader("Estações")
    render_map(stations_df)
    st.write(f"Total de Estações: {len(stations_df)}")

    return stations_df

def get_stations(cols=None):
    stations_df = pd.read_csv("../data/monitor_ar/EstacoesMonitorAr-Nov-2022.csv", sep=";", usecols=cols)

    return stations_df

def get_monitors(cols=None):
    jan_mar_df = pd.read_csv("../data/monitor_ar/Dados_monitorar_jan_mar.csv", encoding="latin", sep=";", usecols=cols)
    abr_jun_df = pd.read_csv("../data/monitor_ar/Dados_monitorar_abr_jun.csv", encoding="latin", sep=";", usecols=cols)
    jul_nov_df = pd.read_csv("../data/monitor_ar/Dados_monitorar_jul_nov.csv", encoding="latin", sep=";", usecols=cols)

    # Junta as três tabelas de monitores
    monitors_df = pd.concat([jan_mar_df, abr_jun_df, jul_nov_df], axis=0)

    return monitors_df
