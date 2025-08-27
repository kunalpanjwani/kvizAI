"""
User management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List

from app.core.database import get_db
from app.models.user import User
from app.models.quiz_attempt import QuizAttempt
from app.models.quiz import Quiz
from app.schemas.user import UserProfile, UserProfileUpdate, UserStats, UserPublicProfile
from app.schemas.auth import UserResponse
from app.utils.auth import get_current_active_user

router = APIRouter()


@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_active_user)):
    """Get current user profile"""
    # Convert UUID to string for response
    user_dict = {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "profile_picture": current_user.profile_picture,
        "bio": current_user.bio,
        "total_score": current_user.total_score,
        "quizzes_taken": current_user.quizzes_taken,
        "quizzes_created": current_user.quizzes_created,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }
    return UserProfile.model_validate(user_dict)


@router.put("/profile", response_model=UserProfile)
async def update_profile(
    profile_data: UserProfileUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update user profile"""
    
    # Check if username is being changed and if it's already taken
    if profile_data.username and profile_data.username != current_user.username:
        existing_user = await db.execute(
            select(User).where(
                User.username == profile_data.username,
                User.id != current_user.id
            )
        )
        if existing_user.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )
        current_user.username = profile_data.username
    
    # Update other fields if provided
    if profile_data.bio is not None:
        current_user.bio = profile_data.bio
    
    if profile_data.profile_picture is not None:
        current_user.profile_picture = profile_data.profile_picture
    
    await db.commit()
    await db.refresh(current_user)
    
    # Convert UUID to string for response
    user_dict = {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "profile_picture": current_user.profile_picture,
        "bio": current_user.bio,
        "total_score": current_user.total_score,
        "quizzes_taken": current_user.quizzes_taken,
        "quizzes_created": current_user.quizzes_created,
        "is_active": current_user.is_active,
        "is_verified": current_user.is_verified,
        "created_at": current_user.created_at,
        "last_login": current_user.last_login
    }
    return UserProfile.model_validate(user_dict)


@router.get("/stats", response_model=UserStats)
async def get_user_stats(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user statistics"""
    
    # Calculate average score (use percentage for consistency)
    avg_score_result = await db.execute(
        select(func.avg(QuizAttempt.percentage)).where(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.is_completed == True
        )
    )
    avg_score = avg_score_result.scalar() or 0.0
    
    # Get user rank (count users with higher total scores)
    rank_result = await db.execute(
        select(func.count(User.id)).where(
            User.total_score > current_user.total_score,
            User.is_active == True
        )
    )
    rank = rank_result.scalar() + 1  # Add 1 to get actual rank (1-based)
    
    # TODO: Get achievements count when achievement system is implemented
    achievements_count = 0
    
    return UserStats(
        total_score=current_user.total_score,
        quizzes_taken=current_user.quizzes_taken,
        quizzes_created=current_user.quizzes_created,
        average_score=float(avg_score),
        rank=rank,
        achievements_count=achievements_count
    )





@router.get("/", response_model=List[UserPublicProfile])
async def get_users(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db)
):
    """Get list of users (public profiles only)"""
    
    if limit > 100:
        limit = 100  # Prevent excessive queries
    
    users = await db.execute(
        select(User)
        .where(User.is_active == True)
        .order_by(User.total_score.desc())
        .offset(skip)
        .limit(limit)
    )
    users = users.scalars().all()
    
    # Convert UUIDs to strings for response
    response_list = []
    for user in users:
        user_dict = {
            "id": str(user.id),
            "username": user.username,
            "profile_picture": user.profile_picture,
            "bio": user.bio,
            "total_score": user.total_score,
            "quizzes_taken": user.quizzes_taken,
            "quizzes_created": user.quizzes_created,
            "created_at": user.created_at
        }
        response_list.append(UserPublicProfile.model_validate(user_dict))
    
    return response_list


@router.get("/statistics")
async def get_user_statistics(db: AsyncSession = Depends(get_db)):
    """Get general user statistics"""
    
    # Total active users
    total_users_result = await db.execute(
        select(func.count(User.id)).where(User.is_active == True)
    )
    total_users = total_users_result.scalar()
    
    # Total quiz attempts
    total_attempts_result = await db.execute(
        select(func.count(QuizAttempt.id))
    )
    total_attempts = total_attempts_result.scalar()
    
    # Average user score
    avg_score_result = await db.execute(
        select(func.avg(User.total_score)).where(User.is_active == True)
    )
    average_score = avg_score_result.scalar() or 0.0
    
    # Most active users (top 5)
    top_users_result = await db.execute(
        select(User.username, User.total_score, User.quizzes_taken)
        .where(User.is_active == True)
        .order_by(User.total_score.desc())
        .limit(5)
    )
    top_users = [
        {
            "username": username,
            "total_score": total_score,
            "quizzes_taken": quizzes_taken
        }
        for username, total_score, quizzes_taken in top_users_result.all()
    ]
    
    return {
        "total_active_users": total_users,
        "total_quiz_attempts": total_attempts,
        "average_user_score": float(average_score),
        "top_users": top_users
    }


@router.get("/achievements")
async def get_achievements(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user achievements"""
    # For now, return placeholder achievements
    # TODO: Implement real achievement system when Achievement models are ready
    
    placeholder_achievements = [
        {
            "id": "first_quiz",
            "title": "First Steps",
            "description": "Complete your first quiz",
            "icon": "🎯",
            "earned": current_user.quizzes_taken > 0,
            "earned_at": current_user.created_at if current_user.quizzes_taken > 0 else None
        },
        {
            "id": "quiz_creator",
            "title": "Quiz Creator",
            "description": "Create your first questionnaire",
            "icon": "✏️",
            "earned": current_user.quizzes_created > 0,
            "earned_at": current_user.created_at if current_user.quizzes_created > 0 else None
        },
        {
            "id": "high_scorer",
            "title": "High Scorer",
            "description": "Achieve a total score of 500 points",
            "icon": "🏆",
            "earned": current_user.total_score >= 500,
            "earned_at": None
        },
        {
            "id": "quiz_master",
            "title": "Quiz Master",
            "description": "Complete 10 quizzes",
            "icon": "🎓",
            "earned": current_user.quizzes_taken >= 10,
            "earned_at": None
        }
    ]
    
    return {
        "achievements": placeholder_achievements,
        "total_earned": sum(1 for a in placeholder_achievements if a["earned"]),
        "total_available": len(placeholder_achievements)
    }


@router.get("/quiz-attempts")
async def get_user_quiz_attempts(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's quiz attempts with scores"""
    
    # Get user's completed quiz attempts with quiz info
    query = select(
        QuizAttempt.quiz_id,
        QuizAttempt.score,
        QuizAttempt.max_score,
        QuizAttempt.percentage,
        QuizAttempt.completed_at,
        Quiz.title
    ).join(
        Quiz, QuizAttempt.quiz_id == Quiz.id
    ).where(
        QuizAttempt.user_id == current_user.id,
        QuizAttempt.is_completed == True
    ).order_by(
        QuizAttempt.quiz_id,
        QuizAttempt.completed_at.desc()
    )
    
    result = await db.execute(query)
    attempts_data = result.all()
    
    # Group by quiz_id and get the latest attempt for each quiz
    quiz_attempts = {}
    for attempt_data in attempts_data:
        quiz_id = str(attempt_data.quiz_id)
        if quiz_id not in quiz_attempts:
            quiz_attempts[quiz_id] = {
                "quiz_id": quiz_id,
                "quiz_title": attempt_data.title,
                "last_score": attempt_data.score,
                "max_score": attempt_data.max_score,
                "last_percentage": round(attempt_data.percentage, 1),
                "last_completed_at": attempt_data.completed_at.isoformat() if attempt_data.completed_at else None
            }
    
    return list(quiz_attempts.values())


@router.get("/{user_id}", response_model=UserPublicProfile)
async def get_public_profile(
    user_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get public user profile by ID"""
    
    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalar_one_or_none()
    
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
    
    # Convert UUID to string for response
    user_dict = {
        "id": str(user.id),
        "username": user.username,
        "profile_picture": user.profile_picture,
        "bio": user.bio,
        "total_score": user.total_score,
        "quizzes_taken": user.quizzes_taken,
        "quizzes_created": user.quizzes_created,
        "created_at": user.created_at
    }
    return UserPublicProfile.model_validate(user_dict) 