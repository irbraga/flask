from flask_restx import Namespace, Resource

system_ns = Namespace('System Admin', path='/system')

@system_ns.route('/')
class SystemAdminResource(Resource):

    def get(self):
        return {
            'message': 'System Admin here!'
        }
