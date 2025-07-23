import streamlit as st

from .filters import state_filter, pollutant_filter

from .graphs import big_numbers, compare_pollutant_state, line_mensal, pollution_map, poluicao_estado

def render_monitorar():
    st.title("Monitor Ar")
    
    st.divider()
    
    pollutant = pollutant_filter()
        
    st.subheader("Maior Impacto por Poluente")
    
    big_numbers(pollutant)

    st.divider()

    # pollutant, states = render_filters()

    with st.container(border=True):
        
        states = state_filter()

        col1, col2 = st.columns(2)

        with col1:
            compare_pollutant_state(pollutant, states)
            
        with col2:
            pollution_map(pollutant, states)

        col3, col4 = st.columns(2)

        with col3:
            line_mensal(states)

        with col4:
            poluicao_estado(states)