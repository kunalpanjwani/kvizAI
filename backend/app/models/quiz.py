"""
Quiz model for kvizAI application
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base, UUIDType


class Quiz(Base):
    """Quiz model for generated quizzes"""
    
    __tablename__ = "quizzes"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    questionnaire_id = Column(UUIDType(), ForeignKey("questionnaires.id"), nullable=True)
    creator_id = Column(UUIDType(), ForeignKey("users.id"), nullable=True)
    
    # Basic information
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)
    
    # Quiz content
    questions = Column(JSON, nullable=False)  # Store questions as JSON
    correct_answers = Column(JSON, nullable=False)  # Store correct answers as JSON
    
    # Quiz settings
    time_limit = Column(Integer, nullable=True)  # minutes, null = no limit
    difficulty = Column(String(20), nullable=False, default="medium")  # easy, medium, hard
    max_score = Column(Integer, nullable=False, default=100)
    
    # Quiz type and visibility
    is_global = Column(Boolean, default=False)  # For quick quizzes
    is_public = Column(Boolean, default=True)
    is_template = Column(Boolean, default=False)  # For template quizzes
    
    # AI generation info
    ai_model_used = Column(String(50), nullable=True)  # llama, gemini, template
    generation_time = Column(Integer, nullable=True)  # seconds taken to generate
    
    # Statistics
    times_taken = Column(Integer, default=0)
    average_score = Column(Integer, default=0)
    average_time = Column(Integer, default=0)  # average time taken in seconds
    
    # Expiration
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    questionnaire = relationship("Questionnaire", back_populates="quizzes")
    creator = relationship("User", back_populates="created_quizzes")
    attempts = relationship("QuizAttempt", back_populates="quiz")
    leaderboard_entries = relationship("Leaderboard", back_populates="quiz")
    
    def __repr__(self):
        return f"<Quiz(id={self.id}, title='{self.title}', subject='{self.subject}')>"
    
    def increment_usage(self):
        """Increment times taken counter"""
        self.times_taken += 1
    
    def update_average_score(self, new_score: int):
        """Update average score"""
        if self.average_score == 0:
            self.average_score = new_score
        else:
            # Simple average update
            self.average_score = (self.average_score + new_score) // 2
    
    def update_average_time(self, new_time: int):
        """Update average time taken"""
        if self.average_time == 0:
            self.average_time = new_time
        else:
            # Simple average update
            self.average_time = (self.average_time + new_time) // 2 