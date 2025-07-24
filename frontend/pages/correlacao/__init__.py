import streamlit as st

from .graphs import big_numbers, compara_estado, compara_mensal

from .filters import render_filters

def render_correlacao():
    st.title("Correlação MonitorAr x DataSUS")

    big_numbers()

    st.divider()

    st.subheader("Filtros")
    pollutants, srags = render_filters()

    st.divider()

    compara_mensal(pollutants, srags)

    st.divider()

    compara_estado(pollutants, srags)