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

### Marco 2: Bootstrap de Dados (✅ Concluído para Quina)

O objetivo deste marco é criar a base de dados histórica inicial. O bootstrap para a **Quina** já foi realizado, com o arquivo `data/quina.csv` populado a partir do arquivo oficial da Caixa.

- **Entregas (Quina):**
  - `[X]` **Arquivo Histórico Processado:** O arquivo `data/quina.csv` foi gerado.
  - `[X]` **Schema Definido:** O schema do `.csv` da Quina está estabelecido e pronto para ser usado pelo script de atualização.

- **Próximos Passos (Outras Loterias):**
  - `[ ]` Implementar o processo de bootstrap para a Mega-Sena.
  - `[ ]` Implementar o processo de bootstrap para a Lotofácil.

### Marco 3: Automação de Atualização Contínua (✅ Concluído)

A infraestrutura para a atualização automática já está implementada e pronta para ser utilizada.

- **Entregas:**
  - `[X]` Workflow do GitHub Actions (`.github/workflows/update_results.yml`) configurado para rodar diariamente.
  - `[X]` O workflow está preparado para executar o script de atualização, fazer o commit e o push das alterações.

### Marco 4: Implementação da Lógica de Atualização (▶️ Em Progresso)

Com o bootstrap da Quina concluído, o foco agora é implementar a lógica que busca e adiciona os novos resultados para esta loteria.

- **Entregas:**
  - `[ ]` **Implementar `scripts/update.py` (para a Quina):**
    - `[ ]` Lógica para ler o `data/quina.csv` e encontrar o último concurso.
    - `[ ]` Lógica para chamar a API da Caixa e buscar os concursos seguintes.
    - `[ ]` **Função de Transformação:** Mapear os campos do JSON da API para as colunas do `data/quina.csv`.
    - `[ ]` Lógica para adicionar os novos registros ao arquivo `.csv`.
    - `[ ]` Implementar validações de dados para garantir a integridade.

### Marco 5: Testes e Validação (⏳ A Fazer)

Garantir a robustez e a confiabilidade do sistema através de testes automatizados.

- **Entregas:**
  - `[ ]` **Testes de Unidade (`pytest`):**
    - `[ ]` Criar testes para a função de transformação de dados em `update.py` para a Quina.
    - `[ ]` Simular respostas da API (`requests-mock`) para testar cenários de sucesso e de falha.
  - `[ ]` **Configurar CI:** Integrar a execução dos testes no workflow do GitHub Actions.

## Resumo do Estado Atual

O projeto tem uma base sólida de arquitetura e automação, e o bootstrap da **Quina** está finalizado. O foco principal agora é **implementar a lógica de atualização em `scripts/update.py` para a Quina**, o que tornará o repositório totalmente funcional para esta loteria, alcançando a visão "set up and forget it". Após isso, o próximo passo será a criação de testes para validar o processo.
