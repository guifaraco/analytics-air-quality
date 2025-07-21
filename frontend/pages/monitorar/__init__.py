import streamlit as st

from .graphs import big_numbers, media_mensal

from .filters import render_filters

def render_monitorar():
    st.title("Monitor Ar")
    
    st.divider()

    big_numbers()

    st.divider()

    filters = render_filters()

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Concentração Mensal")
        media_mensal(filters)
        st.write("Gráfico relação Mes x Média de Concentração por cada poluente")
        
    with col2:
        st.subheader("Concentração Mensal")
        media_mensal(filters)
        st.write("Gráfico relação Mes x Média de Concentração por cada poluente")