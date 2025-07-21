import streamlit as st
from utils.execute_query import select

def render_filters():
    state_df = select('dim_locations', ['state_code'], distinct=True)
    state_list = list(state_df['state_code'].sort_values())

    filters = {}
    
    with st.expander("Filtros"):
        col1, col2 = st.columns(2, gap='medium')

        with col1:
            # 1. Armazena a seleção do estado em uma variável temporária
            state = st.selectbox(
                "Estado", 
                state_list, 
                key='state_code', 
                index=None, 
                placeholder="Selecione um estado"
            )

        if state:
            filters['state_code'] = state
            with col2:
                # 2. Se um estado foi selecionado, adiciona ao dicionário e mostra o filtro de cidade
                city_df = select('dim_locations', ['city_name'], filters={'state_code': state} , distinct=True)
                city_list = list(city_df['city_name'].sort_values())
                # 3. Armazena a seleção da cidade em outra variável
                city = st.selectbox(
                    "Município", 
                    city_list, 
                    key='city_name', 
                    index=None, 
                    placeholder="Selecione um município"
                )
        
                if city:
                    filters['city_name'] = city

    # Retorna o dicionário apenas com os filtros que foram de fato selecionados
    return filters