from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


class GenericModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    deleted: bool = False
    deleted_at: datetime | None = None
