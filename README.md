# Songs and Lyrics Search Engine

## Synopsis
The goal of this project is to make a web page for searching artists and displaying albums, songs and lyrics using Python3, Flask, and SQLite.

## Data Sources
1. Spotify API
- OAuth2: Need client_id and client_secret
- [Instructiton](https://developer.spotify.com/web-api/tutorial/)
- Save clident_id and client_secret into 'spotify_secret.py'
    ```Python3
    client_id = 'xxxxxxxxxxx'
    client_secret = 'xxxxxxxxxxxxxx'
    ```
2. Genius API
- API Key: Need client_id, client_secret and client_token
- [Instruction](https://docs.genius.com/)
- Save clident_id, client_secret and client_token into 'genius_secret.py'
    ```Python3
    client_id = 'xxxxxxxxxxx'
    client_secret = 'xxxxxxxxxxxxxx'
    client_token = 'xxxxxxxxxxxxx'
    ```
3. Lyrics Page
- Depends on different songs. i.e. https://genius.com/Xxxtentacion-sad-lyrics

## Code
1. Using Spotify API to search an artist information via his name to get {genre, popularity, albums, songs in the albums, songs information} and caching the results into 'artist.json'
- **get_data_from_spotify.py**

2. Using Genius API to search the api_path of the lyrics of the song by using the artist name and song name in artist.json. Once the user gets the api_path of the lyrics, he/she can get the lyrics via api_path.
- The user can't get api_path if aliaing problems between different APIs happen.(Same artist, different name in Spotify and Genius) To solve this issue, the user will search the exact url of the page of the song and then manually scrapes the lyrics from the page.
- All the lyrics will be cached in 'songs.json'
- **get_data_from_genius.py**
3. Creating 2 classes, one is Artist and the other is Song.
    Creating a Database called SpotifyAndGenius and add two tables, *Songs* and *Artists* using sqlite3. Add the information of Artist and Song instances into database.
- **create_database.py**
```Python3
    class Artist():
        def __init__(self, name = "No Name", id = None, genre = "No genre", popularity = None,
                    related_artists = None, json_dict = None):
            pass
    class Song():
        def __init__(self, song_id = "No id", name = "No Name", track_id = None, artist = "No Artist",
                    album = "No album", popularity = None, duration_ms = None,
                    valence = None, energy = None,lyrics = "No lyrics", json_dict = None):
            pass
```
4. All the functions for data processing. i.e.: Getting all artists information from the database, getting all abums information of a specific artist from the database, etc.
- **database_function.py**
5. Four testcases testing basic functions of the above code, using unittest.
- **test_cases.py**
6. Run the app. All the code of the web (controller/main, static, templates) are in app folder.
- **app.py**
| File        | Function           |
| ---------------------------------------------- |:----------------------------------------:|
| main.py      | Show the current artist in database. |

- | album.py      | Show top10 wors of the artist, or show all albums of the artist|
| songs.py | Show all songs in the album, show all songs whose valence are larger than 0.8 or show valence vs. energy of all songs|
| lyrics.py | Show lyrics of the song|





