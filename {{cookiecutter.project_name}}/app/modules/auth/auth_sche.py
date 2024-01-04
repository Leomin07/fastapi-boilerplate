from email_validator import EmailNotValidError
from pydantic import BaseModel, field_validator, validate_email


class register_schema(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return value

    full_name: str | None = None
    password: str
    phone: str | None = None


class login_schema(BaseModel):
    email: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        try:
            validate_email(value)
        except EmailNotValidError:
            raise ValueError("Invalid email format")
        return value

    password: str


class token(BaseModel):
    access_token: str
    token_type: str


class refresh_token_schema(BaseModel):
    refresh_token: str
