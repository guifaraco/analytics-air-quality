import streamlit as st

from utils.components import sidebar
from utils.monitorar import render_monitorar
from utils.datasus import render_datasus

st.set_page_config(
    page_title="MonitorAr x DataSUS",
    page_icon='🏥',
    layout="wide"
)

sidebar()

st.title("🏥 MonitorAr x DataSUS")

main, monitorar, datasus = st.tabs(["Dashboard", "MonitorAr", "DataSUS"])

with monitorar:
    ma_df = render_monitorar()
with datasus:
    render_datasus(ma_df=ma_df)

