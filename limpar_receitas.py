import sqlite3

# Conectar ao banco de dados
conexao = sqlite3.connect('receitas.db')
cursor = conexao.cursor()

# Excluir receitas específicas (exemplo: id 1, 2 e 3)
ids_para_excluir = []  # Coloque aqui os IDs das receitas de teste que você quer excluir

for id_receita in ids_para_excluir:
    cursor.execute('DELETE FROM receitas WHERE id = ?', (id_receita,))
    print(f"Receita com ID {id_receita} excluída.")

conexao.commit()
conexao.close()

print("Limpeza finalizada!")
