import streamlit as st

from utils.dashboard import render_dashboard
from utils.components import render_filters

st.set_page_config(
    page_title="MonitorAr x DataSUS",
    page_icon='🏥',
    layout="wide"
)


st.title("🏥 MonitorAr x DataSUS")

filters = render_filters()

render_dashboard(filters)

