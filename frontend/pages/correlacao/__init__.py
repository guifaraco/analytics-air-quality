import streamlit as st

from .graphs import compara_mensal

from .filters import render_filters

def render_correlacao():
    st.title("Correlação MonitorAr x DataSUS")

    st.divider()

    st.subheader("Filtros")
    pollutant, states, srag = render_filters()

    st.divider()

    col1, col2 = st.columns(2)
    
    with col1:
        compara_mensal(pollutant, states)
    
    with col2:
        casos_poluente(pollutant, states, srag)