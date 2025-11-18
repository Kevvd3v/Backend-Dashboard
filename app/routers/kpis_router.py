from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
from app.deps import get_session
from app.models import Happiness

router = APIRouter(prefix="/api/kpis", tags=["kpis"])

@router.get("/avg-happiness")
async def avg_happiness(year: int, session: AsyncSession = Depends(get_session)):
    q = select(func.avg(Happiness.happiness_score)).where(Happiness.year == year)
    r = await session.exec(q)
    val = r.one()
    return {"year": year, "avg_happiness": float(val) if val is not None else None}

@router.get("/trend")
async def trend(country: str, session: AsyncSession = Depends(get_session)):
    # retorna serie {year, score}
    q = select(Happiness).join_from(Happiness, Happiness) 
    from sqlmodel import select
    from app.models import Country
    q = select(Happiness).join(Country).where(Country.name == country).order_by(Happiness.year)
    r = await session.exec(q)
    rows = r.all()
    return [{"year": x.year, "happiness_score": x.happiness_score} for x in rows]
