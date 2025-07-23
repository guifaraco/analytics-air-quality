import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from frontend.utils import get_month_name
from utils.monitorar.graph_queries import query_big_numbers, query_compare_pollutant_state, query_media_mensal, query_poluicao_estado

def get_pollutant_data(df, polutant):
    row = df[df['pollutant_code'] == polutant].iloc[0]
    return f"{row['state_code']} <br> {row['avg_pollution']:.2f} {row['measurement_unit']}"

def big_numbers(pollutant):
    metrics = query_big_numbers()

    # Filtra apenas os dados do poluente selecionado
    pollutant_data = metrics[metrics['pollutant_code'] == pollutant]

    most_impacted_state = pollutant_data.loc[pollutant_data['avg_pollution'].idxmax(), 'state_code']
    highest_avg = float(pollutant_data['avg_pollution'].max())   
   
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric('Estado Mais Impactado', most_impacted_state)
    
    with col2: 
        st.metric('Maior média registrada', f'{highest_avg:.2f}')

def line_mensal(states):
    df = query_media_mensal()

    # Converter para datetime e extrair o mês
    df['year_month'] = pd.to_datetime(df['year_month'])
    df['month'] = df['year_month'].dt.month

    # Ordenar por data
    df.sort_values(by='year_month', inplace=True)

    df = get_month_name(df, coluna_mes='month')

    df = filter_media_mensal(df, states)

    fig = px.area(
        df,
        x='month',
        y='monthly_avg_pollution',
        color='pollutant_code',
        symbol='pollutant_code',
        markers=True,
        category_orders=get_month_order_dict(),
        labels={
            "month": "Mês",
            "monthly_avg_pollution": "Concentração Média",
            "pollutant_code": "Poluente"
        },
        title="Média Mensal de Poluição por Poluente",
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def compare_pollutant_state(pollutant, states):
    df = query_compare_pollutant_state()


    # Converter para datetime e extrair o mês
    df['year_month'] = pd.to_datetime(df['year_month'])
    df['month'] = df['year_month'].dt.month

    # Ordenar por data
    df.sort_values(by='year_month', inplace=True)
    
    df = get_month_name(df)

    if pollutant:
        df = df[df['pollutant_code'] == pollutant]

    if states:
        df = df[df['state_code'].isin(states)]

    df = df.groupby(['month', 'state_code'], as_index=False)['monthly_avg_pollution'].mean()

    df = df.dropna()

    available_states = list(df['state_code'].unique())

    fig = px.line(
        df,
        x='month',
        y='monthly_avg_pollution',
        color='state_code',
        symbol='state_code',
        markers=True,
        category_orders=get_month_order_dict(),
        labels={
            "month": "Mês",
            "monthly_avg_pollution": "Concentração Média",
            "state_code": "Estado"
        },
        title=f"Comparação de {pollutant} entre os Estados: {(', '.join(available_states)).replace("'", "")}",
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def poluicao_estado(states):
    df = query_poluicao_estado()

    df = filter_poluicao_estado(df, states=states)

    fig = px.histogram(
        df, 
        x="state_code", 
        y="avg_pollution",
        color='pollutant_code', 
        barmode='group',
        histfunc='avg',
        labels={
            "state_code": "Estado",
            "avg_pollution": "Concentração Média",
            "pollutant_code": "Poluente"
        },
        title="Estados com as maiores médias de poluição",
        height=400
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)
    
def pollution_map(pollutant, states):
    df = query_poluicao_estado()

    df = filter_poluicao_estado(df, states=states, pollutant=pollutant)

    br_states = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 
        'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 
        'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
    ]
    
    # Cria um DataFrame "base" que servirá como a lista completa
    df_todos_estados = pd.DataFrame(br_states, columns=['state_code'])

    # Junta o DataFrame completo com os dados da query
    # O 'how="left"' garante que todos os estados da lista completa sejam mantidos.
    # Para os estados que não estavam no resultado da query, o valor de 'avg_pollution' será NaN (nulo).
    df = pd.merge(df_todos_estados, df, on='state_code', how='left')

    # Todos os campos de média de poluição Nulos serão tratados como 0 para que apareça no mapa
    df['avg_pollution'] = df['avg_pollution'].fillna(0)
    
    geojson = get_geojson()

    fig = go.Figure(data=go.Choropleth(
        geojson=geojson,
        locations=df['state_code'],
        z = df['avg_pollution'].astype(float),
    ))

    fig.update_layout(
        title_text = 'Poluição Média em cada estado',
    )

    fig.update_geos(fitbounds="locations", visible=False)

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

@st.cache_data
def get_geojson():
    geojson = json.load(open("./assets/geojson.json"))

    return geojson

def get_month_order_dict():
    return {
        'month': [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
    }

def filter_media_mensal(df, states):
    if states:
        df = df[df['state_code'].isin(states)]

    df = df.groupby(['month', 'pollutant_code'], as_index=False)['monthly_avg_pollution'].mean().dropna()

    return df

def filter_poluicao_estado(df, states, pollutant=''):
    if states:
        df = df[df['state_code'].isin(states)]
    if pollutant:
        df = df[df['pollutant_code'] == pollutant]

    return df