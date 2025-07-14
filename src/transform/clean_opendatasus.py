import pandas as pd
def opendatasus_light_transform(df: pd.DataFrame) -> pd.DataFrame:
    # Colunas importantes
    cols_names = ["DT_SIN_PRI", "CS_SEXO", "DT_NASC", "CS_RACA", "CS_ESCOL_N", "SG_UF", "ID_MN_RESI", "CO_MUN_RES", "CLASSI_FIN", "CRITERIO", "EVOLUCAO", "DT_EVOLUCA"]

    df_filtered = df[cols_names].copy()
    # Alterar as colunas para lower case
    df_filtered.columns = df_filtered.columns.str.lower()
    return df_filtered
    
