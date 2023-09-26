import inspect
import os
from pathlib import Path
from typing import Type, TypeVar, List

import fake_store
from server import ROOT_DIR
from server.lib.dynamic_import import load_modules_from_project_directory

KLASS = TypeVar('KLASS')


class FakeDatasources:

    def __init__(self):
        self._bind_domain_objects()
        self._store = fake_store.Store()
        self._load_fake_server()

    def get(self, _klass: Type[KLASS], key: str) -> List[KLASS]:
        return self._store.mutable_collection(_klass, key)

    def _bind_domain_objects(self):
        libs = load_modules_from_project_directory(
            os.path.join(ROOT_DIR, "server/domain/entity"),
            "server.domain.entity",
            recursive=True
        )

        for lib in libs:
            for _klass_name, _klass in lib.__dict__.items():
                if inspect.isclass(_klass):
                    fake_store.bind_class(_klass_name, _klass)

    def _load_fake_server(self):
        fake_dir = os.path.join(ROOT_DIR, "fake/fake_datasources")
        files = list(Path(fake_dir).rglob("*.yml"))

        for file in files:
            relative_path: str = os.path.relpath(file, fake_dir)
            key = relative_path.replace('.yml', '').replace('/', '.')
            try:
                self._store.load_collection(key, str(file))
            except Exception as exception:
                raise ValueError(f"fails to load {key} from {file} - {exception}") from exception
