"""
Database initialization script with sample data for kvizAI
"""

import asyncio
import sys
import os
import json
import sqlalchemy as sa
from datetime import datetime, timedelta

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db, engine, Base, AsyncSessionLocal
from app.models import *
from app.core.config import settings


async def create_sample_quiz_templates():
    """Create sample quiz templates for quick quizzes"""
    session = AsyncSessionLocal()
    try:
        
        # Sample quiz templates
        templates = [
            {
                "name": "General Knowledge Quiz",
                "description": "Test your general knowledge with this comprehensive quiz",
                "subject": "General Knowledge",
                "category": "general",
                "questions": [
                    {
                        "id": "q1",
                        "text": "What is the capital of France?",
                        "type": "multiple_choice",
                        "options": ["London", "Paris", "Berlin", "Madrid"],
                        "points": 10
                    },
                    {
                        "id": "q2",
                        "text": "Which planet is known as the Red Planet?",
                        "type": "multiple_choice",
                        "options": ["Venus", "Mars", "Jupiter", "Saturn"],
                        "points": 10
                    },
                    {
                        "id": "q3",
                        "text": "Who wrote 'Romeo and Juliet'?",
                        "type": "multiple_choice",
                        "options": ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"],
                        "points": 10
                    },
                    {
                        "id": "q4",
                        "text": "What is the largest ocean on Earth?",
                        "type": "multiple_choice",
                        "options": ["Atlantic", "Indian", "Arctic", "Pacific"],
                        "points": 10
                    },
                    {
                        "id": "q5",
                        "text": "The Great Wall of China is visible from space.",
                        "type": "true_false",
                        "options": ["True", "False"],
                        "points": 10
                    }
                ],
                "correct_answers": [1, 1, 1, 3, 1],  # 0-indexed
                "difficulty": "medium",
                "time_limit": 300,  # 5 minutes
                "question_count": 5,
                "max_score": 50,
                "template_type": "quick",
                "is_active": True,
                "is_featured": True,
                "tags": ["general", "knowledge", "beginner"],
                "language": "en"
            },
            {
                "name": "Science Quiz",
                "description": "Explore the wonders of science with this quiz",
                "subject": "Science",
                "category": "science",
                "questions": [
                    {
                        "id": "q1",
                        "text": "What is the chemical symbol for gold?",
                        "type": "multiple_choice",
                        "options": ["Ag", "Au", "Fe", "Cu"],
                        "points": 10
                    },
                    {
                        "id": "q2",
                        "text": "What is the hardest natural substance on Earth?",
                        "type": "multiple_choice",
                        "options": ["Steel", "Diamond", "Granite", "Iron"],
                        "points": 10
                    },
                    {
                        "id": "q3",
                        "text": "What is the largest organ in the human body?",
                        "type": "multiple_choice",
                        "options": ["Heart", "Brain", "Liver", "Skin"],
                        "points": 10
                    },
                    {
                        "id": "q4",
                        "text": "What is the speed of light?",
                        "type": "multiple_choice",
                        "options": ["299,792 km/s", "199,792 km/s", "399,792 km/s", "499,792 km/s"],
                        "points": 10
                    },
                    {
                        "id": "q5",
                        "text": "DNA stands for Deoxyribonucleic Acid.",
                        "type": "true_false",
                        "options": ["True", "False"],
                        "points": 10
                    }
                ],
                "correct_answers": [1, 1, 3, 0, 0],  # 0-indexed
                "difficulty": "medium",
                "time_limit": 300,  # 5 minutes
                "question_count": 5,
                "max_score": 50,
                "template_type": "quick",
                "is_active": True,
                "is_featured": False,
                "tags": ["science", "chemistry", "biology", "physics"],
                "language": "en"
            },
            {
                "name": "History Quiz",
                "description": "Journey through time with this history quiz",
                "subject": "History",
                "category": "history",
                "questions": [
                    {
                        "id": "q1",
                        "text": "In which year did World War II end?",
                        "type": "multiple_choice",
                        "options": ["1943", "1944", "1945", "1946"],
                        "points": 10
                    },
                    {
                        "id": "q2",
                        "text": "Who was the first President of the United States?",
                        "type": "multiple_choice",
                        "options": ["Thomas Jefferson", "John Adams", "George Washington", "Benjamin Franklin"],
                        "points": 10
                    },
                    {
                        "id": "q3",
                        "text": "The ancient city of Rome was founded in 753 BC.",
                        "type": "true_false",
                        "options": ["True", "False"],
                        "points": 10
                    },
                    {
                        "id": "q4",
                        "text": "Which empire was ruled by Genghis Khan?",
                        "type": "multiple_choice",
                        "options": ["Roman Empire", "Mongol Empire", "Ottoman Empire", "British Empire"],
                        "points": 10
                    },
                    {
                        "id": "q5",
                        "text": "The Declaration of Independence was signed in 1776.",
                        "type": "true_false",
                        "options": ["True", "False"],
                        "points": 10
                    }
                ],
                "correct_answers": [2, 2, 0, 1, 0],  # 0-indexed
                "difficulty": "medium",
                "time_limit": 300,  # 5 minutes
                "question_count": 5,
                "max_score": 50,
                "template_type": "quick",
                "is_active": True,
                "is_featured": False,
                "tags": ["history", "world-war", "presidents", "ancient"],
                "language": "en"
            }
        ]
        
        for template_data in templates:
            # Check if template already exists
            result = await session.execute(
                sa.select(QuizTemplate).where(QuizTemplate.name == template_data["name"])
            )
            if result.scalar_one_or_none():
                continue
                
            template = QuizTemplate(**template_data)
            session.add(template)
        
        await session.commit()
        print(f"Created {len(templates)} sample quiz templates")
    finally:
        await session.close()


async def create_sample_achievements():
    """Create sample achievements for users"""
    session = AsyncSessionLocal()
    try:
        
        achievements = [
            {
                "name": "First Quiz",
                "description": "Complete your first quiz",
                "icon": "🎯",
                "category": "quiz",
                "criteria_type": "quizzes_taken",
                "criteria_value": 1,
                "criteria_condition": "gte",
                "rarity": "common"
            },
            {
                "name": "Quiz Master",
                "description": "Complete 10 quizzes",
                "icon": "🏆",
                "category": "quiz",
                "criteria_type": "quizzes_taken",
                "criteria_value": 10,
                "criteria_condition": "gte",
                "rarity": "rare"
            },
            {
                "name": "Perfect Score",
                "description": "Get 100% on any quiz",
                "icon": "⭐",
                "category": "score",
                "criteria_type": "perfect_score",
                "criteria_value": 1,
                "criteria_condition": "gte",
                "rarity": "epic"
            },
            {
                "name": "Speed Demon",
                "description": "Complete a quiz in under 2 minutes",
                "icon": "⚡",
                "category": "time",
                "criteria_type": "fast_completion",
                "criteria_value": 120,  # seconds
                "criteria_condition": "lte",
                "rarity": "rare"
            },
            {
                "name": "Creator",
                "description": "Create your first questionnaire",
                "icon": "📝",
                "category": "creation",
                "criteria_type": "questionnaires_created",
                "criteria_value": 1,
                "criteria_condition": "gte",
                "rarity": "common"
            }
        ]
        
        for achievement_data in achievements:
            # Check if achievement already exists
            result = await session.execute(
                sa.select(Achievement).where(Achievement.name == achievement_data["name"])
            )
            if result.scalar_one_or_none():
                continue
                
            achievement = Achievement(**achievement_data)
            session.add(achievement)
        
        await session.commit()
        print(f"Created {len(achievements)} sample achievements")
    finally:
        await session.close()


async def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("Database tables created successfully!")


async def main():
    """Main initialization function"""
    print("Initializing kvizAI database with sample data...")
    
    try:
        # Create tables
        await create_tables()
        
        # Create sample data
        await create_sample_quiz_templates()
        await create_sample_achievements()
        
        print("Database initialization completed successfully!")
        print("Sample data has been added:")
        print("- 3 Quiz Templates (General Knowledge, Science, History)")
        print("- 5 Achievements (First Quiz, Quiz Master, Perfect Score, Speed Demon, Creator)")
        print("\nYou can now run the application with: uvicorn main:app --reload")
        
    except Exception as e:
        print(f"Error during database initialization: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 