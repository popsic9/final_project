from app import create_app

if __name__ == '__main__':
    app = create_app()
    print('starting Flask app', app.name)
    app.run(debug = True)