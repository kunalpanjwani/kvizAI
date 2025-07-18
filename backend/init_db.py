"""
Database initialization script for kvizAI
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db, engine, Base
from app.models import *
from app.core.config import settings


async def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database tables created successfully!")


async def main():
    """Main initialization function"""
    print("Initializing kvizAI database...")
    
    try:
        # Create tables
        await create_tables()
        
        print("Database initialization completed successfully!")
        print("You can now run the application with: uvicorn main:app --reload")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 