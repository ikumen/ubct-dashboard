import logging

from flask import Flask, jsonify
from backend import settings, api, frontend, auth, services, datastores, helpers


def create_config_only_app():
    """Create a Flask app with only the settings configured. Serves
    as a base for test, manage, and regular app contexts.
    """
    config = settings.Config()
    app = Flask(config.APP_NAME, static_url_path='')
    config.init_app(app, silent=True)

    logging.basicConfig(level=app.config['APP_LOG_LVL'],
        format='[%(asctime)s] [%(levelname)-8s] %(name)s: %(message)s')

    logging.getLogger('azure').setLevel(app.config['AZURE_LOG_LVL'])
    logging.getLogger('urllib3').setLevel(app.config['URLLIB_LOG_LVL'])
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
    
    return app


def register_oauth_providers(app, cache):
    """Authlib will pickup most of the OAuth provider configs, but we still
    need to explicitly set the JWKS configs as the "well known config" endpoint
    is broken for Azure.
    """
    for id in app.config['OAUTH_PROVIDERS'].keys():
        jwks_config = f'{id.upper()}_JWKS_URI'
        services.oauth_service.register(id, jwks_uri=app.config.get(jwks_config))
    services.oauth_service.init_app(app, cache=cache)


def create_app():
    # Get and build on the Flask app
    app = create_config_only_app()
    
    app.json_encoder = helpers.JSONEncoder

    datastores.db.init_app(app)
    services.user_service.init_app(app)
    services.app_service.init_app(app)
    services.slackuser_service.init_app(app)
    services.slackchannel_service.init_app(app)
    services.slackmessage_service.init_app(app)
    services.slackemoji_service.init_app(app)
    services.slackfile_service.init_app(app)
    services.slackreaction_service.init_app(app)
    services.storage_service.init_app(app)
    
    services.cache.init_app(app)
    register_oauth_providers(app, services.cache)

    app.register_blueprint(frontend.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(api.bp)
    
    app.errorhandler(500)(lambda e: (jsonify(dict(error="Doh, please try again later!")), 500))
    app.errorhandler(404)(lambda e: (jsonify(dict(error="Sorry, we can't seem to find the requested page.")), 404))
    app.errorhandler(401)(lambda e: (jsonify(dict(error="Whoa there buddy, doesn't look like you're authorized.")), 401))
    
    return app
    

