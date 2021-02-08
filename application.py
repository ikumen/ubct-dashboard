from werkzeug.middleware.proxy_fix import ProxyFix
from backend import factory

app = factory.create_app()
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=app.config['DEBUG'])

