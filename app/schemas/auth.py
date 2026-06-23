from pydantic import BaseModel, EmailStr, field_validator

import re

from app.validation.password import PasswordValidator


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator(
        "password"
    )
    @classmethod
    def validate_password(
        cls,
        value
    ):
        return PasswordValidator.validate(
            value
        )
    

class RegisterForm(
    RegisterRequest
):
    pass


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

