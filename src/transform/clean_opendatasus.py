import pandas as pd
def opendatasus_light_transform(df: pd.DataFrame) -> pd.DataFrame:
    # Colunas que fazem sentido serem eliminadas
    cols = [14,17,59,61,62,63,66,92,94,106,123,144,149,163,164,169,170,175,176,180,181,185,186,188,189]
    # Pegando os nomes das colunas
    cols_names = []
    for col in cols:
        cols_names.append(df.columns[col])
    # Eliminando as colunas
    df.drop(cols_names, inplace=True, axis=1)
    return