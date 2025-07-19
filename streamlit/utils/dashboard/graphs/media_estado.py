import streamlit as st

from utils.execute_query import select

def media_estado(filters):
    cols = [
        'Estado', 'Sigla', 'Concentracao'
    ]
    # df = get_measurements(filters=filters, cols=cols)
    df = select('mart_health_vs_air_quality', cols=['state_code', 'pollutant_code', 'monthly_avg_pollution'], filters=filters)

    df['Sigla'] = df['Sigla'].apply(apply_measure_unit)
    
    grouped = (
        df
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
