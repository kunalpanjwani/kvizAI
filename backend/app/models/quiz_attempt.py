"""
QuizAttempt model for kvizAI application
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base, UUIDType


class QuizAttempt(Base):
    """QuizAttempt model for tracking user quiz attempts"""
    
    __tablename__ = "quiz_attempts"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    user_id = Column(UUIDType(), ForeignKey("users.id"), nullable=False)
    quiz_id = Column(UUIDType(), ForeignKey("quizzes.id"), nullable=False)
    
    # Attempt details
    score = Column(Integer, default=0)
    max_score = Column(Integer, nullable=False)
    percentage = Column(Integer, default=0)  # Percentage score
    
    # Time tracking
    time_taken = Column(Integer, default=0)  # seconds
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Attempt status
    is_completed = Column(Boolean, default=False)
    is_timed_out = Column(Boolean, default=False)
    
    # User answers and results
    answers = Column(JSON, nullable=True)  # Store user answers as JSON
    correct_answers = Column(Integer, default=0)
    incorrect_answers = Column(Integer, default=0)
    skipped_answers = Column(Integer, default=0)
    
    # Performance metrics
    accuracy = Column(Integer, default=0)  # Percentage accuracy
    speed = Column(Integer, default=0)  # Average time per question in seconds
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="quiz_attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    
    def __repr__(self):
        return f"<QuizAttempt(id={self.id}, user_id={self.user_id}, quiz_id={self.quiz_id}, score={self.score})>"
    
    def calculate_percentage(self):
        """Calculate percentage score"""
        if self.max_score > 0:
            self.percentage = int((self.score / self.max_score) * 100)
        return self.percentage
    
    def calculate_accuracy(self):
        """Calculate accuracy percentage"""
        total_answered = self.correct_answers + self.incorrect_answers
        if total_answered > 0:
            self.accuracy = int((self.correct_answers / total_answered) * 100)
        return self.accuracy
    
    def calculate_speed(self):
        """Calculate average time per question"""
        total_questions = self.correct_answers + self.incorrect_answers + self.skipped_answers
        if total_questions > 0 and self.time_taken > 0:
            self.speed = int(self.time_taken / total_questions)
        return self.speed
    
    def complete_attempt(self, completion_time: int = None):
        """Mark attempt as completed"""
        self.is_completed = True
        self.completed_at = func.now()
        if completion_time:
            self.time_taken = completion_time
        
        # Calculate metrics
        self.calculate_percentage()
        self.calculate_accuracy()
        self.calculate_speed()
    
    def timeout_attempt(self):
        """Mark attempt as timed out"""
        self.is_timed_out = True
        self.is_completed = True
        self.completed_at = func.now() 