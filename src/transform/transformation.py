import pandas as pd
def correct_numbers(value):
    """
    Corrige uma string de número onde tanto os separadores inteiros quanto o decimal são pontos.
    Ex: '1.234.56' -> '1234.56'
    """
    if isinstance(value, str):
        # Conta quantos pontos existem na string
        if value.count('.') > 1:
            # Remove o primeiro ponto
            # O valor.count('.')-1 no final do replace diz para ele deixar apenas a última ocorrência do ponto
            return value.replace('.', '', value.count('.') - 1)
    # Se não for uma string ou se tiver 1 ou 0 pontos, retorna o valor como está
    return value

def transform_air_measurements(df_raw: pd.DataFrame) -> pd.DataFrame:
    """Aplica as transformações leves específicas para os dados do MonitorAr."""
    df = df_raw.copy()
    
    # Aplica a função de correção na coluna problemática
    df['Concentracao'] = df['Concentracao'].apply(correct_numbers)
    df['iqar'] = df['iqar'].apply(correct_numbers)
    return df

def transform_srag(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    cols_to_convert = [
        'CO_MUN_RES', 'CS_RACA', 'CS_ESCOL_N', 'CS_GESTANT', 'FATOR_RISC',
        'PUERPERA', 'CARDIOPATI', 'HEMATOLOGI', 'SIND_DOWN', 'HEPATICA',
        'ASMA', 'DIABETES', 'NEUROLOGIC', 'PNEUMOPATI', 'IMUNODEPRE',
        'RENAL', 'OBESIDADE', 'FEBRE', 'TOSSE', 'GARGANTA',
        'DISPNEIA', 'DESC_RESP', 'SATURACAO', 'DIARREIA', 'VOMITO',
        'FADIGA', 'PERD_OLFT', 'PERD_PALA', 'HOSPITAL', 'UTI',
        'SUPORT_VEN', 'CLASSI_FIN', 'CRITERIO', 'EVOLUCAO'
    ]
    for col in cols_to_convert:
        # Verifica se a coluna existe no DataFrame antes de tentar converter
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')
    return df