import json
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from frontend.utils import get_month_name
from utils.monitorar.graph_queries import query_big_numbers, query_compare_pollutant_state, query_media_mensal, query_poluicao_estado

def big_numbers():
    metrics = query_big_numbers()

    emoji_map = {
        "CO": "🔥", "MP10": "🌫️", "MP2,5": "🌫️",
        "NO2": "🧪", "SO2": "🧪", "O3": "☁️"
    }

    rows = list(metrics.itertuples(index=False))
    for row_number in range(2):  # 2 linhas
        cols = st.columns(3, gap='large')
        for i in range(3):  # 3 colunas por linha
            j = row_number * 3 + i  # índice real da métrica
            row = rows[j]
            pol = row.pollutant_code
            uf = row.state_code
            unit = row.measurement_unit
            val = float(row.avg_pollution)
            icon = emoji_map.get(pol, "")

            with cols[i]:
                st.markdown(f"""
                    <div class='metric-datasus' style="text-align:center; line-height:1.6; height:300px">
                        <h3 style="margin-bottom:0;margin-left:25px;">{icon} {pol}</h3>
                        <p style="margin:0; font-size:15px; color:#888;">Estado mais impactado</p>
                        <h4 style="margin:0;margin-left:25px;">{uf}</h4>
                        <p style="margin:0; font-size:15px; color:#888;">Média registrada</p>
                        <h3 style="margin:0; margin-left:25px;">{val:.2f} {unit}</h3>
                    </div>
                """, unsafe_allow_html=True)
            st.write('')

def line_mensal(states):
    df = query_media_mensal(states)

    df = get_month_name(df)

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

def bar_mensal(states):
    df = query_media_mensal(states)

    df = get_month_name(df)

    fig = px.histogram(
        df, 
        x="month", 
        y="monthly_avg_pollution",
        color='pollutant_code', 
        barmode='group',
        histfunc='avg',
        category_orders=get_month_order_dict(),
        labels={
            "month": "Mês",
            "monthly_avg_pollution": "Concentração Média",
            "pollutant_code": "Poluente"
        },
        height=400
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def compare_pollutant_state(pollutant, states):
    if not pollutant:
        st.warning('Selecione um poluente para exibir esse gráfico', icon="⚠️")
        return
    
    df = query_compare_pollutant_state(pollutant, states)

    df = get_month_name(df)

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
        title=f"Comparação de {pollutant} entre os Estados: {(', '.join(states)).replace("'", "")}",
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def poluicao_estado(pollutant, states):
    df = query_poluicao_estado(pollutant, states)

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
        height=400
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)
    
def pollution_map(pollutant, states):
    df = query_poluicao_estado(pollutant, states)

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
        z = df['avg_pollution'].astype(float)
    ))

    fig.update_layout(
        title_text = 'Poluição Média em cada estado',
        margin={"r":0, "t":0, "l":0, "b":0},
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