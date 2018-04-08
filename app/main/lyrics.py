from flask import Blueprint, render_template, request
from create_database import *
from database_function import *

lyrics = Blueprint('lyrics', __name__,template_folder='templates')

@lyrics.route('/lyrics', methods = ['GET'])
def index():
    song = request.args.get('song')
    b = None
    if song:
        try:
            lyrics = get_lyrics_of_song(song)
            album = get_album_with_songs(song)
            album = album[0][0]
            url = '+'.join(album.split(" "))
        except:
            lyrics = None
            album = None
            url = None
            b = 1
    return render_template('lyrics.html', song = song, lyrics = lyrics, url = url, album = album, b = b)