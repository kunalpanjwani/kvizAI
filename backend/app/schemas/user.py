"""
User-related schemas for profile management
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserProfileUpdate(BaseModel):
    """Schema for updating user profile"""
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="Username (3-50 characters)")
    bio: Optional[str] = Field(None, max_length=500, description="User biography (max 500 characters)")
    profile_picture: Optional[str] = Field(None, description="URL to profile picture")


class UserProfile(BaseModel):
    """Schema for user profile response"""
    id: str
    username: str
    email: str
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    total_score: int = 0
    quizzes_taken: int = 0
    quizzes_created: int = 0
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserStats(BaseModel):
    """Schema for user statistics"""
    total_score: int
    quizzes_taken: int
    quizzes_created: int
    average_score: float = 0.0
    rank: Optional[int] = None
    achievements_count: int = 0


class UserPublicProfile(BaseModel):
    """Schema for public user profile (limited information)"""
    id: str
    username: str
    profile_picture: Optional[str] = None
    bio: Optional[str] = None
    total_score: int = 0
    quizzes_taken: int = 0
    quizzes_created: int = 0
    created_at: datetime
    
    class Config:
        from_attributes = True