import streamlit as st

from frontend.utils import get_states_list

def render_filters():
    filters = {}

    states_list = get_states_list()

    pollutant_list = ["CO", "MP10", "MP2,5", "NO2", "SO2","O3"]
    
    st.header("Filtros")
    col1, col2 = st.columns(2, gap='medium')

    with col1:
        state = st.selectbox(
            "Estado", 
            states_list, 
            key='state_code', 
            index=None, 
            placeholder="Selecione um estado"
        )

    if state:
        filters['state_code'] = state

    with col2:
        pollutant = st.selectbox(
            "Poluente", 
            pollutant_list, 
            key='pollutant_code', 
            index=None, 
            placeholder="Selecione um poluente"
        )

    if pollutant:
        filters['pollutant_code'] = pollutant

    # Retorna o dicionário apenas com os filtros que foram de fato selecionados
    return filters