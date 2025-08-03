from flask import Flask, request, render_template, flash, redirect, url_for, make_response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import json
import sqlite3
from user import User
import os
from werkzeug.utils import secure_filename



app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_qualquer'


app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
    nome_cookie = request.cookies.get('nome_usuario')
    nome = current_user.nome if current_user.is_authenticated else nome_cookie
    return render_template('index.html', usuario=nome)


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
            resposta = make_response(redirect(url_for('perfil')))
            resposta.set_cookie('nome_usuario', user.nome, max_age=60*60*24)  
            return resposta
        else:
            flash('E-mail ou senha incorretos.', 'erro')
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout realizado com sucesso!', 'sucesso')
    resposta = make_response(redirect(url_for('index')))
    resposta.set_cookie('nome_usuario', '', expires=0)
    return resposta

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
    return render_template('excluir_perfil.html')

@app.route('/receitas')
def listar_receitas():
    with sqlite3.connect('receitas.db') as conexao:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM receitas')
        receitas_rows = cursor.fetchall()  

        receitas = [dict(r) for r in receitas_rows]

    print(f"Receitas carregadas: {len(receitas)}")
    for r in receitas:
        print(r['titulo'])

    return render_template('receitas.html', receitas=receitas)

@app.route('/receita/<int:receita_id>')
def detalhe_receita(receita_id):
    with sqlite3.connect('receitas.db') as conexao:
        conexao.row_factory = sqlite3.Row
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM receitas WHERE id = ?', (receita_id,))
        receita = cursor.fetchone()
    
    if receita is None:
        return "Receita não encontrada", 404
    
    return render_template('detalhe_receita.html', receita=receita)

@app.route('/receita/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_receita():
    if request.method == 'POST':
        titulo = request.form['titulo']
        imagem = request.files['imagem']
        imagem_filename = None
        categoria = request.form['categoria']
        tempo_preparo = request.form['tempo_preparo']
        descricao = request.form['descricao']
        Ingredientes = request.form['Ingredientes']
        modo_preparo = request.form['modo_preparo']
        if imagem and allowed_file(imagem.filename):
            extensao = imagem.filename.rsplit('.', 1)[1].lower()
            nome_seguro = secure_filename(f"{titulo}-{current_user.id}.{extensao}")
            caminho_final = os.path.join(app.config['UPLOAD_FOLDER'], nome_seguro)
            imagem.save(caminho_final)
            imagem_filename = caminho_final
        
        with sqlite3.connect('receitas.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute('INSERT INTO receitas (titulo, imagem_url, categoria, tempo_preparo, descricao, Ingredientes, modo_preparo) VALUES (?, ?, ?, ?, ?, ?, ?)', 
                           (titulo, imagem_filename, categoria, tempo_preparo, descricao, Ingredientes, modo_preparo))
            conexao.commit()
            flash('Receita adicionada com sucesso!', 'sucesso')
            return redirect(url_for('listar_receitas'))
    
    return render_template('adicionar_receita.html')


@app.route('/receita/editar/<int:receita_id>', methods=['GET', 'POST'])
@login_required
def editar_receita(receita_id):
    with sqlite3.connect('receitas.db') as conexao:
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM receitas WHERE id = ?', (receita_id,))
        receita = cursor.fetchone()
    
    if receita is None:
        return "Receita não encontrada", 404

    if request.method == 'POST':
        titulo = request.form['titulo']
        imagem_url = request.form['imagem_url']
        categoria = request.form['categoria']
        tempo_preparo = request.form['tempo_preparo']
        descricao = request.form['descricao']
        
        with sqlite3.connect('receitas.db') as conexao:
            cursor = conexao.cursor()
            cursor.execute('UPDATE receitas SET titulo = ?, imagem_url = ?, categoria = ?, tempo_preparo = ?, descricao = ? WHERE id = ?', 
                           (titulo, imagem_url, categoria, tempo_preparo, descricao, receita_id))
            conexao.commit()
            flash('Receita atualizada com sucesso!', 'sucesso')
            return redirect(url_for('listar_receitas')) 
    
    return render_template('editar_receita.html', receita=receita)

@app.errorhandler(404)
def pagina_nao_encontrada(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def erro_interno(e):
    return render_template('500.html'), 500

