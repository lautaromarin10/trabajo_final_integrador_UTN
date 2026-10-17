from sqlalchemy import func
from sqlalchemy.sql.elements import ColumnElement
from sqlmodel import Session, col, select

from app.core.roles import PortalRole
from app.models.portal_user import PortalUser
from app.repositories.base import Repository


class PortalUserRepository(Repository[PortalUser]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, PortalUser)

    def get_by_email(
        self, email: str, include_deleted: bool = False
    ) -> PortalUser | None:
        statement = select(PortalUser).where(PortalUser.email == email)
        if not include_deleted:
            statement = statement.where(PortalUser.deleted == False)
        return self.session.exec(statement).first()

    def get_active(self, portal_user_id: int) -> PortalUser | None:
        return self.session.exec(
            select(PortalUser).where(
                PortalUser.id == portal_user_id,
                PortalUser.deleted == False,
            )
        ).first()

    def get_page(
        self,
        skip: int,
        limit: int,
        email: str | None,
        role: PortalRole | None,
    ) -> tuple[int, list[PortalUser]]:
        filters: list[ColumnElement[bool]] = [col(PortalUser.deleted) == False]
        if email:
            filters.append(func.lower(col(PortalUser.email)).like(f"%{email.lower()}%"))
        if role:
            filters.append(col(PortalUser.role) == role)

        total = self.session.exec(
            select(func.count()).select_from(PortalUser).where(*filters)
        ).one()
        items = self.session.exec(
            select(PortalUser)
            .where(*filters)
            .order_by(col(PortalUser.id))
            .offset(skip)
            .limit(limit)
        ).all()
        return total, list(items)
