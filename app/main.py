from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import auth_router, happiness_router, kpis_router

app = FastAPI(title="Happiness API")

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

app.include_router(auth_router.router)
app.include_router(happiness_router.router)
app.include_router(kpis_router.router)
