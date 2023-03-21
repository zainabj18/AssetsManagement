
from typing import List,Optional
from pydantic import BaseModel, Field,Extra


class ProjectBase(BaseModel):
    name: str=Field(..., alias="projectName")
    description: Optional[str]=Field(..., alias="projectDescription")
    class Config:
        allow_population_by_field_name = True

class ProjectInDBBase(ProjectBase):
    id:int=Field(..., alias="projectID")
    class Config:
        allow_population_by_field_name = True

class Project(BaseModel):
    id: Optional[int]=Field(None, alias="projectID")
    name: str=Field(..., alias="projectName")
    description: Optional[str]=Field(..., alias="projectDescription")
    accounts: Optional[List[int]]

    class Config:
        allow_population_by_field_name = True
        extra = Extra.allow
