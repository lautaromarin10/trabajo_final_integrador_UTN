from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class GenericSchema(BaseModel):
    id: int = Field(..., examples=[1])
    created_at: datetime = Field(..., examples=[datetime.now()])
    updated_at: datetime = Field(..., examples=[datetime.now()])
    deleted: bool = Field(..., examples=[False])
    deleted_at: Optional[datetime] = None