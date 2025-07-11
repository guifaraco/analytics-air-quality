import os
import psycopg
import subprocess
from dotenv import load_dotenv
from src.extract import from_csv
# Executa a função para carregar as variáveis do arquivo .env no ambiente
load_dotenv()

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados."""
    try:
        conn = psycopg.connect(
            host="localhost",
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT")
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        raise e

def run_dbt_transformations():
    """Executa os comandos do dbt localmente."""
    print("\n--- Iniciando transformações com dbt ---")
    try:
        dbt_project_path = "postgres_dw"
        # Executa 'dbt run' especificando o diretório do projeto dbt.
        subprocess.run(
            ["dbt", "run", "--project-dir", dbt_project_path], 
            check=True
        )
        print("--- Transformações dbt concluídas com sucesso ---\n")
    except FileNotFoundError:
        print("ERRO: O comando 'dbt' não foi encontrado.")
        print("Verifique se o dbt-postgres está instalado e se você ativou o ambiente virtual (uv sync).")
        raise
    except subprocess.CalledProcessError as e:
        print("--- ERRO ao executar dbt run ---")
        raise e

def main():
    print("Iniciando pipeline ELT localmente...")
    
    path_monitor_ar_dados_qualidade = "data/monitor-ar_csv/dados_qualidade"
    path_estacoes = "data/monitorar_csv/estacoes.csv"
    path_opendatasus = "data/open_data_sus_csv/INFLUD22-26-06-2025.csv"

    df_monitor_ar = from_csv.extract_from_csv(path_monitor_ar_dados_qualidade)
    df_estacoes = from_csv.extract_from_csv(path_estacoes)
    df_datasus = from_csv.extract_from_csv(path_opendatasus)

    # Eliminação de algumas colunas "problematicas" do csv do openDataSUS
    cols = [14,17,59,61,62,63,66,92,94,106,123,144,149,163,164,169,170,175,176,180,181,185,186,188,189]
    cols_names = []
    for col in cols:
        cols_names.append(df_datasus.columns[col])
    df_datasus.drop(cols_names, inplace=True, axis=1)
    

    # ETAPAS E e L
    # Esta parte do seu código usaria get_db_connection() para se conectar.
    # conn = get_db_connection()
    # ...seu código de extract e load...
    # conn.commit()
    # conn.close()
    print("Etapas de Extração e Carga concluídas (simulado).")

    # ETAPA T
    run_dbt_transformations()

    print("Pipeline ELT concluído com sucesso.")

if __name__ == "__main__":
    main()