import os
from typing import List

from flask import Flask, Blueprint
from flask_restx import Api, Namespace

from server import ROOT_DIR
from server.host_context import HostContext
from server.lib.dynamic_import import load_modules_from_project_directory

blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(
    blueprint,
    title='Ainomy - Internal Api' + (' (fake)' if HostContext().fake_data() else ' (local)'),
    version='1.0',
    description='Internal API of Ainomy. The signature of endpoints can change any time without notification',
    doc='/'
)


def init_app(flask: Flask, host_context: HostContext):
    """
    Integration by blueprint allows you to have several instances of Flask RestX.
    Governance of the endpoint group is easier. It is possible to hide the documentation
    of the internal API and to leave the documentation of the public API accessible.
    """
    if not host_context.debug():
        # In operation, especially on production, we don't want the swagger documentation to be
        # visible.
        api._doc = False  # pylint: disable=protected-access

    flask.register_blueprint(blueprint)
    namespaces = load_api_endpoints()
    for namespace in namespaces:
        api.add_namespace(namespace)


def load_api_endpoints() -> List[Namespace]:
    namespaces: List[Namespace] = []
    apis_path = os.path.join(ROOT_DIR, 'server', 'app', 'web', 'apis', 'namespaces')
    modules = load_modules_from_project_directory(apis_path, 'server.app.web.apis.namespaces')
    for module in modules:
        if hasattr(module, 'api') and isinstance(module.api, Namespace):
            namespaces.append(module.api)

    namespaces = sorted(namespaces, key=lambda n: n.name)
    return namespaces
