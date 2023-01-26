from pydantic import BaseModel,Field
from typing import List,Any
from app.db import DataAccess

class Attribute(BaseModel):
    attribute_name:str=Field(...,alias="attributeName")
    attribute_type:str=Field(...,alias="attributeType")
    attribute_value:Any=Field(...,alias="attributeValue")
    class Config:
        allow_population_by_field_name = True

class AssetBase(BaseModel):
    name:str
    link:str
    type:str
    description:str
    tags:List[str]
    access_level:DataAccess
    metadata:List[Attribute]