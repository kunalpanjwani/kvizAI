"""
Leaderboard endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, desc
from typing import List, Optional

from app.core.database import get_db
from app.models.user import User
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.models.leaderboard import Leaderboard
from app.schemas.leaderboard import LeaderboardEntry, GlobalLeaderboardEntry, UserLeaderboardStats
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/quiz/{quiz_id}", response_model=List[LeaderboardEntry])
async def get_quiz_leaderboard(
    quiz_id: str,
    limit: int = Query(50, ge=1, le=100, description="Number of entries to return"),
    db: AsyncSession = Depends(get_db)
):
    """Get leaderboard for a specific quiz"""
    
    # Verify quiz exists
    quiz_result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = quiz_result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Get top attempts for this quiz
    query = select(
        QuizAttempt,
        User.username,
        User.profile_picture,
        Quiz.title,
        Quiz.subject
    ).join(
        User, QuizAttempt.user_id == User.id
    ).join(
        Quiz, QuizAttempt.quiz_id == Quiz.id
    ).where(
        QuizAttempt.quiz_id == quiz_id,
        QuizAttempt.is_completed == True
    ).order_by(
        desc(QuizAttempt.score),
        QuizAttempt.time_taken.asc(),
        QuizAttempt.completed_at.asc()
    ).limit(limit)
    
    result = await db.execute(query)
    attempts_data = result.all()
    
    # Prepare response with ranks
    leaderboard_entries = []
    for rank, (attempt, username, profile_picture, quiz_title, quiz_subject) in enumerate(attempts_data, 1):
        entry = LeaderboardEntry(
            id=str(attempt.id),
            user_id=str(attempt.user_id),
            quiz_id=str(attempt.quiz_id),
            score=attempt.score,
            max_score=attempt.max_score,
            percentage=attempt.percentage,
            time_taken=attempt.time_taken,
            rank=rank,
            created_at=attempt.completed_at or attempt.created_at,
            username=username,
            profile_picture=profile_picture,
            quiz_title=quiz_title,
            quiz_subject=quiz_subject
        )
        leaderboard_entries.append(entry)
    
    return leaderboard_entries


@router.get("/global", response_model=List[GlobalLeaderboardEntry])
async def get_global_leaderboard(
    limit: int = Query(50, ge=1, le=100, description="Number of entries to return"),
    db: AsyncSession = Depends(get_db)
):
    """Get global leaderboard based on total scores"""
    
    # Get users with highest total scores
    query = select(
        User.id,
        User.username,
        User.profile_picture,
        User.total_score,
        User.quizzes_taken,
        User.quizzes_created,
        func.coalesce(func.avg(QuizAttempt.score), 0).label('average_score')
    ).outerjoin(
        QuizAttempt, User.id == QuizAttempt.user_id
    ).where(
        User.is_active == True,
        User.quizzes_taken > 0
    ).group_by(
        User.id,
        User.username,
        User.profile_picture,
        User.total_score,
        User.quizzes_taken,
        User.quizzes_created
    ).order_by(
        desc(User.total_score),
        desc(User.quizzes_taken)
    ).limit(limit)
    
    result = await db.execute(query)
    users_data = result.all()
    
    # Prepare response with ranks
    leaderboard_entries = []
    for rank, user_data in enumerate(users_data, 1):
        entry = GlobalLeaderboardEntry(
            user_id=str(user_data.id),
            username=user_data.username,
            profile_picture=user_data.profile_picture,
            total_score=user_data.total_score,
            quizzes_taken=user_data.quizzes_taken,
            quizzes_created=user_data.quizzes_created,
            average_score=float(user_data.average_score),
            rank=rank
        )
        leaderboard_entries.append(entry)
    
    return leaderboard_entries


@router.get("/user/{user_id}", response_model=UserLeaderboardStats)
async def get_user_leaderboard_stats(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get user's leaderboard statistics"""
    
    # Get user
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get user's global rank
    rank_result = await db.execute(
        select(func.count(User.id)).where(
            User.total_score > user.total_score,
            User.is_active == True
        )
    )
    global_rank = rank_result.scalar() + 1
    
    # Get user's average score
    avg_score_result = await db.execute(
        select(func.avg(QuizAttempt.score)).where(
            QuizAttempt.user_id == user.id,
            QuizAttempt.is_completed == True
        )
    )
    average_score = avg_score_result.scalar() or 0.0
    
    # Get user's best quiz score
    best_score_result = await db.execute(
        select(func.max(QuizAttempt.score)).where(
            QuizAttempt.user_id == user.id,
            QuizAttempt.is_completed == True
        )
    )
    best_quiz_score = best_score_result.scalar()
    
    # Get recent attempts count (last 7 days)
    from datetime import datetime, timedelta
    recent_cutoff = datetime.utcnow() - timedelta(days=7)
    recent_attempts_result = await db.execute(
        select(func.count(QuizAttempt.id)).where(
            QuizAttempt.user_id == user.id,
            QuizAttempt.created_at >= recent_cutoff
        )
    )
    recent_attempts = recent_attempts_result.scalar()
    
    return UserLeaderboardStats(
        user_id=str(user.id),
        username=user.username,
        global_rank=global_rank,
        total_score=user.total_score,
        quizzes_taken=user.quizzes_taken,
        average_score=float(average_score),
        best_quiz_score=best_quiz_score,
        recent_attempts=recent_attempts,
        achievements_count=0  # TODO: Implement when achievements are ready
    )


@router.get("/me", response_model=UserLeaderboardStats)
async def get_my_leaderboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's leaderboard statistics"""
    return await get_user_leaderboard_stats(str(current_user.id), db)