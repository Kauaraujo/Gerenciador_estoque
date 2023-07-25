import mysql.connector
import hashlib

# Conecte-se ao banco de dados MySQL
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aa362514",
    database="my_db"
)
cursor = db.cursor()

# Consulta para obter todos os registros da tabela "users"
cursor.execute("SELECT * FROM users")
results = cursor.fetchall()

# Atualizar as senhas para o formato de hash SHA-256
for result in results:
    user_id = result[0]
    senha_antiga = result[4]  # Senha antiga, em formato de texto
    senha_hash = hashlib.sha256(senha_antiga.encode()).hexdigest()  # Hash da senha

    # Atualizar o registro no banco de dados com a senha em formato de hash
    cursor.execute("UPDATE users SET senha = %s WHERE id = %s", (senha_hash, user_id))
    db.commit()

# Feche o objeto de cursor e a conexão com o banco de dados
cursor.close()
db.close()
