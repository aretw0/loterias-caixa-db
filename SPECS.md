# SPECS.md

## 1. Visão Geral

O projeto **Loterias Caixa DB** tem como objetivo criar e manter um repositório de dados com resultados históricos e atualizados das loterias da Caixa Econômica Federal. O sistema automatizará a coleta de novos resultados, garantindo que os dados estejam sempre recentes para uso em análises, estudos e aplicações.

## 2. Requisitos Funcionais

| ID | Requisito | Descrição |
|----|-----------|-------------|
| RF-01 | **Bootstrap de Dados** | O sistema deve ser capaz de gerar arquivos de dados `.csv` a partir de arquivos de resultados oficiais (baixados manualmente do site da Caixa), servindo como a carga inicial da base de dados. |
| RF-02 | **Atualização Automática** | O sistema deve buscar, de forma automática e agendada, os resultados mais recentes das loterias através de uma API oficial da Caixa. |
| RF-03 | **Armazenamento de Dados** | Os resultados de cada modalidade de loteria devem ser armazenados em arquivos `.csv` distintos e bem-estruturados. |
| RF-04 | **Consistência de Dados** | O processo de atualização deve ser idempotente, adicionando apenas concursos novos e evitando a duplicação de registros. |
| RF-05 | **Suporte a Múltiplas Loterias** | O sistema deve ser extensível para suportar diversas modalidades de loterias. O escopo inicial inclui: **Mega-Sena**, **Quina** e **Lotofácil**. |

## 3. Requisitos Não-Funcionais

| ID | Requisito | Descrição |
|----|-----------|-------------|
| RNF-01 | **Automação** | O processo de atualização deve ser totalmente automatizado, sem necessidade de intervenção manual, utilizando GitHub Actions. |
| RNF-02 | **Agendamento** | As atualizações devem ocorrer em intervalos de tempo pré-definidos (e.g., diariamente). |
| RNF-03 | **Documentação** | O repositório deve conter uma documentação clara sobre a estrutura dos dados, o funcionamento do projeto e como utilizá-lo. |
| RNF-04 | **Extensibilidade** | A arquitetura deve facilitar a adição de novas modalidades de loterias no futuro com o mínimo de esforço. |

## 4. Fonte de Dados

- **API:** API de Loterias da Caixa.
- **Endpoint Exemplo:** `https://servicebus2.caixa.gov.br/portaldeloterias/api/{loteria}`
- **Exemplo (Quina):** `https://servicebus2.caixa.gov.br/portaldeloterias/api/quina`

## 5. Schema dos Dados (CSV)

O schema dos arquivos `.csv` será **diretamente derivado** da estrutura dos arquivos de resultados históricos disponibilizados pela Caixa Econômica Federal para download. O processo de bootstrap (RF-01) converterá o arquivo oficial (e.g., um `.xlsx`) para `.csv` mantendo o schema original (nomes e ordem das colunas).

**Responsabilidade do Script de Atualização:**

O script de atualização (`update.py`) será responsável por consumir os dados da API da Caixa (que possui um schema próprio) e **transformá-los** para que se ajustem perfeitamente ao schema do arquivo `.csv` existente.

Isso garante que os dados adicionados pela automação sejam consistentes com os dados históricos originais. O mapeamento entre os campos da API e as colunas do CSV será uma parte fundamental da lógica do script de atualização e deverá ser configurado para cada modalidade de loteria.

**Exemplo (Hipotético):**

Se o arquivo `quina.xlsx` da Caixa, após a conversão, gerar um `quina.csv` com as colunas `["Concurso", "Data Sorteio", "Dezena1", "Dezena2", ..., "Ganhadores Quina"]`, o script de atualização deverá pegar o JSON da API e mapear:
- `numero` -> `Concurso`
- `dataApuracao` -> `Data Sorteio`
- `listaDezenas[0]` -> `Dezena1`
- `listaDezenas[1]` -> `Dezena2`
- `listaRateioPremio[0].numeroDeGanhadores` -> `Ganhadores Quina`
- etc.

O schema exato para cada loteria será definido assim que o primeiro arquivo oficial for analisado durante a fase de implementação.
