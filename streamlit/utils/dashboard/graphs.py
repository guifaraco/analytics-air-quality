import streamlit as st
import pydeck as pdk
import matplotlib.pyplot as plt
import pandas as pd

from .tools import join_df

from utils.datasus import get_datasus
from utils.monitorar import get_monitors, get_stations

def render_map(filters):
    stations_df = get_stations(filters=filters)
    datasus_df = get_datasus(filters=filters)

    df = join_df(stations_df, datasus_df)

    found = len(df)

    df['coordinates'] = df[['Longitude', 'Latitude']].values.tolist()
    df = df[['ID_MN_RESI', 'coordinates']]
    df = df.rename(columns={"ID_MN_RESI":"municipio"})
    df = df.groupby('municipio').agg(
        coordinates=('coordinates', 'first'),
        count=('municipio', 'count')
    ).reset_index()

    layer = pdk.Layer(
        'ColumnLayer',
        data=df,
        get_position='coordinates',
        get_elevation='count',
        elevation_scale=10,
        radius=5000,
        get_fill_color=[255, 140, 0, 150],
        pickable=True,
        extruded=True,
    )

    view_state = pdk.ViewState(latitude=-23, longitude=-50, zoom=4, bearing=-45, pitch=45)

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{municipio} \nCount: {count}"},
    )

    st.pydeck_chart(r)

    return found

def evolucao_mensal(filters):
    cols=[
        'Nome do Município', 'Estado', 'Nome da Estação', 'Sigla', 'Concentracao', 'iqar', 'Data'
    ]
    monitors_df = get_monitors(filters=filters, cols=cols)

    monitors_df.rename(columns = {
        "Nome do Município": "Nome_Municipio",
        "Nome da Estação": "Nome_Estacao"
    }, inplace=True)

    #### 2. Filtrar Monitoramentos que possuem ``iqar``
    monitors_df['iqar'] = pd.to_numeric(monitors_df['iqar'], errors='coerce')

    monitors_df = monitors_df.dropna(subset=['iqar'])

    ### 1.2 DataSUS
    cols = [
        'CO_MUN_RES'
    ]
        
    datasus_df = get_datasus(filters=filters, cols=cols)

    municipios_code = datasus_df.rename(columns={
        "CO_MUN_RES": "Codigo_IBGE"
    })

    municipios_code.dropna(subset=['Codigo_IBGE'], inplace=True)
    municipios_code["Codigo_IBGE"] = municipios_code["Codigo_IBGE"].astype(int)
    municipios_code.drop_duplicates(subset=['Codigo_IBGE'])
    municipios_code = municipios_code['Codigo_IBGE']

    ### 2. Plotar o gráfico
    monitors_df['Data'] = pd.to_datetime(monitors_df['Data'])
    monitors_df['Mes'] = monitors_df['Data'].dt.month_name()
    monitors_df.sort_values(by='Data', inplace=True)

    # Agrupando com sort=False para manter a ordem cronológica
    month_count = monitors_df.groupby('Mes', sort=False).size()

    # --- Plotando com st.line_chart ---
    st.subheader("Gráfico de Linha Nativo do Streamlit")

    # É só isso! Apenas uma linha de código.
    st.line_chart(month_count)
    