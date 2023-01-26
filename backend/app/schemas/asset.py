from pydantic import BaseModel
from typing import List
from app.db import DataAccess

class AssetBase(BaseModel):
    name:str
    link:str
    type:str
    description:str
    tags:List[str]
    access_level:DataAccess