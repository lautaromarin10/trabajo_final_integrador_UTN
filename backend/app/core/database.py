import os
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

from app.core.unit_of_work import UnitOfWork

DATABASE_URL = os.getenv("DATABASE_URL")
IS_PRODUCTION = os.getenv("PRODUCTION", "false").strip().lower() == "true"

if not DATABASE_URL:
    raise RuntimeError("La DATABASE_URL es requerida")

engine = create_engine(DATABASE_URL, echo=not IS_PRODUCTION)


def get_unit_of_work():
    with UnitOfWork(lambda: Session(engine, expire_on_commit=False)) as unit_of_work:
        yield unit_of_work


UnitOfWorkDep = Annotated[UnitOfWork, Depends(get_unit_of_work)]


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
