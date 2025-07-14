from src.transform.clean_opendatasus import opendatasus_light_transform
from src.transform.clean_monitor_ar import *
from src.extract import from_csv

def test_opendatasus_filtering_df():
    """
    Checagem se está filtrando o dataset do OpenDataSUS
    """
    df = from_csv.extract_from_csv("data/opendatasus/INFLUD22-26-06-2025.csv")
    df_filtered = opendatasus_light_transform(df)
    cols_names = ["DT_SIN_PRI", "CS_SEXO", "DT_NASC", "CS_RACA", "CS_ESCOL_N", "SG_UF", "ID_MN_RESI", "CO_MUN_RES", "CLASSI_FIN", "CRITERIO", "EVOLUCAO", "DT_EVOLUCA"]
    new_names = list(map(lambda x: x.lower(), cols_names))
    assert df_filtered.columns.to_list() == new_names

def test_monitorar_monitoring_stations_filtering_df():
    """
    Checagem se está filtrando o dataset das estações de monitoramento do MonitorAr
    """
    df = from_csv.extract_from_csv("data/monitor_ar/estacoes.csv")
    df_filtered = monitoring_stations_light_transform(df)
    cols_names = ["cod_mun", "nome_municipio", "estado", "source_id_estacao", "nome_estacao", "latitude", "longitude"]
    assert df_filtered.columns.to_list() == cols_names

def test_monitorar_air_quality_measurements_filtering_df():
    """
    Checagem se está filtrando o dataset das medidas de qualidade do ar do MonitorAr
    """
    df = from_csv.extract_from_csv("data/monitor_ar/dados_qualidade")
    df_filtered = air_quality_measurements_light_transform(df)
    cols_names = ["nome_municipio", "estado", "nome_estacao", "poluente_descricao", "poluente_sigla", "concentracao", "iqar", "data"]
    assert df_filtered.columns.to_list() == cols_names