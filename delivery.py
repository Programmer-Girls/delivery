# Importa o módulo para trabalhar com bancos de dados SQLite
import sqlite3
# Importa o módulo para trabalhar com arquivos e diretórios do sistema operacional
import os

# Configura o caminho para o banco de dados no mesmo diretório do script
# Obtém o diretório atual onde este arquivo está localizado
DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
# Cria o caminho completo para o arquivo do banco de dados
CAMINHO_DB = os.path.join(DIRETORIO_ATUAL, 'entrega.db')

def criar_banco_de_dados():
    # Cria o banco de dados e as tabelas necessárias (se não existirem)
    print(f"Banco de dados será criado em: {CAMINHO_DB}")

    # Conecta ao banco de dados (cria se não existir)
    conn = sqlite3.connect(CAMINHO_DB)
    # Cria um cursor para executar comandos SQL
    cursor = conn.cursor()
    
    # Executa comando SQL para criar tabela de restaurantes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS restaurantes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Número único que identifica cada restaurante
            nome TEXT UNIQUE                       -- Nome do restaurante (não pode repetir)
        )
    ''')
    
    # Executa comando SQL para criar tabela de pratos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pratos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Número único que identifica cada prato
            restaurante_id INTEGER,                -- Referência ao ID do restaurante
            nome TEXT,                             -- Nome do prato
            preco REAL,                            -- Preço (número com casas decimais)
            UNIQUE(restaurante_id, nome),          -- Combinação restaurante + prato não pode repetir
            FOREIGN KEY(restaurante_id) REFERENCES restaurantes(id)  -- Liga ao restaurante
        )
    ''')
    
    # Salva as alterações no banco de dados
    conn.commit()
    # Fecha a conexão com o banco
    conn.close()
    print("Banco de dados e tabelas criadas com sucesso!")

def popular_dados_iniciais():
    # Adiciona informações iniciais ao banco de dados (caso não existam)
    conn = sqlite3.connect(CAMINHO_DB)
    cursor = conn.cursor()
    
    # Lista de restaurantes para cadastrar
    restaurantes = ['Pizzaria', 'Casa de Sushi']

    # Para cada restaurante na lista...
    for nome in restaurantes:
        # Insere o nome na tabela, ignorando se já existir
        cursor.execute('INSERT OR IGNORE INTO restaurantes (nome) VALUES (?)', (nome,))
    
    # Salva as alterações antes de continuar
    conn.commit()

    # Busca todos os restaurantes cadastrados para obter seus IDs
    cursor.execute('SELECT id, nome FROM restaurantes')
    # Cria um dicionário: nome do restaurante -> ID
    restaurantes_dict = {nome: id for id, nome in cursor.fetchall()}

    # Lista de pratos para cadastrar (nome do restaurante, nome do prato, preço)
    pratos = [
        ('Pizzaria', 'Pizza de queijo', 25.00),
        ('Pizzaria', 'Pizza de calabresa', 30.00),
        ('Casa de Sushi', 'Sushi Combo', 40.00),
        ('Casa de Sushi', 'Temaki Salmão', 20.00)
    ]

    # Para cada prato na lista...
    for restaurante_nome, nome, preco in pratos:
        # Pega o ID do restaurante correspondente
        restaurante_id = restaurantes_dict.get(restaurante_nome)
        if restaurante_id:
            # Insere o prato na tabela, ignorando se já existir
            cursor.execute('''
                INSERT OR IGNORE INTO pratos (restaurante_id, nome, preco)
                VALUES (?, ?, ?)
            ''', (restaurante_id, nome, preco))
    
    # Salva todas as alterações
    conn.commit()
    conn.close()
    print("Dados iniciais inseridos com sucesso!")

def listar_restaurantes():
    # Obtém e retorna a lista de todos os restaurantes cadastrados
    conn = sqlite3.connect(CAMINHO_DB)
    cursor = conn.cursor()
    # Busca todos os restaurantes (ID e nome)
    cursor.execute('SELECT id, nome FROM restaurantes')
    # Retorna todos os resultados
    restaurantes = cursor.fetchall()
    conn.close()
    return restaurantes

def escolher_restaurante():
    # Mostra restaurantes e permite ao usuário escolher um
    restaurantes = listar_restaurantes()
    
    # Mostra cada restaurante com um número
    for i, (id, nome) in enumerate(restaurantes, start=1):
        print(f"{i}. {nome}")
    
    # Loop até receber uma escolha válida
    while True:
        try:
            # Pede ao usuário para digitar um número
            escolha = int(input("Escolha o número do restaurante: "))
            # Verifica se o número está na lista
            if 1 <= escolha <= len(restaurantes):
                # Retorna o ID do restaurante escolhido
                return restaurantes[escolha - 1][0]
            else:
                print(f"Escolha um número entre 1 e {len(restaurantes)}!")
        except ValueError:  # Se digitar algo que não é número
            print("Erro: Digite um número válido!")

def listar_pratos(restaurante_id):
    # Busca e retorna os pratos de um restaurante específico
    conn = sqlite3.connect(CAMINHO_DB)
    cursor = conn.cursor()
    # Busca pratos do restaurante pelo seu ID
    cursor.execute('SELECT id, nome, preco FROM pratos WHERE restaurante_id = ?', (restaurante_id,))
    pratos = cursor.fetchall()
    conn.close()
    
    # Cria uma lista de pratos com números para escolha (começa em 1)
    return [(i + 1, prato[0], prato[1], prato[2]) for i, prato in enumerate(pratos)]

def escolher_prato(pratos):
    # Mostra os pratos e permite ao usuário escolher um
    if not pratos:
        print("Nenhum prato disponível neste restaurante.")
        return None
    
    print("\nCardápio:")
    # Mostra cada prato com número, nome e preço
    for num, _, nome, preco in pratos:
        print(f"{num}. {nome} - R${preco:.2f}")
    
    while True:
        try:
            escolha = int(input("Escolha o número do prato: "))
            # Procura o prato com o número escolhido
            for num, id_real, nome, preco in pratos:
                if num == escolha:
                    # Retorna os dados do prato escolhido
                    return (id_real, nome, preco)
            print("Opção inválida. Escolha um prato da lista!")
        except ValueError:
            print("Erro: Digite um número válido!")

def confirmar_pedido(prato_id):
    # Mostra a confirmação do pedido com detalhes do prato
    conn = sqlite3.connect(CAMINHO_DB)
    cursor = conn.cursor()
    # Busca o nome e preço do prato pelo ID
    cursor.execute('SELECT nome, preco FROM pratos WHERE id = ?', (prato_id,))
    nome, preco = cursor.fetchone()
    conn.close()
    # Mostra mensagem de confirmação
    print(f"Você pediu {nome} por R${preco:.2f}. Pedido confirmado!")

def main():
    # Função principal que controla o fluxo do programa
    # Prepara o banco de dados
    criar_banco_de_dados()
    # Insere dados iniciais
    popular_dados_iniciais()

    print("\nRestaurantes disponíveis:")
    # Mostra restaurantes e permite escolha
    restaurante_id = escolher_restaurante()
    # Busca pratos do restaurante escolhido
    pratos = listar_pratos(restaurante_id)

    if not pratos:
        print("Este restaurante não possui pratos disponíveis.")
        return
    
    # Permite escolher um prato
    prato_escolhido = escolher_prato(pratos)
    if prato_escolhido:
        # Confirma o pedido
        confirmar_pedido(prato_escolhido[0])

# Executa o programa quando o arquivo é aberto diretamente
if __name__ == "__main__":
    main()