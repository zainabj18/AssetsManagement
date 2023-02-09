from typing import Optional

from app.db import DataAccess, UserRole
from pydantic import BaseModel, Field, SecretStr, validator

SPECIAL_CHARECTERS = list("$#@!*&")
PASSWORD_MIN_LENGTH = 10
PASSWORD_MAX_LENGTH = 20


class UserBase(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    username: str
    account_type: UserRole = Field(UserRole.VIEWER, alias="accountType")
    account_privileges: DataAccess = Field(DataAccess.PUBLIC, alias="accountPrivileges")

    class Config:
        allow_population_by_field_name = True


class UserInDB(UserBase):
    account_id: str
    hashed_password: SecretStr


class UserCreate(UserBase):
    password: SecretStr
    confirm_password: SecretStr = Field(..., alias="confirmPassword")

    class Config:
        allow_population_by_field_name = True

    @validator("confirm_password")
    def passwords_match(cls, v, values):
        if (
            "password" in values
            and v.get_secret_value() != values["password"].get_secret_value()
        ):
            raise ValueError("Passwords do not match")
        return v

    @validator("password")
    def passwords_valid(cls, v):
        pwd = v.get_secret_value()
        pwd_len = len(pwd)
        is_digits = [i.isdigit() for i in pwd]
        assert (
            pwd_len >= PASSWORD_MIN_LENGTH
        ), f"password length must be greater than {PASSWORD_MIN_LENGTH}"
        assert (
            pwd_len <= PASSWORD_MAX_LENGTH
        ), f"password length must be less than {PASSWORD_MAX_LENGTH}"
        assert any(is_digits) and not all(
            is_digits
        ), "password must be contain letters and numbers"
        assert any(
            i.isdigit() for i in pwd
        ), "password must be contain letters and numbers"
        assert any(letter.islower() for letter in pwd) and any(
            letter.isupper() for letter in pwd
        ), "password must be mixed case"
        assert (
            len(set(SPECIAL_CHARECTERS).intersection(set(pwd))) > 0
        ), f"password must contain a charecter from {SPECIAL_CHARECTERS}"
        return v


# data=jwt.decode(token,current_app.config['SECRET_KEY'],algorithms=[current_app.config['JWT_ALGO']])
