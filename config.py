'''
Module with the variables for Flask and other extensions.
'''
import datetime

# pylint: disable=too-few-public-methods

class ServerConfig:
    '''
    Class config for Flask and other extensions.
    '''

    # Flask-JWT-Extended
    JWT_SECRET_KEY = 'andromeda'
    JWT_BLACKLIST_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

    # Flask-SQLAlchemy
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
