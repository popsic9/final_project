from flask import Blueprint, render_template, request
from create_database import *
import requests

lyrics = Blueprint('lyrics', __name__,template_folder='templates')

@lyrics.route('/lyrics', methods = ['GET'])
def index():
    song = request.args.get('song')
    if song:
        try:
            lyrics = get_lyrics_of_song(song)
        except:
            lyrics = ('The Name is Wrong, Please Return',)
    return render_template('lyrics.html', song = song, lyrics = lyrics)