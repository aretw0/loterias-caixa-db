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

### Marco 2: Bootstrap de Dados (▶️ Em Progresso)

Este é o passo **essencial** para alcançar a visão "set up and forget it". O objetivo é criar a base de dados histórica inicial a partir de uma fonte oficial. Atualmente, este processo ainda é um pré-requisito manual.

- **Entregas:**
  - `[ ]` **Obter Arquivo Histórico Oficial:** Baixar o arquivo de resultados completo (e.g., `.xlsx` ou `.html`) do site da Caixa.
  - `[ ]` **Implementar `scripts/bootstrap.py`:** Desenvolver o script que:
    - Lê o arquivo histórico oficial.
    - Converte os dados para um formato limpo e estruturado.
    - Salva os dados no arquivo `.csv` correspondente em `data/`, definindo o schema de dados que será usado dali em diante.
  - `[ ]` **Automatizar o Bootstrap (Visão "Set up and forget it"):**
    - Para que o projeto seja verdadeiramente "set up and forget it" para um novo usuário (ou para adicionar uma nova loteria), o ideal é que o processo de bootstrap seja o mais simples possível.
    - **Solução Proposta:** O script `bootstrap.py` poderia ser projetado para baixar o arquivo histórico diretamente de uma URL conhecida no site da Caixa, se disponível. Caso contrário, a documentação deve ser extremamente clara sobre onde encontrar o arquivo e como executar o comando de bootstrap.
    - `[ ]` Criar um comando `task bootstrap {loteria}` para simplificar a execução.

- **Status de "Pronto" para o Usuário:**
  - O projeto será considerado "pronto para bootstrap" quando um usuário puder clonar o repositório, executar um único comando (ex: `task bootstrap megasena`) e ter o arquivo `data/megasena.csv` populado com o histórico completo de resultados, sem precisar de passos manuais complexos.

### Marco 3: Automação de Atualização Contínua (✅ Concluído)

A infraestrutura para a atualização automática já está implementada e pronta para ser utilizada.

- **Entregas:**
  - `[X]` Workflow do GitHub Actions (`.github/workflows/update_results.yml`) configurado para rodar diariamente.
  - `[X]` O workflow está preparado para executar o script de atualização, fazer o commit e o push das alterações.

### Marco 4: Implementação da Lógica de Atualização (⏳ A Fazer)

Com o bootstrap definido, o próximo passo é implementar a lógica que busca e adiciona os novos resultados.

- **Entregas:**
  - `[ ]` **Implementar `scripts/update.py`:**
    - `[ ]` Lógica para ler o `.csv` existente e encontrar o último concurso.
    - `[ ]` Lógica para chamar a API da Caixa e buscar os concursos seguintes.
    - `[ ]` **Função de Transformação:** Mapear os campos do JSON da API para as colunas do `.csv` (conforme definido no Marco 2).
    - `[ ]` Lógica para adicionar os novos registros ao arquivo `.csv`.
    - `[ ]` Implementar validações de dados (defensive programming) para garantir a integridade dos dados.

### Marco 5: Testes e Validação (⏳ A Fazer)

Garantir a robustez e a confiabilidade do sistema através de testes automatizados.

- **Entregas:**
  - `[ ]` **Testes de Unidade (`pytest`):**
    - `[ ]` Criar testes para a função de transformação de dados em `update.py`.
    - `[ ]` Simular respostas da API (`requests-mock`) para testar cenários de sucesso e de falha.
  - `[ ]` **Configurar CI:** Integrar a execução dos testes no workflow do GitHub Actions para rodar a cada push/pull request.

## Resumo do Estado Atual

O projeto tem uma base sólida de arquitetura e automação. O foco principal agora é a **implementação da camada de dados**, começando pelo processo de **bootstrap**, que é o desbloqueio para todo o resto do fluxo de valor. Uma vez que o bootstrap esteja funcional e simplificado, a implementação da lógica de atualização e dos testes seguirá de forma mais direta.
