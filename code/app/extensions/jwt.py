'''
Module for the Flask-JWT-Extended extension configuration.
'''
import uuid
from http import HTTPStatus
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.exceptions import Unauthorized
from app.entities.user import User
from app.entities.blocklist import TokenBlockList

jwt_manager = JWTManager()

# pylint: disable=unused-argument

def generate_tokens(user):
    '''
    Creates an access_token and a refresh_token.
    '''
    access_token = create_access_token(identity=user,fresh=True)
    refresh_token = create_refresh_token(identity=user.uuid)
    return access_token, refresh_token

def renew_access_token(user):
    '''
    Creates an access_token from a refresh_token.
    '''
    return create_access_token(identity=user, fresh=False)

# https://flask-jwt-extended.readthedocs.io/en/stable/api/
@jwt_manager.user_identity_loader
def get_identity(data):
    '''
    Callback executed when setting the identity to create a jwt token.
    '''
    if isinstance(data, uuid.UUID):
        return {
            'uuid': str(data)
        }
    elif isinstance(data, str):
        return {
            'uuid': data
        }
    elif isinstance(data, dict):
        return {
            'uuid': data['uuid']
        }

    return {
        'uuid': str(data.uuid),
        'name': data.name,
        'position': data.position,
        'role': data.role.name
    }

@jwt_manager.user_lookup_loader
def get_user(jwt_header, jwt_data):
    '''
    Callback executed when current_user/get_current_user()/get_jwt_identity() is invoked any place
    in the API using the flask_jwt_extended proxy object.
    '''
    return User.find_by_uuid(jwt_data['sub']['uuid'])

@jwt_manager.user_lookup_error_loader
def user_not_found(jwt_header, jwt_data):
    '''
    Callback executed when the user is not found using the UUID extrated from token.
    '''
    return {
        'message': 'Invalid token. Unregistered user extracted from token.'
    }, HTTPStatus.UNAUTHORIZED

@jwt_manager.token_in_blocklist_loader
def check_jwt_blocklist(jwt_header, jwt_data):
    '''
    Callback executed when receive a token to check if its already blocked.
    '''
    return TokenBlockList.is_blocked(jwt_data['jti'])

@jwt_manager.revoked_token_loader
def token_revoked_message(jwt_header, jwt_data):
    '''
    Callback executed when a token is blocked.
    '''
    return {
        'message': 'Token is blocklisted.'
    }, HTTPStatus.UNAUTHORIZED

@jwt_manager.unauthorized_loader
def override_unauthorized_message(message):
    '''
    Overrriding the default behavior when a jwt token is used.
    '''
    raise Unauthorized('JWT token was not provided.')
