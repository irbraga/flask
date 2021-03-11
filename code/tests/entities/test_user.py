'''
Module with User object testing methods.
'''
from app.entities.user import User
from app.entities.types import RoleType

# pylint: disable=unused-argument

def test_query_user(app, client):
    '''
    Querying for a persisted user.
    '''
    joe = User.find_by_username('joe.pesci')

    assert joe
    assert joe.name == 'Joe Pesci'

    joe_by_uuid = User.find_by_uuid(joe.uuid)

    assert joe_by_uuid
    assert joe_by_uuid.name == 'Joe Pesci'

def test_check_password(app, client):
    '''
    Testing checking the user's password.
    '''
    joe = User.find_by_username('joe.pesci')

    assert joe
    assert joe.check_password('nickysantoro')
    assert joe.password == b'bmlja3lzYW50b3Jv'
    assert not joe.check_password('wrong_password')

def test_list_admin_users(app, client):
    '''
    List all admin users.
    '''

    admin_users = User.list_by_role('ADMINISTRATOR')

    assert admin_users
    assert len(admin_users) == 1
    assert admin_users[0].name == 'Joe Pesci'

    admin_users_enum = User.list_by_role(RoleType.ADMINISTRATOR)

    assert admin_users_enum
    assert len(admin_users_enum) == 1
    assert admin_users_enum[0].name == 'Joe Pesci'
