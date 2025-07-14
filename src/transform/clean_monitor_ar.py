import pandas as pd
from src.extract import from_csv
def monitoring_stations_light_transform(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # Colunas importantes
        cols_names = ['ï»¿CÃ³digo IBGE do MunicÃ­pio', 'Nome do MunicÃ­pio', 'Estado',
        'ID da EstaÃ§Ã£o', 'Nome da EstaÃ§Ã£o', 'Latitude', 'Longitude']

        df_filtered = df[cols_names].copy()

        new_names = ["cod_mun", "nome_municipio", "estado", "source_id_estacao", "nome_estacao", "latitude", "longitude"]
        # Criação de um dicionário com o nome atual da coluna e o novo nome
        dict = {}
        for i, j in zip(cols_names, new_names):
            dict[i] = j

        # Renomeando as colunas
        df_filtered.rename(dict, axis=1, inplace=True)
        return df_filtered
    except Exception as e:
        raise e

def air_quality_measurements_light_transform(df: pd.DataFrame) -> pd.DataFrame:
    try:
        # Colunas importantes
        cols_names = ["Nome do Município", "Estado", "Nome da Estação", "Item_monitorado", "Sigla", "Concentracao", "iqar", "Data"]
        df_filtered = df[cols_names].copy()
        new_names = ["nome_municipio", "estado", "nome_estacao", "poluente_descricao", "poluente_sigla", "concentracao", "iqar", "data"]
        # Criação de um dicionário com o nome atual da coluna e o novo nome
        dict = {}
        for i, j in zip(cols_names, new_names):
            dict[i] = j

        # Renomeando as colunas
        df_filtered.rename(dict, axis=1, inplace=True)
        return df_filtered
    except Exception as e:
        raise e


