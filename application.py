from backend import factory

app = factory.create_app()

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=app.config['DEBUG'])

