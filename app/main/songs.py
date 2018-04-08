from flask import Blueprint, render_template, request
from create_database import *
from database_function import *

import plotly.graph_objs as go
import plotly.offline as offline

songs = Blueprint('songs', __name__,template_folder='templates')



def plot(song_list):
    song_title = []
    varience = []
    energy = []
    for i in song_list:
        song_title.append(i[0])
        varience.append(i[1])
        energy.append(i[2])

    trace0 = go.Scatter(
        x = varience,
        y = song_title,
        mode='markers',
        name='Valence',
        marker=dict(
            color='rgba(156, 165, 196, 0.95)',
            line=dict(
                color='rgba(156, 165, 196, 1.0)',
                width=1,
            ),
            symbol='circle',
            size=16,
        )
    )

    trace1 = go.Scatter(
        x = energy,
        y = song_title,
        mode='markers',
        name='Energe',
        marker=dict(
            color='rgba(204, 204, 204, 0.95)',
            line=dict(
                color='rgba(217, 217, 217, 1.0)',
                width=1,
            ),
            symbol='circle',
            size=16,
        )
    )
    data = [trace0, trace1]
    layout = go.Layout(
        title = "Valence vs. Energy of All Songs in the Album",
        xaxis=dict(
            showgrid = False,
            showline = True,
            linecolor = 'rgb(102, 102, 102)',
            titlefont = dict(
                color = 'rgb(204, 204, 204)'
            ),
            tickfont=dict(
                color='rgb(102, 102, 102)',
            ),
            autotick = False,
            tick0 = 0,
            dtick = 0.1,
            ticks='outside',
            tickcolor='rgb(102, 102, 102)',
        ),
        margin=dict(
            l = 250,
            r = 40,
            b = 50,
            t = 80
        ),
        legend=dict(
            font=dict(
                size=10,
            ),
            yanchor='middle',
            xanchor='right',
        ),
        width = 800,
        height=600,
        hovermode='closest',
    )

    fig = go.Figure(data = data, layout = layout)
    div = offline.plot(fig, include_plotlyjs=False, output_type='div')
    return div



@songs.route('/songs', methods = ['GET'])
def index():
    album = request.args.get('album')
    if album:
        songs = get_songs_in_albums(album)
        if songs == []:
            songs = [('The Name is Wrong, Please Return',)]
    return render_template('songs.html', album = album, songs = songs)

@songs.route('/songsVal', methods = ['GET'])
def index_2():
    album = request.args.get('album')
    if album:
        songs_val = get_songs_valences(album)
        if songs_val == []:
            songs_val = [("There is no song whose valence is larger than 0.8 in this album", "")]
    return render_template('songs_val.html', album = album,songs_val = songs_val)

@songs.route('/songs/plot', methods = ['GET'])
def index_3():
    album = request.args.get('album')
    if album:
        songs = get_songs_in_albums(album)
        if songs == []:
            songs = [('The Name is Wrong, Please Return',)]
            div = "<p> The Name is Wrong, Please Return</p>"
        else:
            song_list = get_songs_valences_energy(album)
            div = plot(song_list)
    return render_template('songs_vs.html', album = album, plot = div)