from flask import Flask, request, render_template, flash, redirect, url_for, session
import json 
import sqlite3

app = Flask(__name__)
app.secret_key = 'uma_chave_secreta_qualquer'


def carregar_dicas():
    with open('dicas.json', 'r', encoding='utf-8') as f:
        return json.load(f)


@app.route('/')
def index():
    return render_template('index.html')

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
            email TEXT NOT NULL,
            senha TEXT NOT NULL
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
        
        conexao = sqlite3.connect('usuarios.db')
        cursor = conexao.cursor()
        cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
        conexao.commit()
        conexao.close()
        
        flash('Cadastro realizado com sucesso!', 'sucesso')
        return redirect(url_for('cadastro'))
    
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conexao = sqlite3.connect('usuarios.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
        usuario = cursor.fetchone()
        conexao.close()

        if usuario:
            session['usuario_id'] = usuario[0]
            session['usuario_nome'] = usuario[1]
            flash('Login realizado com sucesso!', 'sucesso')
            return redirect(url_for('index'))
        else:
            flash('E-mail ou senha incorretos.', 'erro')
            return redirect(url_for('login'))

    return render_template('login.html')