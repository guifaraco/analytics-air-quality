import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from frontend.utils import get_month_name
from frontend.utils.correlacao.graph_queries import query_casos_mensais_estado, query_correlacao_poluicao_casos
from frontend.utils.monitorar.graph_queries import query_media_mensal

def compara_mensal(pollutants, states, srags):
    df_casos = query_casos_mensais_estado()
    df_casos = get_month_name(df_casos)

    if states:
        df_casos = df_casos[df_casos['state_code'].isin(states)]

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
            title="Legenda",
            x=1.1,
            y=1,
            xanchor='left',
            yanchor='top'
        )
    )

    st.plotly_chart(fig, use_container_width=True)


def correlacao_poluicao_casos(pollutants, states, srags):
    df = query_correlacao_poluicao_casos()

    # Converter para datetime e extrair o mês
    df['ano_mes'] = pd.to_datetime(df['ano_mes'])
    df['mes'] = df['ano_mes'].dt.month

    df = get_month_name(df, 'mes')

    fig = go.Figure()

    for poluente in df['poluente'].unique():
        subset = df[df['poluente'] == poluente]
        
        # Adicionar pontos
        fig.add_trace(go.Scatter(
            x=subset['media_poluicao'],
            y=subset['numero_total_casos'],
            mode='markers',
            name=poluente,
            hovertext=subset.apply(lambda row: f"UF: {row['uf']}<br>Mês: {row['mes']}", axis=1)
        ))
        
        # Calcular regressão linear manualmente
        x = subset['media_poluicao'].values.astype(float)
        y = subset['numero_total_casos'].values.astype(float)
        coeffs = np.polyfit(x, y, 1)
        trendline = np.poly1d(coeffs)
        
        # Adicionar linha de tendência
        fig.add_trace(go.Scatter(
            x=x,
            y=trendline(x),
            mode='lines',
            name=f'Tendência {poluente}',
            line=dict(dash='dash')
        ))

    fig.update_layout(
        title='Correlação entre Poluição e Casos de Saúde',
        xaxis_title='Média Mensal de Poluição (µg/m³)',
        yaxis_title='Número Total de Casos de Saúde',
        width=1000,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)