import streamlit as st
import pydeck as pdk

from ..tools import join_df

from utils.datasus import get_datasus
from utils.monitorar import get_stations

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

