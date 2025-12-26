import pandas as pd
import sys
import os

# Add local directory to path to allow importing utils when run directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils import clean_currency
from lottery_config import LOTTERY_CONFIG

def migrate_csvs():
    """
    Iterates over all configured lotteries and cleans their CSV files
    converting currency strings to floats.
    """
    print("Iniciando migração dos arquivos CSV...")

    for lottery_name, config in LOTTERY_CONFIG.items():
        csv_path = f"data/{lottery_name}.csv"
        
        if not os.path.exists(csv_path):
            print(f"Skipping {lottery_name}: {csv_path} not found.")
            continue

        print(f"Processando {lottery_name}...")
        
        try:
            df = pd.read_csv(csv_path)
            
            # Identificar colunas monetárias
            monetary_columns = []
            
            # Adicionar colunas de rateio
            for tier in config["prize_tiers"].values():
                monetary_columns.append(tier["rateio"])
            
            # Adicionar outras colunas monetárias se existirem no config
            if "total_collected_column" in config:
                monetary_columns.append(config["total_collected_column"])
            if "estimated_prize_column" in config:
                monetary_columns.append(config["estimated_prize_column"])
            if "special_prize_column" in config:
                monetary_columns.append(config["special_prize_column"])
            
            # Coluna de Acumulado (ex: Acumulado 5 acertos)
            accumulated_col = f"Acumulado {config['balls']} acertos"
            monetary_columns.append(accumulated_col)

            cleaned_count = 0
            for col in monetary_columns:
                if col in df.columns:
                    # Aplica a limpeza
                    df[col] = df[col].apply(clean_currency)
                    cleaned_count += 1
            
            if cleaned_count > 0:
                df.to_csv(csv_path, index=False)
                print(f"  -> Atualizado {lottery_name} com sucesso. {cleaned_count} colunas limpas.")
            else:
                print(f"  -> Nenhuma coluna precisou ser limpa em {lottery_name}.")

        except Exception as e:
            print(f"Erro ao processar {lottery_name}: {e}")

    print("Migração concluída.")

if __name__ == "__main__":
    migrate_csvs()
