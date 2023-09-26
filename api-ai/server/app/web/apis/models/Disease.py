from flask_restx import OrderedModel, fields

tag_fields = {
    'name': fields.String(required=True, description='Tag name'),
    'color': fields.String(required=True, description='Tag color')
}

key_factor_fields = {
    'name': fields.String(required=True, description='Key factor name')
}

model = OrderedModel('Disease', {
    'name': fields.String(required=True, description='Disease name'),
    'description': fields.String(required=True, description='Disease description'),
    'key_factors': fields.List(fields.Nested(key_factor_fields), required=False, description='Key factors'),
    'category': fields.String(required=True, description='Category'),
    'tags': fields.List(fields.Nested(tag_fields), required=False, description='Tags'),
    'created_at': fields.DateTime(required=False, description='Created at'),
    'updated_at': fields.DateTime(required=False, description='Updated at'),
})
