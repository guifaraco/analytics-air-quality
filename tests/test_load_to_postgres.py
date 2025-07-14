from src.load import to_postgres
from src.extract import from_csv
from src.transform import clean_monitor_ar, clean_opendatasus
from src.main import get_db_connection
import pandas as pd
import pytest

conn = get_db_connection()
# Extract
df_air_measurements = from_csv.extract_from_csv("data/monitor_ar/dados_qualidade")
df_monitoring_stations = from_csv.extract_from_csv("data/monitor_ar/estacoes.csv")
df_datasus = from_csv.extract_from_csv("data/opendatasus/INFLUD22-26-06-2025.csv")

# Light Transform
df_air_measurements = clean_monitor_ar.air_quality_measurements_light_transform(df_air_measurements)
df_monitoring_stations = clean_monitor_ar.monitoring_stations_light_transform(df_monitoring_stations)
df_datasus = clean_opendatasus.opendatasus_light_transform(df_datasus)

to_postgres.load_to_postgres(df_monitoring_stations, conn, "bronze", "monitorar_stations")
to_postgres.load_to_postgres(df_datasus, conn, "bronze", "opendatasus_srag_cases")

def test_passing_empty_df():
    """
    Testa se a excessão é levantada quando passamos um DataFrame vazio.
    """
    with pytest.raises(Exception):
        to_postgres.load_to_postgres(pd.DataFrame(), conn, "bronze", "monitorar_measurements")



