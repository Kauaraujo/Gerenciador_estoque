import csv
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_file, json
import hashlib
import os

app = Flask(__name__)

itensList = []
users = []
insumos_descricoes = {}  # Dicionário para armazenar códigos e descrições dos itens


def carregar_usuarios():
    global users
    try:
        with open('modulos/login.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Pular o cabeçalho

            for row in reader:
                if len(row) >= 4:
                    nome, sobrenome, email, senha = row
                    user = {"nome": nome, "sobrenome": sobrenome, "email": email, "senha": senha}
                    users.append(user)
                else:
                    print(f"A linha não possui dados suficientes: {row}")
    except FileNotFoundError:
        users = []


# Chame a função para carregar os usuários
carregar_usuarios()


print("Usuários carregados:", users)


def create_user(nome, sobrenome, email, senha):
    senha_hash = hashlib.sha256(senha.encode()).hexdigest()
    user = {"nome": nome, "sobrenome": sobrenome, "email": email, "senha": senha_hash}

    # Verificar se o arquivo existe
    file_exists = os.path.isfile('modulos/login.csv')

    # Adicionar o novo usuário ao arquivo login.csv
    with open('modulos/login.csv', 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['nome', 'sobrenome', 'email', 'senha']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()  # Se o arquivo não existir, escreva o cabeçalho

        writer.writerow(user)
    users.append(user)  # Adicionar o usuário à lista de usuários em memória


def criar_dicionario_de_insumos():
    global insumos_descricoes
    with open('modulos/dados.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Pular a primeira linha
        for row in reader:
            codigo, descricao = map(str.strip, row[0].split('-'))
            insumos_descricoes[int(codigo)] = descricao


@app.route('/home', methods=['GET', 'POST'])
def home():
    global itensList
    if request.method == 'POST':
        codigo = request.form['item_codigo']
        quantidade = request.form['item_quantidade']

        if codigo.strip() == "" or quantidade.strip() == "":
            error_msg = "Por favor, preencha todos os campos."
            return render_template('index.html', error=error_msg, itensList=itensList)

        descricao = insumos_descricoes.get(int(codigo), "")  # Obter a descrição do dicionário

        item = {"codigo": codigo, "descricao": descricao, "quantidade": quantidade}
        itensList.append(item)

    return render_template('index.html', itensList=itensList)


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        senha_hash_digitada = hashlib.sha256(senha.encode()).hexdigest()

        with open('modulos/login.csv', 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Pular o cabeçalho
            for row in reader:
                nome, sobrenome, email_csv, senha_csv = row
                if email_csv == email and senha_csv == senha_hash_digitada:
                    return redirect(url_for('home'))

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

        create_user(nome, sobrenome, email, senha)

        return redirect(url_for('home', success='Cadastro realizado com sucesso'))

    return render_template("register.html")


@app.route('/adicionar_item', methods=['POST'])
def adicionar_item():
    if request.method == 'POST':
        data = request.get_json()
        codigo = data.get('codigo')
        descricao = data.get('descricao')
        quantidade = data.get('quantidade')

        for item in itensList:
            if item['codigo'] == codigo:
                return jsonify({"success": False, "message": "Item já adicionado à lista."})

        itensList.append({"codigo": codigo, "descricao": descricao, "quantidade": quantidade})
        response = jsonify({"success": True})
        return response


@app.route('/buscar_descricao', methods=['POST'])
def buscar_descricao():
    if request.method == 'POST':
        data = request.get_json()
        codigo = data.get('codigo')

        descricao = insumos_descricoes.get(int(codigo))

        if descricao:
            return jsonify({"success": True, "descricao": descricao})
        else:
            return jsonify({"success": False, "descricao": "Código não encontrado."})


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
    criar_dicionario_de_insumos()  # Chamar a função para criar o dicionário de descrições
    app.run(debug=True)
