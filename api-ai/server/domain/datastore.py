from sqlalchemy.orm import Session


class Datastore:

    @property
    def session(self) -> Session:
        raise NotImplementedError
