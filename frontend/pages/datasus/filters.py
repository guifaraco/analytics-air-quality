import streamlit as st
from frontend.utils import execute_query, get_states_list
from utils.datasus.graph_queries import pegando_distinct_outcomes

def render_filters_mensal():
    states_list = ["TODOS"] + get_states_list()

    srag_list = ["TODAS"] + get_srag_list()

    filters = {}


    with st.container(border=True):
        col1, col2 = st.columns(2, gap='medium')
        
        with col1:  # Agora dentro do container
            state = st.selectbox(
                "Estado", 
                states_list, 
                key='state_code', 
                index=0, 
                placeholder="Selecione um estado"
            )

        if state:
            filters['state_code'] = state

        with col2:  # Também dentro do container
            srag = st.selectbox(
                "SRAG", 
                srag_list, 
                key='final_classification', 
                index=0, 
                placeholder="Selecione uma SRAG"
            )

        if srag:
            filters['final_classification'] = srag

    # Retorna o dicionário apenas com os filtros que foram de fato selecionados
    return filters

def render_filters_geral():
    filters = {}
    srag_list = ["TODAS"] + get_srag_list()
    evolucao = get_outcomes_list()

    # 2. Filtros Clínicos
    st.write("**Dados Clínicos**")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            srag = st.selectbox("SRAG",
                                srag_list,
                                key='final_classification_2',
                                index=0,
                                placeholder='Selecione uma SRAG'
                                )
        if srag:
            filters['final_classification'] = srag

        with col2:
            desfecho = st.multiselect("Desfecho",
                                    evolucao,
                                    default=["OBITO", "CURA"])
        if desfecho:
            filters['desfecho'] = desfecho

    return filters

def get_srag_list():
    srag_df = execute_query('''
        SELECT DISTINCT
            srag
        FROM 
            gold.mart_total_cases_per_srag_and_evolution
        '''
    )
    
    srag_list= list(srag_df['srag'])

    return srag_list

def get_outcomes_list():
    df = pegando_distinct_outcomes()

    outcome_list = list(df['evolucao'])

    return outcome_list