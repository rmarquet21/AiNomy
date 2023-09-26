from flask_restx import OrderedModel, fields

model = OrderedModel('Report', {
    'id': fields.Integer(required=True, description='Report id'),
    'created_at': fields.DateTime(required=False, description='Created at'),
    'updated_at': fields.DateTime(required=False, description='Updated at'),
    'img_bytes': fields.String(required=True, description='Image bytes'),
    'model_name': fields.String(required=True, description='Model name'),
    'prediction': fields.String(required=True, description='Prediction'),
    'is_valid': fields.Boolean(required=True, description='Is valid'),
})
