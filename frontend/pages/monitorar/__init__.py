import streamlit as st

from .filters import state_filter, pollutant_filter

from .graphs import bar_mensal, big_numbers, compare_pollutant_state, line_mensal, pollution_map, poluicao_estado

def render_monitorar():
    st.title("Monitor Ar")
    
    st.divider()

    st.subheader("Maior Impacto por Poluente")
    big_numbers()

    st.divider()

    # pollutant, states = render_filters()

    with st.container(border=True):
        
        states = state_filter()

        col1, col2 = st.columns(2)

        with col1:
            line_mensal(states)
            
        with col2:
            poluicao_estado(states)


        pollutant = pollutant_filter()
        
        col3, col4 = st.columns(2)

        with col3:
            compare_pollutant_state(pollutant, states)

        with col4:
            pollution_map(pollutant, states)