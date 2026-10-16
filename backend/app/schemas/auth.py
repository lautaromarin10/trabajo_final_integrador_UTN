from calendar import monthrange
from datetime import date

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.person import PersonBase
from app.utils.validators import Password


class RegisterRequest(PersonBase):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr = Field(..., max_length=255)
    password: Password

    @field_validator("fecha_nacimiento")
    @classmethod
    def require_adult(cls, value: date) -> date:
        today = date.today()
        minimum_birth_date = date(
            today.year - 18,
            today.month,
            min(today.day, monthrange(today.year - 18, today.month)[1]),
        )
        if value > minimum_birth_date:
            raise ValueError("La persona debe tener al menos 18 años")
        return value


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=128)


class LoginResponse(BaseModel):
    expires_in: int = 30 * 60
