import unittest 
from create_database import *
from database_function import *


###################################################
#              Part 1  Access Data                #
###################################################
class TestSpotifyAPI(unittest.TestCase):
    def test_get_artist_info(self):
        res = spotify.get_artist_info("Justin Bieber")
        self.assertEqual(res[0], "1uNFoZAHBGtllmzznpCI3s")

    def test_get_related_artist(self):
        res = spotify.get_related_artist("1uNFoZAHBGtllmzznpCI3s")
        self.assertIn('Shawn Mendes', res)

    def test_get_artist_albums(self):
        res = spotify.get_artist_albums("1uNFoZAHBGtllmzznpCI3s")
        flag = 0
        for i in res:
            n = list(i.keys())
            if n[0] == "Journals":
                flag = 1
        self.assertEqual(flag, 1)

    def test_get_album_tracks(self):
        res = spotify.get_album_tracks("6Fr2rQkZ383FcMqFyT7yPr")
        self.assertEqual(len(res), 19)

class TestGeniusAndLyrics(unittest.TestCase):
    def test_search_song(self):
        res = genius.search_song("Brown Eyes", "Lady Gaga")
        self.assertEqual(res["result"]["api_path"], "/songs/80385")

    def test_get_lyrics(self):
        res = genius.get_lyrics("/songs/80385")
        self.assertEqual(len(res),1230)
    
    def test_get_lyrics_without_api(self):
        res = genius.get_lyrics_without_api("Brown Eyes", "Lady Gaga")
        self.assertEqual(len(res), 1230)





###################################################
#              Part 2  Class                      #
###################################################
class TestClass(unittest.TestCase):
    def test_Artist_init(self):
        artist = Artist(name = "Chen", id = 1, genre = "Pop", popularity = 100, related_artists = ["Sun"])
        self.assertEqual(artist.name, "Chen")

    def test_Artist_str(self):
        artist = Artist(name = "Chen", id = 1, genre = "Pop", popularity = 100, related_artists = ["Sun"])
        string = "Chen, None, Pop, 100"
        self.assertEqual(artist.__str__(), string)
    
    def test_Songs_init(self):
        song = Song(song_id = "1", name = "Happy", track_id = 1, artist = "Chen", album = "Day", popularity = 1, 
                duration_ms = 200, valence = 70, energy = 80, lyrics = "No lyrics")
        self.assertEqual(song.duration_ms, 200)
    
    def test_Songs_str(self):
        song = Song(song_id = "1", name = "Happy", track_id = 1, artist = "Chen", album = "Day", popularity = 1, 
                duration_ms = 200, valence = 70, energy = 80, lyrics = "No lyrics")
        string = "Happy, Chen, Day, 1, No lyrics"
        self.assertEqual(song.__str__(), string)






###################################################
#              Part 3  Construct DataBase         #
###################################################
class TestDatabase(unittest.TestCase):
    def open_json(self):
        try:
            with open('test_songs.json', 'r') as f:
                song_dict = json.loads(f.read())
        except:
            song_dict = {}
        try:
            with open('test_artists.json', 'r') as f:
                artist_dict = json.loads(f.read())
        except:
            artist_dict = {}
        self.artist_dict = artist_dict
        self.song_dict = song_dict
    
    def test_add_artist(self):
        self.open_json()
        create_db()
        check = add_artists(artist_dict = self.artist_dict)
        self.assertTrue(check)
    
    def test_add_songs(self):
        self.open_json()
        create_db()
        add_artists(artist_dict = self.artist_dict)
        check = add_songs(artist_dict = self.artist_dict, song_dict = self.song_dict)
        self.assertTrue(check)


###################################################
#              Part 4  DataBase  Function         #
###################################################
#class TestDB(unittest.TestCase):
def create_test_db():
    try:
        with open('test_songs.json', 'r') as f:
            song_dict = json.loads(f.read())
    except:
        song_dict = {}
    try:
        with open('test_artists.json', 'r') as f:
            artist_dict = json.loads(f.read())
    except:
        artist_dict = {}
    create_db()
    add_artists(artist_dict)
    add_songs(artist_dict, song_dict)
    
class TestDBFunction(unittest.TestCase):
    create_test_db()
    def test_get_artists(self):
        res = get_artists()
        self.assertEqual(res[0][0], "Katy Perry")
    
    def test_get_albums(self):
        res = get_albums("Katy Perry")
        self.assertEqual(res[1][0], "Witness")
    
    def test_get_songs(self):
        res = get_songs("Katy Perry")
        self.assertEqual(res[3][0], "Swish Swish")
    
    def test_get_songs_in_albums(self):
        res = get_songs_in_albums("Witness")
        self.assertEqual(res[5][0], "Power")
        
    def test_get_songs_valences(self):
        res = get_songs_in_albums("Witness")
        self.assertEqual(res[5][0], "Power")
    
    def test_get_lyrics_of_song(self):
        res = get_lyrics_of_song("Power")
        self.assertEqual(len(res[0][0]),1359)


unittest.main(verbosity=2)

