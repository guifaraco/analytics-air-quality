import streamlit as st

from .graphs import big_numbers, compara_estado, compara_mensal

from .filters import render_filters

def render_correlacao():
    st.title("Correlação MonitorAr x DataSUS")

    big_numbers()

    with st.container(border=True):
        pollutants, srags = render_filters()

        compara_mensal(pollutants, srags)

        compara_estado(pollutants, srags)