from typing import List, Optional

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    id: Optional[int]
    name: str = Field(..., min_length=1)


class TagInDB(TagBase):
    id: int


class TagBulkRequest(BaseModel):
    to_tag_id: int = Field(..., alias="toTagID")
    assest_ids: List[int] = Field(..., alias="assetIDs")

    class Config:
        allow_population_by_field_name = True
