from flask import Flask, request, render_template, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import json
import sqlite3
from user import User

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_qualquer'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (user_id,))
    resultado = cursor.fetchone()
    conexao.close()

    if resultado:
        return User(id=resultado[0], nome=resultado[1], email=resultado[2], senha_hash=resultado[3])
    return None

def carregar_dicas():
    with open('dicas.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    return render_template('index.html', usuario=current_user if current_user.is_authenticated else None)

receitas_dic = [
    {
        "id": 1,
        "titulo": "Bolo de Cenoura",
        "imagem_url": "/static/images/bolo_cenoura.jpg",
        "categoria": "Bolos",
        "tempo_preparo": 60,
        "descricao": "Um delicioso bolo de cenoura fofinho para todas as ocasiões."
    },
    {
        "id": 2,
        "titulo": "Brigadeiro",
        "imagem_url": "/static/images/brigadeiro.jpg",
        "categoria": "Doces",
        "tempo_preparo": 30,
        "descricao": "O tradicional doce brasileiro, perfeito para festas e sobremesas."
    }
]

@app.route('/receitas')
def receitas():
    return render_template('receitas.html', receitas=receitas_dic)


@app.route('/receita/<int:receita_id>')
def detalhe_receita(receita_id):
    receita = None
    for r in receitas_dic:
        if r["id"] == receita_id:
            receita = r
            break
    if receita is None:
        return "Receita não encontrada", 404
    return f"<h1>{receita['titulo']}</h1><p>{receita['descricao']}</p>"

@app.route('/blog')
def blog():
    dicas = carregar_dicas()
    return render_template('blog.html', dicas=dicas)

@app.route('/dica/<int:id>')
def dica(id):
    dicas = carregar_dicas()
    dica_encontrada = next((d for d in dicas if d["id"] == id), None)
    if dica_encontrada:
        return render_template('dica_individual.html', dica=dica_encontrada)
    else:
        return "Dica não encontrada", 404

def criar_tabela():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
    ''')
    conexao.commit()
    conexao.close()

criar_tabela()

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        senha_hash = generate_password_hash(senha)
        
        conexao = sqlite3.connect('usuarios.db')
        cursor = conexao.cursor()

        try:
            cursor.execute('INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)', (nome, email, senha_hash))
            conexao.commit()
            flash('Cadastro realizado com sucesso!', 'sucesso')
            return redirect(url_for('login'))
        
        except sqlite3.IntegrityError:
            flash('Erro: E-mail já cadastrado.', 'erro')

        finally:
            conexao.close()
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        user = User.get(email)
        if user and user.verify_password(senha):
            login_user(user)
            flash('Login realizado com sucesso!', 'sucesso')
            return redirect(url_for('perfil')) 
        else:
            flash('E-mail ou senha incorretos.', 'erro')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'sucesso')
    return redirect(url_for('index'))

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html', usuario=current_user)

@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def editar_perfil():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        
        conexao = sqlite3.connect('usuarios.db')
        cursor = conexao.cursor()

        try:
            cursor.execute('UPDATE usuarios SET nome = ?, email = ? WHERE id = ?', (nome, email, current_user.id))
            conexao.commit()
            flash('Perfil atualizado com sucesso!', 'sucesso')
            return redirect(url_for('perfil'))
        
        except sqlite3.IntegrityError:
            flash('Erro: E-mail já cadastrado.', 'erro')

        finally:
            conexao.close()

    return render_template('editar_perfil.html', usuario=current_user)

@app.route('/perfil/excluir', methods=['POST'])
@login_required
def excluir_conta():
    conexao = sqlite3.connect('usuarios.db')
    cursor = conexao.cursor()

    try:
        cursor.execute('DELETE FROM usuarios WHERE id = ?', (current_user.id,))
        conexao.commit()
        logout_user()
        flash('Conta excluída com sucesso!', 'sucesso')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash('Erro ao excluir conta.', 'erro')

    finally:
        conexao.close()
