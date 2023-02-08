from typing import Optional

from pydantic import BaseModel


class TagBase(BaseModel):
    id: Optional[int]
    name: str
