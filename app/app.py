from flask import Flask, render_template, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("APP.SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'Music Cookie'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/bored')
def bored():
    return render_template('bored.html')

#spotify stuff below

#will figure out the login later

@app.route('/getTracks')
def getTracks():
    return 'the music'

@app.route('/redirect')
def redirect():
    return render_template('Authenticated.html')

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id= os.getenv("CLIENT_ID"),
        client_secret= os.getenv("CLIENT_SECRET"),
        redirect_uri= url_for('/redirect', external=True),
        scope= "user-library-read"
    )

if __name__ == '__main__':
    app.run()

