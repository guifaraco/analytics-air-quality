import streamlit as st
import plotly.express as px
import pydeck as pdk
import pandas as pd
import plotly.graph_objects as go

from utils.datasus.graph_queries import query_big_numbers_primeira_linha, query_big_numbers_segunda_linha
from utils.datasus.graph_queries import query_casos_mensais, query_fatores_risco
from utils.datasus.graph_queries import query_casos_por_faixa_etaria, query_casos_por_srag_e_evolucao
from utils.datasus.graph_queries import query_casos_map, query_evolucao_mensal_por_srag, query_quantidade_total_casos_por_srag
from utils.datasus.graph_queries import query_casos_por_sintomas
from frontend.utils import get_month_name

def df_melted(df, total_cases_col=None, filter_type=None):
    '''
    Retorna o DataFrame melted no modelo utilizado nos gráficos com duas colunas apenas.
    Permite filtrar entre casos totais e casos de UTI.
    
    Parâmetros:
        - df: DataFrame de entrada
        - total_cases_col: Nome da coluna que contém o total de casos (opcional)
        - filter_type: Tipo de filtro ('total' para casos totais, 'icu' para casos UTI)
    
    Colunas retornadas:
        - fator_risco
        - numero_total_casos
    '''
    # Filtra as colunas conforme o tipo especificado
    if filter_type == 'total':
        colunas_para_melt = [col for col in df.columns if col.startswith('total_cases')]
    elif filter_type == 'icu':
        colunas_para_melt = [col for col in df.columns if col.startswith('icu_cases')]
    else:
        # Se nenhum filtro for especificado, usa todas as colunas exceto a de total de casos
        colunas_para_melt = [col for col in df.columns if col != total_cases_col]
    
    # Realiza o melt
    df_melted = df.melt(
        value_vars=colunas_para_melt,
        var_name='fator_risco',
        value_name='numero_total_casos'
    ).sort_values(
        by='numero_total_casos',
        ascending=False
    )
    
    return df_melted


def big_numbers():
    first_row = query_big_numbers_primeira_linha()
    second_row = query_big_numbers_segunda_linha()

    rows_list = [{
        'Total de casos': first_row['total_cases'].sum(),
        'Taxa de Internação': f"{first_row['icu_percentage'].mean():.2f}%",
        'Taxa de Mortalidade': f"{first_row['death_percentage'].mean():.2f}%"
        },
        {
        'SRAG com maior número de casos': f"{second_row['top_classification_by_total_cases'].values[0]} <br> {second_row['max_total_cases'].values[0]} Casos",
        'SRAG com maior taxa de Internação': f"{second_row['top_classification_by_icu_rate'].values[0]} <br> {second_row['max_icu_rate'].values[0]}%",
        'SRAG com maior taxa de Mortalidade': f"{second_row['top_classification_by_death_rate'].values[0]} <br> {second_row['max_death_rate'].values[0]:.2f}%"
    }]

    for row_dict in rows_list:
        cols = st.columns(3, gap='small')
        col_index = 0
        for title, value in row_dict.items():
            with cols[col_index].container():
                render_big_number(title, value)
            col_index = (col_index + 1) % 3
        st.markdown('')

def render_big_number(title, value):
    value = str(value).replace('SRAG', '').replace('POR', '')
    st.markdown(
        f'''
            <div class='metric-datasus'>
                <p>{title}</p>
                <h4>{value}</h4>
            </div>
        ''',
        unsafe_allow_html=True
    )


def casos_mensais(filters):
    df = query_casos_mensais()

    df = get_month_name(df, coluna_mes='month')

    fig = px.area(
        df,
        x='month',
        y='sum',
        markers=True,
        labels={
            "month": "Mês",
            "sum": "Total de Casos",
        },
        title="Total de casos Mensal",
        text='sum'
    )

    # Personalizar a linha e marcadores
    fig.update_traces(
        line=dict(width=3),
        text=df['sum'],  # Valores que aparecem nos marcadores
        textposition="top center"
    )

    # Adicionar os valores em cima de cada ponto
    fig.update_traces(
        texttemplate='%{text:.0f}',
        textfont_size=12,
        showlegend=False
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def casos_map(filters):
    df = query_casos_map()

    df['numero_total_cases'] = pd.to_numeric(df['numero_total_cases'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')

    layer = pdk.Layer(
        'ColumnLayer',
        data=df,
        get_position=['longitude', 'latitude'],
        get_elevation='numero_total_cases',
        elevation_scale=10,
        radius=5000,
        get_fill_color=[255, 140, 0, 150],
        pickable=True,
        extruded=True,
    )

    view_state = pdk.ViewState(
        latitude=-23,
        longitude=-50,
        zoom=4,
        bearing=-45,
        pitch=45
    )

    # Tooltip com nome da cidade e número de casos
    tooltip = {
        "text": "Cidade: {city_name}\nCasos: {numero_total_cases}"
    }

    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip,
    )

    st.pydeck_chart(r)

def casos_mensais_por_srag():
    df = query_evolucao_mensal_por_srag()

    df = get_month_name(df, coluna_mes='month')

    fig = px.area(
        df,
        x='month',
        y='sum',
        color='final_classification',
        markers=True,
        labels={
            "month": "Mês",
            "sum": "Total de Casos",
            "final_classification": "SRAG"
        },
        title="Total de casos Mensal para cada SRAG",
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)

def grafico_pizza_casos_por_srag():
    df = query_quantidade_total_casos_por_srag()

    # Criar o gráfico de pizza com Plotly
    fig = px.pie(
        df,
        values='sum',
        names='srag',
        title='Distribuição de Casos SRAG por Classificação Final',
        labels={'srag': 'Classificação Final', 'sum': 'Total de Casos'},
    )

    # Melhorar a formatação (opcional)
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        hoverinfo='percent+value',
    )

    # Ajustar layout (opcional)
    fig.update_layout(
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        showlegend=True,
    )

    # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)

# query_casos_por_srag_e_evolucao
def casos_por_srag_evolucao():
    df = query_casos_por_srag_e_evolucao()

    # Cores para cada evolução
    cores = {
        'CURA': '#4CAF50',  # Verde
        'OBITO': '#F44336',  # Vermelho
        'OBITO POR OUTRAS CAUSAS': '#FF9800'  # Laranja
    }

    # Preparar dados para o gráfico empilhado
    df_pivot = df.pivot(index='srag', columns='evolucao', values='numero_total_casos').fillna(0)

    # Ordenar por total de casos (opcional)
    df_pivot = df_pivot.sort_values(by='CURA', ascending=False)

        # Calcular totais por SRAG (soma de CURA + OBITO)
    df_pivot['TOTAL'] = df_pivot['CURA'] + df_pivot['OBITO']

    # Ordenar por total de casos (opcional)
    df_pivot = df_pivot.sort_values(by='TOTAL', ascending=False)

    # Criar o gráfico de barras empilhadas HORIZONTAIS
    fig = go.Figure()

    # Adicionar cada evolução como uma barra empilhada
    for evol in ['CURA', 'OBITO']:
        fig.add_trace(go.Bar(
            y=df_pivot.index,
            x=df_pivot[evol],
            name=evol,
            orientation='h',
            marker_color=cores[evol],
            text=df_pivot[evol].apply(lambda x: f'{x:,.0f}' if x > 0 else ''),  # Formata com separador de milhar
            textposition='inside',
            insidetextanchor='middle',
            textfont=dict(color='white', size=12),  # Texto branco para contraste
            hovertemplate='<b>%{y}</b><br>' + evol + ': %{x:,.0f} casos<extra></extra>'
        ))

    # Adicionar rótulos com o TOTAL no final de cada barra
    fig.add_trace(go.Scatter(
        x=df_pivot['TOTAL'] * 1.05,  # Posiciona o texto 5% além do final da barra
        y=df_pivot.index,
        mode='text',
        textfont=dict(color='black', size=12),
        showlegend=False,
        hoverinfo='skip'
    ))

    # Ajustar layout
    fig.update_layout(
        title='<b>Distribuição de Casos de SRAG por Evolução</b>',
        barmode='stack',
        xaxis_title='Número de Casos',
        yaxis_title='Tipo de SRAG',
        hovermode='y unified',
        height=500,
        showlegend=True,
        margin=dict(l=100, r=150)  # Margem direita maior para acomodar os totais
    )

    st.plotly_chart(fig, use_container_width=True)

def casos_por_srag_evolucao_pizza():
    df = query_casos_por_srag_e_evolucao()

    # Criar o gráfico de pizza com Plotly
    fig = px.pie(df, 
                values='numero_total_casos', 
                names='evolucao',
                title= 'Distribuição de Casos SRAG por Evolução/Desfecho',
                hole=0.3,  # Opcional: transforma em donut chart
                color_discrete_sequence=['#4CAF50', '#F44336', '#FF9800'])  # Mesmas cores do gráfico anterior

    # Melhorar a formatação
    fig.update_traces(textposition='inside',
                    textinfo='percent+label',
                    insidetextfont=dict(color='white', size=12),
                    hovertemplate='<b>%{label}</b><br>Casos: %{value:,.0f}<br>Percentual: %{percent}')

    # Ajustar layout
    fig.update_layout(
        uniformtext_minsize=12,
        uniformtext_mode='hide',
        legend_title_text='Evolução',
        title_font=dict(size=20),
        hoverlabel=dict(font_size=14)
    )

    st.plotly_chart(fig, use_container_width=True)

# def casos_por_fator_risco():
#     df = query_fatores_risco()

#     st.dataframe(df)

def casos_por_sintomas():
    df = df_melted(query_casos_por_sintomas(), filter_type='total')

    st.write(df)

