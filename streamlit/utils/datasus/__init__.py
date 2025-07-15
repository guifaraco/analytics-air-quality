import streamlit as st
import pandas as pd

def render_datasus():
    st.header("DataSUS")
    cols = [
        'DT_SIN_PRI', 'CS_SEXO', 'DT_NASC', 'CS_GESTANT', 'CS_RACA', 'CS_ESCOL_N', 'SG_UF', 'ID_MN_RESI', 'CO_MUN_RES', 'CLASSI_FIN',
        'CRITERIO', 'EVOLUCAO', 'DT_EVOLUCA'
    ]
    
    df = get_df(cols=cols)

    st.subheader("Casos")
    st.dataframe(df.head(10))
    st.write(f"Casos encontrados: {len(df)}")

    return df

def get_df(cols=None):
    df = pd.read_csv("data/data_sus/INFLUD22-26-06-2025.csv", sep=";", usecols=cols)
    return df