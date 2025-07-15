import pandas as pd
import os

def extract_from_csv(path: str, encoding: str="utf8") -> pd.DataFrame:
    """
        Extrai os dados de todos os CSVs (Precisa conter as mesmas colunas) dentro do caminho do diretório informado ou extrai os dados do caminho do CSV informado. Após a extração dos dados é feita a conversão em DataFrame.
        Será retornado um DataFrame.
    """
    try:
        abs_workspace_path = os.path.abspath(".")
        
        # Checa se o caminho passado existe
        if not os.path.exists(path):
            raise Exception("O caminho passado não existe.")
        
        abs_path = os.path.abspath(path)

        # Checa se o caminho passado está dentro do diretório do projeto
        if not abs_path.startswith(abs_workspace_path):
            raise Exception("Caminho inválido, o caminho deve estar dentro da raiz do projeto.")

        # Checa se o caminho passado não é um diretório nem um arquivo .csv 
        if not (os.path.isdir(path) or path.lower().endswith(".csv")):
            raise Exception("Caminho inválido, o caminho deve ser de um diretório ou um arquivo csv.")
        
        # Checa se é um diretório
        if os.path.isdir(abs_path):
            # Filtra os arquivos dentro do diretório, e seleciona apenas os .csv
            csv_files = filter(lambda x: x.lower().endswith(".csv"), os.listdir(abs_path))
            if not csv_files:
                raise Exception("Não foi encontrado nenhum arquivo CSV dentro do diretório informado.")
            df_list = []
            # Adiciona na lista o Dataframe
            for csv in csv_files:
                csv_path = os.path.join(abs_path, csv)

                df_csv = pd.read_csv(csv_path, encoding=encoding, sep=';', decimal=',', low_memory=False)
                df_list.append(df_csv)
            
            # Concatena os Dataframes em um só
            return pd.concat(df_list, axis=0)
        
        df_csv = pd.read_csv(abs_path, encoding=encoding, sep=";", decimal=",", low_memory=False)
        return df_csv
        
    except Exception as e:
        raise e
