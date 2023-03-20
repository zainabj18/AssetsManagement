# builds objects for testing
from random import choice, sample, randint
from typing import Optional
from faker import Faker
from app.schemas import Asset, Attribute, Project, TagBase, TypeBase,TagInDB,TypeVersion,Comment
from pydantic_factories import ModelFactory, PostGenerated, Use
f=Faker()

def add_validation_json(name: str, values: dict, *args, **kwds):

    if values["attribute_data_type"] == "num_lmt":
        validation={"min": 4, "max": 10}
    elif values["attribute_data_type"] == "list":
        validation={"type": "text"}
    elif values["attribute_data_type"] == "options":
        validation={"values": f.words(10), "isMulti": True}
    else:
        validation={}
    validation["isOptional"]=False
    return validation


def add_value(name: str, values: dict, *args, **kwds):
    match values["attribute_data_type"]:
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
            return values["attribute_data_type"] + "-" + values["attribute_name"]


class AttributeFactory(ModelFactory):
    __model__ = Attribute

    attribute_data_type = Use(
        choice,
        ["text", "number", "checkbox", "datetime-local", "num_lmt", "options", "list"],
    )
    validation_data = PostGenerated(add_validation_json)
    attribute_value = PostGenerated(add_value)


class AssetFactory(ModelFactory):
    __model__ = Asset
    link=Faker().unique.url()
    assets=[]
    tags = lambda: sample(range(1, 10), k=randint(1, 5))
    projects = lambda: sample(range(1, 10), k=randint(1, 5))
    metadata = lambda: sample(list(AttributeFactory.batch(size=20)), k=5)+[(AttributeFactory.build(attribute_data_type="text",validation_data={"isOptional":True}))]


class ProjectFactory(ModelFactory):
    __model__ = Project


class TagFactory(ModelFactory):
    __model__ = TagBase


class TagInDBFactory(ModelFactory):
    __model__ = TagInDB

class TypeFactory(ModelFactory):
    __model__ = TypeBase

class TypeVersionFactory(ModelFactory):
    __model__ = TypeVersion

class CommentFactory(ModelFactory):
    __model__ = Comment