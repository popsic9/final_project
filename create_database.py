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
#                     Create DB                   #
###################################################
'''
    Create the database and two tables: 'Artists', 'Songs'
'''
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



###################################################
#                 Create Two Class                #
###################################################
class Artist():
    def __init__(self, name = "No Name", id = None, genre = "No genre", popularity = None, related_artists = None, json_dict = None):
        self.name = name
        if json_dict is None:
            self.id = None
            self.genre = genre
            self.popularity = popularity
            self.related_artists = related_artists
        else:
            self.id = json_dict['info'][0]
            self.genre = json_dict['info'][1]
            self.popularity = json_dict['info'][2]
            self.related_artists = json_dict['info'][3]
    def __str__(self):
        return "%s, %s, %s, %d"%(self.name, self.id, self.genre, self.popularity)

class Song():
    def __init__(self, song_id = "No id", name = "No Name", track_id = None, artist = "No Artist", album = "No album", popularity = None, 
                duration_ms = None, valence = None, energy = None, lyrics = "No lyrics", json_dict = None):
        self.song_id = song_id
        self.name = name
        self.track_id = track_id
        self.artist = artist
        self.album = album
        self.popularity = popularity
        self.duration_ms = duration_ms
        self.valence = valence
        self.energy = energy
        if json_dict is None:
            self.lyrics = lyrics
        else:
            try:
                self.lyrics = json_dict[self.song_id].strip()
            except:
                self.lyrics = lyrics

    def __str__(self):
        return "%s, %s, %s, %d, %s"%(self.name, self.artist, self.album, self.popularity, self.lyrics)






###################################################
#                   Add Data to DB                #
###################################################
'''
    Get artist information from the cached spotify file and create Artist instance
    Add Artist instance into "Artists" Table
'''
def add_artists(artist_dict):
    try:
        conn = sqlite3.connect(DB_NAME)
    except:
        sys.exit(1)
    cur = conn.cursor()

    for artistName in artist_dict:
        artist = Artist(name = artistName, json_dict = artist_dict[artistName])
        statement = '''
            INSERT INTO 'Artists'
            VALUES(?, ?, ?, ?)
        '''
        insertion = (None, artist.name, artist.genre, artist.popularity)
        cur.execute(statement, insertion)
    conn.commit()
    conn.close()
    return True

'''
    Get artist information from the cached spotify and genius file and create Songs instance
    Lyrics is in genius file, and other information are in spotify file
    Add Song instance into "Songs" Table
'''
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
                song = Song(song_id = song_id,name = song_features[1].split("-")[0].strip(), track_id = song_features[0], 
                            artist = artist, album = album_name, popularity = pop, duration_ms = song_features[2], 
                            valence = song_features[3], energy = song_features[4],json_dict = song_dict[artist])

                statement = '''
                    SELECT Id FROM 'Artists'
                    WHERE Name = ?
                '''
                insertion = (song.artist, )
                cur.execute(statement, insertion)
                id_temp = cur.fetchall()
                artist_id = int(id_temp[0][0])

                statement = '''
                    INSERT INTO 'Songs'
                    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                '''
                insertion = (None, song.name, song.track_id, song.artist, artist_id,song.album, song.popularity,
                            song.duration_ms, song.valence, song.energy, song.lyrics)
                cur.execute(statement, insertion)
    
    conn.commit()
    conn.close()
    return True

