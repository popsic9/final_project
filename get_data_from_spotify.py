import requests_oauthlib
import requests
import json
from spotify_secret import *
import webbrowser
import re
from datetime import datetime
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

CLIENT_ID = client_id
CLIENT_SECRET = client_secret

CACHE_FNAME = "artists.json"
TOKEN = 'spotify_token.json'

AUTHORIZATION_URL = 'https://accounts.spotify.com/authorize'
REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth'
TOKEN_URL = 'https://accounts.spotify.com/api/token'

def check_if_cached(cache_name):
    try:
        with open(cache_name, 'r') as cache_file:
            cache_json = cache_file.read()
            CACHE_DICTION = json.loads(cache_json)
    except:
        CACHE_DICTION = {}
    return CACHE_DICTION


###################################################
#                     Token                       #
###################################################
def get_token_from_cache():
    with open(TOKEN, 'r') as f:
        token_json = f.read()
        token_dict = json.loads(token_json)
        return token_dict

def save_token(token_dict):
    token_dict['timestamp'] = datetime.now().strftime(DATETIME_FORMAT)
    
    with open(TOKEN, 'w') as f:
        token_json = json.dumps(token_dict)
        f.write(token_json)

def has_token_expired(timestamp_str):
    now = datetime.now()
    cache_timestamp = datetime.strptime(timestamp_str, DATETIME_FORMAT)
    delta = datetime.now() - cache_timestamp
    if delta.seconds > 3600:
        return True 
    else:
        return False  


###################################################
#                 Authentication                  #
###################################################
'''
Get authentication from Spotify
Param: None
Return: an oauth2inst instance
'''
def authentication_session():
    # if the token has never been saved, assign it to None
    try:
        token = get_token_from_cache()
    except FileNotFoundError:
        token = None
    # if token was cached and hasn't expired
    if token:
        if not has_token_expired(token['timestamp']):
            oauth2inst = requests_oauthlib.OAuth2Session(CLIENT_ID, token=token)
            return oauth2inst
    # If token either doesn't exist or has expired
    print('Getting token...')
    oauth2inst = requests_oauthlib.OAuth2Session( CLIENT_ID, redirect_uri = REDIRECT_URI)
    authorization_url, state = oauth2inst.authorization_url(AUTHORIZATION_URL)
    webbrowser.open(authorization_url)
    authorization_response = input('Authenticate and then enter the full callback URL: ').strip()
    token = oauth2inst.fetch_token(TOKEN_URL, authorization_response = authorization_response, client_secret = CLIENT_SECRET)
    save_token(token)
    return oauth2inst


###################################################
#                  Cache Data                     #
###################################################
'''
Get Data from cache and store new data into cache
Params: name of the artist
Return: cached informaiton of the artist
'''
def get_cached_data(artist_name):
    cached_artist_data = check_if_cached(CACHE_FNAME)
    artist_dict = cached_artist_data.get(artist_name)

    if artist_dict:
        print("Getting Cached Data for artist {}".format(artist_name))
        return artist_dict
    else:
        print('Making a request for new artist info: {}'.format(artist_name))

        artist_dict = {'info': {}, 'albums': {}}

        artist_info = get_artist_info(artist_name)
        artist_dict['info'] = artist_info

        artist_id = artist_info[0]
        album_list = get_artist_albums(artist_id)
        artist_dict['albums'] = album_list

        cached_artist_data[artist_name] = artist_dict
        with open(CACHE_FNAME, 'w') as f:
            f.write(json.dumps(cached_artist_data))
        return artist_dict



###################################################
#               Processing Data                   #
###################################################
def cleanWord(word):
    word = re.sub("'", "", word)
    word = re.sub('"', '', word)
    return word


'''
Get artist information
Param: an artist's name
Return: a dictionary of the artist's information
        {'info': { artists informaiton }, 'albums': { all albums of the artist}}
'''
def get_artist_info(artist_name):
    # get the url needed to make the oauth2 request
    artist = {'q': "{}".format(artist_name), 'type': 'artist'}
    artist_url = requests.get("https://api.spotify.com/v1/search", artist).url
    
    oauth2inst = authentication_session()
    artist = oauth2inst.get(artist_url)

    # access the dictionary with the desired information
    artist_info = json.loads(artist.text)['artists']['items'][0]
    try:
        artist_genre = artist_info.get('genres')[0]
    except:
        artist_genre = None
    artist_id = artist_info.get('id')
    artist_popularity = artist_info.get("popularity")
    related_artists = get_related_artist(artist_id)

    artist_info = [artist_id, artist_genre, artist_popularity, related_artists]
    
    return artist_info


'''
Get artist information
Param: an artist's id
Return: an list of related artists
'''
def get_related_artist(artist_id, limit = 3):
    base_url = "https://api.spotify.com/v1/artists/{}/related-artists".format(artist_id)
    oauth2inst = authentication_session()
    related_artists = oauth2inst.get(base_url).text

    related_list = json.loads(related_artists)['artists']
    related_artists = []
    for i in range(limit):
        related_artists.append(cleanWord(related_list[i]['name']))
    return related_artists



'''
Get albums information of an artist
Param: an artist's id
Return: an dictionary of albums inforamtions
        {'albumId':{ all songs in this album}, 'pop'{ popularity }}
'''
def get_artist_albums(artist_id):
    """ track_id: track name, ID, number, and duration, energy,
        valence
    """
    base_url = "https://api.spotify.com/v1/artists/{}/albums".format(artist_id)
    artist_params = {"album_type": "album"}
    album_url = requests.get(base_url, artist_params).url
    oauth2inst = authentication_session()
    album_session = oauth2inst.get(album_url)

    albums_info = json.loads(album_session.text)['items']
    album_dict = {}
    for album in albums_info:
        url = 'https://api.spotify.com/v1/albums/' + album['id']
        detail_url = requests.get(url).url
        oauth2inst2 = authentication_session()
        detail_text = oauth2inst2.get(detail_url).text
        json_dict = json.loads(detail_text)
        popularity = json_dict["popularity"]

        album_name = cleanWord(album['name'])
        album_dict[album_name] = [album['id'], popularity]
    album_list = []
    for album_name, value in album_dict.items():
        track_dict = get_album_tracks(value[0])
        pop = value[1]
        if track_dict is None:
            continue
        album_list.append({album_name: [pop, track_dict]})
    return album_list



'''
Get songs information of an album
Param: id of the album
Return: an dictionary of songs inforamtions
        {'songId':{ 'track_number':{}, 'track_name':{}, 'duration_ms': {}}}
'''
def get_album_tracks(album_id):
    tracks_url = "https://api.spotify.com/v1/albums/{}/tracks".format(album_id)
    oauth2inst = authentication_session()
    tracks = oauth2inst.get(tracks_url)
    tracks_info = json.loads(tracks.text)['items']
    track_dict = {}
    for track in tracks_info:
        track_name = cleanWord(track.get('name'))
        track_dict[track['id']] = [track.get("track_number"), track_name, track.get('duration_ms')]
    track_dict = get_track_info(track_dict)
    return track_dict
    
'''
Add audio features to above songs dictionary
Param: an dictionary of songs inforamtions
Return: an dictionary of songs inforamtions
        {'songId':{ 'track_number':{}, 'track_name':{}, 'duration_ms': {}, 
                    'energy':{}, 'valence':{}}}
'''
def get_track_info(track_dict):
    track_keys_by_number = sorted(track_dict.items(), key = lambda x: x[1][0])
    track_keys_by_number = [x[0] for x in track_keys_by_number]
    url = 'https://api.spotify.com/v1/audio-features?ids={}'.format(','.join(list(track_dict.keys())))
    oauth2inst = authentication_session()
    track_features = oauth2inst.get(url)
    features = json.loads(track_features.text)
    features = features['audio_features']
    for ind, key in enumerate(track_keys_by_number):
        feats = features[ind]
        if feats is None:
            return None
        else:
            energy = feats.get('energy')
            valence = feats.get('valence')
            more_info = [energy,valence]
            track_dict[key].extend(more_info)
    return track_dict

