from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Region, Country, Happiness, User

async def get_or_create_region(session: AsyncSession, name: str):
    q = select(Region).where(Region.name == name)
    r = await session.exec(q)
    region = r.first()
    if region:
        return region
    region = Region(name=name)
    session.add(region)
    await session.commit()
    await session.refresh(region)
    return region

async def get_or_create_country(session: AsyncSession, name: str, region_id: int | None = None):
    q = select(Country).where(Country.name == name)
    r = await session.exec(q)
    c = r.first()
    if c:
        return c
    country = Country(name=name, region_id=region_id)
    session.add(country)
    await session.commit()
    await session.refresh(country)
    return country

async def create_happiness(session: AsyncSession, **data):
    h = Happiness(**data)
    session.add(h)
    await session.commit()
    await session.refresh(h)
    return h

async def get_user_by_email(session: AsyncSession, email: str):
    q = select(User).where(User.email == email)
    r = await session.exec(q)
    return r.first()

async def create_user(session: AsyncSession, email: str, password_hash: str, role: str = "viewer"):
    u = User(email=email, password_hash=password_hash, role=role)
    session.add(u)
    await session.commit()
    await session.refresh(u)
    return u
