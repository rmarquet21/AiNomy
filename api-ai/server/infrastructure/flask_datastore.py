from flask_sqlalchemy import SQLAlchemy
from injector import inject
from sqlalchemy.orm import Session
from server.domain.datastore import Datastore


class FlaskDatastore(Datastore):

    @inject
    def __init__(self, db: SQLAlchemy):
        self._db = db

    @property
    def session(self) -> Session:
        return self._db.session
