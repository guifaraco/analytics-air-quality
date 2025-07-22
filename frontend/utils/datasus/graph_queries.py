import streamlit as st

from frontend.utils import get_month_name, execute_query

def query_big_numbers_primeira_linha(): # ok
    '''
        Retorna os valores utilizados na primeira linha de big numbers.
        Colunas retornadas:
            - final_classification: nome da srag
            - total_cases: numero total de casos da srag
            - icu_percentage: taxa de internações na uti
            - death_percentage: taxa de mortalidade por srag 
    '''

    query = '''
            SELECT 
                *
            FROM
                gold.mart_datasus_total_big_numbers
            '''

    return execute_query(query)

def query_big_numbers_segunda_linha(): # ok
    '''
        Retorna os valores utilizados na segunda linha de big numbers.
        Colunas retornadas:
            - top_classification_by_total_cases: nome da srag com maior número de casos
            - max_total_cases: numero total de casos relativo a srag anterior
            - top_classification_by_icu_rate: nome da srag com maior taxa de uti
            - max_icu_rate: taxa de uti relativo a srag anterior
            - top_classification_by_death_rate: nome da srag com maior taxa de mortalidade
            - max_death_rate: taxa de mortalidade relativa a srag anterior
    '''

    query = '''
                SELECT 
                    * 
                FROM
                    gold.mart_datasus_big_numbers_per_rank
            '''

    return execute_query(query)

def query_casos_mensais(): # ok

    ''' 
        Retorna o DataFrame Utilizado para fazer o gráfico de Série Temporal de Casos.
        Colunas retornadas: 
            - sum: total de casos por mês
            - month: mês 
    '''

    query = '''
                SELECT 
                    *
                FROM
                    gold.mart_total_cases_monthly
            '''

    return execute_query(query)

def query_fatores_risco():

    ''' 
        Retorna o DataFrame Utilizado para fazer o gráfico de Análise dos Fatores de Risco.
        Colunas retornadas: 
            - total_cases_(nome do fator de risco): total de casos por mês de acordo com o fator de risco
            - icu_cases_(nome do fator de risco): total de casos por mês que precisou de uti de acordo com o fator de risco
    '''

    query = '''
                SELECT 
                    *
                FROM
                    gold.mart_total_cases_per_risk_factor
            '''

    return execute_query(query)

def query_casos_por_faixa_etaria():
    '''
        Retorna o DataFrame utilizado para elaborar o gráfico de Distribuição Demográfica dos Casos:
        Colunas retornadas:
            - genero: masculino x feminino
            - faixa_etaria: faixa etária 
            - numero_total_casos: número total de casos por faixa etária e gênero
    '''

    query = '''
                SELECT 
                    *
                FROM
                    gold.mart_total_cases_per_age_group_and_gender
            '''
    
    return execute_query(query)

def query_casos_por_srag_e_evolucao(): # ok
    '''
        Retorna o DataFrame utilizado para elabora o Gráfico Total de Casos por SRAG e evolução.
        Colunas retornadas:
            - srag: nome da srag
            - evolução: cura, óbito e óbito por outras causas
            - numero_total_casos: número total de casos por srag e evolução
    '''

    query = '''
                SELECT
                    *
                FROM
                    gold.mart_total_cases_per_srag_and_evolution
                WHERE evolucao != 'OBITO POR OUTRAS CAUSAS'
            '''
    
    return execute_query(query)

def query_casos_map(): #Ok
    '''
        Retorna o dataframe utilizado para renderizar o mapa.
        Colunas retornadas:
            - city_name: nome da cidade
            - state_code: uf
            - latitude: latitude referente a cidade
            - longitude: longitude referente a cidade
            - total_health_cases: numero total de casos por cidade
    '''

    query = '''
                SELECT
                    city_name,
                    latitude,
                    longitude,
                    total_health_cases AS numero_total_cases
                FROM
                    gold.mart_map
            '''

    return execute_query(query)

def query_evolucao_mensal_por_srag(): # Ok
    '''
        Retorna o DataFrame utilizado na elaboração do gráfico de Mês x Total Casos X SRAG
        Colunas retornadas:
            - final_classification: srag
            - month: mês
            - sum: número total de casos por srag
    '''

    query = '''
                SELECT
                    final_classification,
                    month,
                    SUM(sum)
                FROM
                    gold.mart_monthly_evolution_monthly_srag
                GROUP BY
                    final_classification,
                    month
            '''
    
    return execute_query(query)

def query_quantidade_total_casos_por_srag(): # Ok
    '''
        Retorna o DataFrame utilizado na elaboração do gráfico de pizza de distribuição de srag
        Colunas Retornadas:
            - srag: nome srag
            - numero_total_casos
    '''

    query = '''
                SELECT
                    srag,
                    SUM(numero_total_casos)
                FROM
                    gold.mart_total_cases_per_srag_and_evolution
                GROUP BY
                    srag
            '''
    
    return execute_query(query)

def query_casos_por_sintomas():
    '''
        Retorna o DataFrame utilizado na elaboração do gráfico de barras com a quantidade de casos por sintomas
    '''

    query = '''
                SELECT
                    *
                FROM
                    gold.mart_total_cases_per_symptoms
            '''

    return execute_query(query)