import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from frontend.utils import get_month_name
from frontend.utils.monitorar.graph_queries import query_media_mensal
from frontend.utils.datasus.graph_queries import query_casos_mensais

def compara_mensal(pollutant, states):
    df_casos = query_casos_mensais()
    df_casos = get_month_name(df_casos)

    # Cria os gráficos separados com px
    fig_casos = px.bar(
        df_casos,
        x='month',
        y='sum'
    )

    df_pol = query_media_mensal()
    df_pol = get_month_name(df_pol)

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
            title="",
            overlaying="y",
            side="right"
        ),
        legend=dict(title="Legenda"),
    )

    st.plotly_chart(fig, use_container_width=True)