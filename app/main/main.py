from flask import Blueprint, render_template, request
from create_database import *
from database_function import *
import requests
create_db()
add_artists(artist_dict)
add_songs(artist_dict, song_dict)

main = Blueprint('main', __name__,template_folder='templates')

@main.route('/')
def home():
    artists = get_artists()
    return render_template('index.html', artists = artists)

@main.route('/info')
def show_info():
    artist = request.args.get('artist_name')
    url = '+'.join(artist.split(" "))
    if artist:
        try: 
            album_list = get_albums(artist)
        except:
            # cache new data
            spotify.get_cached_data(artist)
            # open nearest cache file
            with open(SPOTIFY_CACHE, 'r') as f:
                artist_dict = json.loads(f.read())
            # # repeat for related artists
            # for related_artist in artist_dict[artist]['info'][-1]:
            #     spotify.get_cached_data(related_artist)
            # with open(SPOTIFY_CACHE, 'r') as f:
            #     artist_dict = json.loads(f.read())

            # get songs for specified artists and related artists
            genius.get_cached_lyrics(artist_dict)
            with open(GENIUS_CACHE, 'r') as f:
                song_dict = json.loads(f.read())
        
            # put into database
            add_artists(artist_dict)
            add_songs(artist_dict, song_dict)
    return render_template('info.html', artist = artist, url = url)
