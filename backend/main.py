import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.person import router as person_router
from app.routers.portal_user import router as portal_user_router


def create_app() -> FastAPI:

    FRONTEND_URL = os.getenv("FRONTEND_URL", "")

    app = FastAPI(
        title="Backend | Integrador UTN",
    )

    app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    )

    # ROUTERS
    app.include_router(auth_router)
    app.include_router(health_router)
    app.include_router(person_router)
    app.include_router(portal_user_router)

    # Creación de DB
    create_db_and_tables()

    return app


app = create_app()
