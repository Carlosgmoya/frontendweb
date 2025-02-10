from flask import Flask, redirect, url_for, render_template, session
from authlib.integrations.flask_client import OAuth
import requests
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
oauth = OAuth(app)

google = oauth.register(
    name='google',

    
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email profile'},
)

@app.route('/')
def index():
    user = session.get('user')  # Obtiene el usuario si está en sesión
    return render_template('index.html', user=user)

@app.route('/login')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/login/authorize')
def authorize():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    session['user'] = user_info
    return redirect(url_for('index'))


@app.route('/crearPelicula')
def crearPelicula():
    user = session.get('user')  # Obtiene el usuario si está en sesión
    return render_template('pelicula.html', user=user)

@app.route('/crearSala')
def crearSala():
    user = session.get('user')  # Obtiene el usuario si está en sesión
    return render_template('sala.html', user=user)

@app.route('/crearProy')
def crearProy():
    user = session.get('user')  # Obtiene el usuario si está en sesión
    return render_template('proyeccion.html', user=user)

@app.route('/buscarPelicula')
def buscarPelicula():
    user = session.get('user')  # Obtiene el usuario si está en sesión
    return render_template('buscar.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
