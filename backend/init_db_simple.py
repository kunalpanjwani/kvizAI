"""
Simple database initialization script for kvizAI
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
    print("Tables created:")
    print("- users")
    print("- questionnaires") 
    print("- quizzes")
    print("- quiz_attempts")
    print("- leaderboards")
    print("- achievements")
    print("- user_achievements")
    print("- ai_model_usage")
    print("- quiz_templates")


async def main():
    """Main initialization function"""
    print("Initializing kvizAI database...")
    
    try:
        # Create tables
        await create_tables()
        
        print("\nDatabase initialization completed successfully!")
        print("All models are now available:")
        print("- User (authentication and profiles)")
        print("- Questionnaire (custom quiz creation)")
        print("- Quiz (generated quizzes)")
        print("- QuizAttempt (user quiz attempts)")
        print("- Leaderboard (rankings and scores)")
        print("- Achievement & UserAchievement (achievement system)")
        print("- AIModelUsage (AI performance tracking)")
        print("- QuizTemplate (pre-generated quiz templates)")
        print("\nYou can now run the application with: uvicorn main:app --reload")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 