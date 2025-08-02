import sqlite3
conexao = sqlite3.connect('receitas.db')
cursor = conexao.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS receitas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        imagem_url TEXT,
        categoria TEXT,
        tempo_preparo INTEGER,
        descricao TEXT
    )
''')
conexao.commit()
conexao.close()
print("Banco de dados e tabela 'receitas' criados com sucesso!")
