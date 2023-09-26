import os
from contextlib import contextmanager
from typing import ContextManager, Optional, List

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_injector import FlaskInjector
from injector import Injector, Module, Binder, singleton

from server import ROOT_DIR
from server.domain.datastore import Datastore
from server.domain.repository.category_repository import CategoryRepository
from server.domain.repository.disease_repository import DiseaseRepository
from server.domain.repository.improve_model_repository import ImproveModelRepository
from server.domain.repository.key_factor_repository import KeyFactorRepository
from server.domain.repository.prediction_alzheimer_repository import PredictionAlzheimerRepository
from server.domain.repository.prediction_pneumonia_repository import PredictionPneumoniaRepository
from server.domain.repository.tag_repository import TagRepository
from server.host_context import HostContext
from server.app.web import apis
from server.infrastructure.flask_datastore import FlaskDatastore
from server.infrastructure.repository.database_category_repository import DatabaseCategoryRepository
from server.infrastructure.repository.database_disease_repository import DatabaseDiseaseRepository
from server.infrastructure.repository.database_improve_model_repository import DatabaseImproveModelRepository
from server.infrastructure.repository.database_key_factor_repository import DatabaseKeyFactorRepository
from server.infrastructure.repository.database_tag_repository import DatabaseTagRepository
from server.infrastructure.repository.fake_category_repository import FakeCategoryRepository
from server.infrastructure.repository.fake_disease_repository import FakeDiseaseRepository
from server.infrastructure.repository.fake_key_factor_repository import FakeKeyFactorRepository
from server.infrastructure.repository.fake_prediction_pneumonia_repository import FakePredictionPneumoniaRepository
from server.infrastructure.repository.fake_prediction_alzheimer_repository import FakePredictionAlzheimerRepository
from server.infrastructure.repository.fake_tag_repository import FakeTagRepository
from server.infrastructure.repository.helper.fake_datasources import FakeDatasources
from server.infrastructure.repository.model_prediction_alzheimer_repository import ModelPredictionAlzheimerRepository
from server.infrastructure.repository.model_prediction_pneumonia_repository import ModelPredictionPneumoniaRepository
from server.lib.dynamic_import import load_modules_from_project_directory

_global_injector = None


@contextmanager
def configure_global_injector(host_context: Optional[HostContext] = None) -> ContextManager[Injector]:
    global _global_injector  # pylint: disable=global-statement,invalid-name
    _global_injector = Injector([BindingRules(host_context)])
    yield _global_injector


def get_injector() -> Injector:
    # auto_bind at False is required to manage dependency ingestion
    # on actors
    return Injector([BindingRules()]) if _global_injector is None else _global_injector


class BindingRules(Module):
    def __init__(self, host_context: Optional[HostContext] = None):
        self._host_context: HostContext = host_context if host_context else HostContext()
        self._db = SQLAlchemy()

    def configure(self, binder: Binder):
        fake_data = self._host_context.fake_data()

        binder.bind(HostContext, self._host_context, scope=singleton)
        binder.bind(FakeDatasources, FakeDatasources, scope=singleton)
        binder.bind(PredictionPneumoniaRepository, ModelPredictionPneumoniaRepository if not fake_data else FakePredictionPneumoniaRepository,  scope=singleton)
        binder.bind(PredictionAlzheimerRepository, ModelPredictionAlzheimerRepository if not fake_data else FakePredictionAlzheimerRepository,  scope=singleton)
        binder.bind(DiseaseRepository, DatabaseDiseaseRepository if not fake_data else FakeDiseaseRepository, scope=singleton)
        binder.bind(CategoryRepository, DatabaseCategoryRepository if not fake_data else FakeCategoryRepository, scope=singleton)
        binder.bind(TagRepository, DatabaseTagRepository if not fake_data else FakeTagRepository, scope=singleton)
        binder.bind(KeyFactorRepository, DatabaseKeyFactorRepository if not fake_data else FakeKeyFactorRepository, scope=singleton)
        binder.bind(ImproveModelRepository, DatabaseImproveModelRepository, scope=singleton)

        if not fake_data:
            binder.bind(SQLAlchemy, self._db, scope=singleton)

        binder.bind(Flask, to=self._configure_web)

    def _configure_web(self) -> Flask:
        host_context = self._host_context
        self.__injector__.binder.bind(Datastore, FlaskDatastore, scope=singleton)
        webapp = Flask(__name__)
        webapp.debug = host_context.debug()
        webapp.secret_key = host_context.flask_secret()
        apis.init_app(webapp, host_context)

        if not self._host_context.fake_data():
            webapp.config.update(
                SQLALCHEMY_DATABASE_URI=self._host_context.datastore_connection_string(),
                SQLALCHEMY_TRACK_MODIFICATIONS=False,
                SQLALCHEMY_ENGINE_OPTIONS={
                    "pool_recycle": 1800
                })

            self._db.init_app(webapp)

        FlaskInjector(app=webapp, injector=self.__injector__)

        return webapp


def _load_models() -> List:
    models: List = []
    apis_path = os.path.join(ROOT_DIR, 'server', 'infrastructure', 'model')
    modules = load_modules_from_project_directory(apis_path, 'server.infrastructure.model')
    for module in modules:
        models.extend([cls for cls in module.__dict__.values() if hasattr(cls, '__table__')])

    return models
