import streamlit as st

from .graphs import compara_mensal, correlacao_poluicao_casos

from .filters import render_filters

def render_correlacao():
    st.title("Correlação MonitorAr x DataSUS")

    # Big Number
    # Selecionar um mes (janeiro não exibir delta)
    # Taxa de mortalidade -> compara com o mes anterior
    # Total de casos -> comparando com o mes anterior
    # Taxa de UTI   -> comparando com o mês anterior
    # Média geral de concentração de poluiente -> media de poluição

    st.divider()

    st.subheader("Filtros")
    pollutants, states, srags = render_filters()

    st.divider()

    compara_mensal(pollutants, states, srags)

    # Tirar filtros de estado
    # Fazer o mesmo gráfico anterior

    st.divider()