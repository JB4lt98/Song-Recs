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
    if 'token_info' not in session:
        return render_template('index.html') 
    else:
        return render_template('authenticated.html')


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
    return redirect(url_for('index')) 


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
        scope="user-library-read playlist-modify-public playlist-modify-private"
    )


#Music Time !!!!

@app.route('/get_genres', methods=['GET'])
def get_genres():
    token_info = session.get('token_info')
    if not token_info:
        return redirect(url_for('login'))  # Redirect to login if token is missing

    sp = spotipy.Spotify(auth=token_info['access_token'])
    available_genres = sp.recommendation_genre_seeds()
    genres = available_genres['genres']

    # Print genres to check if the call to Spotify API is successful
    print(genres)

    # Pass genres to the template
    return render_template('authenticated.html', genres=genres)


if __name__ == '__main__':
    app.run()