import streamlit as st
import pandas as pd
import altair as alt
from utils.execute_query import select, execute_query

def evolucao_mensal(filters):
    df = execute_query('')
    # df = select('mart_health_vs_air_quality', cols=['year_month', 'state_code', 'pollutant_code', 'monthly_avg_pollution'], filters=filters)
    st.write(df.head(10))
    # df['year_month'] = pd.to_datetime(df['year_month'])
    # df['month'] = df['year_month'].dt.month_name(locale='pt_BR')
    # df.sort_values(by='year_month', inplace=True)


    # # Captura a ordem dos meses
    # ordem_cronologica = list(df['Mes'].unique())
    
    # grouped = (
    #     df
    #     .groupby(['Sigla', 'Mes'])['Concentracao']
    #     .mean()
    #     .reset_index()
    # )

    # # Cria a seleção e o gráfico Altair com todos os seus requisitos
    # selecao_legenda = alt.selection_multi(fields=['Sigla'], bind='legend')

    # chart = alt.Chart(grouped).mark_line(point=True).encode(
    #     x=alt.X('Mes', sort=ordem_cronologica, title='Mês'),
    #     y=alt.Y('Concentracao', title='Concentração Média'),
    #     color=alt.Color('Sigla', title='Métrica'),
    #     opacity=alt.condition(selecao_legenda, alt.value(1.0), alt.value(0.2)),
    #     tooltip=[
    #         alt.Tooltip('Mes', title='Período'),
    #         alt.Tooltip('Sigla', title='Métrica'),
    #         alt.Tooltip('Concentracao', title='Valor Médio', format='.2f')
    #     ]
    # ).add_selection(
    #     selecao_legenda
    # ).properties(
    #     title='Análise Comparativa Mensal Interativa'
    # ).interactive()

    # # 4. Remove o st.line_chart e exibe o novo gráfico Altair
    # st.altair_chart(chart, use_container_width=True)