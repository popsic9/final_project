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


| **File**        | **Function**           |
| ------------- |-------------|
| *main.py*      | Show the current artist in database |
| *album.py*      | Show top10 words of the artist, or show all albums of the artist      |
| *songs.py* | Show all songs in the albumshow all songs whose valence are larger than 0.8 or show valence vs. energy of all songs     |
| *lyrics.py* | Show lyrics of the song     |

- In *album.py*, there are two function, *top_10_words* and *plot()*, to show the graph of top 10 words of the title of the songs owned by the artist, using ploty
- In *songs.py*, there is a function called *plot()* to show the valence vs. energy graph, using ploty. Valance is a number to describe whether the song is likely to make listener feel happy or sad.

## User Guide
- Clone the repository.
- Get client secrets and API keys of Spotify and Genius following the instruction. Store the value into `spotify_secret.py` and `genius_secret.py`  separately.
- Run `app.py` and go to the homepage of this search engine, `http://127.0.0.1:5000/`. The homepage will show all the artists in the current database, ordering by their popularity. You can choose a artist in or not in the database. (* If the input artist is not in the database, the termial may ask you to do the OAuth2 authentication, getting the url and pasting into the terminal, and then it may take a quite long time to cache lyrics of all songs of the artist. So please be patient.)




#### Song Visualization
- The song visualization part of this app starts at the root url, ie `http://127.0.0.1:5000/`.
- You should enter an artist that is on Spotify and spell their name *exactly* how it is in Spotify. For example, there is an artist named "ScHoolboy Q", and the 'H' should indeed be capitalized. This helps both Spotify and Genius search for the correct artist.
- If you misspell an artist, there is nothing in the code that will catch it, this is because Spotify will still find an artist that may be the intended artist or something else entirely. For example, Spotify found an when I just searched the letter "K", and the artist didn't even have K as the first letter of their name.
- After you enter the artist, the tables (Songs and Artists) will be filled via the cached data and if the artist doesn't exist in the cache, it will search for that artist as well as one of their related artists (dictated by Spotify).
- It will then cache that data.
- You will then be asked which albums to include in the visualization. You must spell it exactly how it shows up on the site (I recommend copy and pasting it in the form). Don't include the extra comma at the end or the quotation marks.
- Lastly, you will be asked which features to include. Again, you should spell the exactly how they are shown and I recommend copy and pasting it in the form. Then, voila!
- If you want to see a safe example without having to wait for an artist to be searched and cached, start at `http://127.0.0.1:5000` and search "SZA" for the visualization part. Choose Ctrl, Z for the albums. Choose valence, energy for the features. You should get a plot like the one below
- ![alt text](images/sza_plot.png)


#### Song Recommendations
- The url to go to is `http://127.0.0.1:5000/recommend`. Then, enter up to 5 artists, separated by Spotify. As mentioned in the other section, they should be spelled exactly how they're spelled in Spotify. As there are up to 5 artists that must be searched and cached, this may take a while.
- Eventually, you will be asked to rank several song features from 1-5. There is an example to follow on the page. Then, you will receive 20 song recommendations.

The recommendations are given by using your ranking to give each song feature a weight. Then a weighted sum is calculated for each song. We take the average of all weighted sums for the artists that were given, then find the 20 songs whose weighted sum is close to the average weighted sum of the given artists (all songs will be from artists different from the given artists).
- For a safe search for the recommendation part, start at `http://127.0.0.1:5000/recommend` and search "Chance The Rapper, KAYTRANADA". Rank the features 1,2,3,4,5. You should get something like below
- ![alt text](images/recommend.png)

#### Notes
- There might be repeated songs. This is because some artists have both clean and explicit versions of each album or song, so both are captured when getting data from the Spotify API.
- After getting the song visualization, you must restart the app if you want to see a different visualization (instead of just pressing backspace). This is due to how the plot html is utilized in the code.
- If length_lyrics has value 0, then that means the song was found via spotify, but the request for the lyrics via Genius failed.
- The song recommendation will probably suck. This is because it depends on what's already cached. There might not be many artists that are related to the ones you specify (I try to remedy this by also searching for one related artist), but no promises hehe.
- Remember, spelling is very important!

#### Other Documentation
- Plotly: [found here](https://plot.ly/python/)


