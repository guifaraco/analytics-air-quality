import streamlit as st

from .graphs import big_numbers, media_mensal

from .filters import render_filters

def render_monitorar():
    filters = render_filters()

    st.header("Big Numbers")
    big_numbers(filters)

    st.divider()

    st.subheader("Concentração Mensal")
    media_mensal(filters)
    st.write("Gráfico relação Mes x Média de Concentração por cada poluente")

    st.divider()