from collections.abc import Callable
from types import TracebackType
from typing import Self

from sqlmodel import Session

from app.repositories.person import PersonRepository
from app.repositories.portal_user import PortalUserRepository


class UnitOfWork:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self.session = session_factory()
        self.persons = PersonRepository(self.session)
        self.portal_users = PortalUserRepository(self.session)

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool:
        try:
            if exc_type is None and exc_value is None and traceback is None:
                self.session.commit()
            else:
                self.session.rollback()
        except Exception:
            self.session.rollback()
            raise
        finally:
            self.session.close()
        return False
