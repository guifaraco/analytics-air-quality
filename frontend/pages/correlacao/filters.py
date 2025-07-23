import streamlit as st

from frontend.pages.monitorar.filters import pollutant_filter
from frontend.utils import get_srag_list, get_states_list

def render_filters():
    col1, col2, col3 = st.columns(3)

    with col1:
        pollutant = pollutant_filter()

    with col2:
        srag = srag_filter()

    with col3:
        states = state_filter()

    return pollutant, states, srag

def state_filter():
    states_list = get_states_list()
    
    states = st.multiselect(
        "Estados", 
        states_list, 
        key='state_code',
        placeholder="Selecione um estado"
    )

    return states

def srag_filter():
    srag_list = ["TODAS"] + get_srag_list()

    srag = st.selectbox(
        "SRAG",
        srag_list,
        key='final_classification_2',
        index=0,
        placeholder='Selecione uma SRAG'
    )

    return srag