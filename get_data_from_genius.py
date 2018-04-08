import requests
from bs4 import BeautifulSoup
import json
from genius_secret import *
import re

GENIUS_CACHE = 'songs.json'
SPOTIFY_CACHE = 'artists.json'
CLIENT_ACCESS_TOKEN = client_token

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


headers = {'Authorization': 'Bearer {}'.format(CLIENT_ACCESS_TOKEN)}

###################################################
#                  Cache Data                     #
###################################################
'''
Get Data from cache and store new data into cache
Params: name of the artist
Return: cached lyrics of the song
'''
def get_cached_lyrics(artist_dict):
    for artist, value in artist_dict.items():
        if song_dict.get(artist):
            print("Getting data for {}".format(artist))
            continue
        song_dict[artist] = {}
        print('Making Requests for Song Lyrics for {}'.format(artist))
        for album in value['albums']:
            album_name = list(album.keys())[0]
            for song_id, song_features in album[album_name][1].items():
                if song_dict.get(song_id):
                    continue
                song_title = song_features[1].split('-')[0].strip()
                print(song_title,'--', artist)
                song_info = search_song(song_title, artist)
                if song_info:
                    song_api_path = song_info["result"]["api_path"]
                    lyrics = get_lyrics(song_api_path)
                    song_dict[artist][song_id] = lyrics
                else:
                    lyrics = get_lyrics_without_api(song_title, artist)
                    if lyrics:
                        song_dict[artist][song_id] = lyrics
                    else:
                        print("Can't find lyrics for {}".format(song_title))
                        continue
    with open(GENIUS_CACHE, 'w') as f:
        f.write(json.dumps(song_dict))




###################################################
#              Functions to Get Data              #
###################################################
'''
Get song information from Genius Api
Param: artist's name, title of the song from cached Spotify
Return: a dictionary of the songs's information
        {'result': {'api_path':{}}}
'''
def search_song(song_title, artist_name):
    global headers
    base_url = "https://api.genius.com"
    url = base_url + "/search"
    search_params = {'q': song_title}
    response = requests.get(url, params = search_params, headers = headers)
    try:
        json_dict = json.loads(response.text)
    except:
        return None
    for song in json_dict["response"]["hits"]:
        if song["result"]["primary_artist"]["name"] == artist_name:
            song_info = song
            return song_info


'''
Get lyrics from Genius Api
Param: api_path
Return: lytics of the song, string
'''
def get_lyrics(api_path):
    global headers
    base_url = "https://api.genius.com"
    
    url = base_url + api_path
    response = requests.get(url, headers = headers)
    json_dict = response.json()
    # get the relative url to the lyrics
    relative_lyrics_url = json_dict["response"]["song"]["path"]
    # create the full url to scrape
    url = "http://genius.com" + relative_lyrics_url
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    #[h.extract() for h in soup('script')]
    lyrics = soup.find("div", class_="lyrics").get_text()
    return lyrics

'''
Get lyrics by scraping Genius webpage
Param: artist's name, title of the song
Return: lytics of the song, string
'''
def get_lyrics_without_api(song_title, artist_name):
    artist = '-'.join(artist_name.split())
    song_title = '-'.join(song_title.split())
    base = "https://genius.com/" + '-'.join([artist, song_title]) + '-lyrics'
    response = requests.get(base)
    # if the request was successful, try to scrape the lyrics
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        #[h.extract() for h in soup('script')]
        lyrics = soup.find("div", class_="lyrics").get_text()
        return lyrics
    return None
