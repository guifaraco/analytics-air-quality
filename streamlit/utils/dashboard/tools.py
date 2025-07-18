import pandas as pd
import streamlit as st

def join_df(map_df: pd.DataFrame, data_df: pd.DataFrame) -> pd.DataFrame:
    # Faz uma cópia para não modificar o DataFrame original fora da função
    coords = map_df.copy()

    # Renomeia, normaliza a chave IBGE (7->6 dígitos) e converte tipos em uma única cadeia
    coords = coords.rename(columns={"Código IBGE do Município": "Código IBGE"})

    coords['Latitude'] = coords['Latitude'].str.replace(',','.')
    coords['Longitude'] = coords['Longitude'].str.replace(',','.')

    # Converte lat/lon para numérico, tratando erros
    coords['Latitude'] = pd.to_numeric(coords['Latitude'], errors='coerce')
    coords['Longitude'] = pd.to_numeric(coords['Longitude'], errors='coerce')
    coords.dropna(subset=['Latitude', 'Longitude', 'Código IBGE'], inplace=True)
    
    # A otimização principal: cria um DataFrame com UMA coordenada média por IBGE
    lookup_coordenadas = coords.groupby('Código IBGE', as_index=False).agg(
        Latitude=('Latitude', 'mean'),
        Longitude=('Longitude', 'mean')
    )

    # --- 2. Preparar o DataFrame de dados principal ---
    data = data_df.copy()
    data = data.rename(columns={"CO_MUN_RES": "Código IBGE"})
    data.dropna(subset=['Código IBGE'], inplace=True)
    data['Código IBGE'] = data['Código IBGE'].astype(int)

    # --- 3. Realizar o Merge (Junção) ---
    # Usa 'inner' join para retornar data APENAS onde coords também está disponível
    df_final = pd.merge(
        left=data,
        right=lookup_coordenadas,
        on='Código IBGE',
        how='inner'
    )
    
    return df_final