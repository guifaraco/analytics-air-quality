import streamlit as st

from frontend.pages.correlacao import render_correlacao
from frontend.pages.datasus import render_datasus
from frontend.pages.monitorar import render_monitorar
from frontend.palletes import render_select_pallete

def load_css():
    try:
        with open("style.css") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Arquivo 'style.css' não encontrado. Crie o arquivo na mesma pasta.")

st.set_page_config(
    page_title="MonitorAr x DataSUS",
    page_icon='🏥',
    layout="wide",
)

load_css()

render_select_pallete()

pg = st.navigation([
    st.Page(render_datasus, title="DataSus", icon="🏥"),
    st.Page(render_monitorar, title="Monitorar", icon="📈"),
    st.Page(render_correlacao, title="Correlação MonitorAr x DataSUS", icon="🔗")
])

pg.run()
