from flask import Flask, render_template, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'Music Cookie'


@app.route('/')
def index():
    if 'token_info' not in session:  # Check if the user is NOT authenticated
        return render_template('index.html')  # Show the unauthenticated page first
    else:
        return render_template('authenticated.html')  # Show the authenticated page


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/bored')
def bored():
    return render_template('bored.html')


# Spotify authentication routes
@app.route('/login')
def login():
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route('/redirect')
def redirectPage():
    sp_oauth = create_spotify_oauth()
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))  # Redirect back to home after successful authentication


# Logout route
@app.route('/logout')
def logout():
    session.clear()  # Clear session to log out the user
    return redirect(url_for('index'))  # Redirect to home page after logout


# Spotify OAuth helper function
def create_spotify_oauth():
    return SpotifyOAuth(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        redirect_uri=url_for('redirectPage', _external=True),
        scope="user-library-read"
    )


if __name__ == '__main__':
    app.run()