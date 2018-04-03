import sqlite3
import get_data_from_spotify as spotify

import json
import sys


DB_NAME = 'SpotifyAndGenius.sqlite'
#GENIUS_CACHE_FNAME = 'songs.json'
SPOTIFY_CACHE = 'artists.json'
# try:
#     with open(GENIUS_CACHE_FNAME, 'r') as f:
#         song_dict = json.loads(f.read())
# except:
#     song_dict = {}
try:
    with open(SPOTIFY_CACHE, 'r') as f:
        artist_dict = json.loads(f.read())
except:
    artist_dict = {}


# Create DB
def create_db():
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("DROP TABLE IF EXISTS 'Songs'")
        cur.execute("DROP TABLE IF EXISTS 'Artists'")

        print("Creating Tables...")
        statement = """
            CREATE TABLE 'Artists'(
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Name' TEXT,
                'Genre' TEXT,
                'Popularity' INTEGER
            );
            """
        cur.execute(statement)
        conn.commit()

        statement = '''
            CREATE TABLE 'Songs'(
                'Id' TEXT PRIMARY KEY,
                'Name' TEXT,
                'Track_Number' INTEGER,
                'Artist_Name' TEXT,
                'Album_Name' TEXT,
                'Duration_MS' REAL,
                'Valence' REAL,
                'Energy' REAL,
                'Tempo' REAL,
                'Speechiness' REAL,
                'Danceability' REAL,
                'Lyrics' TEXT
                );
        '''
        cur.execute(statement)
        conn.commit()
        conn.close()
    except:
        sys.exit(1)


def add_artists():
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()
    for artist in artist_dict:
        artist_id, genre, artist_popularity, related_artists = artist_dict[artist]['info']
        statement = '''
            INSERT INTO Artists(Name, Genre, Popularity) 
            VALUES(?, ?, ?)
        '''
        insertion = (artist, genre, artist_popularity,)
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

create_db()
add_artists()