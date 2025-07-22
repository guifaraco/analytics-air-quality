import streamlit as st
import plotly.express as px
import pydeck as pdk

from utils.datasus.graph_queries import query_big_numbers, query_casos_map, query_casos_mensais

def big_numbers():
    first_row, second_row = query_big_numbers()

    rows_list = [{
        'Total de casos': first_row['total_cases'],
        'Taxa de Internação': f"{first_row['icu_percentage']}%",
        'Taxa de Mortalidade': f"{first_row['death_percentage']}%"
        },
        {
        'SRAG com maior número de casos': f"{second_row['srag_total_cases']} <br> ({second_row['max_total_cases']} casos)",
        'SRAG com maior taxa de Internação': f"{second_row['srag_icu_percentage']} <br> ({second_row['max_icu_percentage']}%)",
        'SRAG com maior taxa de Mortalidade': f"{second_row['srag_death_percentage']} <br> ({second_row['max_death_percentage']}%)"
    }]

    for row_dict in rows_list:
        cols = st.columns(3, gap='small')
        col_index = 0
        for title, value in row_dict.items():
            with cols[col_index].container():
                render_big_number(title, value)
            col_index = (col_index + 1) % 3


def render_big_number(title, value):
    st.metric(label=title, value=value)


def casos_mensais(filters):
    df = query_casos_mensais(filters)

    fig = px.area(
        df,
        x='month_name',
        y='total_cases',
        color='final_classification',
        markers=True,
        labels={
            "month_name": "Mês",
            "total_cases": "Total de Casos",
            "final_classification": "SRAG"
        },
        title="Total de casos Mensal para cada SRAG"
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def casos_map(filters):
    df = query_casos_map(filters)

    layer = pdk.Layer(
        'ColumnLayer',
        data=df,
        get_position='coordinates',
        get_elevation='total_cases',
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

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{city_name} \nCasos: {total_cases}"},
    )

    st.pydeck_chart(r)
