"""
Database configuration and session management
"""

from sqlalchemy import create_engine, TypeDecorator, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.pool import StaticPool
import asyncio
import uuid

from app.core.config import settings


class UUIDType(TypeDecorator):
    """Custom UUID type that works with SQLite"""
    
    impl = String
    cache_ok = True
    
    def __init__(self):
        super().__init__(length=36)
    
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, str):
            return value
        return str(value)
    
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return uuid.UUID(value)


# Database URL configuration
DATABASE_URL = settings.DATABASE_URL

# For SQLite, use async support
if DATABASE_URL.startswith("sqlite"):
    # Convert to async SQLite URL
    ASYNC_DATABASE_URL = DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
    
    # Create async engine for SQLite
    engine = create_async_engine(
        ASYNC_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    # For PostgreSQL, use async URL
    ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
    
    # Create async engine for PostgreSQL
    engine = create_async_engine(
        ASYNC_DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True
    )

# Create async session factory
AsyncSessionLocal = sessionmaker(
    class_=AsyncSession,
    expire_on_commit=False
)

# Create base class for models
Base = declarative_base()


async def get_db():
    """Dependency to get database session"""
    session = AsyncSessionLocal(bind=engine)
    try:
        yield session
    finally:
        await session.close()


async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db():
    """Close database connections"""
    await engine.dispose() 