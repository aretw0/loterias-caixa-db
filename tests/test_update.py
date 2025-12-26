import pytest
import pandas as pd
from scripts.update import transform_data
from scripts.lottery_config import LOTTERY_CONFIG

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

# Sample API data for Mega-Sena (Contest 1)
sample_api_data_megasena = {
    "acumulado": False,
    "dataApuracao": "11/03/1996",
    "dataProximoConcurso": "",
    "dezenasSorteadasOrdemSorteio": ["04", "05", "30", "33", "41", "52"],
    "exibirDetalhamentoPorCidade": True,
    "id": None,
    "indicadorConcursoEspecial": 0,
    "listaDezenas": ["04", "05", "30", "33", "41", "52"],
    "listaDezenasSegundoSorteio": None,
    "listaMunicipioUFGanhadores": [],
    "listaRateioPremio": [
        {"descricaoFaixa": "6 acertos", "faixa": 1, "numeroDeGanhadores": 0, "valorPremio": 0.0},
        {"descricaoFaixa": "5 acertos", "faixa": 2, "numeroDeGanhadores": 17, "valorPremio": 39158.92},
        {"descricaoFaixa": "4 acertos", "faixa": 3, "numeroDeGanhadores": 2016, "valorPremio": 330.21}
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
    "tipoJogo": "MEGASENA",
    "tipoPublicacao": 3,
    "ultimoConcurso": True,
    "valorArrecadado": 0.0,
    "valorAcumuladoConcurso_0_5": 1714650.23,
    "valorAcumuladoConcursoEspecial": 0.0,
    "valorAcumuladoProximoConcurso": 0.0,
    "valorEstimadoProximoConcurso": 0.0,
    "valorSaldoReservaGarantidora": 0.0,
    "valorTotalPremioFaixaUm": 0.0
}

# Sample API data for Lotofácil (Contest 1)
sample_api_data_lotofacil = {
    "acumulado": False,
    "dataApuracao": "29/09/2003",
    "dataProximoConcurso": "",
    "dezenasSorteadasOrdemSorteio": ["02", "03", "05", "06", "09", "10", "11", "13", "14", "16", "18", "20", "23", "24", "25"],
    "exibirDetalhamentoPorCidade": True,
    "id": None,
    "indicadorConcursoEspecial": 0,
    "listaDezenas": ["02", "03", "05", "06", "09", "10", "11", "13", "14", "16", "18", "20", "23", "24", "25"],
    "listaDezenasSegundoSorteio": None,
    "listaMunicipioUFGanhadores": [
        {"ganhadores": 1, "municipio": "SAO PAULO", "uf": "SP"},
        {"ganhadores": 1, "municipio": "CURITIBA", "uf": "PR"},
        {"ganhadores": 1, "municipio": "SALVADOR", "uf": "BA"},
        {"ganhadores": 1, "municipio": "BELO HORIZONTE", "uf": "MG"},
        {"ganhadores": 1, "municipio": "BRASILIA", "uf": "DF"}
    ],
    "listaRateioPremio": [
        {"descricaoFaixa": "15 acertos", "faixa": 1, "numeroDeGanhadores": 5, "valorPremio": 49765.82},
        {"descricaoFaixa": "14 acertos", "faixa": 2, "numeroDeGanhadores": 154, "valorPremio": 689.84},
        {"descricaoFaixa": "13 acertos", "faixa": 3, "numeroDeGanhadores": 4645, "valorPremio": 10.00},
        {"descricaoFaixa": "12 acertos", "faixa": 4, "numeroDeGanhadores": 48807, "valorPremio": 4.00},
        {"descricaoFaixa": "11 acertos", "faixa": 5, "numeroDeGanhadores": 257593, "valorPremio": 2.00}
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
    "observacao": "Estimativa de prêmio (15 ACERTOS) próximo concurso: R$250.000,00.",
    "premiacaoContingencia": None,
    "tipoJogo": "LOTOFACIL",
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


def test_transform_data_quina():
    """
    Test the transform_data function for Quina lottery.
    """
    lottery_name = "quina"
    config = LOTTERY_CONFIG[lottery_name]
    transformed = transform_data(lottery_name, sample_api_data_quina)

    assert transformed['Concurso'] == 1
    assert transformed[config["date_column"]] == '13/03/1994'
    assert transformed['Bola1'] == '25'
    assert transformed['Bola5'] == '79'
    assert transformed[config["prize_tiers"]["5 acertos"]["ganhadores"]] == 3
    assert transformed[config["prize_tiers"]["5 acertos"]["rateio"]] == 75731225.0
    assert transformed[config["prize_tiers"]["4 acertos"]["ganhadores"]] == 127
    assert transformed[config["prize_tiers"]["4 acertos"]["rateio"]] == 1788927.0
    assert transformed[config["prize_tiers"]["3 acertos"]["ganhadores"]] == 7030
    assert transformed[config["prize_tiers"]["3 acertos"]["rateio"]] == 42982.0
    assert transformed[config["prize_tiers"]["2 acertos"]["ganhadores"]] == 0 # Should be 0 as not present in sample_api_data_quina
    assert transformed[config["prize_tiers"]["2 acertos"]["rateio"]] == 0.0 # Should be 0.0 as not present
    assert transformed[f'Acumulado {config["balls"]} acertos'] == 0.0
    assert transformed[config["total_collected_column"]] == 0.0
    assert transformed[config["estimated_prize_column"]] == 0.0
    assert transformed[config["special_prize_column"]] == 0.0
    assert transformed[config["observation_column"]] == ''
    assert transformed['Cidade / UF'] == ''

    # Ensure all columns are present
    for col in config["csv_columns"]:
        assert col in transformed

def test_transform_data_megasena():
    """
    Test the transform_data function for Mega-Sena lottery.
    """
    lottery_name = "megasena"
    config = LOTTERY_CONFIG[lottery_name]
    transformed = transform_data(lottery_name, sample_api_data_megasena)

    assert transformed['Concurso'] == 1
    assert transformed[config["date_column"]] == '11/03/1996'
    assert transformed['Bola1'] == '04'
    assert transformed['Bola6'] == '52'
    assert transformed[config["prize_tiers"]["6 acertos"]["ganhadores"]] == 0
    assert transformed[config["prize_tiers"]["6 acertos"]["rateio"]] == 0.0
    assert transformed[config["prize_tiers"]["5 acertos"]["ganhadores"]] == 17
    assert transformed[config["prize_tiers"]["5 acertos"]["rateio"]] == 39158.92
    assert transformed[config["prize_tiers"]["4 acertos"]["ganhadores"]] == 2016
    assert transformed[config["prize_tiers"]["4 acertos"]["rateio"]] == 330.21
    assert transformed[f'Acumulado {config["balls"]} acertos'] == 0.0
    assert transformed[config["total_collected_column"]] == 0.0
    assert transformed[config["estimated_prize_column"]] == 0.0
    assert transformed[config["special_prize_column"]] == 0.0
    assert transformed[config["observation_column"]] == ''
    assert transformed['Cidade / UF'] == ''

    # Ensure all columns are present
    for col in config["csv_columns"]:
        assert col in transformed

def test_transform_data_lotofacil():
    """
    Test the transform_data function for Lotofácil lottery.
    """
    lottery_name = "lotofacil"
    config = LOTTERY_CONFIG[lottery_name]
    transformed = transform_data(lottery_name, sample_api_data_lotofacil)

    assert transformed['Concurso'] == 1
    assert transformed[config["date_column"]] == '29/09/2003'
    assert transformed['Bola1'] == '02'
    assert transformed['Bola15'] == '25'
    assert transformed[config["prize_tiers"]["15 acertos"]["ganhadores"]] == 5
    assert transformed[config["prize_tiers"]["15 acertos"]["rateio"]] == 49765.82
    assert transformed[config["prize_tiers"]["14 acertos"]["ganhadores"]] == 154
    assert transformed[config["prize_tiers"]["14 acertos"]["rateio"]] == 689.84
    assert transformed[config["prize_tiers"]["13 acertos"]["ganhadores"]] == 4645
    assert transformed[config["prize_tiers"]["13 acertos"]["rateio"]] == 10.00
    assert transformed[config["prize_tiers"]["12 acertos"]["ganhadores"]] == 48807
    assert transformed[config["prize_tiers"]["12 acertos"]["rateio"]] == 4.00
    assert transformed[config["prize_tiers"]["11 acertos"]["ganhadores"]] == 257593
    assert transformed[config["prize_tiers"]["11 acertos"]["rateio"]] == 2.00
    assert transformed[f'Acumulado {config["balls"]} acertos'] == 0.0
    assert transformed[config["total_collected_column"]] == 0.0
    assert transformed[config["estimated_prize_column"]] == 0.0
    assert transformed[config["special_prize_column"]] == 0.0
    assert transformed[config["observation_column"]] == 'Estimativa de prêmio (15 ACERTOS) próximo concurso: R$250.000,00.'
    assert transformed['Cidade / UF'] == ''

    # Ensure all columns are present
    for col in config["csv_columns"]:
        assert col in transformed
