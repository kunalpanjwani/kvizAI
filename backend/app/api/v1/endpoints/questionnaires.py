"""
Questionnaire management endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from typing import List, Optional

from app.core.database import get_db
from app.models.user import User
from app.models.questionnaire import Questionnaire
from app.schemas.questionnaire import (
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireResponse,
    QuestionnaireListResponse,
    QuestionnaireStats,
    DifficultyLevel
)
from app.utils.auth import get_current_active_user
from app.utils.serializers import questionnaire_to_dict, questionnaire_to_list_dict

router = APIRouter()


@router.post("/", response_model=QuestionnaireResponse)
async def create_questionnaire(
    questionnaire_data: QuestionnaireCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new questionnaire"""
    
    # Convert questions to JSON format
    questions_json = [question.model_dump() for question in questionnaire_data.questions]
    
    # Create new questionnaire
    new_questionnaire = Questionnaire(
        creator_id=current_user.id,
        title=questionnaire_data.title,
        description=questionnaire_data.description,
        subject=questionnaire_data.subject,
        difficulty_level=questionnaire_data.difficulty_level.value,
        questions=questions_json,
        is_public=questionnaire_data.is_public
    )
    
    db.add(new_questionnaire)
    await db.commit()
    await db.refresh(new_questionnaire)
    
    # Update user's questionnaire count
    current_user.increment_quizzes_created()
    await db.commit()
    
    # Prepare response with creator info - convert UUIDs to strings
    questionnaire_dict = questionnaire_to_dict(new_questionnaire, current_user.username)
    return QuestionnaireResponse.model_validate(questionnaire_dict)


@router.get("/", response_model=List[QuestionnaireListResponse])
async def get_questionnaires(
    skip: int = Query(0, ge=0, description="Number of questionnaires to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of questionnaires to return"),
    subject: Optional[str] = Query(None, description="Filter by subject"),
    difficulty: Optional[DifficultyLevel] = Query(None, description="Filter by difficulty level"),
    is_public: Optional[bool] = Query(None, description="Filter by public/private status"),
    search: Optional[str] = Query(None, description="Search in title and description"),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of questionnaires"""
    
    query = select(Questionnaire, User.username).join(User, Questionnaire.creator_id == User.id)
    
    # Apply filters
    conditions = []
    
    # Show public questionnaires and user's own questionnaires
    if current_user:
        conditions.append(
            or_(
                Questionnaire.is_public == True,
                Questionnaire.creator_id == current_user.id
            )
        )
    else:
        conditions.append(Questionnaire.is_public == True)
    
    if subject:
        conditions.append(Questionnaire.subject.ilike(f"%{subject}%"))
    
    if difficulty:
        conditions.append(Questionnaire.difficulty_level == difficulty.value)
    
    if is_public is not None:
        conditions.append(Questionnaire.is_public == is_public)
    
    if search:
        search_condition = or_(
            Questionnaire.title.ilike(f"%{search}%"),
            Questionnaire.description.ilike(f"%{search}%")
        )
        conditions.append(search_condition)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    # Order by most recent first
    query = query.order_by(Questionnaire.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    questionnaires_with_creators = result.all()
    
    # Prepare response - convert UUIDs to strings
    response_list = []
    for questionnaire, creator_username in questionnaires_with_creators:
        questionnaire_dict = questionnaire_to_list_dict(questionnaire, creator_username)
        response_list.append(QuestionnaireListResponse.model_validate(questionnaire_dict))
    
    return response_list


@router.get("/my", response_model=List[QuestionnaireListResponse])
async def get_my_questionnaires(
    skip: int = Query(0, ge=0, description="Number of questionnaires to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of questionnaires to return"),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user's questionnaires"""
    
    query = select(Questionnaire).where(
        Questionnaire.creator_id == current_user.id
    ).order_by(Questionnaire.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    questionnaires = result.scalars().all()
    
    # Prepare response - convert UUIDs to strings
    response_list = []
    for questionnaire in questionnaires:
        questionnaire_dict = questionnaire_to_list_dict(questionnaire, current_user.username)
        response_list.append(QuestionnaireListResponse.model_validate(questionnaire_dict))
    
    return response_list


@router.get("/{questionnaire_id}", response_model=QuestionnaireResponse)
async def get_questionnaire(
    questionnaire_id: str,
    current_user: Optional[User] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific questionnaire by ID"""
    
    # Get questionnaire with creator info
    query = select(Questionnaire, User.username).join(
        User, Questionnaire.creator_id == User.id
    ).where(Questionnaire.id == questionnaire_id)
    
    result = await db.execute(query)
    questionnaire_with_creator = result.first()
    
    if not questionnaire_with_creator:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )
    
    questionnaire, creator_username = questionnaire_with_creator
    
    # Check access permissions
    if not questionnaire.is_public and (
        not current_user or questionnaire.creator_id != current_user.id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to private questionnaire"
        )
    
    # Prepare response - convert UUIDs to strings
    questionnaire_dict = questionnaire_to_dict(questionnaire, creator_username)
    return QuestionnaireResponse.model_validate(questionnaire_dict)


@router.put("/{questionnaire_id}", response_model=QuestionnaireResponse)
async def update_questionnaire(
    questionnaire_id: str,
    questionnaire_data: QuestionnaireUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Update a questionnaire"""
    
    # Get questionnaire
    result = await db.execute(
        select(Questionnaire).where(Questionnaire.id == questionnaire_id)
    )
    questionnaire = result.scalar_one_or_none()
    
    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )
    
    # Check ownership
    if questionnaire.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own questionnaires"
        )
    
    # Update fields
    if questionnaire_data.title is not None:
        questionnaire.title = questionnaire_data.title
    
    if questionnaire_data.description is not None:
        questionnaire.description = questionnaire_data.description
    
    if questionnaire_data.subject is not None:
        questionnaire.subject = questionnaire_data.subject
    
    if questionnaire_data.difficulty_level is not None:
        questionnaire.difficulty_level = questionnaire_data.difficulty_level.value
    
    if questionnaire_data.questions is not None:
        questionnaire.questions = [q.model_dump() for q in questionnaire_data.questions]
        questionnaire.version += 1
    
    if questionnaire_data.is_public is not None:
        questionnaire.is_public = questionnaire_data.is_public
    
    await db.commit()
    await db.refresh(questionnaire)
    
    # Prepare response - convert UUIDs to strings
    questionnaire_dict = questionnaire_to_dict(questionnaire, current_user.username)
    return QuestionnaireResponse.model_validate(questionnaire_dict)


@router.delete("/{questionnaire_id}")
async def delete_questionnaire(
    questionnaire_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a questionnaire"""
    
    # Get questionnaire
    result = await db.execute(
        select(Questionnaire).where(Questionnaire.id == questionnaire_id)
    )
    questionnaire = result.scalar_one_or_none()
    
    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )
    
    # Check ownership
    if questionnaire.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own questionnaires"
        )
    
    await db.delete(questionnaire)
    await db.commit()
    
    # Update user's questionnaire count
    current_user.quizzes_created = max(0, current_user.quizzes_created - 1)
    await db.commit()
    
    return {"message": "Questionnaire deleted successfully"}


@router.get("/stats/overview", response_model=QuestionnaireStats)
async def get_questionnaire_stats(db: AsyncSession = Depends(get_db)):
    """Get questionnaire statistics overview"""
    
    # Total questionnaires
    total_result = await db.execute(select(func.count(Questionnaire.id)))
    total_questionnaires = total_result.scalar()
    
    # Public questionnaires
    public_result = await db.execute(
        select(func.count(Questionnaire.id)).where(Questionnaire.is_public == True)
    )
    public_questionnaires = public_result.scalar()
    
    # Template questionnaires
    template_result = await db.execute(
        select(func.count(Questionnaire.id)).where(Questionnaire.is_template == True)
    )
    template_questionnaires = template_result.scalar()
    
    # Most popular subjects
    subjects_result = await db.execute(
        select(Questionnaire.subject, func.count(Questionnaire.id).label('count'))
        .group_by(Questionnaire.subject)
        .order_by(func.count(Questionnaire.id).desc())
        .limit(10)
    )
    most_popular_subjects = [
        {"subject": subject, "count": count} 
        for subject, count in subjects_result.all()
    ]
    
    # Difficulty distribution
    difficulty_result = await db.execute(
        select(Questionnaire.difficulty_level, func.count(Questionnaire.id).label('count'))
        .group_by(Questionnaire.difficulty_level)
    )
    difficulty_distribution = {
        difficulty: count for difficulty, count in difficulty_result.all()
    }
    
    return QuestionnaireStats(
        total_questionnaires=total_questionnaires,
        public_questionnaires=public_questionnaires,
        template_questionnaires=template_questionnaires,
        user_questionnaires=total_questionnaires - public_questionnaires,
        most_popular_subjects=most_popular_subjects,
        difficulty_distribution=difficulty_distribution
    )