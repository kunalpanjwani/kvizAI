"""
QuizTemplate model for kvizAI application
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, JSON
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, UUIDType


class QuizTemplate(Base):
    """QuizTemplate model for pre-generated quiz templates and quick quizzes"""
    
    __tablename__ = "quiz_templates"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Template information
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)
    category = Column(String(100), nullable=False)  # general, science, history, etc.
    
    # Template content
    questions = Column(JSON, nullable=False)  # Pre-generated questions
    correct_answers = Column(JSON, nullable=False)  # Correct answer indices
    difficulty = Column(String(20), nullable=False, default="medium")  # easy, medium, hard
    
    # Template settings
    time_limit = Column(Integer, nullable=True)  # minutes, null = no limit
    question_count = Column(Integer, nullable=False, default=10)
    max_score = Column(Integer, nullable=False, default=100)
    
    # Template type and visibility
    template_type = Column(String(50), nullable=False, default="quick")  # quick, daily, weekly, custom
    is_active = Column(Boolean, default=True)
    is_featured = Column(Boolean, default=False)
    
    # Usage statistics
    times_used = Column(Integer, default=0)
    average_score = Column(Integer, default=0)
    average_time = Column(Integer, default=0)  # average time taken in seconds
    
    # Scheduling (for daily/weekly quizzes)
    schedule_type = Column(String(20), nullable=True)  # daily, weekly, monthly
    next_schedule = Column(DateTime(timezone=True), nullable=True)
    last_scheduled = Column(DateTime(timezone=True), nullable=True)
    
    # Metadata
    tags = Column(JSON, nullable=True)  # Array of tags
    language = Column(String(10), default="en")
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<QuizTemplate(id={self.id}, name='{self.name}', subject='{self.subject}')>" 