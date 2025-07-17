from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

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
    return render_template('blog.html')