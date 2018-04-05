from flask import Blueprint, render_template, request
from create_database import *
import requests

songs = Blueprint('songs', __name__,template_folder='templates')

@songs.route('/songs', methods = ['GET'])
def index():
    album = request.args.get('album')
    print(artist)
    if album:
        try:
            songs = get_songs_in_albums(album)
            songs_val = get_songs_valences(album)
            if songs_val == []:
                songs_val = [("There is no song whose valence is larger than 0.8 in this album", "")]
        except:
            songs = ('The Name is Wrong, Please Return',)
    return render_template('songs.html', album = album, songs = songs, songs_val = songs_val)
