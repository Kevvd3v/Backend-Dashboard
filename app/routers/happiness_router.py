from fastapi import APIRouter, Depends, Query
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from app.deps import get_session, require_role
from app.models import Happiness, Country

router = APIRouter(prefix="/api/happiness", tags=["happiness"])

@router.get("", response_model=List[Happiness])
async def list_happiness(year: Optional[int] = None, limit: int = Query(100, ge=1, le=1000), session: AsyncSession = Depends(get_session)):
    q = select(Happiness).order_by(Happiness.happiness_score.desc()).limit(limit)
    if year:
        q = q.where(Happiness.year == year)
    res = await session.exec(q)
    return res.all()

@router.get("/top-countries")
async def top_countries(year: int, limit: int = 10, session: AsyncSession = Depends(get_session)):
    q = select(Happiness, Country).join(Country).where(Happiness.year == year).order_by(Happiness.happiness_score.desc()).limit(limit)
    rows = await session.exec(q)
    results = []
    for h, c in rows:
        results.append({"country": c.name, "happiness_score": h.happiness_score})
    return results

@router.post("", dependencies=[Depends(require_role("editor"))])
async def create_h(session: AsyncSession = Depends(get_session), payload: dict = {}):
    return await session.run_sync(lambda: None)  
