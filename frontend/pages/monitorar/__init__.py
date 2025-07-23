import streamlit as st

from .filters import render_filters

from .graphs import bar_mensal, big_numbers, compare_pollutant_state, line_mensal, pollution_map, poluicao_estado

def render_monitorar():
    st.title("Monitor Ar")
    
    st.divider()

    st.subheader("Maior Impacto por Poluente")
    big_numbers()

    st.divider()

    st.subheader("Filtros")
    pollutant, states = render_filters()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        line_tab, bar_tab = st.tabs(["Gráfico de Linha", "Gráfico de Barras"])

    with line_tab:
        st.subheader("Concentração Mensal (Linha)")
        line_mensal(states)
        
    with bar_tab:
        st.subheader("Concentração Mensal (Barras)")
        bar_mensal(states)

    with col2:
        st.subheader("Comparação entre um Poluente x Estados")
        compare_pollutant_state(pollutant, states)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Estados com as maiores médias de poluição")
        poluicao_estado(states)

    with col4:
        st.subheader("Qualidade do Ar por Estado")
        pollution_map(pollutant, states)