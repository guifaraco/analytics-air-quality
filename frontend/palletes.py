import streamlit as st
import plotly.io as pio

PALETTES = {
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
    'for_achromatopsia': [
        '#F0F0F0',  # Branco
        '#BDBDBD',  # Cinza Claro
        '#757575',  # Cinza Médio
        '#424242',  # Cinza Escuro
        '#000000',  # Preto
    ]
}

def apply_palette(color_vision_deficiency: str):
    # Fetch the corresponding color list from the master dictionary
    palette = PALETTES.get(color_vision_deficiency, PALETTES['inclusive_standard'])

    # Create a new template object to avoid modifying the base template
    custom_theme = pio.templates["plotly_white"]
    custom_theme.layout.colorway = palette

    # Set the new theme as the default for all subsequent charts
    pio.templates.default = custom_theme

def render_select_pallete():
    palette_options = {
        "Padrão": "inclusive_standard",
        "Deuteranopia/Protanopia": "for_deuteranopia_protanopia",
        "Tritanopia": "for_tritanopia",
        "Acromatopsia (tons de cinza)": "for_achromatopsia"
    }

    # Creates the radio button selector in the sidebar
    selected_vision_label = st.sidebar.selectbox(
        "Acessibilidade",
        options=list(palette_options.keys())
    )

    # Gets the key corresponding to the user's selection
    selected_vision_key = palette_options[selected_vision_label]

    # Applies the selected palette globally
    apply_palette(selected_vision_key)