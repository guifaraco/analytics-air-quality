import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from .filters import month_filter, singlepollutant_filter
from frontend.utils import get_month_name
from frontend.utils.correlacao.graph_queries import query_casos_mensais_estado, query_total_casos
from frontend.utils.monitorar.graph_queries import query_media_mensal

def big_numbers():
    col1, col2 = st.columns(2)

    with col1:
        month = month_filter()
    
    with col2:
        pollutant = singlepollutant_filter()

    # taxa_mortalidade = query_taxa_mortalidade()
    total_casos = query_total_casos()

    col3, col4 = st.columns(2)

    big_total_casos(total_casos, month)

def big_total_casos(df, month):
    st.write(df)

    value = int(df[df['month'] == month]['sum'].iloc[0])

    st.metric(
        "Total de Casos",
        value
    )
    


def compara_mensal(pollutants, srags):
    df_casos = query_casos_mensais_estado()
    df_casos = get_month_name(df_casos)

    if srags:
        df_casos = df_casos[df_casos['final_classification'].isin(srags)]

    df_casos = df_casos.groupby(['final_classification', 'month'], as_index=False)['total_cases'].sum()

    # Remove o Mês de Dezembro pois não existem registros de poluição desse mês em nosso dataset
    df_casos = df_casos[df_casos['month'] != 'Dezembro']

    # Cria os gráficos separados com px
    fig_casos = px.bar(
        df_casos,
        x='month',
        y='total_cases',
        color='final_classification'
    )

    df_pol = query_media_mensal()

    # Converter para datetime e extrair o mês
    df_pol['year_month'] = pd.to_datetime(df_pol['year_month'])
    df_pol['month'] = df_pol['year_month'].dt.month

    df_pol = get_month_name(df_pol)

    if pollutants:
        df_pol = df_pol[df_pol['pollutant_code'].isin(pollutants)]

    df_pol = df_pol.groupby(['month', 'pollutant_code'], as_index=False)['monthly_avg_pollution'].mean().dropna()

    fig_pol = px.line(
        df_pol,
        x='month',
        y='monthly_avg_pollution',
        color='pollutant_code',
        symbol='pollutant_code',
        markers=True
    )

    # Cria figura final e adiciona os traces dos dois gráficos
    fig = go.Figure()

    # Adiciona os traces dos casos
    for trace in fig_casos.data:
        trace.yaxis = 'y1'
        fig.add_trace(trace)

    # Adiciona os traces da poluição
    for trace in fig_pol.data:
        trace.yaxis = 'y2'
        fig.add_trace(trace)

    # Configura dois eixos Y (um à esquerda e outro à direita)
    fig.update_layout(
        title="Casos de SRAG e Poluição Mensal",
        xaxis=dict(title="Mês"),
        yaxis=dict(
            title="Total de Casos",
            side="left"
        ),
        yaxis2=dict(
            title="Média de Concentração",
            overlaying="y",
            side="right"
        ),
        legend=dict(
            title="Legenda",
            x=1.1,
            y=1,
            xanchor='left',
            yanchor='top'
        )
    )

    st.plotly_chart(fig, use_container_width=True)

def compara_estado(pollutants, srags):
    df_casos = query_casos_mensais_estado()

    if srags:
        df_casos = df_casos[df_casos['final_classification'].isin(srags)]

    # Remove o Mês de Dezembro pois não existem registros de poluição desse mês em nosso dataset
    df_casos = df_casos[df_casos['month'] != 12]

    df_casos = df_casos.groupby(['final_classification', 'state_code'], as_index=False)['total_cases'].sum()


    # Cria os gráficos separados com px
    fig_casos = px.bar(
        df_casos,
        x='state_code',
        y='total_cases',
        color='final_classification'
    )

    df_pol = query_media_mensal()

    if pollutants:
        df_pol = df_pol[df_pol['pollutant_code'].isin(pollutants)]

    df_pol = df_pol.groupby(['state_code', 'pollutant_code'], as_index=False)['monthly_avg_pollution'].mean().dropna()

    fig_pol = px.line(
        df_pol,
        x='state_code',
        y='monthly_avg_pollution',
        color='pollutant_code',
        symbol='pollutant_code',
        markers=True
    )

    # Cria figura final e adiciona os traces dos dois gráficos
    fig = go.Figure()

    # Adiciona os traces dos casos
    for trace in fig_casos.data:
        trace.yaxis = 'y1'
        fig.add_trace(trace)

    # Adiciona os traces da poluição
    for trace in fig_pol.data:
        trace.yaxis = 'y2'
        fig.add_trace(trace)

    # Configura dois eixos Y (um à esquerda e outro à direita)
    fig.update_layout(
        title="Casos de SRAG e Poluição por Estado",
        xaxis=dict(title="Mês"),
        yaxis=dict(
            title="Total de Casos",
            side="left"
        ),
        yaxis2=dict(
            title="Média de Concentração",
            overlaying="y",
            side="right"
        ),
        legend=dict(
            title="Legenda",
            x=1.1,
            y=1,
            xanchor='left',
            yanchor='top'
        )
    )

    st.plotly_chart(fig, use_container_width=True)