# builds objects for testing
from random import choice, sample, randint
from typing import Optional

from app.schemas import Asset, AttributeInDB, Project, TagBase, TypeBase
from pydantic_factories import ModelFactory, PostGenerated, Use


def add_validation_json(name: str, values: dict, *args, **kwds):
    if values["attribute_type"] == "num_lmt":
        return {"min": 4, "max": 10}
    if values["attribute_type"] == "list":
        return {"type": "text"}
    if values["attribute_type"] == "options":
        return {"values": ["MIT", "GNU"], "isMulti": True}
    return None


def add_value(name: str, values: dict, *args, **kwds):
    if values["attribute_type"] == "num_lmt":
        return 6
    if values["attribute_type"] == "list":
        return ["hello", "good"]
    if values["attribute_type"] == "options":
        return ["MIT", "GNU"]
    return values["attribute_type"] + "-" + values["attribute_name"]


class AttributeFactory(ModelFactory):
    __model__ = AttributeInDB

    attribute_type = Use(
        choice,
        ["text", "number", "checkbox", "datetime-local", "num_lmt", "options", "list"],
    )
    validation_data = PostGenerated(add_validation_json)
    attribute_value = PostGenerated(add_value)


class AssetFactory(ModelFactory):
    __model__ = Asset
    tags = lambda: sample(range(1, 10), k=randint(1, 5))
    projects = lambda: sample(range(1, 10), k=randint(1, 5))
    metadata = list(AttributeFactory.batch(size=5))


class ProjectFactory(ModelFactory):
    __model__ = Project


class TagFactory(ModelFactory):
    __model__ = TagBase


class TypeFactory(ModelFactory):
    __model__ = TypeBase
