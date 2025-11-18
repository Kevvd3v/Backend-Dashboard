from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

class Region(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    countries: List["Country"] = Relationship(back_populates="region")

class Country(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    region_id: Optional[int] = Field(default=None, foreign_key="region.id")
    region: Optional[Region] = Relationship(back_populates="countries")
    happiness: List["Happiness"] = Relationship(back_populates="country")

class Happiness(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    country_id: int = Field(foreign_key="country.id", index=True)
    year: int
    happiness_score: float
    gdp_per_capita: Optional[float] = None
    social_support: Optional[float] = None
    life_expectancy: Optional[float] = None
    freedom: Optional[float] = None
    generosity: Optional[float] = None
    corruption: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    country: Optional[Country] = Relationship(back_populates="happiness")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="viewer")
    created_at: datetime = Field(default_factory=datetime.utcnow)
