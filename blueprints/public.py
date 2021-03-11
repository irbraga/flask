'''
Module to define a Blueprint for Public access.
'''
from flask import Blueprint
from flask_restx import Api
from namespaces.public.authentication import auth_ns
from namespaces.public.info import info_ns

public_blueprint = Blueprint(name='public', import_name=__name__, url_prefix='/public')

public_api = Api(public_blueprint,
                    title='Public API',
                    description='Api endpoints with public access.',
                    version='00.01',
                    default_mediatype='application/json')

public_api.add_namespace(auth_ns)
public_api.add_namespace(info_ns)
