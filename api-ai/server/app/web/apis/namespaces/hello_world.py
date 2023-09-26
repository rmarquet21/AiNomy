from flask_restx import Namespace, Resource

api = Namespace(name="Health", path='/health', description='Health check')
api.param('version', 'Version of the API', type=str, default='1.0')


@api.route('/')
class HealthResource(Resource):

    @api.response(200, 'Success')
    def get(self):
        return {'status': 'ok'}
