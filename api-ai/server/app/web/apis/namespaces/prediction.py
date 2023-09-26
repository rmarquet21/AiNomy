from flask_restx import Namespace, Resource
from injector import inject
from werkzeug.datastructures import FileStorage

from server.domain.repository.prediction_alzheimer_repository import PredictionAlzheimerRepository
from server.domain.repository.prediction_pneumonia_repository import PredictionPneumoniaRepository

api = Namespace(name="Prediction", path='/predict', description='Pneumonia prediction')

upload_parser = api.parser()
upload_parser.add_argument('img', location='files', type=FileStorage, required=True)


@api.route('/pneumonia')
@api.expect(upload_parser)
class PredictionResourcePneumonia(Resource):

    @inject
    def __init__(self, *args, model_prediction_pneumonia_repository: PredictionPneumoniaRepository, **kwargs):
        self.model_prediction_pneumonia_repository = model_prediction_pneumonia_repository
        super().__init__(*args, **kwargs)

    def post(self):
        args = upload_parser.parse_args()
        img_bytes = args['img'].read()
        if img_bytes is None:
            return {'error': 'img is required'}, 400
        return self.model_prediction_pneumonia_repository.get_prediction_pneumonia(img_bytes)


@api.route('/alzheimer')
@api.expect(upload_parser)
class PredictionResourceAlzheimer(Resource):

    @inject
    def __init__(self, *args, model_prediction_alzheimer_repository: PredictionAlzheimerRepository, **kwargs):
        self.model_prediction_alzheimer_repository = model_prediction_alzheimer_repository
        super().__init__(*args, **kwargs)

    def post(self):
        args = upload_parser.parse_args()
        img_bytes = args['img'].read()
        if img_bytes is None:
            return {'error': 'img is required'}, 400
        return self.model_prediction_alzheimer_repository.get_prediction_alzheimer(img_bytes)
