import streamlit as st
import plotly.express as px
import pydeck as pdk

from utils.datasus.graph_queries import query_big_numbers, query_casos_map, query_casos_mensais

def big_numbers(filters):
    metrics = query_big_numbers(filters)
    rows = list(metrics.itertuples(index=False))

    for row in rows:
        final_class = row.final_classification
        total_cases = row.total_cases
        death_percentage = float(row.death_percentage)
        age_group = row.age_group

        with st.expander(final_class):
            col1, col2, col3 = st.columns(3, gap='small')

        with col1:
            st.markdown(f"""
                <div style="text-align:center">
                    <p style="color:#888; font-size:15px;">Total de internações</p>
                    <h2 style="margin-top:0; color:#00d4ff;">{total_cases}</h2>
                </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
                <div style="text-align:center">
                    <p style="color:#888; font-size:15px;">Taxa de Mortalidade</p>
                    <h2 style="margin-top:0; color:#ff4c4c;">{death_percentage}%</h2>
                </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
                <div style="text-align:center">
                    <p style="color:#888; font-size:15px;">Faixa Etária mais comum</p>
                    <h2 style="margin-top:0; color:#facc15;">{age_group}</h2>
                </div>
            """, unsafe_allow_html=True)

def casos_mensais(filters):
    df = query_casos_mensais(filters)

    fig = px.line(
        df,
        x='month',
        y='total_cases',
        color='final_classification',
        markers=True,
        labels={
            "month": "Mês",
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
        get_position=['longitude', 'latitude'],
        get_elevation='total_casos',
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
        tooltip={"text": "{municipio} \nCasos: {total_casos}"},
    )

    st.pydeck_chart(r)