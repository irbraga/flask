'''
Module to configure the application for tests.
'''
import datetime
import pytest
from wsgi import create_app
from config import UnitTestConfig
from app.extensions.sqlalchemy import db
from app.entities.user import User

@pytest.fixture(scope='module')
def app():
    '''
    Returns an instance of Flask configured for unit testing.
    '''
    flask_app = create_app(UnitTestConfig)

    # Push the application context to refer to Flask-SQAlquemy and
    # make it ready to work.
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/
    with flask_app.app_context():
        db.create_all()
        load_pre_condicions()

        db.session.commit()

    yield flask_app

def load_pre_condicions():
    '''
    Load all preconditions for testing.
    '''
    add_users()

def add_users():
    '''
    Add all users used on tests.
    '''
    joe = User(name='Joe Pesci', position='Sys Admin', role='ADMINISTRATOR',
                birth=datetime.date(year=1943, month=2, day=9),
                username='joe.pesci', password='nickysantoro')

    db.session.add(joe)
