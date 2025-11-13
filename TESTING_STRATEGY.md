# TESTING_STRATEGY.md

## 1. Filosofia de Testes

A estratégia de testes para o projeto **Loterias Caixa DB** foca em garantir a **confiabilidade dos dados**, a **robustez do processo de automação** e a **manutenibilidade do código**. Adotaremos uma abordagem em camadas, combinando testes de unidade, testes de integração e validação de dados para cobrir os diferentes componentes do sistema.

## 2. Tipos de Teste

### 2.1. Testes de Unidade

- **Objetivo:** Verificar o comportamento de pequenas e isoladas partes do código, principalmente as funções dentro do script `scripts/update.py`.
- **Ferramentas:** `pytest` para a estrutura de testes e `requests-mock` para simular as respostas da API da Caixa.
- **Escopo dos Testes:**
  - **Funções de Parsing:** Testar as funções que convertem o JSON da API para o formato do DataFrame, garantindo que todos os campos são mapeados corretamente.
  - **Lógica de Requisição:** Simular diferentes respostas da API (sucesso, erro 404, JSON malformado) e verificar se o script se comporta como esperado.
  - **Manipulação de Dados:** Testar a lógica que identifica o último concurso e prepara os novos dados para serem adicionados ao CSV.
- **Execução:**
  - **Localmente:** A execução dos testes de unidade deve ser feita através do Taskfile para garantir que eles rodem no ambiente Docker consistente.

      ```bash
      task test
      ```

  - **CI/CD:** Os testes de unidade serão executados automaticamente via GitHub Actions a cada `push` ou `pull_request` para a branch principal, garantindo que novas alterações não quebrem a lógica existente.

### 2.2. Testes de Integração

- **Objetivo:** Garantir que os diferentes componentes do sistema (script, API, sistema de arquivos) funcionam corretamente em conjunto.
- **Ferramentas:** O próprio workflow do GitHub Actions servirá como nosso principal mecanismo de teste de integração.
- **Escopo dos Testes:**
  - **Fluxo de Atualização Completo:** O teste validará o processo de ponta a ponta:
        1. Leitura do arquivo `.csv` existente.
        2. Chamada real (limitada) à API da Caixa para buscar um concurso conhecido.
        3. Escrita do novo resultado no arquivo `.csv`.
        4. Commit e push bem-sucedidos no repositório.
  - **Cenário de "Nenhuma Atualização":** Testar o caso em que o script roda, mas não há novos concursos, garantindo que nenhum commit desnecessário seja feito.
- **Execução:**
  - **Manual:** O workflow poderá ser acionado manualmente (`workflow_dispatch`) para fins de teste, especialmente após uma refatoração ou mudança significativa.
  - **Agendada:** A execução diária do workflow principal atua como um teste de integração contínuo, e qualquer falha gerará uma notificação para análise.

### 2.3. Validação de Dados (Defensive Programming)

- **Objetivo:** Proteger a base de dados contra a inserção de dados inválidos ou corrompidos, especialmente devido a mudanças inesperadas na API da Caixa.
- **Implementação:** A validação será implementada diretamente no script `scripts/update.py`.
- **Verificações:**
  - **Schema da API:** Antes de processar a resposta da API, o script verificará se os campos-chave esperados (`numero`, `dataApuracao`, `listaDezenas`, etc.) estão presentes no JSON.
  - **Tipos de Dados:** Verificar se os dados recebidos correspondem aos tipos esperados (e.g., se `numero` é um inteiro, se `listaDezenas` é uma lista).
  - **Consistência do Concurso:** Garantir que o número do concurso recebido da API é o esperado (sequencial ao último salvo).
- **Tratamento de Erros:** Se qualquer validação falhar, o script deve:
    1. Registrar um erro detalhado no log da execução do GitHub Actions.
    2. Interromper a execução para aquela loteria específica, evitando a corrupção do arquivo `.csv`.
    3. Finalizar com um código de erro que faça o job do workflow falhar, disparando uma notificação.

## 3. Estrutura de Testes no Repositório

Para organizar os testes de unidade, uma nova pasta `tests/` será criada:

```text
loterias-caixa-db/
├── tests/
│   ├── test_update.py      # Testes de unidade para o script update.py
│   └── conftest.py         # Fixtures do pytest (e.g., dados de exemplo)
├── .github/
...
```

O workflow de CI no GitHub Actions será configurado para descobrir e executar os testes automaticamente a partir deste diretório.
