from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app import crud, auth
from app.deps import get_session

router = APIRouter(prefix="/api/auth", tags=["auth"])

class RegisterIn(BaseModel):
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

@router.post("/register")
async def register(payload: RegisterIn, session: AsyncSession = Depends(get_session)):
    existing = await crud.get_user_by_email(session, payload.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    if not payload.password or len(payload.password.encode("utf-8")) > 1024:
        raise HTTPException(status_code=400, detail="Contraseña invalida (max 1024 bytes)")
    if len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Contraseña denegada (min 6 chars)")

    hashed = auth.hash_password(payload.password)
    user = await crud.create_user(session, payload.email, hashed)
    token = auth.create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/login")
async def login(payload: LoginIn, session: AsyncSession = Depends(get_session)):
    user = await crud.get_user_by_email(session, payload.email)
    if not user or not auth.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    token = auth.create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
