import streamlit as st
import plotly.express as px
import pydeck as pdk
import pandas as pd
import plotly.graph_objects as go

from utils.datasus.graph_queries import query_big_numbers_primeira_linha, query_big_numbers_segunda_linha
from utils.datasus.graph_queries import query_casos_mensais, query_fatores_risco
from utils.datasus.graph_queries import query_casos_por_faixa_etaria, query_casos_por_srag_e_evolucao
from utils.datasus.graph_queries import query_casos_map, query_evolucao_mensal_por_srag, query_quantidade_total_casos_por_srag
from utils.datasus.graph_queries import query_casos_por_sintomas, evolucao_mensal_por_desfecho
from frontend.utils import get_month_name

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

    df_filtrado = df.copy()

    # Filtrar dados
    if 'state_code' in filters and filters['state_code'] != "TODOS":
        df_filtrado = df_filtrado[df_filtrado['state_code'] == filters['state_code']]

    # Agrupa por mês SEMPRE, independente do filtro
    df_agrupado = df_filtrado.groupby('month', as_index=False)['sum'].sum()

    # Gráfico
    fig = px.area(
        df_agrupado,
        x='month',
        y='sum',
        markers=True,
        labels={"month": "Mês", "sum": "Total de Casos"},
        title=f"Total de Casos Mensais {'(Todos os Estados)' if filters['state_code'] == 'TODOS' else f'(Estado: {filters['state_code']})'}",
        text='sum'
    )

    # Personalizações
    fig.update_traces(
        line=dict(width=3),
        texttemplate='%{text:.0f}',
        textposition="top center",
        textfont_size=12,
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

def casos_map():
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
        'CURA': '#5CB860',  # Verde
        'OBITO': "#F54747",  # Vermelho  # Laranja
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
        title='<b>Distribuição de Casos de SRAG por Desfecho</b>',
        barmode='stack',
        xaxis_title='Número de Casos',
        yaxis_title='Tipo de SRAG',
        hovermode='y unified',
        height=500,
        showlegend=True,
        margin=dict(l=100, r=150)  # Margem direita maior para acomodar os totais
    )

    st.plotly_chart(fig, use_container_width=True)

def evolucao_mensal_desfecho():
    df = query_evolucao_mensal_por_srag()

    df = get_month_name(df, coluna_mes='month')

    fig = px.line(
        df,
        x='month',
        y='sum',
        markers=True,
        labels={
            "month": "Mês",
            "sum": "Total de Casos",
        },
        color='final_classification',
        title="Total de casos Mensal"
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
        showlegend=True
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)    

def casos_por_fator_risco():
    df = query_fatores_risco()

    df['total_cases'] = df['total_non_icu_cases'] + df['total_icu_cases']
    df = df.sort_values('total_cases', ascending=True)

    # Criar gráfico
    fig = go.Figure()

    # Barra de casos não-ICU com valores
    fig.add_trace(go.Bar(
        y=df['risk_factor_name'],
        x=df['total_non_icu_cases'],
        name='Casos não-UTI',
        orientation='h',
        hovertemplate='<b>%{y}</b><br>Casos não-ICU: %{x:,}<extra></extra>',
        text=[f'{x:,}' for x in df['total_non_icu_cases']],  # Texto para mostrar valores
        textposition='inside',
        insidetextanchor='middle'
    ))

    # Barra de casos ICU com valores
    fig.add_trace(go.Bar(
        y=df['risk_factor_name'],
        x=df['total_icu_cases'],
        name='Casos UTI',
        orientation='h',
        hovertemplate='<b>%{y}</b><br>Casos ICU: %{x:,}<extra></extra>',
        base=df['total_non_icu_cases'],
        text=[f'{x:,}' for x in df['total_icu_cases']],  # Texto para mostrar valores
        textposition='inside',
        insidetextanchor='middle'
    ))

    # Adicionar totais no final de cada barra
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row['total_cases'],
            y=row['risk_factor_name'],
            text=f"<b>{row['total_cases']:,}</b>",
            showarrow=False,
            xanchor='left',
            xshift=10,
            font=dict(size=10, color='black')
        )

    # Layout do gráfico
    fig.update_layout(
        title='Distribuição de Casos por Fator de Risco',
        xaxis_title='Número de Casos',
        yaxis_title='Fatores de Risco',
        barmode='stack',
        height=600,
        width=800,
        hovermode='y unified',
        plot_bgcolor='white',
        uniformtext_minsize=8,  # Tamanho mínimo do texto dentro das barras
        uniformtext_mode='hide'  # Esconde texto que não couber
    )

    # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)

def casos_por_sintomas():
    df = query_casos_por_sintomas()

    df['total_cases'] = df['total_non_icu_cases'] + df['total_icu_cases']
    df = df.sort_values('total_cases', ascending=True)

    # Criar gráfico
    fig = go.Figure()

    # Barra de casos não-ICU com valores
    fig.add_trace(go.Bar(
        y=df['symptom_name'],
        x=df['total_non_icu_cases'],
        name='Casos não-UTI',
        orientation='h',
        hovertemplate='<b>%{y}</b><br>Casos não-ICU: %{x:,}<extra></extra>',
        text=[f'{x:,}' for x in df['total_non_icu_cases']],  # Texto para mostrar valores
        textposition='inside',
        insidetextanchor='middle'
    ))

    # Barra de casos ICU com valores
    fig.add_trace(go.Bar(
        y=df['symptom_name'],
        x=df['total_icu_cases'],
        name='Casos UTI',
        orientation='h',
        hovertemplate='<b>%{y}</b><br>Casos UTI: %{x:,}<extra></extra>',
        base=df['total_non_icu_cases'],
        text=[f'{x:,}' for x in df['total_icu_cases']],  # Texto para mostrar valores
        textposition='inside',
        insidetextanchor='middle'
    ))

    # Adicionar totais no final de cada barra
    for i, row in df.iterrows():
        fig.add_annotation(
            x=row['total_cases'],
            y=row['symptom_name'],
            text=f"<b>{row['total_cases']:,}</b>",
            showarrow=False,
            xanchor='left',
            xshift=10,
            font=dict(size=10, color='black')
        )

    # Layout do gráfico
    fig.update_layout(
        title='Distribuição de Casos por Sintomas',
        xaxis_title='Número de Casos',
        yaxis_title='Sintomas',
        barmode='stack',
        height=600,
        width=800,
        hovermode='y unified',
        plot_bgcolor='white',
        uniformtext_minsize=8,  # Tamanho mínimo do texto dentro das barras
        uniformtext_mode='hide'  # Esconde texto que não couber
    )

    # Exibir no Streamlit
    st.plotly_chart(fig, use_container_width=True)

def faixa_etaria():
    df = query_casos_por_faixa_etaria()

    # Paleta de cores pastéis
    cores_pasteis = {
        'MASCULINO': '#89CFF0',  # Azul bebê pastel
        'FEMININO': '#FFB6C1'    # Rosa claro pastel
    }


    # Criando o gráfico
    fig = go.Figure()

    # Adicionando barras para cada gênero
    for genero in df['genero'].unique():
        df_genero = df[df['genero'] == genero]
        fig.add_trace(go.Bar(
            x=df_genero['faixa_etaria'],
            y=df_genero['numero_total_casos'],
            name=genero,
            marker_color=cores_pasteis[genero],
            text=df_genero['numero_total_casos'],
            texttemplate='%{text:,}',
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>%{fullData.name}: %{y:,} casos<extra></extra>'
        ))

    # Personalizando o layout
    fig.update_layout(
        title='Distribuição de Casos por Gênero e Faixa Etária',
        xaxis_title='Faixa Etária',
        yaxis_title='Número Total de Casos',
        barmode='group',
        plot_bgcolor='white',
        height=600,
        hovermode='x unified',
        yaxis=dict(
            tickformat=',.0f',
            separatethousands=True
        ),
        legend=dict(
            title='Gênero',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )
    )

    # Exibindo no Streamlit
    st.plotly_chart(fig, use_container_width=True)

def evolucao_mensal_por_srag(filters):
    df = query_evolucao_mensal_por_srag()

    df = get_month_name(df, coluna_mes='month')


    # Inicializa o DataFrame filtrado
    df_filtrado = df.copy()

    # Aplica filtros
    if filters:
        # Filtro por estado
        # if 'state_code' in filters and filters['state_code'] != "TODOS":
        #     df_filtrado = df_filtrado[df_filtrado['state_code'] == filters['state_code']]
        
        # Filtro por SRAG
        if 'final_classification' in filters:
            if filters['final_classification'] != "TODAS":
                df_filtrado = df_filtrado[df_filtrado['final_classification'] == filters['final_classification']]

    # Verifica se há dados
    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
    else:
        # Lógica diferente para "TODAS" vs SRAG específica
        if 'final_classification' in filters and filters['final_classification'] != "TODAS":
            # Caso 1: SRAG específica selecionada - gráfico simples
            df_agrupado = df_filtrado.groupby('month', as_index=False)['sum'].sum()
            
            fig = px.line(
                df_agrupado,
                x='month',
                y='sum',
                markers=True,
                labels={
                    "month": "Mês",
                    "sum": "Total de Casos"
                },
                title=f"Casos de {filters['final_classification']} por Mês" #+ 
                    # (f" - Estado: {filters['state_code']}" if 'state_code' in filters and filters['state_code'] != 'TODOS' else '')
            )
            
            # Personalização para gráfico único
            fig.update_traces(
                line=dict(width=3, color='#1f77b4'),
                marker=dict(size=8),
                text=df_agrupado['sum'],
                textposition="top center"
            )
        else:
            # Caso 2: "TODAS" as SRAGs - gráfico com múltiplas linhas coloridas
            df_agrupado = df_filtrado.groupby(['month', 'final_classification'], as_index=False)['sum'].sum()
            
            fig = px.line(
                df_agrupado,
                x='month',
                y='sum',
                color='final_classification',
                markers=True,
                labels={
                    "month": "Mês",
                    "sum": "Total de Casos",
                    "final_classification": "Tipo de SRAG"
                },
                title="Distribuição Mensal de Casos por Tipo de SRAG" # + 
                    # (f" - Estado: {filters['state_code']}" if 'state_code' in filters and filters['state_code'] != 'TODOS' else '')
            )
            
            # Personalização para gráfico múltiplo
            fig.update_traces(
                line=dict(width=2.5),
                marker=dict(size=6),
                textposition="top center"
            )
            fig.update_layout(legend_title_text='Classificação SRAG')

        # Configurações comuns a ambos os casos
        fig.update_traces(
            texttemplate='%{text:.0f}',
            textfont_size=10,
            showlegend=True
        )
        fig.update_layout(hovermode='x unified')
        
        st.plotly_chart(fig, use_container_width=True)  
    
def evolucao_mensal_desfecho():
    df = evolucao_mensal_por_desfecho()

    df = get_month_name(df, coluna_mes='month')


    fig = px.line(
        df,
        x='month',
        y='sum',
        markers=True,
        labels={
            "month": "Mês",
            "sum": "Total de Casos",
        },
        color='case_outcome',
        title="Distribuição Mensal por Desfecho"
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
        showlegend=True
    )

    # Usa st.plotly_chart para exibir o gráfico interativo
    st.plotly_chart(fig, use_container_width=True)    
