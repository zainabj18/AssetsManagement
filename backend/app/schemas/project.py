from pydantic import BaseModel, Field


class Project(BaseModel):
    name: str
    description: str

    class Config:
        allow_population_by_field_name = True
