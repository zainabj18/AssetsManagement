from datetime import datetime
from typing import Any, List, Optional
from app.db import DataAccess
from pydantic import BaseModel, Field, ValidationError, validator,Extra
from enum import Enum
from .attribute import Attribute
from .project import ProjectInDBBase
from .tag import TagInDB

class QueryOperation(Enum):
    EQUALS = "EQUALS"
    LIKE = "LIKE"
    HAS="HAS"
class QueryJoin(Enum):  
    AND="AND"
    OR="OR"

class AttributeSearcher(BaseModel):
    attribute_id: int = Field(..., alias="attributeID")
    attribute_value: Any = Field(None, alias="attributeValue")
    operation:QueryOperation=QueryOperation.EQUALS

    class Config:
        allow_population_by_field_name = True

class FilterSearch(BaseModel):
    tags:List[int]=[]
    projects:List[int]=[]
    types:List[int]=[]
    classifications:Optional[List[DataAccess]]=[]
    attributes:List[AttributeSearcher]=[]
    operation: QueryJoin = Field(QueryJoin.OR, alias="operation")
    tag_operation: QueryJoin = Field(QueryJoin.OR, alias="tagOperation")
    project_operation: QueryJoin = Field(QueryJoin.OR, alias="projectOperation")
    attribute_operation: QueryJoin = Field(QueryJoin.OR, alias="attributeOperation")
    class Config:
        allow_population_by_field_name = True

class AssetBase(BaseModel):
    name: str
    link: str
    version_id: int
    description: str
    classification: DataAccess

    class Config:
        json_encoders = {
            DataAccess: lambda a: str(a.value),
        }


class AssetBaseInDB(AssetBase):
    asset_id: Optional[int]=Field(None, alias="assetID")
    created_at: datetime
    last_modified_at: datetime
    is_selected: Optional[bool]=Field(None, alias="isSelected")
    class Config:
        extra = Extra.allow


class Asset(AssetBase):
    projects: List[int]
    tags: List[int]
    assets: Optional[List[int]]
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

class AssetOut(AssetBaseInDB):
    type_name: Optional[str]
    projects: Optional[List[ProjectInDBBase]]
    tags: Optional[List[TagInDB]]
    assets: Optional[List[Any]]
    metadata: Optional[List[Attribute]]
    class Config:
        allow_population_by_field_name = True

