from injector import inject

from flask_restx import Namespace, Resource
from werkzeug.datastructures import FileStorage

from server.domain.entity.improve_model import ImproveModel
from server.domain.repository.improve_model_repository import ImproveModelRepository

api = Namespace(name="Improve Model", path='/improve', description='Improve model')

upload_parser = api.parser()
upload_parser.add_argument('img', location='files', type=FileStorage, required=True)
upload_parser.add_argument('is_valid', location='form', type=bool, required=True)
upload_parser.add_argument('prediction', location='form', type=str, required=True)


@api.route('/<string:model_name>')
@api.expect(upload_parser)
class ImproveModelResource(Resource):
    @inject
    def __init__(self, *args, improve_model_repository: ImproveModelRepository, **kwargs):
        self.improve_model_repository = improve_model_repository
        super().__init__(*args, **kwargs)

    def post(self, model_name: str):
        args = upload_parser.parse_args()

        img_bytes = args['img'].read()
        prediction = args['prediction']
        is_valid = args['is_valid']

        if img_bytes is None:
            return {'error': 'img is required'}, 400
        if prediction is None:
            return {'error': 'prediction is required'}, 400
        if is_valid is None:
            return {'error': 'is_valid is required'}, 400

        entity = ImproveModel(
            img_bytes=img_bytes,
            model_name=model_name,
            prediction=prediction,
            is_valid=is_valid
        )

        self.improve_model_repository.save_improve_model(entity)

        return {'message': 'success'}, 200
