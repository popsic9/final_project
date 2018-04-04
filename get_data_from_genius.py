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

def parse_lyrics(lyrics):
    lyrics = re.sub("\n\n", " ", lyrics)
    lyrics = re.sub("\n", " ", lyrics)
    lyrics = re.sub('  ', ' ', lyrics).strip()
    lyrics = re.sub("([\(\[]).*?([\)\]])", '', lyrics)
    lyrics = re.sub('[^\w\s]', '', lyrics)
    return lyrics

def get_lyrics(song_url):
    global headers
    base_url = "https://api.genius.com"
    
    url = base_url + song_url
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
    lyrics = parse_lyrics(lyrics)
    return lyrics

def get_lyrics_without_api(song_title, artist_name):
    artist = '-'.join(artist_name.split())
    song_title = '-'.join(song_title.split())
    base = "https://genius.com/" + '-'.join([artist, song_title]) + '-lyrics'
    print(base)
    response = requests.get(base)
    # if the request was successful, try to scrape the lyrics
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        #[h.extract() for h in soup('script')]
        lyrics = soup.find("div", class_="lyrics").get_text()
        lyrics = parse_lyrics(lyrics)
        return lyrics
    return None

def get_cached_lyrics():
    for artist, value in artist_dict.items():
        if song_dict.get(artist):
            print("Getting data for {}".format(artist))
            continue
        song_dict[artist] = {}
        print('Making Requests for Song Lyrics for {}'.format(artist))
        for album in value['albums']:
            album_name = list(album.keys())[0]
            for song_id, song_features in album[album_name].items():
                if song_dict.get(song_id):
                    continue
                song_title = song_features[1].split('-')[0].strip()
                print(song_title, artist)
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




#get_lyrics("/songs/82381")


get_cached_lyrics()
# text = get_lyrics_without_api('Hey Jude','The Beatles')
# print(text)
# text = search_song('Hey Jude','The Beatles')
# print(text)

# text = search_song('Ticket To Ride', 'The Beatles')
# print(text)