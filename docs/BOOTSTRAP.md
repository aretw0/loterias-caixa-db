# Documento de Processo de Bootstrap

Este documento descreve o procedimento manual necessário para realizar o bootstrap de dados históricos de uma nova loteria no projeto.

## Procedimento

1. **Acessar o Site da Caixa:** Navegue até o site das [Loterias Caixa](https://loterias.caixa.gov.br/Paginas/default.aspx).

2. **Selecionar a Loteria:** No menu de loterias, escolha a modalidade desejada (e.g., Quina, Mega-Sena, Lotofácil).

3. **Encontrar a Seção de Resultados:** Na página da loteria, role para baixo até encontrar a seção de "Resultados".

4. **Fazer o Download:** Procure por um link para "Download de resultados" ou similar. Clique neste link para baixar o arquivo histórico, que geralmente está no formato `.xlsx` ou `.html`.

5. **Mover o Arquivo:** Coloque o arquivo baixado no diretório `data/` do projeto.

6. **Executar o Bootstrap:** Execute o comando `task` apropriado para processar o arquivo e popular o `.csv` correspondente.

    ```bash
    # Exemplo para a Quina, assumindo que 'quina.xlsx' está em data/
    task bootstrap-quina
    ```

Este processo inicial é um pré-requisito para que a automação de atualização diária (`scripts/update.py`) funcione corretamente, pois ele cria a base de dados e define o schema que será seguido.
