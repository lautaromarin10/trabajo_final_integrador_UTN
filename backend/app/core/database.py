from sqlmodel import create_engine, Session, SQLModel
import os
from typing import Annotated
from fastapi import Depends

DATABASE_URL = os.getenv("DATABASE_URL")
IS_PRODUCTION = os.getenv("PRODUCTION", "false").strip().lower() == "true"

if not DATABASE_URL:
    raise RuntimeError("La DATABASE_URL es requerida")

engine = create_engine(DATABASE_URL, echo= not IS_PRODUCTION)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)