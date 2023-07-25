from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, json
import mysql.connector
from flask_socketio import SocketIO
import hashlib
import csv

app = Flask(__name__)
socketio = SocketIO(app)

itensList = []

# Configurações do banco de dados
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="aa362514",
    database="my_db"
)
cursor = db.cursor()


@app.route('/home', methods=['GET', 'POST'])
def home():
    global itensList
    if request.method == 'POST':
        codigo = request.form['item_codigo']
        quantidade = request.form['item_quantidade']

        # Validar se todos os campos foram preenchidos
        if codigo.strip() == "" or quantidade.strip() == "":
            error_msg = "Por favor, preencha todos os campos."
            return render_template('index.html', error=error_msg, itensList=itensList)

        # Aqui, não precisamos mais buscar a descrição usando 'request.form'
        # porque a descrição é buscada através da requisição AJAX no front-end.

        # Adicionar o item à lista global de itens
        item = {"codigo": codigo, "descricao": "", "quantidade": quantidade}
        itensList.append(item)

    return render_template('index.html', itensList=itensList)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Conecte-se ao banco de dados MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aa362514",
            database="my_db"
        )
        cursor = db.cursor()

        # Execute a consulta SELECT usando o objeto de cursor
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        result = cursor.fetchone()

        # Feche o objeto de cursor e a conexão com o banco de dados
        cursor.close()
        db.close()

        if result:
            # Obtenha a senha armazenada no banco de dados
            senha_hash_banco = result[4]  # A coluna de senha está na posição 4

            # Hash da senha digitada pelo usuário
            senha_hash_digitada = hashlib.sha256(senha.encode()).hexdigest()

            if senha_hash_banco == senha_hash_digitada:
                # Login bem-sucedido
                return redirect(url_for('home'))

        # Credenciais inválidas, renderiza a página de login novamente com uma mensagem de erro
        error_msg = 'Credenciais inválidas. Verifique seu e-mail e senha.'
        return render_template('login.html', error=error_msg)

    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        sobrenome = request.form['sobrenome']
        email = request.form['email']
        senha = request.form['senha']

        # Hash da senha antes de armazená-la no banco de dados
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        # Conecte-se ao banco de dados MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aa362514",
            database="my_db"
        )
        cursor = db.cursor()

        # Execute a inserção na tabela de usuários
        cursor.execute("INSERT INTO users (nome, sobrenome, email, senha) VALUES (%s, %s, %s, %s)",
                       (nome, sobrenome, email, senha_hash))
        db.commit()

        # Feche o objeto de cursor e a conexão com o banco de dados
        cursor.close()
        db.close()

        return redirect(url_for('home', success='Cadastro realizado com sucesso'))

    return render_template("register.html")


@app.route('/adicionar_item', methods=['POST'])
def adicionar_item():
    if request.method == 'POST':
        data = request.get_json()
        codigo = data.get('codigo')
        descricao = data.get('descricao')
        quantidade = data.get('quantidade')

        # Carrega a lista de itens já adicionados anteriormente
        itens_list = request.cookies.get('itens_list', '[]')
        itens_list = json.loads(itens_list)

        # Verifica se o item já foi adicionado à lista
        for item in itens_list:
            if item['codigo'] == codigo:
                return jsonify({"success": False, "message": "Item já adicionado à lista."})

        # Adiciona o item à lista
        itens_list.append({"codigo": codigo, "descricao": descricao, "quantidade": quantidade})

        # Armazena a lista atualizada na resposta do cookie
        response = jsonify({"success": True})
        response.set_cookie('itens_list', json.dumps(itens_list))

        return response


@app.route('/buscar_descricao', methods=['POST'])
def buscar_descricao():
    if request.method == 'POST':
        data = request.get_json()
        codigo = data.get('codigo')

        # Conecte-se ao banco de dados MySQL
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="aa362514",  # <-- Insira a senha do seu banco de dados
            database="my_db"
        )
        cursor = db.cursor()

        # Execute a consulta SELECT usando o objeto de cursor
        cursor.execute("SELECT descricao FROM itens WHERE codigo = %s", (codigo,))
        result = cursor.fetchone()

        # Feche o objeto de cursor e a conexão com o banco de dados
        cursor.close()
        db.close()

        if result:
            descricao = result[0]
            return jsonify({"success": True, "descricao": descricao})
        else:
            return jsonify({"success": False})


@app.route('/gerar_csv', methods=['POST'])
def gerar_csv():
    global itensList  # Acessar a lista global de itens

    if request.method == 'POST':
        data = request.get_json()
        itens_list = data.get('itensList', [])

        # Verifica se há itens na lista
        if not itens_list:
            return jsonify({"success": False, "message": "Nenhum item foi adicionado."})

        # Gera o arquivo CSV com os dados
        with open('itens.csv', 'w', newline='') as csvfile:
            fieldnames = ['codigo', 'descricao', 'quantidade']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for item in itens_list:
                writer.writerow(item)

        # Envia o arquivo CSV para o cliente
        return send_file('itens.csv', as_attachment=True)


if __name__ == '__main__':
    socketio.run(app, debug=True)
