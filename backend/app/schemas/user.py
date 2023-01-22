from pydantic import BaseModel,ValidationError, validator
from typing import Optional
from app.db import DataAccess,UserRole

class UserBase(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    username:str
    account_type:UserRole=UserRole.VIEWER
    account_privileges:DataAccess=DataAccess.PUBLIC

class UserCreate(BaseModel):
    password:str
    confirm_password:str

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v