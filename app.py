from flask import Flask, redirect, render_template, request, url_for, session
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.secret_key = 'uma_chave_secreta_qualquer'

app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def login():
    session['origem'] = 'login'
    return render_template('login.html')

@app.route('/adicionar', methods=['POST'])
def adicionar():
    nome = request.form['nome']
    session['nome'] = nome

    return redirect(url_for('perfil', nome=nome))

@app.route('/perfil')
def perfil():
    if 'nome' not in session:
        return redirect(url_for('login'))
    session['origem'] = 'perfil'
    nome = session.get('nome')
    foto = session.get('foto')
    return render_template('perfil.html', nome=nome, foto=foto)

@app.route('/upload_foto', methods=['POST'])
def upload_foto():
    
    if 'foto' not in request.files:
        return redirect(url_for('perfil'))
    
    file = request.files['foto']
    
    if file.filename == '':
        return redirect(url_for('perfil'))
    
    if file:    
        filename = secure_filename(file.filename)
        caminho = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(caminho)

        session['foto'] = filename

        return redirect(url_for('perfil'))
    
@app.route('/voltar')
def voltar():
    origem = session.get('origem', 'login')
    if origem == 'calculadora':
       count = session.get('voltar_count', 0)
       if count == 0:
           session['voltar_count'] = 1
           session['origem'] = 'perfil'
           return redirect(url_for('perfil'))
    session.clear()
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/calculadora', methods=['GET','POST'])
def calculadora():
    if 'nome' not in session:
        return redirect(url_for('login'))
    session['origem'] = 'calculadora'
    session['voltar_count'] = 0

    resultado = None
    div = None
    foto = session.get('foto')

    if request.method == 'POST':
        distancia = float(request.form['distancia'])
        consumo_medio = float(request.form['consumo_medio'])
        preco_str = request.form['preco'].replace(',','.')
        preco = float(preco_str)

        div = distancia / consumo_medio
        resultado = div * preco

    return render_template('calculadora.html', resultado=resultado, div=div, foto=foto)
if __name__ == "__main__":
    app.run(debug=True)