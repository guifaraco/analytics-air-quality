import json
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

from frontend.utils import get_month_name
from utils.monitorar.graph_queries import query_big_numbers, query_media_mensal, query_map, query_poluicao_estado

def big_numbers():
    metrics = query_big_numbers()

    emoji_map = {
        "CO": "🔥", "MP10": "🌫️", "MP2,5": "🌫️",
        "NO2": "🧪", "SO2": "🧪", "O3": "☁️"
    }

    rows = list(metrics.itertuples(index=False))
    cols = st.columns(6, gap='medium')
    for j in range(6):
        row = rows[j]
        pol = row.pollutant_code
        uf = row.state_code
        unit = row.measurement_unit
        val = float(row.avg_pollution)
        icon = emoji_map.get(pol, "")

        with cols[j]:
            st.markdown(f"""
                <div style="text-align:center; line-height:1.6;">
                    <h3 style="margin-bottom:0;">{icon} {pol}</h3>
                    <p style="margin:0; font-size:15px; color:#888;">Estado mais impactado</p>
                    <h4 style="margin:0;">{uf}</h4>
                    <p style="margin:0; font-size:15px; color:#888;">Média registrada</p>
                    <h3 style="margin:0; margin-left:25px">{val:.2f} {unit}</h3>
                </div>
            """, unsafe_allow_html=True)
    st.write('')

def line_mensal(filters):
    df = query_media_mensal(filters)

    df = get_month_name(df)

    fig = px.area(
        df,
        x='month',
        y='monthly_avg_pollution',
        color='pollutant_code',
        symbol='pollutant_code',
        markers=True,
        labels={
            "month": "Mês",
            "monthly_avg_pollution": "Concentração Média",
            "pollutant_code": "Poluente"
        },
        title="Média Mensal de Poluição por Poluente",
    )

    fig.update_traces(marker=dict(size=7.5))

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def bar_mensal(filters):
    df = query_media_mensal(filters)

    df = get_month_name(df)

    fig = px.histogram(
        df, 
        x="month", 
        y="monthly_avg_pollution",
        color='pollutant_code', 
        barmode='group',
        histfunc='avg',
        labels={
            "month": "Mês",
            "monthly_avg_pollution": "Concentração Média",
            "pollutant_code": "Poluente"
        },
        height=400
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def poluicao_estado(filters):
    df = query_poluicao_estado(filters)

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
    

def pollution_map(filters):
    df = query_map(filters)

    geojson = json.load(open("./assets/geojson.json"))

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