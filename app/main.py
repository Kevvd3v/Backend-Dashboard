from fastapi import FastAPI
from .database import create_db_and_tables
from .routers import auth_router, happiness_router, kpis_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Happiness API")

origins = [
    "https://frontend-dashboard.vercel.app", # <--- ¡IMPORTANTE!
    "http://localhost:5173", 
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
