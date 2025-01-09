from flask import Flask, render_template
from flask import Flask, request
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/bored')
def bored():
    return render_template('bored.html')

if __name__ == '__main__':
    app.run()

