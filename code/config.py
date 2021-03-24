'''
Module with the variables for Flask and other extensions.
'''
import os
import datetime

# pylint: disable=too-few-public-methods

class DefaultConfig:
    '''
    Class config for Flask and other extensions.
    '''

    # Flask-JWT-Extended
    JWT_SECRET_KEY = 'andromeda'
    JWT_BLACKLIST_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

    # Flask-SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'

class UnitTestConfig:
    '''
    Class for server configuration.
    '''

    # Flask
    TESTING = True

    # Flask-JWT-Extended
    JWT_SECRET_KEY = 'nepal'
    JWT_BLACKLIST_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=5)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(seconds=15)

    # Flask-SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://' # In-memory database

class ProductionConfig:
    '''
    Class for server configuration.
    '''

    # Flask
    TESTING = False

    # Flask-JWT-Extended
    JWT_SECRET_KEY = '$b?(7,zI{UqKm0.:R8g+RCt1,LJ}#r|q'
    JWT_BLACKLIST_ENABLED = True
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)

    # Flask-SQLAlchemy
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod-database.db'

__env_config = dict (
    localhost=DefaultConfig,
    unittest=UnitTestConfig,
    production=ProductionConfig
)

server_config = __env_config.get(os.getenv('APP_CONFIG_ENVIRONMENT', 'localhost'))
