from pydantic import BaseModel, Field,Extra
from typing import  List, Optional
from .attribute import AttributeInDB
class Type(BaseModel):
    type_name: str = Field(..., alias="typeName")
    metadata: List[AttributeInDB]
    depends_on: List[int] = Field(..., alias="dependsOn")


class TypeBase(BaseModel):
    type_id: Optional[int]
    type_name: str

class TypeVersion(BaseModel):
    version_id:int
    version_number:int
    type_id:int
    class Config:
        extra = Extra.allow