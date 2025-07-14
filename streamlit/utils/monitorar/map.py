import streamlit as st
import pydeck as pdk

def render_map(df):
    df = prepare_df(df)

    layer = pdk.Layer(
        "ScatterplotLayer",
        df,
        pickable=True,
        opacity=0.7,
        stroked=True,
        filled=True,
        radius_scale=6,
        radius_min_pixels=5,
        radius_max_pixels=5,
        line_width_min_pixels=1,
        get_position="coordinates",
        get_fill_color=[0, 158, 96],
        get_line_color=[0, 0, 0],
    )

    view_state = pdk.ViewState(latitude=-23, longitude=-50, zoom=3.5, bearing=0, pitch=0)

    html_tooltip = """
        <div style="
            background-color: rgba(255, 255, 255, 0.9); 
            border: 1px solid #d1d1d1;
            border-radius: 8px; 
            padding: 12px; 
            color: #333; 
            font-family: Arial, sans-serif;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            max-width: 300px;
        ">
            <div style="font-size: 16px; font-weight: bold; margin-bottom: 5px; color: #0050ff;">
                {nome_estacao}
            </div>
            
            <div style="margin-bottom: 10px; font-size: 13px;">
                {nome_municipio} - {estado}
            </div>

            <hr style="border: none; border-top: 1px solid #eee; margin: 10px 0;">
        </div>
        """

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip={
            "html": html_tooltip,
            "style": {
            # Remove a seta e o fundo padrão do pydeck
            "backgroundColor": None,
            "border": None,
        }
        },
    )

    r.picking_radius = 100

    st.pydeck_chart(r)

def prepare_df(df):
    df = df.rename(columns={
        "Nome do Município": 'nome_municipio',
        "Estado": 'estado',
        "Nome da Estação": 'nome_estacao'
    })
    df['Latitude'] = df['Latitude'].str.replace(',','.').astype(float)
    df['Longitude'] = df['Longitude'].str.replace(',','.').astype(float)
    df['coordinates'] = df[['Longitude', 'Latitude']].values.tolist()
    return df
