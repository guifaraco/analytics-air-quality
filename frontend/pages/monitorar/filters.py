import streamlit as st
from utils.execute_query import select

def render_filters():
    filters = {}

    state_df = select('dim_locations', ['state_code'], distinct=True)
    state_list = list(state_df['state_code'].sort_values())

    pollutant_list = ["CO", "MP10", "MP2,5", "NO2", "SO2","O3"]
    
    with st.expander("Filtros"):
        col1, col2, col3 = st.columns(3, gap='medium')

        with col1:
            state = st.selectbox(
                "Estado", 
                state_list, 
                key='state_code', 
                index=None, 
                placeholder="Selecione um estado"
            )

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

        if state:
            filters['state_code'] = state
            with col3:
                # Se um estado foi selecionado, adiciona ao dicionário e mostra o filtro de cidade
                city_df = select('dim_locations', ['city_name'], filters={'state_code': state} , distinct=True)
                city_list = list(city_df['city_name'].sort_values())
                # Armazena a seleção da cidade em outra variável
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