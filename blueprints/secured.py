'''
Module to define a Blueprint for Authtenticated users.
'''
from flask import Blueprint
from flask_restx import Api
from blueprints import __auth_types
from namespaces.secured.profile import profile_ns

secured_blueprint = Blueprint(name='secured', import_name=__name__, url_prefix='/secured')

secured_api = Api(secured_blueprint,
                title='Secured API',
                description='Api endpoints for authenticated users.',
                version='00.01',
                default_mediatype='application/json',
                authorizations=__auth_types)

secured_api.add_namespace(profile_ns)
