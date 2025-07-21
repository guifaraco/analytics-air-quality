import streamlit as st
import plotly.express as px

from utils.monitorar.graph_queries import query_big_numbers, query_media_mensal

def big_numbers(filters):
    metrics = query_big_numbers(filters)

    emoji_map = {
        "CO": "🔥", "MP10": "🌫️", "MP2,5": "🌫️",
        "NO2": "🧪", "SO2": "🧪", "O3": "☁️"
    }

    rows = list(metrics.itertuples(index=False))
    for i in range(0, len(rows), 3):
        cols = st.columns(3, gap='medium')
        for j in range(3):
            if i + j < len(rows):
                row = rows[i + j]
                pol = row.pollutant_code
                uf = row.state_code
                unit = row.measurement_unit
                val = float(row.avg_pollution)
                icon = emoji_map.get(pol, "")

                with cols[j].container(border=True):
                    st.markdown(f"""
                        <div style="text-align:center; line-height:1.6; margin-bottom:20px">
                            <h3 style="margin-bottom:0;">{icon} {pol}</h3>
                            <p style="margin:0; font-size:15px; color:#888;">Estado mais impactado</p>
                            <h4 style="margin:0;">{uf}</h4>
                            <p style="margin:0; font-size:15px; color:#888;">Média registrada</p>
                            <h2 style="margin-top:0;">{val:.2f} {unit}</h2>
                        </div>
                    """, unsafe_allow_html=True)
        st.write('')

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