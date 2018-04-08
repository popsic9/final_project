from flask import Blueprint, render_template, request
from create_database import *
from database_function import *

import re
import operator

import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
import plotly.graph_objs as go
import plotly.offline as offline

albums = Blueprint('albums', __name__,template_folder='templates')

def top_10_words(list_of_songs):
    #Code for Part 2:Analyze Tweets
    the_string = ''
    
    for i in list_of_songs:
        the_string += i[0] + " "
    the_string = re.sub(r'[^\w\d\s]','', the_string)

    word_count = {}
    stop_words = set(stopwords.words('english'))
    tokenized = nltk.word_tokenize(the_string)
    filtered_sentence = [w for w in tokenized if not w.lower() in stop_words]

    for i in filtered_sentence:
        if i in word_count:
            word_count[i] += 1;
        else:
            word_count[i] = 1;

    word_count_sorted = sorted(word_count.items(), key = operator.itemgetter(1))
    word_count_sorted.reverse()

    mostTen = []
    mostCounts = []
    for i in range(10):
        mostTen.append(word_count_sorted[i][0])
        mostCounts.append(word_count_sorted[i][1])
    return [mostTen, mostCounts]

def plot(words_count, artist):
    trace = go.Bar(
            x = words_count[0],
            y = words_count[1],
            text = words_count[0],
            marker = dict(
                color='rgb(158,202,225)',
                line=dict(
                    color='rgb(8,48,107)',
                width=1.5,
            )
        ),
        opacity=0.6
    )
    data = [trace]
    layout = go.Layout(
        title = 'Top 10 Words of ' + artist,
    )
    fig = go.Figure(data = data, layout = layout)
    div = offline.plot(fig, include_plotlyjs=False, output_type='div')
    return div



@albums.route('/albums', methods = ['GET'])
def index():
    artist = request.args.get('artist_name')
    if artist:
        album_list = get_albums(artist)
        song_list = get_songs(artist)
        text = top_10_words(song_list)
        div = plot(text, artist)
        url = '+'.join(artist.split(" "))
    return render_template('albums.html', artist = artist, album_list = album_list, url = url)

@albums.route('/album/info', methods = ['GET'])
def show_info():
    album = request.args.get('album')
    url = '+'.join(album.split(" "))
    hre = "/"
    b = None 
    if album:
        songs = get_songs_in_albums(album)
        if songs == []:
            url = None
            b = 1
    return render_template('album_info.html', artist = album, url = url, hre = hre, b = b)




@albums.route('/top10', methods = ['GET'])
def top_ten():
    artist = request.args.get('artist_name')
    if artist:
        song_list = get_songs(artist)
        text = top_10_words(song_list)
        div = plot(text, artist)
        url = '+'.join(artist.split(" "))
    return render_template('top10.html', artist = artist, url = url, plot = div)
