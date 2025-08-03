from flask import Flask, render_template, request, url_for, session, redirect
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
#export FLASK_app=app.py

print("redirect uri:", os.getenv("SPOTIPY_REDIRECT_URI"))


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'Music Cookie'



#@app.route('/')
#def index():
#    if 'token_info' not in session:
#        return render_template('index.html') 
#    else:
#        token_info = session.get('token_info')
#        sp = spotipy.Spotify(auth=token_info['access_token'])
#        available_genres = sp.recommendation_genre_seeds()
#        genres = available_genres['genres']
#        return render_template('authenticated.html')

@app.route('/')
def index():
    token_info = session.get('token_info')
    if not token_info:
        return render_template('index.html') 

    sp_oauth = create_spotify_oauth()

    # Refresh token if expired
    if sp_oauth.is_token_expired(token_info):
        print("Access token expired, refreshing...")
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info

    access_token = token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)

    try:
        available_genres = sp.recommendation_genre_seeds()
        genres = available_genres.get('genres', [])
    except Exception as e:
        print("Error loading genres:", e)
        genres = []

    return render_template('authenticated.html', genres=genres)


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
        scope="user-read-private user-read-email user-library-read playlist-modify-public playlist-modify-private"
    )


                                            ################### Music Time !!!! ##################

@app.route('/get_genres', methods=['GET'])
def get_genres():
    token_info = session.get('token_info')
    if not token_info:
        return redirect(url_for('login'))  # Redirect to login if token is missing

    sp_oauth = create_spotify_oauth()

    # Refresh token if expired
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info  # Save updated token

    access_token = token_info['access_token']
    sp = spotipy.Spotify(auth=access_token)

    try:
        available_genres = sp.recommendation_genre_seeds()
        genres = available_genres.get('genres', [])
    except Exception as e:
        print("Error getting genres from Spotify:", e)
        genres = []

    return render_template('authenticated.html', genres=genres)




if __name__ == '__main__':
    app.run()