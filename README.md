# La Doce Vida

Um site colaborativo de receitas de doces, feito com Flask. Usuários podem visualizar, enviar, comentar e favoritar receitas.

## 🔎 Funcionalidades

- Visualização de receitas
- Envio de novas receitas
- Comentários nas receitas
- Favoritar receitas
- Autenticação de usuários

## 📊 Tecnologias Utilizadas

- Python 3
- Flask
- SQLite
- HTML / CSS

## 🖥️ Instalação

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

## 👥 Contribuintes

- [Emanoelly Francinny](https://github.com/FranbryloB)  
  Desenvolveu funcionalidades CRUD e integração do banco de receitas.  
  Criou páginas de cadastro, estilização de login/registro e banco de dados de usuários.

- [Isabele Fernanda](https://github.com/Isa-Fee)  
  Criadora principal da estrutura do site e do banco de dados.  
  Desenvolveu as páginas e rotas principais, sistema de receitas, páginas do blog e dicas, além de implementação de funcionalidades como exibição, adição e limpeza de receitas.

- [Livia Tainá](https://github.com/LiviaVolieari)  
  Implementou autenticação de usuário (login/cadastro), criou rotas para registro de receitas e corrigiu erros na exibição de páginas.  
  Responsável pelo README do projeto, melhorias na organização e revisão final para a entrega do projeto.

- [Tamíris Medeiros](https://github.com/medeirostamiris)  
  Implementou cookies e tratamento de erros.  
  Adicionou segurança no login usando hash de senha e integração com Flask-Login.
  Adicionou o botão retorno ao início em todas as páginas, incluiu novas receitas e ajustou detalhes sobre o css.
