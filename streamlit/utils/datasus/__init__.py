import pandas as pd

def get_datasus(cols=None, filters=[]):
    if not cols:
        cols = [
            'DT_SIN_PRI', 'CS_SEXO', 'DT_NASC', 'CS_GESTANT', 'CS_RACA', 'CS_ESCOL_N', 'SG_UF', 'ID_MN_RESI', 'CO_MUN_RES', 'CLASSI_FIN',
            'CRITERIO', 'EVOLUCAO', 'DT_EVOLUCA'
        ]

    df = pd.read_csv("data/data_sus/INFLUD22-26-06-2025.csv", sep=";", usecols=cols)
    
    if filters:
        df = apply_filters(df, filters)

    return df

def apply_filters(df, filters):
    if filters['uf']:
        df = df[df['SG_UF'] == filters['uf']]
        if filters['city']:
            df = df[df['ID_MN_RESI'] == filters['city']]

    return df