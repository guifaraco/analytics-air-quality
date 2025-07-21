import streamlit as st

from .graphs import big_numbers, casos_map, casos_mensais

from .filters import render_filters

def render_datasus():
    st.title("DataSus")

    st.divider()

    big_numbers()

    st.divider()

    filters = render_filters()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Casos Mensais")
        casos_mensais(filters)
        st.write("Gráfico relação Mes x Casos por cada SRAG")


    with col2:
        st.subheader("Mapa de Casos Encontrados")
        with st.expander("Mapa de Casos Encontrados"):
            casos_map(filters)