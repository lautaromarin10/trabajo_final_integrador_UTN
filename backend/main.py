from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.routers.health import router as health_router

def create_app() -> FastAPI:

    app = FastAPI(
        title="Backend | Integrador UTN",
    )

    # ROUTERS
    app.include_router(health_router)
    
    # Creación de DB
    create_db_and_tables()

    return app

app = create_app()