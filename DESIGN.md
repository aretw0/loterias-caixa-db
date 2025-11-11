# DESIGN.md

## 1. Arquitetura Geral

A solução será implementada em um repositório GitHub, utilizando Python para os scripts de processamento de dados e GitHub Actions para a orquestração e automação do fluxo de trabalho.

O design foi pensado para ser simples, robusto e extensível.

### Diagrama de Fluxo

```text
┌───────────────────┐      ┌──────────────────┐      ┌───────────────────┐
│  GitHub Actions   │      │  Script Python   │      │   API da Caixa    │
│ (Agendador Cron)  ├─────►│   (update.py)    ├─────►│  (servicebus2...) │
└─────────┬─────────┘      └─────────┬────────┘      └─────────┬─────────┘
          │                          │                          │
          │ (Executa Job)            │ (Busca último concurso)  │ (Retorna JSON)
          │                          │                          │
          │                          ▼                          │
          │                  ┌──────────────────┐               │
          │                  │  Compara Dados   │◄───────────────┘
          │                  └─────────┬────────┘
          │                          │
          │                          │ (Se houver novo concurso)
          │                          │
          │                          ▼
┌─────────▼─────────┐      ┌──────────────────┐
│     Commit &      │      │   Adiciona ao    │
│ Push no Repositório├─────◄│      .csv        │
└───────────────────┘      └──────────────────┘

```

## 2. Estrutura do Repositório

A organização dos arquivos no repositório seguirá a seguinte estrutura:

```text
loterias-caixa-db/
├── .github/
│   └── workflows/
│       └── update_results.yml      # Workflow principal do GitHub Actions
├── data/
│   ├── megasena.csv                # Dados históricos e atualizados da Mega-Sena
│   ├── quina.csv                   # Dados históricos e atualizados da Quina
│   └── lotofacil.csv               # Dados históricos e atualizados da Lotofácil
├── scripts/
│   ├── bootstrap.py                # Script para carga inicial de dados (uso manual)
│   └── update.py                   # Script principal para atualização via API
├── .gitignore                      # Arquivo para ignorar arquivos e diretórios (e.g., __pycache__)
├── requirements.txt                # Lista de dependências Python
└── README.md                       # Documentação geral do projeto
```

## 3. Design dos Componentes

### 3.1. Script de Atualização (`scripts/update.py`)

- **Linguagem:** Python 3.
- **Dependências:** `pandas`, `requests`.
- **Funcionalidade:**
  - O script será modularizado para lidar com as especificidades de cada loteria.
  - Receberá um argumento via linha de comando para definir qual loteria deve ser atualizada (e.g., `python scripts/update.py quina`).
  - **Lógica Principal (ETL - Extract, Transform, Load):**
        1. **Extração (Extract):**
            - Carregar o arquivo `data/{loteria}.csv` para identificar o schema de destino e o número do último concurso registrado.
            - Fazer requisições sequenciais à API da Caixa para os concursos seguintes (`ultimo_concurso + 1`, `+2`, ...), extraindo os dados em formato JSON até que não haja novos concursos.
        2. **Transformação (Transform):**
            - Para cada concurso em JSON obtido da API, aplicar uma camada de transformação.
            - Esta camada irá mapear os campos do JSON para as colunas do `.csv` de destino, conforme o schema definido pelo arquivo de bootstrap. Esta lógica de mapeamento será customizada para cada loteria.
            - Exemplo: Mapear `numero` do JSON para a coluna `Concurso` do CSV, `dataApuracao` para `Data Sorteio`, e assim por diante.
        3. **Carga (Load):**
            - Coletar os registros transformados.
            - Ao final do processo, adicionar os novos registros ao arquivo `{loteria}.csv`, garantindo a consistência com os dados históricos.

### 3.2. Workflow do GitHub Actions (`.github/workflows/update_results.yml`)

- **Gatilho (Trigger):**
  - **Agendado (cron):** Será configurado para rodar diariamente em um horário de baixa atividade (e.g., `0 5 * * *` - todo dia às 5h UTC).
  - **Manual (workflow_dispatch):** Permitirá a execução manual do workflow através da interface do GitHub, útil para testes e manutenções.
- **Jobs:**
  - O workflow terá um *job* separado para cada loteria (`update_quina`, `update_megasena`, etc.). Isso permite que falhas em uma loteria não impeçam a atualização das outras e facilita a visualização dos logs.
  - **Passos de cada Job:**
        1. **Checkout:** `actions/checkout@v3` para obter o código do repositório.
        2. **Setup Python:** `actions/setup-python@v4` para configurar o ambiente Python.
        3. **Install Dependencies:** Instalar as bibliotecas listadas no `requirements.txt`.
        4. **Run Update Script:** Executar `python scripts/update.py {loteria}`.
        5. **Commit and Push:** Usar uma action como `stefanzweifel/git-auto-commit-action@v4` ou um passo de script manual para verificar se houve alterações nos arquivos de dados e, em caso afirmativo, commitar e fazer o push para a branch principal. O commit será feito em nome de um bot (e.g., `github-actions[bot]`).

### 3.3. Script de Bootstrap (`scripts/bootstrap.py`)

- **Uso:** Manual e esporádico.
- **Funcionalidade:**
  - Este script será responsável por ler os arquivos de resultados "crus" baixados do site da Caixa (provavelmente em formato `.html` ou `.xlsx`).
  - Utilizará bibliotecas como `pandas` (com `read_html` ou `read_excel`) e `BeautifulSoup` (se necessário) para extrair os dados.
  - Converterá os dados extraídos para o schema definido em `SPECS.md` e salvará os arquivos `.csv` iniciais no diretório `data/`.
  - A complexidade deste script dependerá muito do formato dos arquivos de origem.
