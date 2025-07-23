import streamlit as st

from .graphs import compara_mensal

from .filters import render_filters

def render_correlacao():
    st.title("Correlação MonitorAr x DataSUS")

    st.divider()

    st.subheader("Filtros")
    pollutants, states, srags = render_filters()

    st.divider()

    compara_mensal(pollutants, states, srags)

    st.divider()