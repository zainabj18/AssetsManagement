from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field, ValidationError, validator

from app.db import DataAccess


class Attribute(BaseModel):
    attribute_name: str = Field(..., alias="attributeName")
    attribute_type: str = Field(..., alias="attributeType")
    attribute_value: Any = Field(..., alias="attributeValue")

    class Config:
        allow_population_by_field_name = True


class AssetBase(BaseModel):
    name: str
    link: str
    type: str
    description: str
    project: str
    tags: List[str]
    access_level: DataAccess
    metadata: List[Attribute]

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
