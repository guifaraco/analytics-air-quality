import streamlit as st

from .graphs import big_numbers, casos_map, casos_mensais

from .filters import render_filters

def render_datasus():
    filters = render_filters()

    st.header("Big Numbers")
    big_numbers(filters)

    st.divider()

    st.subheader("Casos Mensais")
    casos_mensais(filters)
    st.write("Gráfico relação Mes x Casos por cada SRAG")

    st.divider()

    st.subheader("Mapa de Casos Encontrados")
    with st.expander("Mapa de Casos Encontrados"):
        casos_map(filters)