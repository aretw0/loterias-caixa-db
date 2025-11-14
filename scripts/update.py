import argparse
import pandas as pd
import requests
import logging
from typing import Dict, Any
from scripts.lottery_config import LOTTERY_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_last_contest(file_path: str) -> int:
    """
    Reads the CSV file and returns the last contest number.
    Returns 0 if the file is empty or doesn't exist.
    """
    try:
        df = pd.read_csv(file_path)
        if not df.empty and 'Concurso' in df.columns:
            # Ensure the 'Concurso' column is numeric, coercing errors to NaN and then filling with 0
            return int(pd.to_numeric(df['Concurso'], errors='coerce').fillna(0).max())
    except FileNotFoundError:
        logging.info(f"File {file_path} not found. Starting from contest 0.")
        return 0
    except Exception as e:
        logging.error(f"Error reading CSV file {file_path}: {e}")
        return 0
    return 0

def fetch_contest_data(lottery_name: str, contest_number: int) -> Dict[str, Any] | None:
    """
    Fetches data for a specific contest from the Caixa API.
    """
    api_url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/{lottery_name}/{contest_number}"
    try:
        response = requests.get(api_url) # Removed verify=False
        response.raise_for_status() # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.warning(f"Could not fetch data for {lottery_name} contest {contest_number}: {e}")
        return None

def transform_data(lottery_name: str, api_data: Dict[str, Any]) -> Dict[str, Any] | None:
    """
    Transforms the API data to match the CSV schema for a given lottery.
    """
    config = LOTTERY_CONFIG.get(lottery_name)
    if not config:
        logging.error(f"Configuration for lottery '{lottery_name}' not found.")
        return None

    transformed_row = {}
    csv_columns = config["csv_columns"]

    # Basic fields
    transformed_row['Concurso'] = api_data.get('numero')
    transformed_row[config["date_column"]] = api_data.get('dataApuracao')

    # Dezenas Sorteadas
    for i in range(config["balls"]):
        transformed_row[f'Bola{i+1}'] = api_data['listaDezenas'][i] if i < len(api_data.get('listaDezenas', [])) else ''

    # Ganhadores e Rateio por Faixa
    # Initialize all prize tiers to 0 or empty string
    for tier_config in config["prize_tiers"].values():
        transformed_row[tier_config["ganhadores"]] = 0
        transformed_row[tier_config["rateio"]] = 0.0

    for item in api_data.get('listaRateioPremio', []):
        description = item['descricaoFaixa']
        if description in config["prize_tiers"]:
            tier_config = config["prize_tiers"][description]
            transformed_row[tier_config["ganhadores"]] = item['numeroDeGanhadores']
            transformed_row[tier_config["rateio"]] = item['valorPremio']

    # Acumulado
    transformed_row[f'Acumulado {config["balls"]} acertos'] = 'SIM' if api_data.get('acumulado') else 'NAO'
    transformed_row[config["total_collected_column"]] = api_data.get('valorArrecadado')
    transformed_row[config["estimated_prize_column"]] = api_data.get('valorEstimadoProximoConcurso')
    
    if config["special_prize_column"]:
        transformed_row[config["special_prize_column"]] = api_data.get('valorAcumuladoConcursoEspecial')
    
    transformed_row[config["observation_column"]] = api_data.get('observacao', '')
    
    # Cidade / UF - leaving empty for now as per initial observation
    transformed_row['Cidade / UF'] = '' # Handle if listaMunicipioUFGanhadores is ever populated

    # Ensure all CSV columns are present, even if empty or None
    final_row = {col: transformed_row.get(col, '') for col in csv_columns}
    
    return final_row

def update_lottery_data(lottery_name: str):
    """
    Main function to update the data for a specific lottery.
    """
    logging.info(f"Iniciando atualização para: {lottery_name}")
    
    config = LOTTERY_CONFIG.get(lottery_name)
    if not config:
        logging.error(f"Configuration for lottery '{lottery_name}' not found. Exiting.")
        return

    csv_path = f"data/{lottery_name}.csv"
    csv_columns = config["csv_columns"]

    # Check if the CSV file exists and has content
    try:
        df = pd.read_csv(csv_path)
        if df.empty:
            logging.warning(f"Arquivo {csv_path} está vazio. Verifique o processo de bootstrap.")
            last_contest = 0
        else:
            last_contest = get_last_contest(csv_path)
    except FileNotFoundError:
        logging.error(f"Arquivo {csv_path} não encontrado. Execute o bootstrap primeiro. Exiting.")
        return
    except Exception as e:
        logging.error(f"Error reading {csv_path}: {e}. Exiting.")
        return

    logging.info(f"Último concurso encontrado: {last_contest}")

    new_results = []
    next_contest = last_contest + 1

    while True:
        logging.info(f"Buscando concurso: {next_contest}")
        api_data = fetch_contest_data(lottery_name, next_contest)

        if api_data and api_data.get('numero'): # Check if 'numero' key exists to ensure valid data
            transformed_row = transform_data(lottery_name, api_data)
            if transformed_row:
                new_results.append(transformed_row)
            next_contest += 1
        else:
            logging.info(f"Nenhum dado encontrado para o concurso {next_contest} ou dados inválidos. Fim da atualização.")
            break
    
    if new_results:
        new_df = pd.DataFrame(new_results, columns=csv_columns) # Ensure columns match the config
        updated_df = pd.concat([df, new_df], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)
        logging.info(f"{len(new_results)} novos resultados foram adicionados a {csv_path}.")
    else:
        logging.info("Nenhum novo resultado para adicionar.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atualiza os dados de uma loteria específica.")
    parser.add_argument("lottery", help="O nome da loteria a ser atualizada (e.g., quina, megasena).")
    
    args = parser.parse_args()
    
    update_lottery_data(args.lottery)
