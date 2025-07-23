import streamlit as st

from frontend.utils import get_states_list

def pollutant_filter():
    pollutant_list = ["CO", "MP10", "MP2,5", "NO2", "SO2","O3"]

    pollutant = st.selectbox(
        "Poluente",
        pollutant_list,
        key='pollutant_code',
        placeholder="Selecione um poluente"
    )

    # Retorna o filtro selecionado
    return pollutant


def state_filter():
    states_list = get_states_list()
    
    states = st.multiselect(
        "Estados", 
        states_list, 
        key='state_code',
        placeholder="Selecione um estado"
    )

    return states