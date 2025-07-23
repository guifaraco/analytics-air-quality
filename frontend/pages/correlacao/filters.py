import streamlit as st

from frontend.utils import get_srag_list

def month_filter():
    months = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
              "Julho", "Agosto", "Setembro", "Outubro", "Novembro"]

    name = st.selectbox("Mês", months, key="month", placeholder="Selecione um Mês")
    number = months.index(name) + 1

    return number

def render_filters():
    col1, col2 = st.columns(2)

    with col1:
        pollutants = multipollutant_filter()

    with col2:
        srags = srag_filter()

    return pollutants, srags

def singlepollutant_filter():
    pollutant_list = ["CO", "MP10", "MP2,5", "NO2", "SO2","O3"]

    pollutant = st.selectbox(
        "Poluente",
        pollutant_list,
        key='single_pollutant_code',
        placeholder="TODOS"
    )

    # Retorna o filtro selecionado
    return pollutant

def multipollutant_filter():
    pollutant_list = ["CO", "MP10", "MP2,5", "NO2", "SO2","O3"]

    pollutants = st.multiselect(
        "Poluentes",
        pollutant_list,
        key='multi_pollutant_code',
        placeholder="TODOS"
    )

    # Retorna o filtro selecionado
    return pollutants

def srag_filter():
    srag_list = get_srag_list()

    srags = st.multiselect(
        "SRAG",
        srag_list,
        key='final_classification_2',
        placeholder='TODAS'
    )

    return srags