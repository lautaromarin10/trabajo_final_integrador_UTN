from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Enum as SAEnum
from sqlmodel import Field

from app.core.roles import PortalRole
from app.models.generic_model import GenericModel


class PortalUser(GenericModel, table=True):
    __tablename__ = "usuario_portal"

    persona_id: Optional[int] = Field(
        default=None, foreign_key="persona.id", unique=True
    )
    role: PortalRole = Field(default=PortalRole.USER, sa_column=Column(
            SAEnum(PortalRole, values_callable=lambda enum: [item.value for item in enum]),
            nullable=False,
            index=True,
        ),
    )
    email: str = Field(unique=True, index=True)
    password_hash: str
    ultimo_ingreso: Optional[datetime] = None
