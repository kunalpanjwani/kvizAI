"""
User model for kvizAI application
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean
from sqlalchemy.sql import func
import uuid
from app.core.database import Base, UUIDType


class User(Base):
    """User model for authentication and profile management"""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Authentication fields
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    
    # Profile fields
    profile_picture = Column(String(500), nullable=True)  # URL to profile picture
    bio = Column(Text, nullable=True)
    
    # Status fields
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    
    # Statistics fields
    total_score = Column(Integer, default=0)
    quizzes_taken = Column(Integer, default=0)
    quizzes_created = Column(Integer, default=0)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"
    
    @property
    def display_name(self):
        """Return display name (username)"""
        return self.username
    
    def increment_quizzes_taken(self):
        """Increment quizzes taken counter"""
        self.quizzes_taken += 1
    
    def increment_quizzes_created(self):
        """Increment quizzes created counter"""
        self.quizzes_created += 1
    
    def add_score(self, score: int):
        """Add score to total score"""
        self.total_score += score 