import streamlit as st

from .graphs import bar_mensal, big_numbers, line_mensal, pollution_map, poluicao_estado

from .filters import render_filters

def render_monitorar():
    st.title("Monitor Ar")
    
    st.divider()

    st.subheader("Maior Impacto por Poluente")
    big_numbers()

    st.divider()

    filters = render_filters()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Concentração Mensal (Linha)")
        line_mensal(filters)
        
    with col2:
        st.subheader("Concentração Mensal (Barras)")
        bar_mensal(filters)
        
    st.divider()

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Estados com as maiores médias de poluição")
        poluicao_estado(filters)

    with col4:
        st.subheader("Qualidade do Ar por Estado")
        pollution_map(filters)