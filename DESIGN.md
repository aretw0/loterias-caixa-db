# DESIGN.md

## 1. Arquitetura Geral

A solução é implementada em um repositório GitHub, utilizando Python para os scripts de processamento de dados, GitHub Actions para automação de CI/CD e Docker para criar um ambiente de execução consistente.

### 1.1. Ambiente de Execução

O projeto é totalmente containerizado com Docker para encapsular as dependências e o ambiente Python, eliminando a necessidade de configuração manual da máquina local. O `Taskfile.yml` atua como um `Makefile`, fornecendo comandos simples (`task update {loteria}`) para interagir com o ambiente Docker.

### 1.2. Diagrama de Fluxo

O fluxo de dados permanece o mesmo, com a execução do script sendo abstraída pelo Docker.

```text
┌───────────────────┐      ┌────────────────────────┐      ┌───────────────────┐
│  GitHub Actions   │      │ Docker + Script Python │      │   API da Caixa    │
│ (Agendador Cron)  ├─────►│      (update.py)       ├─────►│  (servicebus2...) │
└─────────┬─────────┘      └──────────┬─────────────┘      └─────────┬─────────┘
          │                           │                             │
          │ (Executa Job)             │ (Busca último concurso)     │ (Retorna JSON)
          │                           │                             │
          │                           ▼                             │
          │                  ┌──────────────────┐                   │
          │                  │  Compara Dados   │◄───────────────────┘
          │                  └─────────┬────────┘
          │                            │
          │                            │ (Se houver novo concurso)
          │                            │
          │                            ▼
┌─────────▼─────────┐      ┌──────────────────┐
│     Commit &      │      │   Adiciona ao    │
│ Push no Repositório├─────◄│      .csv        │
└───────────────────┘      └──────────────────┘
```

## 2. Estrutura do Repositório

```text
loterias-caixa-db/
├── .github/
│   └── workflows/
│       └── update_results.yml
├── data/
│   ├── megasena.csv
│   ├── quina.csv
│   └── lotofacil.csv
├── scripts/
│   ├── bootstrap.py
│   └── update.py
├── .gitignore
├── Dockerfile                  # Define a imagem Docker da aplicação
├── docker-compose.yml          # Orquestra os serviços Docker
├── requirements.txt
├── Taskfile.yml                # Define tarefas de automação (como um Makefile)
└── README.md
```

## 3. Design dos Componentes

### 3.1. Script de Atualização (`scripts/update.py`)

- **Linguagem:** Python 3.
- **Dependências:** `pandas`, `requests`.
- **Execução Local:** `task update {nome_da_loteria}`.
- **Funcionalidade:**
    - O script é executado dentro de um contêiner Docker, garantindo consistência.
    - Recebe o nome da loteria como argumento de linha de comando.
    - **Lógica Principal (ETL - Extract, Transform, Load):**
        1.  **Extração (Extract):** Carrega o `.csv` local, identifica o último concurso e busca os dados dos concursos seguintes na API da Caixa.
        2.  **Transformação (Transform):** Mapeia os dados do JSON da API para o schema do `.csv` de destino.
        3.  **Carga (Load):** Adiciona os novos registros ao arquivo `.csv`.

### 3.2. Workflow do GitHub Actions (`.github/workflows/update_results.yml`)

- **Lógica:** Permanece a mesma. O workflow irá configurar um ambiente Python no executor do GitHub Actions, instalar as dependências e rodar o script, pois a automação em nuvem não depende do ambiente Docker local.

### 3.3. Script de Bootstrap (`scripts/bootstrap.py`)

- **Uso:** Manual e esporádico, executado via `task`.
- **Funcionalidade:** Permanece a mesma. Será adaptado para ser executado também via `task bootstrap`, por exemplo.
