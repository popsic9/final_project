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
