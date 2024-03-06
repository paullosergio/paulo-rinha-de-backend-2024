from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://admin:123@db/rinha"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    future=True,
    pool_pre_ping=True,  # Recommended for asyncpg
)

SessionLocal = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()
