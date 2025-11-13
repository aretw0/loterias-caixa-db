# ROADMAP.md

Este documento descreve o roadmap de desenvolvimento para o projeto **Loterias Caixa DB**, detalhando os marcos, o estado atual e os próximos passos.

## Visão do Produto

O objetivo final é criar um sistema **"set up and forget it"**: um repositório que, uma vez configurado, se mantém atualizado de forma autônoma, fornecendo uma base de dados de resultados de loterias sempre recente e confiável, sem a necessidade de qualquer intervenção manual.

## Marcos do Projeto

### Marco 1: Estrutura e Configuração do Projeto (✅ Concluído)

Este marco inicial estabeleceu a fundação do projeto.

- **Entregas:**
  - `[X]` Estrutura de diretórios (`data/`, `scripts/`, `tests/`).
  - `[X]` Arquivos de configuração (`Dockerfile`, `docker-compose.yml`, `requirements.txt`).
  - `[X]` Ferramenta de automação local (`Taskfile.yml`).
  - `[X]` Documentação inicial (`README.md`, `SPECS.md`, `DESIGN.md`, `TESTING_STRATEGY.md`).
  - `[X]` Arquivos `.csv` vazios para as loterias iniciais.

### Marco 2: Bootstrap de Dados (✅ Concluído)

O objetivo deste marco é criar a base de dados histórica inicial. O bootstrap para a **Quina**, **Mega-Sena** e **Lotofácil** já foi realizado, com os arquivos `data/quina.csv`, `data/megasena.csv` e `data/lotofacil.csv` populados a partir dos arquivos oficiais da Caixa.

- **Entregas:**
  - `[X]` **Arquivos Históricos Processados:** Os arquivos `data/quina.csv`, `data/megasena.csv` e `data/lotofacil.csv` foram gerados.
  - `[X]` **Schema Definido:** O schema dos arquivos `.csv` está estabelecido e pronto para ser usado pelo script de atualização.

### Marco 3: Automação de Atualização Contínua (✅ Concluído)

A infraestrutura para a atualização automática já está implementada e pronta para ser utilizada.

- **Entregas:**
  - `[X]` Workflow do GitHub Actions (`.github/workflows/update_results.yml`) configurado para rodar diariamente.
  - `[X]` O workflow está preparado para executar o script de atualização, fazer o commit e o push das alterações.

### Marco 4: Implementação da Lógica de Atualização (✅ Concluído)

A lógica que busca e adiciona os novos resultados para todas as loterias configuradas foi implementada.

- **Entregas:**
  - `[X]` **Implementar `scripts/update.py` (Genérico):**
    - `[X]` Lógica para ler o `data/{lottery}.csv` e encontrar o último concurso.
    - `[X]` Lógica para chamar a API da Caixa e buscar os concursos seguintes.
    - `[X]` **Função de Transformação:** Mapear os campos do JSON da API para as colunas do `data/{lottery}.csv` usando configuração.
    - `[X]` Lógica para adicionar os novos registros ao arquivo `.csv`.
    - `[X]` Implementar validações de dados para garantir a integridade. (Abordado nos testes)

### Marco 5: Testes e Validação (✅ Concluído)

Garantir a robustez e a confiabilidade do sistema através de testes automatizados.

- **Entregas:**
  - `[X]` **Testes de Unidade (`pytest`):**
    - `[X]` Criar testes para a função de transformação de dados em `update.py` para a Quina, Mega-Sena e Lotofácil.
    - `[X]` Simular respostas da API (`requests-mock`) para testar cenários de sucesso e de falha.
  - `[ ]` **Configurar CI:** Integrar a execução dos testes no workflow do GitHub Actions. (Próximo passo)

## Resumo do Estado Atual

O projeto tem uma base sólida de arquitetura e automação, e o bootstrap de todas as loterias está finalizado. A lógica de atualização genérica em `scripts/update.py` foi implementada e validada com testes de unidade. O foco principal agora é **integrar a execução dos testes no workflow do GitHub Actions**, o que tornará o repositório totalmente funcional e confiável, alcançando a visão "set up and forget it".
