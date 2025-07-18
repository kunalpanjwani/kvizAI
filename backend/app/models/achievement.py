"""
Achievement model for kvizAI application
"""

from sqlalchemy import Column, String, DateTime, Integer, Text, Boolean, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base, UUIDType


class Achievement(Base):
    """Achievement model for user badges and accomplishments"""
    
    __tablename__ = "achievements"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Achievement details
    name = Column(String(100), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    icon = Column(String(100), nullable=True)  # Icon identifier
    category = Column(String(50), nullable=False)  # quiz, score, time, streak, etc.
    
    # Achievement criteria
    criteria_type = Column(String(50), nullable=False)  # quizzes_taken, score_threshold, etc.
    criteria_value = Column(Integer, nullable=False)  # Value needed to unlock
    criteria_condition = Column(String(20), nullable=False, default="gte")  # gte, lte, eq
    
    # Achievement rarity
    rarity = Column(String(20), nullable=False, default="common")  # common, rare, epic, legendary
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user_achievements = relationship("UserAchievement", back_populates="achievement")
    
    def __repr__(self):
        return f"<Achievement(id={self.id}, name='{self.name}', category='{self.category}')>"


class UserAchievement(Base):
    """UserAchievement model for tracking user's earned achievements"""
    
    __tablename__ = "user_achievements"
    
    # Primary key
    id = Column(UUIDType(), primary_key=True, default=uuid.uuid4)
    
    # Relationships
    user_id = Column(UUIDType(), ForeignKey("users.id"), nullable=False)
    achievement_id = Column(UUIDType(), ForeignKey("achievements.id"), nullable=False)
    
    # Achievement progress
    progress = Column(Integer, default=0)  # Current progress towards achievement
    is_unlocked = Column(Boolean, default=False)
    unlocked_at = Column(DateTime(timezone=True), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement", back_populates="user_achievements")
    
    def __repr__(self):
        return f"<UserAchievement(id={self.id}, user_id={self.user_id}, achievement_id={self.achievement_id})>"
    
    def unlock_achievement(self):
        """Mark achievement as unlocked"""
        self.is_unlocked = True
        self.unlocked_at = func.now() 