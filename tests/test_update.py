import pytest
import pandas as pd
from scripts.update import transform_data

# Sample API data for Quina (Contest 1)
sample_api_data_quina = {
    "acumulado": False,
    "dataApuracao": "13/03/1994",
    "dataProximoConcurso": "",
    "dezenasSorteadasOrdemSorteio": ["25", "45", "60", "76", "79"],
    "exibirDetalhamentoPorCidade": True,
    "id": None,
    "indicadorConcursoEspecial": 1,
    "listaDezenas": ["25", "45", "60", "76", "79"],
    "listaDezenasSegundoSorteio": None,
    "listaMunicipioUFGanhadores": [],
    "listaRateioPremio": [
        {"descricaoFaixa": "5 acertos", "faixa": 1, "numeroDeGanhadores": 3, "valorPremio": 75731225.0},
        {"descricaoFaixa": "4 acertos", "faixa": 2, "numeroDeGanhadores": 127, "valorPremio": 1788927.0},
        {"descricaoFaixa": "3 acertos", "faixa": 3, "numeroDeGanhadores": 7030, "valorPremio": 42982.0}
    ],
    "listaResultadoEquipeEsportiva": None,
    "localSorteio": "",
    "nomeMunicipioUFSorteio": "",
    "nomeTimeCoracaoMesSorte": "",
    "numero": 1,
    "numeroConcursoAnterior": 0,
    "numeroConcursoFinal_0_5": 5,
    "numeroConcursoProximo": 2,
    "numeroJogo": 3,
    "observacao": "",
    "premiacaoContingencia": None,
    "tipoJogo": "QUINA",
    "tipoPublicacao": 3,
    "ultimoConcurso": True,
    "valorArrecadado": 0.0,
    "valorAcumuladoConcurso_0_5": 0.0,
    "valorAcumuladoConcursoEspecial": 0.0,
    "valorAcumuladoProximoConcurso": 0.0,
    "valorEstimadoProximoConcurso": 0.0,
    "valorSaldoReservaGarantidora": 0.0,
    "valorTotalPremioFaixaUm": 0.0
}

# Sample CSV columns for Quina
sample_csv_columns_quina = [
    "Concurso", "Data Sorteio", "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
    "Ganhadores 5 acertos", "Cidade / UF", "Rateio 5 acertos",
    "Ganhadores 4 acertos", "Rateio 4 acertos",
    "Ganhadores 3 acertos", "Rateio 3 acertos",
    "Ganhadores 2 acertos", "Rateio 2 acertos",
    "Acumulado 5 acertos", "Arrecadacao Total", "Estimativa Premio",
    "Acumulado Sorteio Especial Quina de São João", "observação"
]

def test_transform_data_quina():
    """
    Test the transform_data function for Quina lottery.
    """
    transformed = transform_data(sample_api_data_quina, sample_csv_columns_quina)

    assert transformed['Concurso'] == 1
    assert transformed['Data Sorteio'] == '13/03/1994'
    assert transformed['Bola1'] == '25'
    assert transformed['Bola5'] == '79'
    assert transformed['Ganhadores 5 acertos'] == 3
    assert transformed['Rateio 5 acertos'] == 75731225.0
    assert transformed['Ganhadores 4 acertos'] == 127
    assert transformed['Rateio 4 acertos'] == 1788927.0
    assert transformed['Ganhadores 3 acertos'] == 7030
    assert transformed['Rateio 3 acertos'] == 42982.0
    assert transformed['Ganhadores 2 acertos'] == 0 # Should be 0 as not present in sample_api_data_quina
    assert transformed['Rateio 2 acertos'] == 0.0 # Should be 0.0 as not present
    assert transformed['Acumulado 5 acertos'] == 'NAO'
    assert transformed['Arrecadacao Total'] == 0.0
    assert transformed['Estimativa Premio'] == 0.0
    assert transformed['Acumulado Sorteio Especial Quina de São João'] == 0.0
    assert transformed['observação'] == ''
    assert transformed['Cidade / UF'] == ''

    # Ensure all columns are present
    for col in sample_csv_columns_quina:
        assert col in transformed
