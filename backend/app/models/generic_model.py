from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel

class GenericModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deleted: bool = False
    deleted_at: Optional[datetime] = None
