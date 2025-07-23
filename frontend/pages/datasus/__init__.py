import streamlit as st

from .graphs import big_numbers, casos_map, casos_mensais, casos_mensais_por_srag
from .graphs import casos_por_srag_evolucao, casos_por_fator_risco, casos_por_sintomas, faixa_etaria
from .graphs import evolucao_mensal_por_srag, evolucao_mensal_desfecho

from .filters import render_filters_mensal, render_filters_geral

def render_datasus():
    st.title("DataSus")

    st.divider()

    big_numbers()

    st.divider()

    tab_distribuicao_mensal, tab_distribuicao_geral = st.tabs(['Distribuição Mensal', 'Distribuição Geral'])

    with tab_distribuicao_mensal:

        with st.container(border=True):
            filters = render_filters_mensal()

            row1_col1, row1_col2 = st.columns(2)

            with row1_col1:
                casos_mensais(filters)

            with row1_col2:
                evolucao_mensal_por_srag(filters)
        
        with st.container(border=True):

            row1_col1, row1_col2 = st.columns(2)
            
            with row1_col1:
                evolucao_mensal_desfecho()
            
            with row1_col2:
                casos_por_srag_evolucao() 

    with tab_distribuicao_geral:

        with st.container(border=True):
            filters = render_filters_geral()

            col1, col2 = st.columns(2)

            with col1:
                casos_por_sintomas(filters)  
                

            with col2:
                casos_por_fator_risco(filters)
            
            faixa_etaria(filters) 

    st.subheader("Mapa de Casos Encontrados")
    with st.expander("Mapa de Casos Encontrados"):
        casos_map()