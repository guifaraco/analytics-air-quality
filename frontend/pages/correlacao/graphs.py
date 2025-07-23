import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from frontend.utils import get_month_name
from frontend.utils.correlacao.graph_queries import query_casos_mensais_estado
from frontend.utils.monitorar.graph_queries import query_media_mensal

def compara_mensal(pollutant, states):
    df_casos = query_casos_mensais_estado()
    df_casos = get_month_name(df_casos)

    df_casos = df_casos[df_casos['month'] != 'Dezembro']

    if states:
        df_casos = df_casos[df_casos['state_code'].isin(states)]

    # Cria os gráficos separados com px
    fig_casos = px.bar(
        df_casos,
        x='month',
        y='total_cases',
        color='final_classification'
    )

    df_pol = query_media_mensal()
    df_pol = get_month_name(df_pol)

    if pollutant:
        df_pol = df_pol[df_pol['pollutant_code'] == pollutant]

    if states:
        df_pol = df_pol[df_pol['state_code'].isin(states)]

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
            title=None,
            x=0.5,
            y=-0.2,
            xanchor='center',
            yanchor='top',
            orientation='h'
        ),
        margin=dict(b=100)
    )

    st.plotly_chart(fig, use_container_width=True)

def casos_poluente(pollutant, states, srag):
    df_casos = query_casos_mensais_estado()
    df_casos = get_month_name(df_casos)

    df_casos = df_casos[df_casos['month'] != 'Dezembro']

    if states:
        df_casos = df_casos[df_casos['state_code'].isin(states)]

    # Cria os gráficos separados com px
    fig_casos = px.bar(
        df_casos,
        x='month',
        y='sum',
        color='state_code'
    )

    df_pol = query_media_mensal()
    df_pol = get_month_name(df_pol)

    if pollutant:
        df_pol = df_pol[df_pol['pollutant_code'] == pollutant]

    if states:
        df_pol = df_pol[df_pol['state_code'].isin(states)]

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
            title=None,
            x=0.5,
            y=-0.2,
            xanchor='center',
            yanchor='top',
            orientation='h'
        ),
        margin=dict(b=100)
    )

    st.plotly_chart(fig, use_container_width=True)