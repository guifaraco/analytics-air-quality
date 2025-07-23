import streamlit as st

from frontend.utils import get_srag_list, get_states_list

def render_filters():
    col1, col2, col3 = st.columns(3)

    with col1:
        pollutants = pollutants_filter()

    with col2:
        srags = srag_filter()

    with col3:
        states = state_filter()

    return pollutants, states, srags

def pollutants_filter():
    pollutant_list = ["CO", "MP10", "MP2,5", "NO2", "SO2","O3"]

    pollutants = st.multiselect(
        "Poluente",
        pollutant_list,
        key='pollutant_code',
        placeholder="TODOS"
    )

    # Retorna o filtro selecionado
    return pollutants

def state_filter():
    states_list = get_states_list()
    
    states = st.multiselect(
        "Estados", 
        states_list, 
        key='state_code',
        placeholder="TODOS"
    )

    return states

def srag_filter():
    srag_list = get_srag_list()

    srags = st.multiselect(
        "SRAG",
        srag_list,
        key='final_classification_2',
        placeholder='TODAS'
    )

    return srags