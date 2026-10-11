from datetime import datetime

from pydantic import BaseModel, Field


class GenericSchema(BaseModel):
    id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=[datetime.now()])
    updated_at: datetime = Field(..., examples=[datetime.now()])
    deleted: bool = Field(..., examples=[False])
    deleted_at: datetime | None = None
