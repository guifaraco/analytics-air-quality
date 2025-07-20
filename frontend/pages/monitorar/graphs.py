import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

from utils.monitorar.graph_queries import query_big_numbers, query_media_mensal

def big_numbers(filters):
    metrics = query_big_numbers(filters)
    
    rows = list(metrics.itertuples(index=False))
    for i in range(0, len(rows), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(rows):
                row = rows[i + j]
                pc = row.pollutant_code
                sc = row.state_code
                ap = round(row.avg_pollution, 2)
                with cols[j].container(border=True):
                    st.header(pc)

                    st.metric(
                        label=f"**Estado com Maior média de Concentração**",
                        value=sc
                    )

                    st.metric(
                        label=f"**Concentração Média do Poluente**",
                        value=f"{ap:.2f}"
                    )




def media_mensal(filters):
    df = query_media_mensal(filters)

    fig = px.line(
        df,
        x='month',
        y='monthly_avg_pollution',
        color='pollutant_code',
        markers=True,
        labels={
            "month": "Mês",
            "monthly_avg_pollution": "Concentração Média",
            "pollutant_code": "Poluente"
        },
        title="Média Mensal de Poluição por Poluente",
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def media_estado(filters):
    cols = [
        'Estado', 'pollutant_code', 'Concentracao'
    ]
    # df = get_measurements(filters=filters, cols=cols)
    df = select('mart_health_vs_air_quality', cols=['state_code', 'pollutant_code', 'monthly_avg_pollution'], filters=filters)

    df['pollutant_code'] = df['pollutant_code'].apply(apply_measure_unit)
    
    grouped = (
        df
        .groupby(['Estado', 'pollutant_code'])['Concentracao']
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

def grafico_duplo(df):
    # Cria a 'tela' (Figure) e o primeiro eixo (Axes) explicitamente.
    fig, ax1 = plt.subplots(figsize=(12, 7))

    # Desenha o gráfico de barras no primeiro eixo (ax1).
    sns.barplot(data=df, x='month', y='total_health_cases', color='lightgray', 
                alpha=0.7, label='Casos de Saúde', errorbar=None, ax=ax1)
    ax1.set_ylabel('Total de Casos de Saúde', color='gray')
    ax1.tick_params(axis='y', labelcolor='gray')
    ax1.set_xlabel('Mês')

    # Cria o segundo eixo (ax2) que compartilha o eixo X com o primeiro.
    ax2 = ax1.twinx()

    # Desenha o gráfico de linhas no segundo eixo (ax2).
    sns.lineplot(data=df, x='month', y='monthly_avg_pollution', hue='pollutant_code', 
                marker='o', errorbar=None, ax=ax2)
    ax2.set_ylabel('Concentração Média de Poluentes')

    # Ajustes finais de layout e legenda
    fig.suptitle('Casos de Saúde vs. Níveis de Poluição', fontsize=16)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    ax1.legend(loc='upper left')
    ax2.legend(title='Poluente', loc='upper right')

    # Usa st.pyplot() para renderizar a figura no Streamlit.
    st.pyplot(fig)

def render_map(filters):

    stations_df = get_stations(filters=filters)
    datasus_df = select('silver_srag_cases', filters)

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