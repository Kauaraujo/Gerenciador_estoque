import csv
import mysql.connector
import pandas as pd

# Conecte-se ao banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aa362514",
    database="my_db"
)
cursor = db.cursor()

# Excluindo a tabela 'itens', caso exista
cursor.execute("DROP TABLE IF EXISTS itens")

# Criação da tabela 'itens' com código maior (VARCHAR(20))
cursor.execute("CREATE TABLE itens (id INT AUTO_INCREMENT PRIMARY KEY, codigo VARCHAR(20), descricao TEXT)")

# Leitura dos dados do arquivo CSV usando pandas
df = pd.read_csv('dados.csv', sep='-', header=None, names=['codigo', 'descricao'])

# Inserção dos dados na tabela 'itens'
for index, row in df.iterrows():
    codigo = row['codigo'].strip()
    descricao = row['descricao'].strip()
    cursor.execute("INSERT INTO itens (codigo, descricao) VALUES (%s, %s)", (codigo, descricao))

# Comita as alterações no banco de dados
db.commit()

# Fechando a conexão com o banco de dados
cursor.close()
db.close()
