import streamlit as st
import pandas as pd

from .graphs import evolucao_mensal, render_map

def render_dashboard(filters):
    st.subheader("Mapa de Casos Encontrados")
    with st.expander("Mapa de Casos Encontrados"):
        found = render_map(filters)
        st.write(f"Casos encontrados: {found}")

    st.subheader("Evolução Mensal")
    evolucao_mensal(filters)