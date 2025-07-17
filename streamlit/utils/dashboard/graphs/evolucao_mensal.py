import streamlit as st
import pandas as pd

from utils.datasus import get_datasus
from utils.monitorar import get_monitors, get_valid_ibge

def evolucao_mensal(filters):
    datasus_count = get_datasus_count(filters)
    monitors_mean = get_monitors_mean(filters)

    month_evo = pd.merge(
        left=datasus_count,
        right=monitors_mean,
        on='Mes',
        how='inner'
    )

    st.write(month_evo)
    st.write(month_evo.dtypes)

    st.line_chart(
        month_evo,
        y=['datasus_count', 'monitors_mean']
    )

def get_datasus_count(filters):
    cols = [
        'DT_SIN_PRI', 'CS_SEXO', 'SG_UF', 'ID_MN_RESI', 'CO_MUN_RES', 'CLASSI_FIN'
    ]
        
    df = get_datasus(filters=filters, cols=cols)

    df = df.rename(columns={
        'DT_SIN_PRI': "Data",
        'CS_SEXO':"Sexo", 
        'SG_UF': "Estado", 
        'ID_MN_RESI': "Municipio", 
        'CO_MUN_RES': "Codigo_IBGE",
        'CLASSI_FIN' : "Classificacao_Final"
    })
    
    df = filter_iqar(df, filters)

    ### 2. Plotar o gráfico
    df['Data'] = pd.to_datetime(df['Data'])
    df['Mes'] = df['Data'].dt.month_name(locale='pt_BR')
    df.sort_values(by='Data', inplace=True)

    # Agrupando com sort=False para manter a ordem cronológica
    datasus_count = df.groupby('Mes', sort=False).size()

    return datasus_count.to_frame('datasus_count')

def get_monitors_mean(filters):
    cols = [
        'Nome do Município', 'Estado', 'Sigla', 'iqar', 'Data'
    ]
        
    df = get_monitors(filters=filters, cols=cols)

    df = df.rename(columns={
        'Nome do Município': "Nome_Municipio"
    })

    ### 2. Plotar o gráfico
    df['Data'] = pd.to_datetime(df['Data'])
    df['Mes'] = df['Data'].dt.month_name(locale='pt_BR')
    df.sort_values(by='Data', inplace=True)

    # Agrupando com sort=False para manter a ordem cronológica
    monitors_mean = df.groupby('Mes', sort=False)['iqar'].mean()

    return monitors_mean.to_frame('monitors_mean')


def filter_iqar(df, filters):
    ibge_codes = get_valid_ibge(filters)

    ## 2. ``Filter`` entre Códigos IBGE no ``DataSUS`` e Métricas com ``iqar``
    df = df[df['Codigo_IBGE'].isin(list(ibge_codes))]

    return df

