from flask_restx import Namespace, Resource, fields

info_ns = Namespace('Api Information', path='/info', description='Return API\'s information.')

@info_ns.route('/')
class InfoResource(Resource):

    info_model = info_ns.model(name='Api Info', model={
        'author': fields.String(required=True, description='Author\'s name.'),
        'version': fields.String(required=True, description='Application version.')
    })

    @info_ns.marshal_with(info_model)
    def get(self):
        '''
        Retreive information about the API.
        '''
        return {
            'author': 'Igor Ribeiro Braga',
            'version': '00.01'
        }
