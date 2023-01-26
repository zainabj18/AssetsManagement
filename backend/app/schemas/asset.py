from pydantic import BaseModel
from typing import List

class AssetBase(BaseModel):
    name:str
    link:str
    type:str
    description:str
    tags:List[str]