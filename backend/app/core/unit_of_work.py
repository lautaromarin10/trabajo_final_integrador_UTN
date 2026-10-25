from collections.abc import Callable
from types import TracebackType
from typing import Self

from sqlmodel import Session

from app.repositories.person import PersonRepository
from app.repositories.portal_user import PortalUserRepository
from app.repositories.room_type import RoomTypeRepository

# HABITACIÓN REFERENCIA A HOTEL.ID, NO LO IMPORTEMOS Y DESCOMENTEMOS HASTA QUE EXISTA LA TABLA HOTEL
# from app.repositories.hotel import HotelRepository
# from app.repositories.room import RoomRepository

class UnitOfWork:
    def __init__(self, session_factory: Callable[[], Session]) -> None:
        self.session = session_factory()
        self.persons = PersonRepository(self.session)
        self.portal_users = PortalUserRepository(self.session)
        self.room_types = RoomTypeRepository(self.session)
        #DESCOMENTAR CUANDO EXISTA LA TABLA HOTEL
        # self.hotels = HotelRepository(self.session)
        # self.rooms = RoomRepository(self.session)

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
