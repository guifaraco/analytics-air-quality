import streamlit as st

from .graphs import big_numbers, casos_map, casos_mensais, casos_mensais_por_srag
from .graphs import casos_por_srag_evolucao, casos_por_fator_risco, casos_por_sintomas, faixa_etaria
from .graphs import evolucao_mensal_por_srag, evolucao_mensal_desfecho

from .filters import render_filters_mensal, render_filters_geral

def render_datasus():
    st.title("DataSus")

    st.subheader('', divider=True)

    big_numbers()

    st.divider()

    st.divider()

    tab_distribuicao_mensal, tab_distribuicao_geral = st.tabs(['Distribuição Mensal', 'Distribuição Geral'])

    with tab_distribuicao_mensal:

        filters = render_filters_mensal()

        col1, col2 = st.columns(2)

        with col1:
            casos_mensais(filters)

        with col2:
            evolucao_mensal_por_srag(filters)
        
        col3, col4 = st.columns(2)

        with col3:
            evolucao_mensal_desfecho()

    with tab_distribuicao_geral:

        filters = render_filters_geral()

        col1, col2 = st.columns(2)

        with col1:
            casos_por_srag_evolucao()

        with col2:
            casos_por_fator_risco()
        
        col3, col4 = st.columns(2)
    
        with col3:
            casos_por_sintomas()       
        
        with col4:
            faixa_etaria()



    col1, col2 = st.columns(2)


    # with col2:
       
        
    st.subheader("Mapa de Casos Encontrados")
    with st.expander("Mapa de Casos Encontrados", expanded=True):
        casos_map()