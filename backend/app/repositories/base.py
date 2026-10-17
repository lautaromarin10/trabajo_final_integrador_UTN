from datetime import UTC, datetime
from typing import Generic, TypeVar

from sqlmodel import Session

from app.models.generic_model import GenericModel

T = TypeVar("T", bound=GenericModel)


class Repository(Generic[T]):
    def __init__(self, session: Session, model: type[T]) -> None:
        self.session = session
        self.model = model

    def add(self, entity: T) -> T:
        self.session.add(entity)
        return entity

    def get(self, entity_id: int) -> T | None:
        return self.session.get(self.model, entity_id)

    def flush(self) -> None:
        self.session.flush()

    def update_fields(self, entity: T, values: dict[str, object]) -> T:
        for key, value in values.items():
            setattr(entity, key, value)
        entity.updated_at = datetime.now(UTC)
        return entity

    def soft_delete(self, entity: T) -> T:
        now = datetime.now(UTC)
        entity.deleted = True
        entity.deleted_at = now
        entity.updated_at = now
        return self.add(entity)

    def reactivate(self, entity: T) -> T:
        entity.deleted = False
        entity.deleted_at = None
        entity.updated_at = datetime.now(UTC)
        return self.add(entity)
