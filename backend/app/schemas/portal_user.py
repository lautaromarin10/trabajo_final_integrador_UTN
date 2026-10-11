from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.core.roles import PortalRole
from app.schemas.generic_schema import GenericSchema
from app.schemas.person import PersonRead, PersonUpdate
from app.utils.validators import Password, reject_null_value

# No hice PortalUserBase porque cada Schema tiene sus propios campos y no se repite en ninguno de ellos.

class PortalUserCreate(BaseModel):
    persona_id: int = Field(..., gt=0, examples=[1])
    email: EmailStr = Field(..., max_length=255, examples=["test@gmail.com"])
    password: Password = Field(examples=["Clave!123"])


class PortalUserUpdate(PersonUpdate):
    model_config = ConfigDict(extra="forbid")

    persona_id: Optional[int] = Field(None, gt=0, examples=[1])
    role: Optional[PortalRole] = Field(None, examples=[PortalRole.USER])
    password: Optional[Password] = Field(None, examples=["Clave!123"])

    @field_validator("role", "password", mode="before")
    @classmethod
    def reject_null_values(cls, value):
        return reject_null_value(value)


class PortalUserRead(GenericSchema):
    model_config = ConfigDict(from_attributes=True)
    persona_id: int
    role: PortalRole
    email: EmailStr
    ultimo_ingreso: Optional[datetime] = None


class PortalUserProfile(PortalUserRead):
    persona: Optional[PersonRead] = None


class PortalUserPage(BaseModel):
    items: list[PortalUserRead]
    total: int
    hasNextPage: bool
    hasPrevPage: bool
