import streamlit as st

from .filters import state_filter, pollutant_filter

from .graphs import big_numbers, compare_pollutant_state, line_mensal, poluicao_estado

def render_monitorar():
    st.title("Monitor Ar")
     
    pollutant = pollutant_filter() # Tirar TODOS do filtro
    
    big_numbers(pollutant) # COlocar unidade de medida

    with st.container(border=True):
        
        states = state_filter()

        col1, col2 = st.columns(2)

        with col1:
            compare_pollutant_state(pollutant, states)
            
        with col2:
            line_mensal(states)


        poluicao_estado(states)