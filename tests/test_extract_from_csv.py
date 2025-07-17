import pytest
import pandas as pd
from src.extract.from_csv import extract_from_csv

def test_extraction_from_csv_passing_other_file_type():
    """
    Checa se está sendo retornado um erro ao passar o caminho de um arquivo que não é CSV nem um caminho de um diretório.
    """
    with pytest.raises(Exception):
        extract_from_csv('tests/tests_csv/test_mixed_types/teste.txt')

def test_extraction_from_csv_a_directory_withou_csv_files():
    """
    Checa se está sendo retornado um erro ao passar o caminho de um diretório sem um arquivo CSV.
    """
    with pytest.raises(Exception):
        extract_from_csv('tests/tests_csv/test_folder_without_csv/teste.txt')

def test_extraction_mixed_types_folder():
    """
    Checa se está extraindo corretamente o DataFrame ao passar uma pasta com arquivos de tipo CSV misturados com outros tipos.
    """
    df = extract_from_csv('tests/tests_csv/test_mixed_types')
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3,4)

def test_extraction_one_csv_file():
    """
    Checa se está extraindo corretamente o DataFrame ao passar um caminho de arquivo CSV.
    """
    df = extract_from_csv('tests/tests_csv/test_mixed_types/vendas.csv')
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3,4)
    assert df['nome_produto'][0] == "celular"
