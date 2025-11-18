from sqlmodel.ext.asyncio.session import AsyncSession
from app.database import async_engine
from sqlmodel import select
from app.models import User
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_session() -> AsyncSession:
    async with AsyncSession(async_engine) as session:
        yield session

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)) -> User:
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    q = select(User).where(User.id == user_id)
    res = await session.exec(q)
    user = res.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    return user

def require_role(min_role: str):
    order = {"viewer": 1, "editor": 2, "admin": 3}
    def _checker(user: User = Depends(get_current_user)):
        if order.get(user.role, 0) < order.get(min_role, 0):
            raise HTTPException(status_code=403, detail="Permisos insuficientes")
        return user
    return _checker
