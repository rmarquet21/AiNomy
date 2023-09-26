# pylint: disable=invalid-name
from sqlalchemy import Column, DateTime, String, Integer, ForeignKey, Table, func, LargeBinary, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

DeclarativeBase = declarative_base()


class Base(DeclarativeBase):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=True, default=func.now())
    updated_at = Column(DateTime, nullable=True, onupdate=func.now(), default=func.now())


class CategoryModel(Base):
    __tablename__ = 'categories'

    name = Column(String(255), nullable=False)

    @property
    def payload(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class KeyFactorModel(Base):
    __tablename__ = 'key_factors'

    name = Column(String(255), nullable=False)

    @property
    def payload(self):
        return {
            'id': self.id,
            'name': self.name,
        }


class TagModel(Base):
    __tablename__ = 'tags'

    name = Column(String(255), nullable=False)
    color = Column(String(255), nullable=False)

    @property
    def payload(self):
        return {
            'id': self.id,
            'name': self.name,
            'color': self.color,
        }


disease_key_factors = Table('disease_key_factors', Base.metadata,
                            Column('disease_id', Integer, ForeignKey('diseases.id')),
                            Column('key_factor_id', Integer, ForeignKey('key_factors.id'))
                            )

disease_tags = Table('disease_tags', Base.metadata,
                     Column('disease_id', Integer, ForeignKey('diseases.id')),
                     Column('tag_id', Integer, ForeignKey('tags.id'))
                     )


class DiseaseModel(Base):
    __tablename__ = 'diseases'

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship('CategoryModel')
    key_factors = relationship(KeyFactorModel, secondary=disease_key_factors, backref='diseases')
    category_id = Column(Integer, ForeignKey(CategoryModel.id), nullable=False)
    tags = relationship('TagModel', secondary=disease_tags, backref='diseases')

    @property
    def payload(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category.payload,
            'key_factors': [kf.payload for kf in self.key_factors],
            'tags': [tag.payload for tag in self.tags],
        }


class PredictionErrorModel(Base):
    __tablename__ = 'prediction_errors'

    img_bytes = Column(LargeBinary, nullable=False)
    model_name = Column(String(255), nullable=False)
    prediction = Column(String(255), nullable=False)
    is_valid = Column(Boolean, nullable=False)

    @property
    def payload(self):
        return {
            'id': self.id,
            'img_bytes': self.img_bytes,
            'model_name': self.model_name,
            'prediction': self.prediction,
            'is_valid': self.is_valid,
        }
