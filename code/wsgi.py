'''
Module with the Flask instance configuration using the factory pattern.
'''
from flask import Flask
from flask.cli import ScriptInfo
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError
from cli import db_cli
from app.extensions.jwt import jwt_manager
from app.extensions.sqlalchemy import db
from app.blueprints.admin import admin_blueprint
from app.blueprints.public import public_blueprint
from app.blueprints.secured import secured_blueprint
from config import DefaultConfig

# pylint: disable=unused-variable

def create_app(config):
    '''
    Flask factory method.
    https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/
    '''

    app = Flask(__name__)

    # Checking if the default object is used by FLask
    if isinstance(config, ScriptInfo):
        # Load default configuration
        app.config.from_object(DefaultConfig)
    else:
        # If not, load the configuration file
        app.config.from_object(config)

    # Registering the Blueprints
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(public_blueprint)
    app.register_blueprint(secured_blueprint)

    # Initialising the Flask-SQLAlquemy
    db.init_app(app)

    # Initialising the Flask-Migrate
    Migrate(app, db)

    # Initialising the Bcrypt-Flask
    Bcrypt(app)

    # Initialising the Flask-Jwt-Extended
    jwt_manager.init_app(app)

    # Adding command line to initialize the database with some data
    app.cli.add_command(db_cli)

    # Handling errors
    @app.errorhandler(BadRequest)
    @app.errorhandler(Unauthorized)
    @app.errorhandler(InternalServerError)
    def handle_bad_request(error):
        '''
        Handling errors.
        '''
        return {
            'message': error.message
        }, error.code

    # Request teardown callback
    @app.teardown_request
    def teardown_request(exception):
        '''
        At the end of a request, check if any exception occured.
        If it's True, rollback the session database transaction.
        Otherwise, commit.
        '''
        if exception:
            db.session.rollback()
        else:
            db.session.commit()

    return app
