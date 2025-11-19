from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, func
from app.deps import get_session
from app.models import Happiness

router = APIRouter(prefix="/api/kpis", tags=["kpis"])

@router.get("/summary")
async def get_kpi_summary(year: int, session: AsyncSession = Depends(get_session)):
    statement = select(
        func.avg(Happiness.happiness_score),
        func.avg(Happiness.gdp_per_capita),
        func.avg(Happiness.social_support)
    ).where(Happiness.year == year)

    result = await session.exec(statement)
    data = result.first() # Retorna una tupla (avg_happiness, avg_gdp, avg_social)

    if not data:
        return {"happiness": 0, "gdp": 0, "social": 0}

    def format_val(val):
        return float(val) if val is not None else 0.0

    return {
        "happiness": format_val(data[0]),
        "gdp": format_val(data[1]),
        "social": format_val(data[2])
    }

@router.get("/trend")
async def trend(country: str, session: AsyncSession = Depends(get_session)):
    from app.models import Country
    q = select(Happiness).join(Country).where(Country.name == country).order_by(Happiness.year)
    r = await session.exec(q)
    rows = r.all()
    return [{"year": x.year, "happiness_score": x.happiness_score} for x in rows]