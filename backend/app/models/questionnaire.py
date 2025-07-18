"""
Questionnaire model for kvizAI application
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base, UUIDType


class Questionnaire(Base):
    """Questionnaire model for custom quiz creation"""
    
    __tablename__ = "questionnaires"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Creator relationship
    creator_id = Column(UUIDType(), ForeignKey("users.id"), nullable=False)
    
    # Basic information
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String(100), nullable=False)
    difficulty_level = Column(String(20), nullable=False, default="medium")  # easy, medium, hard
    
    # Questionnaire content
    questions = Column(JSON, nullable=False)  # Store questions as JSON
    version = Column(Integer, default=1)
    
    # Visibility and sharing
    is_public = Column(Boolean, default=False)
    is_template = Column(Boolean, default=False)  # For template library
    
    # Statistics
    times_used = Column(Integer, default=0)
    average_score = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    creator = relationship("User", back_populates="questionnaires")
    quizzes = relationship("Quiz", back_populates="questionnaire")
    
    def __repr__(self):
        return f"<Questionnaire(id={self.id}, title='{self.title}', subject='{self.subject}')>"
    
    @property
    def question_count(self):
        """Return number of questions in questionnaire"""
        if self.questions:
            return len(self.questions)
        return 0
    
    def increment_usage(self):
        """Increment times used counter"""
        self.times_used += 1
    
    def update_average_score(self, new_score: int):
        """Update average score"""
        if self.average_score == 0:
            self.average_score = new_score
        else:
            # Simple average update (could be improved with weighted average)
            self.average_score = (self.average_score + new_score) // 2 