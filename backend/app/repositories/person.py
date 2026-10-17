from sqlalchemy import func
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import Session, col, select

from app.models.person import Person
from app.repositories.base import Repository


class PersonRepository(Repository[Person]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, Person)

    def get_by_document(
        self,
        tipo_documento: str,
        numero_documento: str,
        exclude_person_id: int | None = None,
    ) -> Person | None:
        statement = select(Person).where(
            Person.tipo_documento == tipo_documento,
            Person.numero_documento == numero_documento,
        )
        if exclude_person_id is not None:
            statement = statement.where(Person.id != exclude_person_id)
        return self.session.exec(statement).first()

    def get_active(self, person_id: int) -> Person | None:
        return self.session.exec(
            select(Person).where(Person.id == person_id, Person.deleted == False)
        ).first()

    def get_page(
        self,
        skip: int,
        limit: int,
        nombre: str | None,
        apellido: str | None,
        tipo_documento: str | None,
        numero_documento: str | None,
    ) -> tuple[int, list[Person]]:
        filters: list[ColumnElement[bool]] = [col(Person.deleted) == False]
        if nombre:
            filters.append(func.lower(col(Person.nombre)).like(f"%{nombre.lower()}%"))
        if apellido:
            filters.append(
                func.lower(col(Person.apellido)).like(f"%{apellido.lower()}%")
            )
        if tipo_documento:
            filters.append(col(Person.tipo_documento) == tipo_documento)
        if numero_documento:
            filters.append(col(Person.numero_documento) == numero_documento)

        total = self.session.exec(
            select(func.count()).select_from(Person).where(*filters)
        ).one()
        items = self.session.exec(
            select(Person)
            .where(*filters)
            .order_by(col(Person.id))
            .offset(skip)
            .limit(limit)
        ).all()
        return total, list(items)
