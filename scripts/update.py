import argparse
import pandas as pd
import requests

def get_last_contest(file_path):
    """
    Reads the CSV file and returns the last contest number.
    Returns 0 if the file is empty or doesn't exist.
    """
    try:
        df = pd.read_csv(file_path)
        if not df.empty and 'Concurso' in df.columns:
            # Ensure the 'Concurso' column is numeric, coercing errors to NaN and then filling with 0
            return pd.to_numeric(df['Concurso'], errors='coerce').fillna(0).max()
    except FileNotFoundError:
        return 0
    return 0

def fetch_contest_data(lottery, contest_number):
    """
    Fetches data for a specific contest from the Caixa API.
    """
    api_url = f"https://servicebus2.caixa.gov.br/portaldeloterias/api/{lottery}/{contest_number}"
    response = requests.get(api_url, verify=False) # verify=False is used to bypass SSL verification issues sometimes found in local environments
    if response.status_code == 200:
        return response.json()
    return None

def transform_data(api_data, csv_columns):
    """
    Transforms the API data to match the CSV schema for Quina.
    """
    transformed_row = {}

    # Basic fields
    transformed_row['Concurso'] = api_data.get('numero')
    transformed_row['Data Sorteio'] = api_data.get('dataApuracao')

    # Dezenas Sorteadas
    for i in range(5):
        transformed_row[f'Bola{i+1}'] = api_data['listaDezenas'][i] if i < len(api_data.get('listaDezenas', [])) else ''

    # Ganhadores e Rateio por Faixa
    # Initialize all prize tiers to 0 or empty string
    for col in ['Ganhadores 5 acertos', 'Rateio 5 acertos',
                'Ganhadores 4 acertos', 'Rateio 4 acertos',
                'Ganhadores 3 acertos', 'Rateio 3 acertos',
                'Ganhadores 2 acertos', 'Rateio 2 acertos']:
        transformed_row[col] = 0 if 'Ganhadores' in col else 0.0

    for item in api_data.get('listaRateioPremio', []):
        if item['descricaoFaixa'] == '5 acertos':
            transformed_row['Ganhadores 5 acertos'] = item['numeroDeGanhadores']
            transformed_row['Rateio 5 acertos'] = item['valorPremio']
        elif item['descricaoFaixa'] == '4 acertos':
            transformed_row['Ganhadores 4 acertos'] = item['numeroDeGanhadores']
            transformed_row['Rateio 4 acertos'] = item['valorPremio']
        elif item['descricaoFaixa'] == '3 acertos':
            transformed_row['Ganhadores 3 acertos'] = item['numeroDeGanhadores']
            transformed_row['Rateio 3 acertos'] = item['valorPremio']
        elif item['descricaoFaixa'] == '2 acertos':
            transformed_row['Ganhadores 2 acertos'] = item['numeroDeGanhadores']
            transformed_row['Rateio 2 acertos'] = item['valorPremio']

    # Acumulado
    transformed_row['Acumulado 5 acertos'] = 'SIM' if api_data.get('acumulado') else 'NAO'
    transformed_row['Arrecadacao Total'] = api_data.get('valorArrecadado')
    transformed_row['Estimativa Premio'] = api_data.get('valorEstimadoProximoConcurso')
    transformed_row['Acumulado Sorteio Especial Quina de São João'] = api_data.get('valorAcumuladoConcursoEspecial')
    transformed_row['observação'] = api_data.get('observacao', '')
    
    # Cidade / UF - leaving empty for now as per initial observation
    transformed_row['Cidade / UF'] = '' # Handle if listaMunicipioUFGanhadores is ever populated

    # Ensure all CSV columns are present, even if empty or None
    final_row = {col: transformed_row.get(col, '') for col in csv_columns}
    
    return final_row

def update_lottery_data(lottery):
    """
    Main function to update the data for a specific lottery.
    """
    print(f"Iniciando atualização para: {lottery}")
    
    csv_path = f"data/{lottery}.csv"
    
    # This is a placeholder for the actual CSV schema, which will be read from the bootstrap file.
    # For now, we can't proceed without the actual file.
    try:
        df = pd.read_csv(csv_path)
        csv_columns = df.columns.tolist()
    except FileNotFoundError:
        print(f"Arquivo {csv_path} não encontrado. Execute o bootstrap primeiro.")
        return

    last_contest = get_last_contest(csv_path)
    print(f"Último concurso encontrado: {last_contest}")

    new_results = []
    next_contest = last_contest + 1

    while True:
        print(f"Buscando concurso: {next_contest}")
        api_data = fetch_contest_data(lottery, next_contest)

        if api_data:
            transformed_row = transform_data(api_data, csv_columns)
            if transformed_row:
                new_results.append(transformed_row)
            next_contest += 1
        else:
            print(f"Nenhum dado encontrado para o concurso {next_contest}. Fim da atualização.")
            break
    
    if new_results:
        new_df = pd.DataFrame(new_results)
        updated_df = pd.concat([df, new_df], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)
        print(f"{len(new_results)} novos resultados foram adicionados.")
    else:
        print("Nenhum novo resultado para adicionar.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Atualiza os dados de uma loteria específica.")
    parser.add_argument("lottery", help="O nome da loteria a ser atualizada (e.g., quina, megasena).")
    
    args = parser.parse_args()
    
    update_lottery_data(args.lottery)
