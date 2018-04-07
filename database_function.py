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


###################################################
#              Date Processing Functions          #
###################################################
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
    conn.close()

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

