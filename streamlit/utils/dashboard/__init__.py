import streamlit as st

from .graphs.map import render_map
from .graphs.media_estado import media_estado
from .graphs.evolucao_mensal import evolucao_mensal

def render_dashboard(filters):
    # st.subheader("Mapa de Casos Encontrados")
    # with st.expander("Mapa de Casos Encontrados"):
    #     found = render_map(filters)
    #     st.write(f"Casos encontrados: {found}")

    st.subheader("Evolução Mensal")
    # evolucao_mensal(filters)

    # st.subheader("Média de Concentração por Estado")
    # media_estado(filters)