import datetime
from flask_restx import Namespace, Resource, fields

profile_ns = Namespace('Profile', path='/profile')

@profile_ns.route('/')
class ProfileResource(Resource):

    user_model = profile_ns.model(name='User', model={
        'name': fields.String(required=True, description='User\'s name.'),
        'birth': fields.Date(required=False, description='User\'s brithdate.')
    })

    @profile_ns.marshal_with(user_model)
    def get(self):
        return {
            'name': 'Igor Ribeiro Braga',
            'birth': datetime.datetime.now()
        }
