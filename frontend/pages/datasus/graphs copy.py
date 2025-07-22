import streamlit as st
import plotly.express as px
import pydeck as pdk
import pandas as pd

from utils.datasus.graph_queries import query_big_numbers_primeira_linha, query_big_numbers_segunda_linha
from utils.datasus.graph_queries import query_casos_mensais, df_melted, query_fatores_risco
from utils.datasus.graph_queries import query_casos_por_faixa_etaria, query_casos_por_srag_e_evolucao
from utils.datasus.graph_queries import query_casos_map
from frontend.utils import get_month_name

def big_numbers():
    first_row = query_big_numbers_primeira_linha()
    second_row = query_big_numbers_segunda_linha()

    rows_list = [{
        'Total de casos': first_row['total_cases'].sum(),
        'Taxa de Internação': f"{first_row['icu_percentage'].mean():.2f}%",
        'Taxa de Mortalidade': f"{first_row['death_percentage'].mean():.2f}%"
        },
        {
        'SRAG com maior número de casos': f"{second_row['top_classification_by_total_cases'].values[0]} <br> {second_row['max_total_cases'].values[0]} Casos",
        'SRAG com maior taxa de Internação': f"{second_row['top_classification_by_icu_rate'].values[0]} <br> {second_row['max_icu_rate'].values[0]}%",
        'SRAG com maior taxa de Mortalidade': f"{second_row['top_classification_by_death_rate'].values[0]} <br> {second_row['max_death_rate'].values[0]:.2f}%"
    }]

    for row_dict in rows_list:
        cols = st.columns(3, gap='small')
        col_index = 0
        for title, value in row_dict.items():
            with cols[col_index].container():
                render_big_number(title, value)
            col_index = (col_index + 1) % 3
        st.markdown('')


def render_big_number(title, value):
    # st.metric(label=title, value=value)
    value = str(value).replace('SRAG', '').replace('POR', '')
    st.markdown(
        f'''
            <div class='metric-datasus'>
                <p>{title}</p>
                <h4>{value}</h4>
            </div>
        ''',
        unsafe_allow_html=True
    )


def casos_mensais(filters):
    df = query_casos_mensais()

    df = get_month_name(df, coluna_mes='month')

    fig = px.area(
        df,
        x='month',
        y='sum',
        markers=True,
        labels={
            "month": "Mês",
            "sum": "Total de Casos",
        },
        title="Total de casos Mensal",
        text='sum'
    )

    # Personalizar a linha e marcadores
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=10),
        text=df['sum'],  # Valores que aparecem nos marcadores
        textposition="top center"
    )

    # Adicionar os valores em cima de cada ponto
    fig.update_traces(
        texttemplate='%{text:.0f}',
        textfont_size=12,
        showlegend=False
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def casos_map(filters):
    df = query_casos_map()

    df['numero_total_cases'] = pd.to_numeric(df['numero_total_cases'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    layer = pdk.Layer(
        'ColumnLayer',
        data=df,
        get_position=['longitude', 'latitude'],
        get_elevation='numero_total_cases',
        elevation_scale=10,
        radius=5000,
        get_fill_color=[255, 140, 0, 150],
        pickable=True,
        extruded=True,
    )

    view_state = pdk.ViewState(
        latitude=-23,
        longitude=-50,
        zoom=4,
        bearing=-45,
        pitch=45
    )

    # Tooltip com nome da cidade e número de casos
    tooltip = {
        "text": "Cidade: {city_name}\nCasos: {numero_total_cases}"
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(r)
