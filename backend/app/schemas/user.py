from pydantic import BaseModel,validator,Field,SecretStr
from typing import Optional
from app.db import DataAccess,UserRole
PASSWORD_MIN_LENGTH=10

class UserBase(BaseModel):
    first_name:Optional[str]
    last_name:Optional[str]
    username:str
    account_type:UserRole=Field(UserRole.VIEWER,alias="accountType")
    account_privileges:DataAccess=Field(DataAccess.PUBLIC,alias="accountPrivileges")

    class Config:
        allow_population_by_field_name = True

class UserCreate(UserBase):
    password:SecretStr
    confirm_password:SecretStr=Field(...,alias="confirmPassword")

    class Config:
        allow_population_by_field_name = True

    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v.get_secret_value() != values['password'].get_secret_value():
            print(values['password'].get_secret_value())
            print(v.get_secret_value())
            raise ValueError('Passwords do not match')
        return v
    
    @validator('password')
    def passwords_valid(cls, v):
        pwd=v.get_secret_value()
        pwd_len=len(pwd)
        assert pwd_len>=PASSWORD_MIN_LENGTH,f'password length must be greater than {PASSWORD_MIN_LENGTH}'
        return v