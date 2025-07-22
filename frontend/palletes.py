import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# --------------------------------------------------------------------------
# DICIONÁRIO 1: PALETAS PARA GRÁFICOS (CORES DISTINTAS)
# Mantivemos a paleta que você forneceu para ser usada em gráficos de barras, linhas, pizza, etc.
# --------------------------------------------------------------------------
CHART_PALETTES = {
    # Paleta principal, projetada para ser universalmente legível e a melhor escolha padrão.
    'inclusive_standard': [
        '#A9D6E5',  # Azul Gelo
        '#61A5C2',  # Azul Aço Claro
        '#2C7DA0',  # Azul Petróleo
        '#014F86',  # Azul Mar
        '#012A4A'   # Azul Meia-noite
    ],
    # Otimizada para Deuteranopia/Protanopia (evita o eixo verde-vermelho).
    'for_deuteranopia_protanopia': [
        '#3D5A80',  # Azul Aço
        '#EE9B00',  # Âmbar
        '#98C1D9',  # Azul Claro
        '#293241',  # Azul Marinho Escuro
        '#7A7A7A'   # Cinza
    ],
    # Otimizada para Tritanopia (evita o eixo azul-amarelo).
    'for_tritanopia': [
        '#D62728',  # Vermelho
        '#2CA02C',  # Verde
        '#17BECF',  # Ciano
        '#8C564B',  # Marrom
        '#4B0082'   # Índigo
    ],
    # Para Acromatopsia, a paleta de cinzas funciona bem para ambos os casos.
    'for_achromatopsia': [
        '#F0F0F0', '#BDBDBD', '#757575', '#424242', '#000000'
    ]
}

# --------------------------------------------------------------------------
# DICIONÁRIO 2: PALETAS PARA MAPAS (GRADIENTE DO BRANCO A UMA COR)
# Novas paletas, onde cada uma é um gradiente do branco a uma cor de alto contraste.
# --------------------------------------------------------------------------
MAP_PALETTES = {
    # Padrão: Branco para um azul escuro de alta legibilidade.
    'inclusive_standard': ['#FFFFFF', '#014F86'],

    # Deuteranopia/Protanopia: Branco para Âmbar/Laranja, cor segura e de alto contraste.
    'for_deuteranopia_protanopia': ['#FFFFFF', '#EE9B00'],

    # Tritanopia: Branco para Vermelho, cor segura para esta condição e de alto contraste.
    'for_tritanopia': ['#FFFFFF', '#D62728'],
    
    # Acromatopsia: Branco para Preto, o gradiente de cinza de maior contraste possível.
    'for_achromatopsia': ['#FFFFFF', '#000000']
}


# --------------------------------------------------------------------------
# FUNÇÃO ATUALIZADA PARA APLICAR AMBAS AS PALETAS
# --------------------------------------------------------------------------
def apply_palette(color_vision_deficiency: str):
    """
    Aplica um tema global que define paletas separadas para gráficos e para mapas.
    """
    # Define a chave padrão caso uma inválida seja passada
    key = color_vision_deficiency if color_vision_deficiency in CHART_PALETTES else 'inclusive_standard'
    
    # Busca a paleta correspondente em cada dicionário
    chart_palette = CHART_PALETTES[key]
    map_palette = MAP_PALETTES[key]

    # Cria um novo objeto de template para aplicar as configurações
    custom_theme = pio.templates["plotly_white"]
    
    # 1. Aplica a paleta de GRÁFICOS (cores distintas) ao 'colorway'
    custom_theme.layout.colorway = chart_palette

    # 2. Aplica a paleta de MAPAS (gradiente) ao 'colorscale' padrão dos coropléticos
    custom_theme.data.choropleth = [go.Choropleth(colorscale=map_palette)]

    # Define o novo tema como padrão global para todos os gráficos
    pio.templates.default = custom_theme

def render_select_pallete():
    palette_options = {
        "Padrão": "inclusive_standard",
        "Deuteranopia/Protanopia": "for_deuteranopia_protanopia",
        "Tritanopia": "for_tritanopia",
        "Acromatopsia (tons de cinza)": "for_achromatopsia"
    }

    # Cria um selectbox para a seleção do grau de daltonismo
    selected_vision_label = st.sidebar.selectbox(
        "Acessibilidade",
        options=list(palette_options.keys())
    )

    # Busca a chave correta para a paleta selecionada pelo usuário
    selected_vision_key = palette_options[selected_vision_label]

    # Aplica a paleta selecionada
    apply_palette(selected_vision_key)