"""
Leaderboard model for kvizAI application
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base, UUIDType


class Leaderboard(Base):
    """Leaderboard model for tracking user rankings"""
    
    __tablename__ = "leaderboards"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    quiz_id = Column(UUIDType(), ForeignKey("quizzes.id"), nullable=False)
    user_id = Column(UUIDType(), ForeignKey("users.id"), nullable=False)
    attempt_id = Column(UUIDType(), ForeignKey("quiz_attempts.id"), nullable=False)
    
    # Ranking information
    rank = Column(Integer, nullable=False)
    score = Column(Integer, nullable=False)
    max_score = Column(Integer, nullable=False)
    percentage = Column(Integer, nullable=False)
    
    # Performance metrics
    time_taken = Column(Integer, nullable=False)  # seconds
    accuracy = Column(Integer, nullable=False)  # percentage
    speed = Column(Integer, nullable=False)  # average time per question
    
    # Leaderboard type
    leaderboard_type = Column(String(50), nullable=False, default="quiz")  # quiz, global, daily
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    quiz = relationship("Quiz", back_populates="leaderboard_entries")
    user = relationship("User", back_populates="leaderboard_entries")
    attempt = relationship("QuizAttempt")
    
    def __repr__(self):
        return f"<Leaderboard(id={self.id}, quiz_id={self.quiz_id}, user_id={self.user_id}, rank={self.rank})>" 