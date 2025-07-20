import streamlit as st

from utils.monitorar import format_month, get_monitorar

from .graphs import grafico_duplo, media_mensal

from .filters import render_filters

def render_monitorar():
    filters = render_filters()

    # df = get_monitorar(filters=filters)

    # df = format_month(df)

    st.subheader("Concentração Mensal")
    media_mensal(filters)
    st.write("Gráfico relação Mes x Média de Concentração por cada poluente")

    st.divider()

    # st.subheader("Gráfico Duplo")
    # st.write("linha -> Série Temporal dos poluentes")
    # st.write("barras -> número de casos")
    # grafico_duplo(df)

    # st.divider()

    # st.subheader("Mapa de Casos Encontrados")
    # with st.expander("Mapa de Casos Encontrados"):
    #     found = render_map(filters)
    #     st.write(f"Casos encontrados: {found}")

    # st.subheader("Média de Concentração por Estado")
    # media_estado(filters)