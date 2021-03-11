'''
Module with namespace for authentication endpoint services.
'''
from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from werkzeug.exceptions import Unauthorized
from app.entities.user import User
from app.entities.blocklist import TokenBlockList
from app.extensions.jwt import generate_tokens, renew_access_token

auth_ns = Namespace('Authentication',
                        path='/auth',
                        description='Group of functionalities related to the user authentication.')

# pylint: disable=no-self-use

@auth_ns.route('/login')
class LoginResource(Resource):
    '''
    Resource for user login.
    '''

    login_model = auth_ns.model(name='Login', model={
        'username': fields.String(required=True, description='Username.'),
        'password': fields.String(required=True, description='Password.')
    })

    token_model = auth_ns.model(name='JWT Tokens', model={
        'access_token': fields.String(required=True, description='JWT Access Token.'),
        'refresh_token': fields.String(required=True, description='JWT Refresh Token.')
    })

    @auth_ns.expect(login_model, validate=True)
    @auth_ns.marshal_with(token_model)
    @auth_ns.response(HTTPStatus.OK.value, 'Success')
    @auth_ns.response(HTTPStatus.BAD_REQUEST.value, 'Username and/or password are incorrect.')
    def post(self):
        '''
        User login authentication.
        '''
        username = request.json['username']
        password = request.json['password']

        user = User.find_by_username(username)

        if user and user.check_password(password):
            access_token, refresh_token = generate_tokens(user)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        raise Unauthorized('Password verification failed.')

@auth_ns.route('/logout')
class LogoutResource(Resource):
    '''
    Resource for user logout.
    '''
    @auth_ns.response(HTTPStatus.NO_CONTENT.value, 'User loggedout successfully.')
    @auth_ns.response(HTTPStatus.BAD_REQUEST.value, 'Missing JWT Token.')
    @jwt_required()
    def post(self):
        '''
        User system logout.
        '''
        token_block_list = TokenBlockList()
        token_block_list.jti = get_jwt()['jti']
        token_block_list.save()

        return None, HTTPStatus.NO_CONTENT

@auth_ns.route('/renew')
class ReviewAccessTokenResource(Resource):
    '''
    Resource for user's token renew.
    '''
    access_token_model = auth_ns.model(name='Access Token', model={
        'access_token': fields.String(required=True, description='Not fresh JWT Access Token.')
    })

    @auth_ns.response(HTTPStatus.OK.value, 'Success')
    @auth_ns.response(HTTPStatus.UNAUTHORIZED.value, 'Missing JWT Refresh Token.')
    @auth_ns.marshal_with(access_token_model)
    @jwt_required(refresh=True)
    def post(self):
        '''
        Use a refresh token to create a new, not fresh, access_token.
        '''
        user = get_jwt_identity()

        return {
            'access_token': renew_access_token(user)
        }
