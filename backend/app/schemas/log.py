from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Extra, Field

from app.db import Actions, DataAccess


class Diff(BaseModel):
    added: Optional[Any]
    removed: Optional[Any]
    changed: Optional[Any]

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
        json_encoders = {DataAccess: lambda a: str(a.value)}


class Log(BaseModel):
    log_id: int = Field(..., alias="logID")
    account_id: int = Field(..., alias="accountID")
    object_id: int = Field(..., alias="objectID")
    model_id: int = Field(..., alias="modelID")
    model_name: Optional[str] = Field(None, alias="modelName")
    username: Optional[str]
    action: Actions
    date: datetime

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
        json_encoders = {
            Actions: lambda a: str(a.name),
        }
