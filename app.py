import csv
import os
from flask import Flask, render_template, request, url_for, redirect

import google.generativeai as genai

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'super secret key')

GENAI_API_KEY = os.getenv("GENAI_API_KEY", "AIzaSyA4SrA5tBmWQm77tD5nb1rsPHxwM_-IIOA")

genai.configure(api_key=GENAI_API_KEY)

def call_gemini_api(question):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')

        response = model.generate_content(question)

        return response.text
    except Exception as e:
        return f"Erro ao chamar a API: {e}"


@app.route('/')
def ola():
    # return '<h1>Olá, mundo!</h1>'
    return render_template('index.html')

@app.route('/sobre_equipe')
def sobre_equipe():
    return render_template('sobre.html')

@app.route('/funcao_procedimentos')
def funcoes_procedimentos():
    return render_template('funcao_procedimentos.html')


@app.route('/tratamentos')
def tratamento():
    return render_template('tratamentos.html')

@app.route('/vetor_matriz')
def vetores_matrizes():
    return render_template('vetor_matriz.html')

@app.route('/estrutura_selecao')
def selecao():
    return render_template('estrutura_selecao.html')


@app.route('/estruturas_repeticao')
def repeticao():
    return render_template('estruturas_repeticao.html')



@app.route('/glossario')
def glossario():

    glossario_de_termos = []

    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        for linha in reader:
            glossario_de_termos.append(linha)

    return render_template('glossario.html', glossario=glossario_de_termos)

@app.route('/novo-termo')
def novo_termo():
    return render_template('novo_termo.html')

@app.route('/criar_termo', methods=['POST'])
def criar_termo():

    termo = request.form['termo']
    definicao = request.form['definicao']

    with open('bd_glossario.csv', 'a', newline='', encoding='utf-8') as arquivo:
        writer = csv.writer(arquivo, delimiter=';')
        writer.writerow([termo, definicao])

    return redirect(url_for('glossario'))


@app.route('/editar_trm/<int:indice>', methods=['GET', 'POST'])
def editar_termo(indice):
    termos = []
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        termos = list(reader)

    if request.method == 'POST':
        novo_termo = request.form['termo']
        nova_definicao = request.form['definicao']
        if 0 <= indice < len(termos):
            termos[indice] = [novo_termo, nova_definicao]
            with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as arquivo:
                writer = csv.writer(arquivo, delimiter=';')
                writer.writerows(termos)
        return redirect(url_for('glossario'))

    if 0 <= indice < len(termos):
        termo, definicao = termos[indice]
        return render_template('editar_trm.html', termo=termo, definicao=definicao)
    else:
        return "Índice inválido", 404


@app.route('/excluir_termo/<int:indice>', methods=['POST'])
def excluir_termo(indice):
    termos = []
    with open('bd_glossario.csv', 'r', newline='', encoding='utf-8') as arquivo:
        reader = csv.reader(arquivo, delimiter=';')
        termos = list(reader)

    if 0 <= indice < len(termos):
        termos.pop(indice)

        with open('bd_glossario.csv', 'w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo, delimiter=';')
            writer.writerows(termos)

    return redirect(url_for('glossario'))

@app.route('/duvidas', methods=['GET', 'POST'])
def duvidas():
    resposta_gemini = None
    pergunta = None
    error = None
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        if pergunta:
            resposta_gemini = call_gemini_api(pergunta)
        else:
            error = "A pergunta não pode estar vazia."
    return render_template('duvida.html', resposta=resposta_gemini, pergunta=pergunta, error=error)

app.run()