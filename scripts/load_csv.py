# scripts/load_csv.py
import os
import asyncio
import pandas as pd
import math

from sqlmodel.ext.asyncio.session import AsyncSession
from app.deps import async_engine  # ensure PYTHONPATH=/app when running
from app.crud import get_or_create_region, get_or_create_country, create_happiness

CSV_PATH = os.getenv("CSV_PATH", "/app/app/data/world_happiness_clean")
BATCH_SIZE = int(os.getenv("LOAD_BATCH_SIZE", "200"))


def clean_str(val, default="Unknown"):
    # Normaliza NaN, None o strings vacíos a default
    if val is None:
        return default
    if isinstance(val, float):
        if math.isnan(val):
            return default
        return str(val)
    s = str(val).strip()
    return s if s != "" else default


def to_float_or_none(val):
    if val is None:
        return None
    try:
        if isinstance(val, str):
            val = val.strip()
            if val == "":
                return None
        f = float(val)
        if math.isnan(f):
            return None
        return f
    except Exception:
        return None


async def process_row(session: AsyncSession, row: pd.Series):
    region_name = clean_str(row.get("region", None), default="Unknown")
    country_name = clean_str(row.get("country", None), default="Unknown")

    region = await get_or_create_region(session, region_name)
    country = await get_or_create_country(session, country_name, region.id)

    data = {
        "country_id": country.id,
        "year": int(row["year"]) if not pd.isna(row.get("year")) else None,
        "happiness_score": to_float_or_none(row.get("happiness_score")),
        "gdp_per_capita": to_float_or_none(row.get("gdp_per_capita")),
        "social_support": to_float_or_none(row.get("social_support")),
        "life_expectancy": to_float_or_none(row.get("life_expectancy")),
        "freedom": to_float_or_none(row.get("freedom")),
        "generosity": to_float_or_none(row.get("generosity")),
        "corruption": to_float_or_none(row.get("corruption")),
    }

    # create_happiness expects complete data; guardamos solo si year y country_id y happiness_score están presentes
    if data["year"] is None or data["happiness_score"] is None:
        # omitimos filas mal formadas (puedes loguearlas)
        return False

    await create_happiness(session, **data)
    return True


async def main():
    if not os.path.exists(CSV_PATH):
        print("CSV not found at", CSV_PATH)
        return

    df = pd.read_csv(CSV_PATH)
    total = len(df)
    print(f"Rows in CSV: {total}")

    inserted = 0
    async with AsyncSession(async_engine) as session:
        i = 0
        for _, row in df.iterrows():
            try:
                ok = await process_row(session, row)
                if ok:
                    inserted += 1
            except Exception as e:
                # log y continuar
                print(f"Error procesando fila {_}: {e}")
            i += 1
            # opcional: imprimir progreso cada batch
            if i % BATCH_SIZE == 0:
                print(f"Processed {i}/{total} rows - inserted so far: {inserted}")

    print("Carga finalizada. Inserted:", inserted)


if __name__ == "__main__":
    asyncio.run(main())
