import streamlit as st
from utils.execute_query import select

def render_filters():
    state_code_list = list(select('dim_locations', ['state_code'], distinct=True))

    filters = {}
    
    with st.expander("Filtros"):
        col1, col2 = st.columns(2, gap='medium')

        with col1:
            # 1. Armazena a seleção do estado em uma variável temporária
            filters['state_code'] = st.selectbox(
                "Estado", 
                state_code_list, 
                key='state_code', 
                index=None, 
                placeholder="Selecione um estado"
            )


        with col2:
            # 2. Se um estado foi selecionado, adiciona ao dicionário e mostra o filtro de cidade
            if filters['state_code']:
                city_list = list(select('dim_locations', ['city_name'], filters={'state_code': filters['state_code']} , distinct=True))
                # 3. Armazena a seleção da cidade em outra variável
                filters['city_name'] = st.selectbox(
                    "Município", 
                    city_list, 
                    key='city_name', 
                    index=None, 
                    placeholder="Selecione um município"
                )

    # Retorna o dicionário apenas com os filtros que foram de fato selecionados
    return filters


