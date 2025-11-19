from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import auth_router, happiness_router, kpis_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Happiness API")

origins = [
    "http://localhost:5173",    # Puerto por defecto de Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # Lista de orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],        # Permitir GET, POST, PUT, DELETE, etc.
    allow_headers=["*"],        # Permitir enviar tokens y cookies
)
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

app.include_router(auth_router.router)
app.include_router(happiness_router.router)
app.include_router(kpis_router.router)
