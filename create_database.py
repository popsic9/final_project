import sqlite3
import get_data_from_spotify as spotify

import json
import sys


DB_NAME = 'SpotifyAndGenius.sqlite'
GENIUS_CACHE_FNAME = 'songs.json'
SPOTIFY_CACHE = 'artists.json'
try:
    with open(GENIUS_CACHE_FNAME, 'r') as f:
        song_dict = json.loads(f.read())
except:
    song_dict = {}
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
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
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
            INSERT INTO 'Artists'
            VALUES(?, ?, ?, ?)
        '''
        insertion = (None, artist, genre, artist_popularity,)
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def add_songs():
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()
    for artist in artist_dict:
        print('-----Artists----{}-------'.format(artist))
        for album in artist_dict[artist]['albums']:
            album_title = list(album.keys())[0]
            for song_id, song_features in album[album_title].items():
                try:
                    lyrics = song_dict[artist][song_id]
                except:
                    lyrics = "None"
                track_number, track_name, duration_ms, danceability, energy, tempo, speechiness, valence = song_features
                statement = '''
                    INSERT INTO 'Songs'
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                insertion = (None, track_name, track_number, artist, album_title,
                            duration_ms, valence, energy, tempo, speechiness, danceability, lyrics)
                cur.execute(statement, insertion)
            print("Inserts All Songs from {}".format(album_title))
    conn.commit()
    conn.close()

def get_albums(artist_name):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()

    statement = '''
        SELECT DISTINCT(Album_Name)
        FROM Songs
        WHERE Artist_Name = ?
    '''
    insertion = (artist_name,)
    cur.execute(statement, insertion)
    album_list = cur.fetchall()
    if album_list == []:
        print('Artist is not in the DataBase, we will add it later')
        raise ValueError
    albums = []
    for i in album_list:
        albums.append(i[0])
    return tuple(albums)

def get_songs_in_albums(album):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()

    statement = """
        SELECT Name, Track_Number, Album_Name, (Duration_MS / 1000 / 60) AS Duration, Valence, Energy,
            Tempo, Speechiness, Danceability
        FROM Songs
        WHERE Album_Name = ? 
        """
    insertion = (album,)
    cur.execute(statement,insertion)
    return cur.fetchall()


create_db()
add_artists()
add_songs()
print(get_albums('The Beatles'))
print(get_songs_in_albums('Let It Be (Remastered)'))