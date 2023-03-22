from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Comment(BaseModel):
    comment: str=Field(...,min_length=1)
    class Config:
        allow_population_by_field_name = True

class CommentOut(Comment):
    comment_id:int
    asset_id:int= Field(..., alias="assetID")
    account_id:int= Field(..., alias="accountID")
    datetime:datetime
    username:Optional[str]
    class Config:
        allow_population_by_field_name = True