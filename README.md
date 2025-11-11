# Loterias Caixa DB

Este repositório tem como objetivo criar e manter uma base de dados atualizada com os resultados das loterias da Caixa Econômica Federal.

## Visão Geral

O sistema utiliza scripts em Python e automação com GitHub Actions para:
1.  Manter arquivos `.csv` com os resultados de diversas loterias (Mega-Sena, Quina, Lotofácil, etc.).
2.  Atualizar automaticamente esses arquivos buscando os resultados mais recentes em uma API da Caixa.

Toda a especificação e design do projeto estão documentados nos arquivos `SPECS.md`, `DESIGN.md` e `TESTING_STRATEGY.md`.

## Ambiente de Execução e Requisitos

O projeto é containerizado para garantir um ambiente de desenvolvimento e execução consistente e de fácil configuração.

- **Requisitos:** Docker, Docker Compose e [Taskfile](https://taskfile.dev/installation/).

O Taskfile é utilizado como um `Makefile` moderno para simplificar a execução de comandos Docker.

## Como Executar

Para atualizar os dados de uma loteria, utilize o comando `task` a partir da raiz do projeto:

```bash
# Exemplo para atualizar a Quina
task update quina

# Exemplo para atualizar a Mega-Sena
task update megasena
```

Este comando utiliza o Docker Compose para iniciar o contêiner da aplicação, executar o script `scripts/update.py` com os argumentos necessários e, em seguida, remover o contêiner.

## Estado Atual do Projeto

A estrutura base do projeto está implementada:
- ✅ Diretórios (`data`, `scripts`, `tests`, `.github/workflows`).
- ✅ Arquivos de configuração (`requirements.txt`, `.gitignore`, `Dockerfile`, `docker-compose.yml`, `Taskfile.yml`).
- ✅ Arquivos de documentação e especificação (`SPECS.md`, `DESIGN.md`, `TESTING_STRATEGY.md`).
- ✅ Script de atualização `scripts/update.py` (estrutura inicial).
- ✅ Workflow de automação `.github/workflows/update_results.yml`.
- ✅ Arquivos de dados `.csv` vazios em `data/`.

## Próximos Passos

O projeto agora está aguardando a implementação da lógica de dados, que depende de um arquivo de resultados oficial da Caixa.

1.  **Obter Arquivo de Bootstrap:** É necessário baixar o arquivo histórico de resultados de uma loteria (e.g., o arquivo `.xlsx` ou `.html` disponível no site da Caixa) e adicioná-lo ao projeto.

2.  **Implementar o `bootstrap.py`:** Desenvolver o script que lê o arquivo oficial, o converte para `.csv` e o salva em `data/`. O schema deste arquivo CSV será a **fonte da verdade** para os dados daquela loteria.

3.  **Implementar a Transformação no `update.py`:** Com o schema do CSV definido, a função `transform_data` no script `update.py` deve ser implementada. Ela será responsável por mapear os campos do JSON vindo da API da Caixa para as colunas corretas do arquivo `.csv`.

4.  **Implementar Testes:** Criar testes de unidade em `tests/` para validar a lógica de transformação e garantir a robustez do processo.

