# builds objects for testing
from random import choice, sample, randint
from typing import Optional
from faker import Faker
from app.schemas import Asset, AttributeInDB, Project, TagBase, TypeBase,TagInDB
from pydantic_factories import ModelFactory, PostGenerated, Use
f=Faker()

def add_validation_json(name: str, values: dict, *args, **kwds):
    if values["attribute_type"] == "num_lmt":
        return {"min": 4, "max": 10}
    if values["attribute_type"] == "list":
        return {"type": "text"}
    if values["attribute_type"] == "options":
        return {"values": f.words(10), "isMulti": True}
    return {"isOptional": False}


def add_value(name: str, values: dict, *args, **kwds):
    match values["attribute_type"]:
        case "num_lmt":
            return randint(values["validation_data"]["min"],values["validation_data"]["max"])
        case "list":
            return f.words()
        case "options":
            return sample(values["validation_data"]["values"],3)
        case "checkbox":
            return choice([True, False])
        case "number":
            return randint(0,100)
        case "datetime-local":
            return str(f.date_time().isoformat("T","minutes"))
        case _:
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
    link=f.url()
    assets=[]
    tags = lambda: sample(range(1, 10), k=randint(1, 5))
    projects = lambda: sample(range(1, 10), k=randint(1, 5))
    metadata = list(AttributeFactory.batch(size=5))


class ProjectFactory(ModelFactory):
    __model__ = Project


class TagFactory(ModelFactory):
    __model__ = TagBase


class TagInDBFactory(ModelFactory):
    __model__ = TagInDB

class TypeFactory(ModelFactory):
    __model__ = TypeBase
