from datetime import datetime
from typing import Any, List, Optional

from app.db import DataAccess
from pydantic import BaseModel, Field, ValidationError, root_validator, validator


class TagBase(BaseModel):
    id: Optional[int]
    name: str = Field(..., min_length=1)

class TagInDB(TagBase):
    id:int

class Attribute_Model(BaseModel):
    attribute_name: str = Field(..., alias="attributeName")
    attribute_type: str = Field(..., alias="attributeType")
    validation_data: Any = Field(None, alias="validation")


class Attribute(Attribute_Model):
    attribute_value: Any = Field(None, alias="attributeValue")
    # cast string to correct type based on attribute type
    @root_validator
    def check_metadata(cls, values):
        t = values.get("attribute_type")
        v = values.get("attribute_value")
        # check if string is actually and array and convert
        if (
            (t == "list" or t == "options")
            and isinstance(v, str)
            and v.startswith("{")
            and v.startswith("{")
        ):
            values["attribute_value"] = v[1:-1].split(",")
        # convert if a number
        if (t == "num_lmt" or t == "number") and isinstance(v, str) and v.isnumeric():
            values["attribute_value"] = int(v)

        return values


class AttributeInDB(Attribute):
    attribute_id: Any = Field(None, alias="attributeID")

    class Config:
        allow_population_by_field_name = True


class Type(BaseModel):
    type_name: str = Field(..., alias="typeName")
    metadata: List[Attribute_Model]


class TypeBase(BaseModel):
    type_id: Optional[int]
    type_name: str


class Project(BaseModel):
    id: Optional[int]
    name: str
    description: str


class AssetBase(BaseModel):
    name: str
    link: str
    type: int
    description: str
    classification: DataAccess

    class Config:
        json_encoders = {
            DataAccess: lambda a: str(a.value),
        }


class AssetBaseInDB(AssetBase):
    asset_id: Optional[int]
    created_at: datetime
    last_modified_at: datetime


class Asset(AssetBase):
    # TODO change to conlist
    projects: List[int]
    tags: List[int]
    metadata: List[AttributeInDB]

    @validator("metadata", each_item=True, pre=True)
    def check_metadata(cls, v):
        if isinstance(v, AttributeInDB):
            return v
        try:
            AttributeInDB(**v)
            return v
        except ValidationError as e:
            raise e


class AssetOut(AssetBaseInDB):
    type: str
    projects: List[Any]
    tags: List[Any]
    metadata: List[AttributeInDB]

class TagCopy(BaseModel):
    to_tag_id:int=Field(..., alias="toTagID")
    assest_ids:List[int]=Field(..., alias="assetIDs")

    class Config:
        allow_population_by_field_name = True
