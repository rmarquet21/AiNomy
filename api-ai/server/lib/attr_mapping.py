# pylint: disable=consider-using-in
"""
Mapping between Model classes from SQL Alchemy and domain Entities defined
with attr requires boilerplate code to perform the transcription.

The purpose of these functions is to provide helpers to do this transcription.
"""
import json
from enum import EnumMeta
from typing import Type, TypeVar, get_args, List, Any

import attr
from server.domain.entity.base import Record

Model = TypeVar('Model')
Entity = TypeVar('Entity')


def to_entity(entity_class: Type[Entity], model: Model, **kwargs) -> Entity:
    attributes = {f.name for f in attr.fields(entity_class)}
    attributes_info = {f.name: f for f in attr.fields(entity_class)}

    values = {}
    for attribute in attributes:
        try:
            attribute_value = getattr(model, attribute)
            if attribute_value is not None and _is_enum(attributes_info[attribute]):
                values[attribute] = attributes_info[attribute].type(attribute_value)
            elif attribute_value is not None and attributes_info[attribute].type == dict:
                values[attribute] = json.loads(attribute_value)
            elif attribute_value is not None and _is_record_list(attributes_info[attribute].type):
                list_inside_type = get_args(attributes_info[attribute].type)[0]
                values[attribute] = json_deserialize_list(list_inside_type, attribute_value)
            elif attribute_value is not None and _is_record(attributes_info[attribute].type):
                _type = attributes_info[attribute].type
                values[attribute] = json_deserialize_record(_type, attribute_value)
            elif attribute_value is not None or not attributes_info[attribute].default:
                values[attribute] = attribute_value
            elif attributes_info[attribute].default:
                values[attribute] = attributes_info[attribute].default
        except AttributeError:
            pass

    for key, _value in kwargs.items():
        values[key] = kwargs[key]

    entity = entity_class(**values)
    return entity


def create_model(model_class: Type[Model], entity: Entity, **kwargs) -> Model:
    """
    build a new model from the entity object. If the entity has a pid, it can
    be merge in an existing row of database
    """
    attributes = {f.name for f in attr.fields(entity.__class__)}
    attributes_info = {f.name: f for f in attr.fields(entity.__class__)}

    values = {}
    for attribute in attributes:
        if hasattr(model_class, attribute):
            attribute_value = getattr(entity, attribute)
            if _is_enum(attributes_info[attribute]):
                values[attribute] = attribute_value.value
            elif attributes_info[attribute].type == dict:
                values[attribute] = json.dumps(attribute_value)
            elif _is_record(attributes_info[attribute].type):
                _type = attributes_info[attribute].type
                values[attribute] = json_serialize_record(_type, attribute_value)
            elif _is_record_list(attributes_info[attribute].type):
                list_inside_type = get_args(attributes_info[attribute].type)[0]
                values[attribute] = json_serialize_list(list_inside_type, attribute_value)
            else:
                values[attribute] = attribute_value

    for key, _value in kwargs.items():
        values[key] = kwargs[key]

    model = model_class(**values)
    return model


def update_model(model: Model, entity: Entity, **kwargs) -> Model:
    attributes = {f.name for f in attr.fields(entity.__class__)}
    attributes_info = {f.name: f for f in attr.fields(entity.__class__)}

    for attribute in attributes:
        if hasattr(model.__class__, attribute):
            attribute_value = getattr(entity, attribute)
            assert attributes_info[attribute].type is not None, \
                f"entity {entity.__class__} - attribute {attribute} is missing type"

            if attribute == 'pid':
                model_value = getattr(model, attribute)
                if model_value is not None:
                    assert model_value == attribute_value, "pid is the primary key and should not change"

                setattr(model, attribute, attribute_value)
            elif _is_enum(attributes_info[attribute]):
                setattr(model, attribute, attribute_value.value)
            elif attributes_info[attribute].type == dict:
                setattr(model, attribute, json.dumps(attribute_value))
            elif _is_record(attributes_info[attribute].type):
                _type = attributes_info[attribute].type
                setattr(model, json_serialize_record(_type, attribute_value))
            elif _is_record_list(attributes_info[attribute].type):
                list_inside_type = get_args(attributes_info[attribute].type)[0]
                setattr(model, attribute, json_serialize_list(list_inside_type, attribute_value))
            else:
                setattr(model, attribute, attribute_value)

    for key, _value in kwargs.items():
        setattr(model, key, kwargs[key])

    return model


def _is_enum(_attribute: attr.Attribute):
    """
    The enumerations are stored as a character string in the database.

    If the value of the attribute is an instance of the enumeration.
    We must retrieve the value in the form of a character string with the `value` property.
    """
    if hasattr(_attribute, "type"):
        return _attribute.type.__class__ == EnumMeta

    return False


def _is_list(_type: Type):
    return _type.__class__.__name__ == "_GenericAlias"


def _is_record(_type: Type):
    if not hasattr(_type, "__base__"):
        return False

    return _type.__base__ == Record


def _is_record_list(_type: Type):
    is_record_list = False
    if _is_list(_type):
        list_inside_type = get_args(_type)[0]
        if _is_record(list_inside_type):
            is_record_list = True

    return is_record_list


def json_serialize_record(inside_type, attribute_value) -> str:  # pylint: disable=unused-argument
    obj = attr.asdict(attribute_value, value_serializer=value_serializer)
    return json.dumps(obj)


def json_serialize_list(inside_type, attribute_value) -> str:  # pylint: disable=unused-argument
    result = [attr.asdict(obj, value_serializer=value_serializer) for obj in attribute_value]
    return json.dumps(result)


def json_deserialize_list(inside_type, attribute_value) -> List[Any]:
    attributes = {f.name for f in attr.fields(inside_type)}
    attributes_info = {f.name: f for f in attr.fields(inside_type)}

    deserialized_list: List[dict] = json.loads(attribute_value)
    values = []
    for obj in deserialized_list:
        for key in obj:
            if key not in attributes:
                continue

            obj[key] = value_deserializer(attributes_info[key], obj[key])

        values.append(inside_type(**obj))

    return values


def json_deserialize_record(inside_type, attribute_value) -> Any:
    attributes = {f.name for f in attr.fields(inside_type)}
    attributes_info = {f.name: f for f in attr.fields(inside_type)}

    obj = json.loads(attribute_value)
    for key in obj:
        if key not in attributes:
            continue

        obj[key] = value_deserializer(attributes_info[key], obj[key])

    try:
        value = inside_type(**obj)
    except TypeError:
        value = inside_type()

    return value


def value_serializer(inst, field, value):  # pylint: disable=unused-argument
    if field is not None \
            and (field.type.__class__ == EnumMeta or value.__class__.__class__ == EnumMeta):
        return value.value

    return value


def value_deserializer(field, value):
    if field is not None and field.type.__class__ == EnumMeta:
        return field.type(value)

    return value
