from fastapi import FastAPI
import os
from .database import create_db_and_tables
from .routers import auth_router, happiness_router, kpis_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Happiness API")

frontend_url_prod = os.environ.get("FRONTEND_URL", "http://localhost:5173")

origins = [
    frontend_url_prod,
    "http://localhost", 
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
app.include_router(auth_router.router)
app.include_router(happiness_router.router)
app.include_router(kpis_router.router)
