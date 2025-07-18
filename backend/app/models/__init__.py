"""
Models package for QuizAI application
"""

from sqlalchemy.orm import relationship
from .user import User
from .questionnaire import Questionnaire
from .quiz import Quiz
from .quiz_attempt import QuizAttempt
from .leaderboard import Leaderboard
from .achievement import Achievement, UserAchievement
from .ai_model_usage import AIModelUsage
from .quiz_template import QuizTemplate

# Import all models for Alembic
__all__ = [
    "User",
    "Questionnaire", 
    "Quiz",
    "QuizAttempt",
    "Leaderboard",
    "Achievement",
    "UserAchievement",
    "AIModelUsage",
    "QuizTemplate"
]

# Set up relationships after all models are imported
def setup_relationships():
    """Set up all model relationships"""
    
    # User relationships
    User.questionnaires = relationship("Questionnaire", back_populates="creator", cascade="all, delete-orphan")
    User.created_quizzes = relationship("Quiz", back_populates="creator", cascade="all, delete-orphan")
    User.quiz_attempts = relationship("QuizAttempt", back_populates="user", cascade="all, delete-orphan")
    User.leaderboard_entries = relationship("Leaderboard", back_populates="user", cascade="all, delete-orphan")
    User.achievements = relationship("UserAchievement", back_populates="user", cascade="all, delete-orphan")
    
    # Questionnaire relationships
    Questionnaire.creator = relationship("User", back_populates="questionnaires")
    Questionnaire.quizzes = relationship("Quiz", back_populates="questionnaire", cascade="all, delete-orphan")
    
    # Quiz relationships
    Quiz.questionnaire = relationship("Questionnaire", back_populates="quizzes")
    Quiz.creator = relationship("User", back_populates="created_quizzes")
    Quiz.attempts = relationship("QuizAttempt", back_populates="quiz", cascade="all, delete-orphan")
    Quiz.leaderboard_entries = relationship("Leaderboard", back_populates="quiz", cascade="all, delete-orphan")
    
    # QuizAttempt relationships
    QuizAttempt.user = relationship("User", back_populates="quiz_attempts")
    QuizAttempt.quiz = relationship("Quiz", back_populates="attempts")
    
    # Leaderboard relationships
    Leaderboard.quiz = relationship("Quiz", back_populates="leaderboard_entries")
    Leaderboard.user = relationship("User", back_populates="leaderboard_entries")
    Leaderboard.attempt = relationship("QuizAttempt")
    
    # Achievement relationships
    Achievement.user_achievements = relationship("UserAchievement", back_populates="achievement", cascade="all, delete-orphan")
    
    # UserAchievement relationships
    UserAchievement.user = relationship("User", back_populates="achievements")
    UserAchievement.achievement = relationship("Achievement", back_populates="user_achievements")

# Call setup function
setup_relationships() 