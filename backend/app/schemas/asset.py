from pydantic import BaseModel

class AssetBase(BaseModel):
    name:str
    link:str