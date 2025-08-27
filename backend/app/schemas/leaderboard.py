"""
Leaderboard schemas for request/response models
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LeaderboardEntry(BaseModel):
    """Schema for leaderboard entry"""
    id: str
    user_id: str
    quiz_id: str
    score: int
    max_score: int
    percentage: int
    time_taken: int
    rank: int
    created_at: datetime
    
    # User information
    username: str
    profile_picture: Optional[str] = None
    
    # Quiz information
    quiz_title: str
    quiz_subject: str
    
    class Config:
        from_attributes = True


class GlobalLeaderboardEntry(BaseModel):
    """Schema for global leaderboard entry"""
    user_id: str
    username: str
    profile_picture: Optional[str] = None
    total_score: int
    quizzes_taken: int
    quizzes_created: int
    average_score: float
    rank: int
    
    class Config:
        from_attributes = True


class UserLeaderboardStats(BaseModel):
    """Schema for user's leaderboard statistics"""
    user_id: str
    username: str
    global_rank: int
    total_score: int
    quizzes_taken: int
    average_score: float
    best_quiz_score: Optional[int] = None
    recent_attempts: int
    achievements_count: int = 0