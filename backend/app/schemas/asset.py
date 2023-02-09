from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field, ValidationError, validator,root_validator

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


    @root_validator
    def check_metadata(cls, values):
        t=values.get('attribute_type')
        print(t)
        v=values.get('attribute_value')
        if (t=='list' or (t=='options' and values.get("validation_data").isMulti)) and isinstance(v,str) and v.startswith("{") and v.startswith("{"):
            values['attribute_value']=v[1:-1].split(',')
        if ((t=='num_lmt' or t=='number') and isinstance(v,str) and v.isnumeric()):
            values['attribute_value']=int(v)

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
    created_at: Optional[datetime]
    last_modified_at: Optional[datetime]

class Asset(AssetBase):
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