import pandas as pd
import sys
import os

def bootstrap_loteria(loteria_name: str):
    """
    Lê um arquivo .xlsx de uma loteria, converte para .csv e salva em data/.
    """
    xlsx_path = f"data/{loteria_name}.xlsx"
    csv_path = f"data/{loteria_name}.csv"

    if not os.path.exists(xlsx_path):
        print(f"Erro: Arquivo '{xlsx_path}' não encontrado.")
        sys.exit(1)

    print(f"Iniciando bootstrap para '{loteria_name}'...")

    # Ler o arquivo .xlsx
    try:
        df = pd.read_excel(xlsx_path)
        
        # Salvar como .csv
        df.to_csv(csv_path, index=False)
        
        print(f"Arquivo '{csv_path}' criado com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python bootstrap.py <nome_da_loteria>")
        sys.exit(1)
    
    loteria = sys.argv[1]
    bootstrap_loteria(loteria)
