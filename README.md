# Loterias Caixa DB

Este repositório mantém uma base de dados atualizada (formato CSV) com os resultados das loterias da Caixa Econômica Federal.

## 🎯 Objetivo

Fornecer arquivos `.csv` limpos e padronizados com o histórico de resultados, atualizados automaticamente via API da Caixa. Ideal para análise de dados, estatísticas e conferência.

## 🚀 Como Funciona

O projeto utiliza **Docker** para garantir um ambiente consistente e scripts em **Python** para processar os dados.

1. **Dados Históricos**: Arquivos base (`data/*.csv`) gerados a partir de planilhas oficiais (Bootstrap).
2. **Atualização**: O script `scripts/update.py` busca novos resultados na API oficial da Caixa e adiciona ao CSV.
3. **Padronização**: Todos os valores monetários são armazenados como `float` (ex: `1234.56`) para facilitar o processamento.

## 🛠️ Como Usar (Localmente)

Pré-requisitos: Docker e Docker Compose.

Use o `Taskfile` (ou execute via `docker-compose` diretamente) para gerenciar o projeto.

### Atualizar Resultados

Para atualizar uma loteria específica (ex: Quina):

```bash
task update quina
# Ou sem Taskfile:
# docker-compose run --rm app python -m scripts.update quina
```

Isso irá:

1. Ler o arquivo local `data/quina.csv`.
2. Verificar o último concurso.
3. Baixar os concursos faltantes da API.
4. Salvar os novos dados no CSV.

### Comandos Disponíveis (`task`)

- `task update [loteria]`: Atualiza os dados de uma loteria.
- `task test`: Roda a suíte de testes (`pytest`).
- `task bootstrap [loteria]`: (Uso interno) Recria o CSV a partir de um arquivo Excel oficial da Caixa.

## 📂 Estrutura

- `data/`: Arquivos CSV com os resultados (Fonte da Verdade).
- `scripts/`: Código fonte Python.
  - `update.py`: Script principal de atualização (ETL).
  - `bootstrap.py`: Conversão inicial de Excel para CSV.
  - `utils.py`: Utilitários de limpeza de dados.
  - `lottery_config.py`: Configurações de colunas e URLs.
- `.github/workflows/`: Automação para rodar a atualização diariamente.

## ⚙️ Detalhes Técnicos

- **Linguagem**: Python 3.11+
- **Bibliotecas**: `pandas`, `requests`
- **Testes**: `pytest` para validação da lógica de transformação.
