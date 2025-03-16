import sqlite3  # Biblioteca para trabalhar com banco de dados SQLite ...

# Criamos uma conexão com o banco de dados (ou criamos um novo se não existir)
conn = sqlite3.connect("delivery.db")
cursor = conn.cursor()

# Criamos tabelas para restaurantes e cardápio, caso ainda não existam
cursor.execute('''
    CREATE TABLE IF NOT EXISTS restaurantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS cardapio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        restaurante_id INTEGER,
        comida TEXT NOT NULL,
        preco REAL,
        FOREIGN KEY (restaurante_id) REFERENCES restaurantes (id)
    )
''')

conn.commit()  # Salvamos as mudanças no banco de dados

# Inserindo dados fictícios para testes
cursor.execute("INSERT INTO restaurantes (nome) VALUES ('Pizza Place'), ('Sushi House')")
cursor.execute("INSERT INTO cardapio (restaurante_id, comida, preco) VALUES (1, 'Pizza Margherita', 25.00), (1, 'Pizza Pepperoni', 30.00), (2, 'Sushi Combo', 40.00), (2, 'Temaki Salmão', 20.00)")
conn.commit()

# Fecha a conexão com o banco de dados no final do programa
conn.close()
