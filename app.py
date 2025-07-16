from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

receitas_dic = [
    {
        "id": 1,
        "titulo": "Bolo de Chocolate",
        "imagem_url": "/static/images/bolo_chocolate.jpg",
        "categoria": "Bolos",
        "tempo_preparo": 60,
        "descricao": "Um delicioso bolo de chocolate fofinho para todas as ocasiões."
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