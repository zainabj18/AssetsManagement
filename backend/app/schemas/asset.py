from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field, ValidationError, validator

from app.db import DataAccess
from .tag import TagBase

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


class AssetBase(BaseModel):
    name: str
    link: str
    type: str
    description: str
    projects: List[int]
    tags: List[int]
    classification: DataAccess
    metadata: List[Attribute]

    class Config:
        json_encoders = {
            DataAccess: "lambda v: v.value",
        }

    @validator("metadata", each_item=True, pre=True)
    def check_metadata(cls, v):
        try:
            Attribute(**v)
        except ValidationError as e:
            raise e
        return v


class AssetBaseInDB(AssetBase):
    created_at: Optional[datetime]
    last_modified_at: Optional[datetime]
