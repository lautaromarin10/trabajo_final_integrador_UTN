from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas.person import PersonBase
from app.utils.validators import Password


class RegisterRequest(PersonBase):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(..., max_length=255)
    password: Password


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=128)


class LoginResponse(BaseModel):
    access_token: str
    token_type: Literal["bearer"] = "bearer"
    expires_in: int = 30 * 60
