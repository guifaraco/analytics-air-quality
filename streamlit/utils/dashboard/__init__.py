import streamlit as st
import pandas as pd

from .graphs.map import render_map
from .graphs.evolucao_mensal import evolucao_mensal

def render_dashboard(filters):
    # st.subheader("Mapa de Casos Encontrados")
    # with st.expander("Mapa de Casos Encontrados"):
    #     found = render_map(filters)
    #     st.write(f"Casos encontrados: {found}")

    st.subheader("Evolução Mensal")
    evolucao_mensal(filters)