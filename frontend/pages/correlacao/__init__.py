import streamlit as st

from .graphs import compara_mensal

from .filters import render_filters

def render_correlacao():
    st.title("Correlação MonitorAr x DataSUS")

    st.divider()

    st.subheader("Filtros")
    pollutant, states = render_filters()

    st.divider()
    
    st.subheader("Comparação Mensal")
    compara_mensal(pollutant, states)