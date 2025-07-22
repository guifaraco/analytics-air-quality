import streamlit as st
from frontend.utils import execute_query, get_states_list

def render_filters():
    states_list = get_states_list()

    srag_list = get_srag_list()

    filters = {}


    with st.container(border=True):
        col1, col2 = st.columns(2, gap='medium')
        
        with col1:  # Agora dentro do container
            state = st.selectbox(
                "Estado", 
                states_list, 
                key='state_code', 
                index=None, 
                placeholder="Selecione um estado"
            )

        if state:
            filters['state_code'] = state

        with col2:  # Também dentro do container
            srag = st.selectbox(
                "SRAG", 
                srag_list, 
                key='final_classification', 
                index=None, 
                placeholder="Selecione uma SRAG"
            )

        if srag:
            filters['final_classification'] = srag

    # Retorna o dicionário apenas com os filtros que foram de fato selecionados
    return filters

def get_srag_list():
    srag_df = execute_query('''
        SELECT DISTINCT
            final_classification
        FROM 
            gold.dim_case_classifications
        WHERE
            final_classification <> 'IGNORADO'
        ORDER BY 
            final_classification'''
    )
    
    srag_list= list(srag_df['final_classification'])

    return srag_list