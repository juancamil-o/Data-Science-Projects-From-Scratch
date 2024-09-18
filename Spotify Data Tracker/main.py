import requests
import datetime
import os
import pandas as pd
import sqlalchemy
import sqlite3
from flask import Flask, session, url_for, request, redirect

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(64)

DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
#USER_ID = "aldex_"
CLIENT_ID = "105268b0478b4c53a5533c91ef18a44e"
CLIENT_SECRET = "685faafc94e0444a8fde5f8a602a6db1"
#SCOPE = 'playlist-read-private'

REDIRECT_URI = "http://localhost:5000/callback"
DAY = 30

SCOPE = "user-read-recently-played"


cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id = CLIENT_ID,
    client_secret = CLIENT_SECRET,
    redirect_uri = REDIRECT_URI,
    scope = SCOPE,
    cache_handler = cache_handler,
    show_dialog = True
)

sp = Spotify(auth_manager=sp_oauth)
def check_if_valid_data(df : pd.DataFrame):
    #Check if dataframe is empty
    if df.empty:
        print("No songs downloaded. Finishing execution")
        return False
    
    #Primary Key check
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key Check is violeted")
    
    #Check for nulls
    if df.isnull().values.any():
        raise Exception("Null values found")
    """
    #Check that all timestamps are of last month's date
    last_month = datetime.datetime.now() - datetime.timedelta(days = DAY)
    last_month = last_month.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    
    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if datetime.datetime.strptime(timestamp, "%Y-%m-%d") != last_month:
            raise Exception("At least one of the returned songs does not come from last 30 days")
    """
    return True
            
    
@app.route('/')
def home():
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    return redirect(url_for('get_user_recently_played_songs'))

@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_user_recently_played_songs'))

@app.route('/get_playlists')
def get_playlists():
     if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
    
     

     playlists = sp.current_user_playlists()
     playlists_info = [(pl['name'], pl['external_urls']['spotify']) for pl in playlists['items']]
     playlists_html = '<br>'.join([f'{name}: {url}' for name, url in playlists_info])
     
     return playlists_html

@app.route('/get_user_recently_played_songs')
def get_user_recently_played_songs():
     if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)
     today = datetime.datetime.now()
     last_month = today - datetime.timedelta(days=DAY)
     last_month_unix_timestamp = int(last_month.timestamp()) * 1000

     songs = sp.current_user_recently_played(after = last_month_unix_timestamp)
     songs_info = [( song['track']['name'], 
                        song['track']['album']['artists'][0]["name"], 
                        song['played_at'],
                        song['played_at'][0:10]) 
                       for song in songs['items']]
          
     song_df = pd.DataFrame(songs_info, columns= ["song_name", "artist_name", "played_at", "timestamp"])
     
     if check_if_valid_data(song_df):
         print("Data valid, proceed to Load stage")
         
     engine = sqlalchemy.create_engine(DATABASE_LOCATION)
     conn = sqlite3.connect("my_played_tracks.sqlite")
     cursor = conn.cursor()
     
     sql_query = """
     CREATE TABLE IF NOT EXISTS my_played_tracks(
         song_name VARCHAR(200),
         artist_name VARCHAR(200),
         played_at VARCHAR(200),
         timestamp VARCHAR(200),
         CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
         ) """
     cursor.execute(sql_query)
     print("Opened database successfully")
     
     try:
         song_df.to_sql("my_played_tracks", engine, index = False, if_exists = 'append')
     except:
         print("Data already exists")
         
     conn.close()
     print("Close data")
     return songs_info
 
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)
    """
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {CLIENT_SECRET}".format(token=CLIENT_SECRET)
    }
    
    """
        #Here we are converting the time into unix format
    """
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=DAY)
    yesterday_unix_timestamp = int(yesterday.timestamp()) * 1000
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix_timestamp), headers = headers)
    
    data = r.json()
    
    print(data)
    """
