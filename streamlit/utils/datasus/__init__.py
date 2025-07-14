import streamlit as st
import pandas as pd
from .map import render_map
from utils.monitorar import get_df as get_ma_df

def render_datasus(ma_df):
    st.header("DataSUS")
    cols = [
        'DT_SIN_PRI', 'CS_SEXO', 'DT_NASC', 'CS_GESTANT', 'CS_RACA', 'CS_ESCOL_N', 'SG_UF', 'ID_MN_RESI', 'CO_MUN_RES', 'CLASSI_FIN',
        'CRITERIO', 'EVOLUCAO', 'DT_EVOLUCA'
    ]
    
    df = get_df(cols=cols)
    st.write(ma_df)

    st.subheader("Casos")
    st.dataframe(df.head(10))

    # render_map(df)

def get_df(cols=None):
    df = pd.read_csv("data/data_sus/INFLUD22-26-06-2025.csv", sep=";", usecols=cols)
    return df