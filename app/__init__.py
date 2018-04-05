from flask import Flask
from app.main import *

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)
    app.register_blueprint(songs)
    app.register_blueprint(lyrics)
    app.register_blueprint(albums)
    return app

