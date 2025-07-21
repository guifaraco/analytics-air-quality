from src.load import to_postgres
from src.extract import from_csv
from src.main import get_db_connection
import pandas as pd
import pytest

conn = get_db_connection()
# Extract
df_air_measurements = from_csv.extract_from_csv("data/monitor_ar/dados_qualidade", "latin1")
df_monitoring_stations = from_csv.extract_from_csv("data/monitor_ar/estacoes.csv", "utf_8_sig")
df_datasus = from_csv.extract_from_csv("data/opendatasus/INFLUD22-26-06-2025.csv", "latin1")

to_postgres.load_to_postgres(df_monitoring_stations, conn, "bronze", "monitorar_stations")
to_postgres.load_to_postgres(df_datasus, conn, "bronze", "opendatasus_srag_cases")

def test_passing_empty_df():
    """
    Testa se a excessão é levantada quando passamos um DataFrame vazio.
    """
    with pytest.raises(Exception):
        to_postgres.load_to_postgres(pd.DataFrame(), conn, "bronze", "monitorar_measurements")
