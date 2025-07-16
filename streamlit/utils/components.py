import streamlit as st

from .monitorar import get_stations

def get_filters():
    df = get_stations(['Nome do Município', 'Estado'])

    return df


def sidebar():
    df = get_filters()

    filters = {}
    with st.sidebar:
        st.header("Filtros")
        st.divider()

        uf_list = sorted(list(df['Estado'].drop_duplicates()))

        # 1. Armazena a seleção do estado em uma variável temporária
        filters['uf'] = st.selectbox(
            "Estado", 
            uf_list, 
            key='uf', 
            index=None, 
            placeholder="Selecione um estado"
        )

        # 2. Se um estado foi selecionado, adiciona ao dicionário e mostra o filtro de cidade
        if filters['uf']:
            city_list = sorted(list(df[df['Estado'] == filters['uf']]['Nome do Município'].drop_duplicates()))

            # 3. Armazena a seleção da cidade em outra variável
            filters['city'] = st.selectbox(
                "Município", 
                city_list, 
                key='city', 
                index=None, 
                placeholder="Selecione um município"
            )

    # Imprime no console onde o Streamlit está rodando
    print(filters)

    # Retorna o dicionário apenas com os filtros que foram de fato selecionados
    return filters


