# Songs and Lyrics Search Engine

## Synopsis
The goal of this project is to make a web page for searching artists and displaying albums, songs and lyrics using Python3, Flask, and SQLite.

## Data Sources
1. Spotify API
- OAuth2: Need client_id and client_secret
- Instruction [found here](https://developer.spotify.com/web-api/tutorial/)
- Save clident_id and client_secret into 'spotify_secret.py'
    ```Python3
    client_id = 'xxxxxxxxxxx'
    client_secret = 'xxxxxxxxxxxxxx'
    ```
2. Genius API
- API Key: Need client_id, client_secret and client_token
- Instruction [found here](https://docs.genius.com/)
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
- `get_data_from_spotify.py`

2. Using Genius API to search the api_path of the lyrics of the song by using the artist name and song name in artist.json. Once the user gets the api_path of the lyrics, he/she can get the lyrics via api_path.
- The user can't get api_path if aliaing problems between different APIs happen.(Same artist, different name in Spotify and Genius) To solve this issue, the user will search the exact url of the page of the song and then manually scrapes the lyrics from the page.
- All the lyrics will be cached in 'songs.json'
- `get_data_from_genius.py`
3. Creating 2 classes, one is Artist and the other is Song.
    Creating a Database called SpotifyAndGenius and add two tables, *Songs* and *Artists* using sqlite3. Add the information of Artist and Song instances into database.
- `create_database.py`
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
- `database_function.py`
5. Four testcases testing basic functions of the above code, using unittest.
- `test_cases.py`
6. Run the app. All the code of the web (controller/main, static, templates) are in app folder.

- `app.py`


| **File**        | **Function**           |
| ------------- |-------------|
| *main.py*      | Show the current artist in database |
| *album.py*      | Show top10 words of the artist, or show all albums of the artist      |
| *songs.py* | Show all songs in the albumshow all songs whose valence are larger than 0.8 or show valence vs. energy of all songs     |
| *lyrics.py* | Show lyrics of the song     |

- In `album.py`, there are two function, *top_10_words* and *plot()*, to show the graph of top 10 words of the title of the songs owned by the artist, using ploty
- In `songs.py`, there is a function called *plot()* to show the valence vs. energy graph, using ploty. Valance is a number to describe whether the song is likely to make listener feel happy or sad.

## User Guide
- Clone the repository.
- Get client secrets and API keys of Spotify and Genius following the instruction. Store the value into `spotify_secret.py` and `genius_secret.py`  separately.
- Run `app.py` and go to the homepage of this search engine, `http://127.0.0.1:5000/`. The homepage will show all the artists in the current database, ordering by their popularity, using HTML table. You can choose a artist in or not in the database. (* If the input artist is not in the database, the termial may ask you to do the OAuth2 authentication, getting the url and pasting into the terminal, and then it may take a quite long time to cache information and lyrics of all songs of the artist and add them into database. So please be patient.)


#### Artist Infomation Page
- After you put in the artist name and click submit button, the webbrowser will direct you to the artist's information page.
- There are two links, `Show Albums` and `Show Top 10`. One is directed to the albums page to show all albums of a this artist, ordered by popularity, using HTML table. The other one is directed to the Top10 page to show a plotly bar chart of top 10 words of the title of the songs owned by the artist.

#### Albums Page
- Like homepage, you can put in the album name and click submit button to go to the album information page.

#### Album Information Page
- After you put in the album name and click submit button, the webbrowser will direct you to the album information page.
- There are three links, `Songs in this album`, `Songs Whose Valence Larger than 0.8` and `Valence vs. Energy`.
- `Songs in this album`: Show all songs in this album, using HTML table
- `Songs Whose Valence Larger than 0.8`: Show all songs whose valence is larger than 0.8, ordered by descending order, using HTML table.
- `Valence vs. Energy`: Show a plotly dot plot of the relationship between valence and energy of different songs in the album. Valance is a number to describe whether the song is likely to make listener feel happy or sad.

#### Lyrics Page
- If you choose `Songs in this album`or  `Songs Whose Valence Larger than 0.8`. You can put in the song name and click submit button to go to lyrics page of the song.

## Other Documentation
- Plotly: [found here](https://plot.ly/python/)


