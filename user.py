from flask_login import UserMixin
from werkzeug.security import check_password_hash
import sqlite3

class User(UserMixin):
    def __init__(self, id, nome, email, senha_hash):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash

    @classmethod
    def get(cls, email):
        conexao = sqlite3.connect('usuarios.db')
        cursor = conexao.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            return cls(id=resultado[0], nome=resultado[1], email=resultado[2], senha_hash=resultado[3])
        return None

    def verify_password(self, password):
        return check_password_hash(self.senha_hash, password)