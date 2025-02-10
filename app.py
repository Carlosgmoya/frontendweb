from flask import Flask, redirect, url_for, render_template, session
from authlib.integrations.flask_client import OAuth
import requests
from dotenv import load_dotenv
import os


load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET'),   
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'email profile'},
)

@app.route('/')
def index():
   # Verifica si el usuario está autenticado
    user = session.get('user')  # Suponiendo que has guardado el usuario en la sesión
    
    if user:
        autor = user.get('email')  # Usa el email del usuario como autor
        response = requests.get(f'https://backendweb-b0ti.onrender.com/parcial/cabecera/{autor}')  # Llama a tu API
        cabeceras = response.json()  # Suponiendo que la API devuelve una lista JSON de elementos

        return render_template('index.html', user=user, cabeceras=cabeceras)
    
    return render_template('index.html', user=None)

@app.route('/mensaje/<id>')
def mensaje(id):
    user = session.get('user')
    if user:
        # Realiza la solicitud a la API
        response = requests.get(f'https://backendweb-b0ti.onrender.com/parcial/mensaje/{id}')
        if response.status_code == 200:
            data = response.json()  # Obtiene la respuesta completa como JSON
            return render_template('mensaje.html', user=user, mensaje=data)
        else:
            # Manejo de error si la API no responde correctamente
            return "Error al obtener el mensaje", 500
    return render_template('index.html', user=None)

@app.route("/crear")
def crear():
    user = session.get('user')  # Obtiene el usuario si está en sesión
    return render_template('crearMensaje.html', user=user)


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


if __name__ == '__main__':
    app.run(debug=True)
