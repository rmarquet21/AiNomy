import unittest
from datetime import datetime

from server.domain.entity.category import Category
from server.domain.entity.disease import Disease
from server.domain.entity.key_factor import KeyFactor
from server.domain.entity.tag import Tag
from server.infrastructure.model.category_model import CategoryModel
from server.infrastructure.model.disease_model import DiseaseModel
from server.infrastructure.model.tag_model import TagModel
from server.lib import attr_mapping


class TestAttrMapping(unittest.TestCase):
    def setUp(self):
        pass

    def test_to_entity_should_load_model(self):
        # Assign
        model = Disease(
            name="test",
            description="test",
            category_id=getCategory('test').id,
            key_factor_id_1=getKeyFactor('test').id,
            key_factor_id_2=getKeyFactor('test').id,
            key_factor_id_3=getKeyFactor('test').id,
            key_factor_id_4=getKeyFactor('test').id,
            tag_id_1=getTag('test', 'FFFFFF').id,
            tag_id_2=getTag('test', 'FFFFFF').id,
            tag_id_3=getTag('test', 'FFFFFF').id,
            tag_id_4=getTag('test', 'FFFFFF').id,
        )

        # Acts
        entity = attr_mapping.to_entity(Disease, model)

        # Assert
        self.assertEqual("test", entity.name)

    def test_to_model_should_transform_entity_into_model(self):
        # Assign
        entity = Disease(
            name="test",
            description="test",
            category_id=getCategory('test').id,
            key_factor_id_1=getKeyFactor('test').id,
            key_factor_id_2=getKeyFactor('test').id,
            key_factor_id_3=getKeyFactor('test').id,
            key_factor_id_4=getKeyFactor('test').id,
            tag_id_1=getTag('test', 'FFFFFF').id,
            tag_id_2=getTag('test', 'FFFFFF').id,
            tag_id_3=getTag('test', 'FFFFFF').id,
            tag_id_4=getTag('test', 'FFFFFF').id,
        )

        # Acts
        model: DiseaseModel = attr_mapping.create_model(DiseaseModel, entity)

        # Assert
        self.assertEqual("test", model.name)

    def test_create_model_should_transform_entity_dict_to_json_in_the_model(self):
        # Assign
        entity = getCategory(name='test')

        # Acts
        model: CategoryModel = attr_mapping.create_model(CategoryModel, entity, id=1)

        # Assert
        self.assertEqual({'id': 1, 'name': 'test'}, model.payload)

    def test_update_model_should_transform_entity_dict_to_json_in_the_model(self):
        # Assign
        entity = getTag(
            name='test',
            color='AAAAAA',
        )

        model_to_update = TagModel(
            name='test',
            color='FFFFFF',
        )

        # Acts
        model = attr_mapping.update_model(model_to_update, entity, id=1)

        # Assert
        self.assertEqual({'id': 1, 'name': 'test', 'color': 'AAAAAA'}, model.payload)


def getCategory(name):
    return Category(id=1, name=name, created_at=datetime.now(), updated_at=datetime.now())


def getKeyFactor(name):
    return KeyFactor(name=name, created_at=datetime.now(), updated_at=datetime.now())


def getTag(name, color):
    return Tag(name=name, color=color, created_at=datetime.now(), updated_at=datetime.now())


if __name__ == '__main__':
    unittest.main()
