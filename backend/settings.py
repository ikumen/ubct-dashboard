import os
import logging
import urllib
import dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
dotenv.load_dotenv(dotenv_path)


def _getbool_from_str(s):
    """Convert given string into bool value. Defaults to False.
    """
    return (s or '').lower() in ['1', 'y', 'yes', 't', 'true']

class Config:
    """Application wide configurations. Unless explicitly set, each configuration 
    is pull from environment variables.
    """
    APP_NAME = os.environ.get('APP_NAME', 'UBTSCT Data API')
    ENV = os.environ.get('FLASK_ENV')
    DEBUG = _getbool_from_str(os.environ.get('FLASK_DEBUG')) # defaults to False
    SECRET_KEY = os.environ.get('FLASK_SECRET_KEY')
    
    APP_LOG_LVL = os.environ.get('LOG_LVL', logging.WARN)
    URLLIB_LOG_LVL = os.environ.get('URLLIB_LOG_LVL', logging.WARN)
    AZURE_LOG_LVL = os.environ.get('AZURE_LOG_LVL', logging.WARN)

    SLACK_TEAM = os.environ.get('SLACK_TEAM')

    OAUTH_PROVIDERS = { 
        # id:label
        'github': 'GitHub',
        'azure': 'Microsoft'
    }

    GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
    GITHUB_AUTHORIZE_URL = 'https://github.com/login/oauth/authorize'
    GITHUB_AUTHORIZE_PARAMS = {'scope': 'user'}
    GITHUB_ACCESS_TOKEN_URL = 'https://github.com/login/oauth/access_token'
    GITHUB_API_BASE_URL = 'https://api.github.com/'

    AZURE_CLIENT_ID = os.environ.get('AZURE_CLIENT_ID')
    AZURE_CLIENT_SECRET = os.environ.get('AZURE_CLIENT_SECRET')
    AZURE_AUTHORIZE_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/authorize'
    AZURE_AUTHORIZE_PARAMS = {'scope': 'openid profile'}
    AZURE_ACCESS_TOKEN_URL = 'https://login.microsoftonline.com/common/oauth2/v2.0/token'
    AZURE_JWKS_URI = 'https://login.microsoftonline.com/common/discovery/v2.0/keys'

    DB_DRIVER = '{ODBC Driver 17 for SQL Server}'
    DB_SERVER_PORT = 1433
    DB_DATABASE = os.environ.get('DB_DATABASE')
    DB_USERNAME = os.environ.get('DB_USERNAME')
    DB_PASSWORD = os.environ.get('DB_PASSWORD')
    DB_SERVER_HOST = os.environ.get('DB_SERVER_HOST')
    DB_ODBC_URI = f'DRIVER={DB_DRIVER};SERVER={DB_SERVER_HOST};PORT={DB_SERVER_PORT};DATABASE={DB_DATABASE};UID={DB_USERNAME};PWD={DB_PASSWORD}'

    SQLALCHEMY_DATABASE_URI = f'mssql+pyodbc:///?odbc_connect={urllib.parse.quote_plus(DB_ODBC_URI)}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


    def init_app(self, app, silent=False):
        """Good place for additional/derived configurations.
        """
        missing_configs = []
        for attr in dir(self):
            if not attr.startswith('__') and attr.isupper() and getattr(self, attr) in ['', None]:
                missing_configs.append(attr)
        if missing_configs:
            message = f'Missing configs: {missing_configs}'
            if silent: 
                print(message)
            else: 
                raise EnvironmentError(message)

        # No missing or ignoring missing configs
        app.config.from_object(self)
