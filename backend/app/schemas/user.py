from pydantic import BaseModel,validator,Field
from typing import Optional
from app.db import DataAccess,UserRole

class UserBase(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    username:str
    account_type:UserRole=Field(UserRole.VIEWER,alias="accountType")
    account_privileges:DataAccess=Field(DataAccess.PUBLIC,alias="accountPrivileges")

    class Config:
        allow_population_by_field_name = True

class UserCreate(UserBase):
    password:str
    confirm_password:str=Field(...,alias="confirmPassword")

    class Config:
        allow_population_by_field_name = True

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    