from app.db import Actions
from pydantic import BaseModel, Field,Extra
from typing import Optional
from datetime import datetime
class Log(BaseModel):
    log_id: int = Field(..., alias="logID")
    account_id: int = Field(..., alias="accountID")
    object_id:int = Field(..., alias="objectID")
    model_id:int = Field(..., alias="modelID")
    model_name:Optional[str] = Field(None, alias="modelName")
    username:Optional[str]
    action:Actions
    date:datetime
    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
        json_encoders = {
            Actions: lambda a: str(a.name),
        }
