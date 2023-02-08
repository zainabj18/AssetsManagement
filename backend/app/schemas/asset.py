from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field, ValidationError, validator

from app.db import DataAccess

class TagBase(BaseModel):
    id: Optional[int]
    name: str

class Attribute_Model(BaseModel):
    attribute_name: str = Field(..., alias="attributeName")
    attribute_type: str = Field(..., alias="attributeType")
    validation_data: Any = Field(None, alias="validation")


class Attribute(Attribute_Model):
    attribute_value: Any = Field(None, alias="attributeValue")

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
class AssetBase(BaseModel):
    name: str
    link: str
    type: str
    description: str
    projects: List[int]
    tags: List[int]
    classification: DataAccess
    metadata: List[Attribute]


    @validator("metadata", each_item=True, pre=True)
    def check_metadata(cls, v):
        if isinstance(v, Attribute):
            return v
        try:
            Attribute(**v)
            return v
        except ValidationError as e:
            raise e


class AssetBaseInDB(AssetBase):
    created_at: Optional[datetime]
    last_modified_at: Optional[datetime]
