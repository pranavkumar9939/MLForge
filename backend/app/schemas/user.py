import re

from pydantic import BaseModel, EmailStr, field_validator


class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Name cannot be empty.")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Za-z]", v) or not re.search(r"[0-9]", v):
            raise ValueError("Password must contain both letters and numbers.")
        return v


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
