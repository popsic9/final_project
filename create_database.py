import sqlite3
import get_data_from_spotify as spotify
import get_data_from_genius as genius
import json
import sys


DB_NAME = 'SpotifyAndGenius.sqlite'
GENIUS_CACHE = 'songs.json'
SPOTIFY_CACHE = 'artists.json'
try:
    with open(GENIUS_CACHE, 'r') as f:
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
                'Artist_ID' INTEGER,
                'Album_Name' TEXT,
                'Album_Popularity' INTEGER,
                'Duration_MS' REAL,
                'Valence' REAL,
                'Energy' REAL,
                'Lyrics' TEXT,
                FOREIGN KEY (Artist_ID) REFERENCES Artists (Id)
                );
        '''
        cur.execute(statement)
        conn.commit()
        conn.close()
    except:
        sys.exit(1)


def add_artists(artist_dict):
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
        insertion = (None, artist, genre, artist_popularity)
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def add_songs(artist_dict, song_dict):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()
    for artist in artist_dict:
        #print('-----Artists----{}-------'.format(artist))
        for album in artist_dict[artist]['albums']:
            album_title = list(album.keys())[0]
            album_name = album_title.split('(')[0].strip()
            pop = album[album_title][0]
            for song_id, song_features in album[album_title][1].items():
                try:
                    lyrics = song_dict[artist][song_id]
                except:
                    lyrics = "None"
                track_number, track_name, duration_ms, energy, valence = song_features
                track_name = track_name.split("-")[0].strip()
                statement = '''
                    SELECT Id FROM 'Artists'
                    WHERE Name = ?
                '''
                insertion = (artist, )
                cur.execute(statement, insertion)
                id_temp = cur.fetchall()
                artist_id = int(id_temp[0][0])
                statement = '''
                    INSERT INTO 'Songs'
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                insertion = (None, track_name, track_number, artist, artist_id,album_name, pop,
                            duration_ms, valence, energy, lyrics)
                cur.execute(statement, insertion)
    conn.commit()
    conn.close()

def get_artists():
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()
    statement = '''
        SELECT DISTINCT(Name), Popularity
        FROM Artists
        ORDER BY Popularity DESC
    '''
    cur.execute(statement)
    artists_list = cur.fetchall()
    return artists_list


def get_albums(artist_name):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()

    statement = '''
        SELECT Album_Name, Album_Popularity
        FROM Songs
        WHERE Artist_Name = ?
        GROUP BY Album_Name
        ORDER BY Album_Popularity DESC
    '''
    insertion = (artist_name,)
    cur.execute(statement, insertion)
    album_list = cur.fetchall()
    conn.close()

    if album_list == []:
        print('Artist is not in the DataBase, we will add it later')
        raise ValueError
    return album_list

def get_songs(artist_name):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()

    statement = '''
        SELECT Name
        FROM Songs
        WHERE Artist_Name = ?
    '''
    insertion = (artist_name,)
    cur.execute(statement, insertion)
    song_list = cur.fetchall()
    conn.close()

    if song_list == []:
        print('Artist is not in the DataBase, we will add it later')
        raise ValueError
    return song_list

def get_songs_in_albums(album):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()

    statement = """
        SELECT Name
        FROM Songs
        WHERE Album_Name = ? 
        """
    insertion = (album,)
    cur.execute(statement,insertion)
    res = cur.fetchall()
    conn.close()
    return res

def get_songs_valences(album):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()

    statement = """
        SELECT Name, Valence
        FROM Songs
        WHERE Album_Name = ? AND Valence > 0.8
        ORDER BY Valence DESC
        """
    insertion = (album,)
    cur.execute(statement,insertion)
    res = cur.fetchall()
    conn.close()
    return res

def get_songs_valences_energy(album):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()

    statement = """
        SELECT Name, Valence, Energy
        FROM Songs
        WHERE Album_Name = ?
        """
    insertion = (album,)
    cur.execute(statement,insertion)
    res = cur.fetchall()
    conn.close()
    return res

def get_lyrics_of_song(song):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)

    cur = conn.cursor()

    statement = """
        SELECT Lyrics
        FROM Songs
        WHERE Name = ?
        """
    insertion = (song,)
    cur.execute(statement,insertion)
    res = cur.fetchall()
    conn.close()
    return res

