import streamlit as st

from utils.dashboard import render_dashboard
from utils.components import sidebar
from utils.monitorar import render_monitorar
from utils.datasus import render_datasus

st.set_page_config(
    page_title="MonitorAr x DataSUS",
    page_icon='🏥',
    layout="wide"
)

filters = sidebar()

st.title("🏥 MonitorAr x DataSUS")

dashboard, monitorar, datasus = st.tabs(["Dashboard", "MonitorAr", "DataSUS"])

with monitorar:
    ma_df = render_monitorar(filters)

with datasus:
    ds_df = render_datasus(filters)

with dashboard:
    render_dashboard(ma_df, ds_df, filters)

