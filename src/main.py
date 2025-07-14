import os
import psycopg
import subprocess
from dotenv import load_dotenv
from src.extract import from_csv
from src.load import to_postgres
from src.transform import clean_monitor_ar, clean_opendatasus

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
    
    # Pegar a conexão com o banco de dados
    conn = get_db_connection()

    # Extract
    df_air_measurements = from_csv.extract_from_csv("data/monitor_ar/dados_qualidade")
    df_monitoring_stations = from_csv.extract_from_csv("data/monitor_ar/estacoes.csv")
    df_datasus = from_csv.extract_from_csv("data/open_data_sus_csv/INFLUD22-26-06-2025.csv")

    # Light Transform
 #   df_air_measurements = clean_monitor_ar.x(df_air_measurements)
 #   df_monitoring_stations = clean_monitor_ar.x(df_monitoring_stations)
    df_datasus = clean_opendatasus.opendatasus_light_transform(df_datasus)
    
    # Load
    to_postgres.load_to_postgres(df_air_measurements, conn, "bronze", "monitorar_measurements")
    to_postgres.load_to_postgres(df_monitoring_stations, conn, "bronze", "monitorar_stations")
    to_postgres.load_to_postgres(df_datasus, conn, "bronze", "opendatasus_srag_cases")

    conn.commit()
    conn.close()
    print("Etapas de Extração e Carga concluídas.")

    # ETAPA T
    run_dbt_transformations()

    print("Pipeline ELT concluído com sucesso.")

if __name__ == "__main__":
    main()