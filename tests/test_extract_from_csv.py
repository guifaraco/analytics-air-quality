import pytest
import pandas as pd
from src.extract.from_csv import extract_from_csv

def test_extraction_from_csv_passing_other_file_type(tmp_path):
    """
    Checa se está sendo retornado um erro ao passar o caminho de um arquivo que não é CSV.
    """
    # Cria um arquivo de texto temporário
    arquivo_txt = tmp_path / "teste.txt"
    arquivo_txt.write_text("isso nao e um csv")

    # Verifica se a exceção é levantada ao passar o caminho do arquivo temporário
    with pytest.raises(Exception):
        extract_from_csv(str(arquivo_txt))

def test_extraction_from_csv_a_directory_without_csv_files(tmp_path):
    """
    Checa se está sendo retornado um erro ao passar o caminho de um diretório sem arquivos CSV.
    """
    # Cria um diretório temporário e um arquivo de texto dentro dele
    pasta_teste = tmp_path / "test_folder"
    pasta_teste.mkdir()
    (pasta_teste / "teste.txt").write_text("outro arquivo de texto")

    # Verifica a exceção
    with pytest.raises(Exception):
        extract_from_csv(str(pasta_teste))

def test_extraction_mixed_types_folder(tmp_path):
    """
    Checa se está extraindo corretamente o DataFrame de uma pasta com tipos de arquivo mistos.
    """
    # Cria um diretório temporário com um CSV e um TXT
    pasta_teste = tmp_path / "test_mixed_types"
    pasta_teste.mkdir()
    (pasta_teste / "vendas.csv").write_text("id;nome_produto;valor;data\n1;celular;1500.00;2024-01-10\n2;teclado;250.50;2024-01-11\n3;mouse;99.99;2024-01-12")
    (pasta_teste / "notas.txt").write_text("ignorar")

    # Executa a função
    df = extract_from_csv(str(pasta_teste))

    # Verifica se apenas o CSV foi lido
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 4)

def test_extraction_one_csv_file(tmp_path):
    """
    Checa se está extraindo corretamente o DataFrame ao passar um único arquivo CSV.
    """
    # Cria um arquivo CSV temporário com conteúdo conhecido
    arquivo_csv = tmp_path / "vendas_unicas.csv"
    conteudo = "id;nome_produto;valor;data\n1;celular;1500.00;2024-01-10\n2;teclado;250.50;2024-01-11\n3;mouse;99.99;2024-01-12"
    arquivo_csv.write_text(conteudo)

    # Executa a função
    df = extract_from_csv(str(arquivo_csv))

    # Verifica o conteúdo do DataFrame
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (3, 4)
    assert df['nome_produto'][0] == "celular"
