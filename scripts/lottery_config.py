# scripts/lottery_config.py

LOTTERY_CONFIG = {
    "quina": {
        "balls": 5,
        "csv_columns": [
            "Concurso", "Data Sorteio", "Bola1", "Bola2", "Bola3", "Bola4", "Bola5",
            "Ganhadores 5 acertos", "Rateio 5 acertos",
            "Ganhadores 4 acertos", "Rateio 4 acertos",
            "Ganhadores 3 acertos", "Rateio 3 acertos",
            "Ganhadores 2 acertos", "Rateio 2 acertos",
            "Acumulado 5 acertos", "Arrecadacao Total", "Estimativa Premio",
            "Acumulado Sorteio Especial Quina de São João", "observação", "Cidade / UF"
        ],
        "prize_tiers": {
            "5 acertos": {"ganhadores": "Ganhadores 5 acertos", "rateio": "Rateio 5 acertos"},
            "4 acertos": {"ganhadores": "Ganhadores 4 acertos", "rateio": "Rateio 4 acertos"},
            "3 acertos": {"ganhadores": "Ganhadores 3 acertos", "rateio": "Rateio 3 acertos"},
            "2 acertos": {"ganhadores": "Ganhadores 2 acertos", "rateio": "Rateio 2 acertos"},
        },
        "special_prize_column": "Acumulado Sorteio Especial Quina de São João",
        "date_column": "Data Sorteio",
        "estimated_prize_column": "Estimativa Premio",
        "total_collected_column": "Arrecadacao Total",
        "observation_column": "observação",
    },
    "megasena": {
        "balls": 6,
        "csv_columns": [
            "Concurso", "Data do Sorteio", "Bola1", "Bola2", "Bola3", "Bola4", "Bola5", "Bola6",
            "Ganhadores 6 acertos", "Cidade / UF", "Rateio 6 acertos",
            "Ganhadores 5 acertos", "Rateio 5 acertos",
            "Ganhadores 4 acertos", "Rateio 4 acertos",
            "Acumulado 6 acertos", "Arrecadação Total", "Estimativa prêmio",
            "Acumulado Sorteio Especial Mega da Virada", "Observação"
        ],
        "prize_tiers": {
            "6 acertos": {"ganhadores": "Ganhadores 6 acertos", "rateio": "Rateio 6 acertos"},
            "5 acertos": {"ganhadores": "Ganhadores 5 acertos", "rateio": "Rateio 5 acertos"},
            "4 acertos": {"ganhadores": "Ganhadores 4 acertos", "rateio": "Rateio 4 acertos"},
        },
        "special_prize_column": "Acumulado Sorteio Especial Mega da Virada",
        "date_column": "Data do Sorteio",
        "estimated_prize_column": "Estimativa prêmio",
        "total_collected_column": "Arrecadação Total",
        "observation_column": "Observação",
    },
    "lotofacil": {
        "balls": 15,
        "csv_columns": [
            "Concurso", "Data Sorteio", "Bola1", "Bola2", "Bola3", "Bola4", "Bola5", "Bola6", "Bola7", "Bola8", "Bola9", "Bola10",
            "Bola11", "Bola12", "Bola13", "Bola14", "Bola15",
            "Ganhadores 15 acertos", "Cidade / UF", "Rateio 15 acertos",
            "Ganhadores 14 acertos", "Rateio 14 acertos",
            "Ganhadores 13 acertos", "Rateio 13 acertos",
            "Ganhadores 12 acertos", "Rateio 12 acertos",
            "Ganhadores 11 acertos", "Rateio 11 acertos",
            "Acumulado 15 acertos", "Arrecadacao Total", "Estimativa Prêmio",
            "Acumulado sorteio especial Lotofácil da Independência", "Observação"
        ],
        "prize_tiers": {
            "15 acertos": {"ganhadores": "Ganhadores 15 acertos", "rateio": "Rateio 15 acertos"},
            "14 acertos": {"ganhadores": "Ganhadores 14 acertos", "rateio": "Rateio 14 acertos"},
            "13 acertos": {"ganhadores": "Ganhadores 13 acertos", "rateio": "Rateio 13 acertos"},
            "12 acertos": {"ganhadores": "Ganhadores 12 acertos", "rateio": "Rateio 12 acertos"},
            "11 acertos": {"ganhadores": "Ganhadores 11 acertos", "rateio": "Rateio 11 acertos"},
        },
        "special_prize_column": "Acumulado sorteio especial Lotofácil da Independência",
        "date_column": "Data Sorteio",
        "estimated_prize_column": "Estimativa Prêmio",
        "total_collected_column": "Arrecadacao Total",
        "observation_column": "Observação",
    },
}
