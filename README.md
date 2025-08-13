# La Doce Vida

Um site colaborativo de receitas de doces, feito com Flask. Usuários podem visualizar, enviar, comentar e favoritar receitas.

## Funcionalidades

- Visualização de receitas
- Envio de novas receitas
- Comentários nas receitas
- Favoritar receitas
- Autenticação de usuários

## Tecnologias Utilizadas

- Python 3
- Flask
- SQLite
- HTML / CSS

## Instalação

1. **Clone o repositório do projeto para sua máquina e entre na pasta do projeto recém-clonada**

    ```git
    git clone https://github.com/Isa-fee/La-Doce-Vida.git
    cd La-Doce-Vida
    ```

2. **Crie e ative o ambiente virtual para isolar as dependências do projeto**

    ```sh
    # Criar...
    python -m venv venv

    # Ativando no Windows...
    venv\Scripts\activate

    # Ativando no Linux/Mac...
    source venv/bin/activate
    ```

3. **Instale todas as bibliotecas necessárias listadas no arquivo requeriments.txt**

    ```sh
    pip install -r requeriments.txt
    ```

4. **Crie o banco de dados inicial (se aplicável)**

    ```sh
    python criar_banco.py
    ```

5. **Execute a aplicação**

    ```sh
    flask run --debug
    ```

## Contribuintes
- [Emanoelly Francinny](https://github.com/FranbryloB)
- [Isabele Fernanda](https://github.com/Isa-Fee)
- [Livia Tainá](https://github.com/LiviaVolieari)
- [Tamíris Medeiros](https://github.com/medeirostamiris)
