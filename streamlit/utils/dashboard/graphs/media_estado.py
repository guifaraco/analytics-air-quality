import streamlit as st
import pandas as pd
import altair as alt

from utils.monitorar import get_monitors

def media_estado(filters):
    cols = [
        'Estado', 'Sigla', 'Concentracao'
    ]
    monitors_df = get_monitors(filters=filters, cols=cols)

    monitors_df['Sigla'] = monitors_df['Sigla'].apply(apply_measure_unit)
    
    grouped = (
        monitors_df
        .groupby(['Estado', 'Sigla'])['Concentracao']
        .mean()
        .to_frame()
    )

    grouped = grouped.unstack(level='Estado')
    grouped.columns = grouped.columns.droplevel(0)

    st.bar_chart(
        grouped,
        use_container_width=True,
        height=400,
        horizontal=True
    )

def apply_measure_unit(pollutant):
    if pollutant == 'CO':
        return (f"{pollutant} (ppm)")
    else:
        return (f"{pollutant} (µg/m³)")
