from flask_restx import Namespace, Resource, marshal
from injector import inject

from server.app.web.apis.models import Disease
from server.domain.repository.category_repository import CategoryRepository
from server.domain.repository.disease_repository import DiseaseRepository
from server.domain.repository.key_factor_repository import KeyFactorRepository
from server.domain.repository.tag_repository import TagRepository

api = Namespace(name="Details", path='/details', description='Disease details')


@api.route('/<string:disease_name>')
class DetailsResource(Resource):

    @inject
    def __init__(
            self,
            disease_repository: DiseaseRepository,
            category_repository: CategoryRepository,
            tag_repository: TagRepository,
            key_factor_repository: KeyFactorRepository,
            *args,
            **kwargs
    ):
        self.disease_repository = disease_repository
        self.category_repository = category_repository
        self.tag_repository = tag_repository
        self.key_factor_repository = key_factor_repository
        super().__init__(*args, **kwargs)

    def get(self, disease_name):
        disease = self.disease_repository.get_disease_by_name(disease_name)

        if disease is None:
            return {'error': 'Disease not found'}, 404

        disease_details: Disease.model = {
            'name': disease.name,
            'description': disease.description,
            'key_factors': disease.key_factors,
            'category': self._get_category(disease.category_id),
            'tags': disease.tags,
            'created_at': disease.created_at,
            'updated_at': disease.updated_at,
        }

        return marshal(disease_details, Disease.model), 200

    def _get_key_factor(self, key_factor_id):
        if key_factor_id is None:
            return None
        return self.key_factor_repository.get_key_factor_by_id(key_factor_id).name

    def _get_category(self, category_id):
        if category_id is None:
            return None
        return self.category_repository.get_category_by_id(category_id).name

    def _get_tag(self, tag_id):
        if tag_id is None:
            return None
        tag = self.tag_repository.get_tag_by_id(tag_id)
        return {'name': tag.name, 'color': tag.color}


@api.route('/')
class AllDetailsResource(Resource):

    @inject
    def __init__(self, disease_repository: DiseaseRepository, *args, **kwargs):
        self.disease_repository = disease_repository
        super().__init__(*args, **kwargs)

    def get(self):
        diseases = self.disease_repository.get_diseases()
        return [disease.name for disease in diseases], 200
