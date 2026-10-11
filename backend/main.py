from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.person import router as person_router
from app.routers.portal_user import router as portal_user_router


def create_app() -> FastAPI:

    app = FastAPI(
        title="Backend | Integrador UTN",
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
