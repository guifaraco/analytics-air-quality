import streamlit as st

from frontend.pages.monitorar import render_monitorar



st.set_page_config(
    page_title="MonitorAr x DataSUS",
    page_icon='🏥',
    layout="wide"
)

pg = st.navigation([
    st.Page(render_monitorar, title="Monitorar", icon="📈")
])

pg.run()