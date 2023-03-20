
from typing import List,Optional
from pydantic import BaseModel, Field,Extra


class Project(BaseModel):
    id: Optional[int]=Field(None, alias="projectID")
    name: str=Field(..., alias="projectName")
    description: Optional[str]=Field(..., alias="projectDescription")
    accounts: Optional[List[int]]

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
