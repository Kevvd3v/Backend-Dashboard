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

from app.models import Happiness, Country, Region

@router.get("/happiness-by-region")
async def get_happiness_by_region(year: int, session: AsyncSession = Depends(get_session)):
    """
    Trae todos los países y los agrupa manualmente para poder separar Oceanía.
    """
    # 1. Pedimos: País, Región y Puntaje
    statement = (
        select(Country.name, Region.name, Happiness.happiness_score)
        .join(Country, Country.id == Happiness.country_id)
        .join(Region, Region.id == Country.region_id)
        .where(Happiness.year == year)
    )

    results = await session.exec(statement)
    rows = results.all()

    # 2. Agrupación Manual en Python
    grupos = {}

    for country_name, region_name, score in rows:
        if score is None:
            continue
            
        # --- AQUÍ ESTÁ EL TRUCO PARA SEPARAR OCEANÍA ---
        if country_name in ["Australia", "New Zealand"]:
            key = "Oceania"  # Nueva región forzada
        elif region_name == "North America and ANZ":
            key = "North America" # Lo que queda (USA + Canada)
        else:
            key = region_name # El resto del mundo sigue igual

        # Acumulamos los puntajes
        if key not in grupos:
            grupos[key] = []
        grupos[key].append(score)

    # 3. Calculamos promedios finales
    labels = []
    values = []

    for key, scores_list in grupos.items():
        promedio = sum(scores_list) / len(scores_list)
        labels.append(key)
        values.append(round(promedio, 2))

    return {"labels": labels, "values": values}

# Asegúrate de que Country y Happiness estén importados al inicio
from app.models import Country, Happiness

@router.get("/map-data")
async def get_map_data(year: int, session: AsyncSession = Depends(get_session)):
    """
    Devuelve el puntaje de felicidad de CADA país para pintar el mapa.
    Retorna: [{"country": "Mexico", "value": 6.5}, ...]
    """
    statement = (
        select(Country.name, Happiness.happiness_score)
        .join(Country, Country.id == Happiness.country_id)
        .where(Happiness.year == year)
    )
    
    results = await session.exec(statement)
    data = results.all()
    
    return [
        {"country": name, "value": round(score, 2)} 
        for name, score in data 
        if score is not None
    ]

@router.get("/global-evolution")
async def get_global_evolution(session: AsyncSession = Depends(get_session)):
    """
    Calcula el promedio global de felicidad por año para la gráfica de línea.
    Utiliza COALESCE para manejar posibles valores NULL en el score.
    """
    statement = (
        select(
            Happiness.year,
            # Aseguramos que el promedio no sea NULL si todos los scores lo son
            func.avg(func.coalesce(Happiness.happiness_score, 0.0))
        )
        .group_by(Happiness.year)
        .order_by(Happiness.year)
    )

    results = await session.exec(statement)
    data = results.all()

    return [
        {"year": year, "score": round(float(avg_score), 4)}
        for year, avg_score in data 
    ] 
    # Eliminamos el 'if avg_score is not None' porque coalesce ya lo maneja


@router.get("/correlation-data")
async def get_correlation_data(year: int, session: AsyncSession = Depends(get_session)):
    """
    Devuelve los pares (PIB per cápita, Puntaje de felicidad) para la gráfica de dispersión.
    Utiliza COALESCE para garantizar que x e y siempre tengan un valor (0.0 si son NULL).
    """
    statement = (
        select(
            func.coalesce(Happiness.gdp_per_capita, 0.0),      # Eje X: PIB
            func.coalesce(Happiness.happiness_score, 0.0)      # Eje Y: Score
        )
        .where(Happiness.year == year)
    )

    results = await session.exec(statement)
    data = results.all()

    # Formato requerido por Chart.js Scatter Plot: [{x: pib, y: score}, ...]
    return [
        {"x": round(float(gdp), 4), "y": round(float(score), 4)}
        for gdp, score in data
    ]
