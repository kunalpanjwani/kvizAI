"""
Quiz management endpoints
"""

from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc, delete
from typing import List, Optional

from app.core.database import get_db
from app.models.user import User
from app.models.questionnaire import Questionnaire
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt
from app.schemas.quiz import (
    QuizCreate,
    QuizDirectCreate,
    QuizResponse,
    QuizListResponse,
    QuizAttemptCreate,
    QuizAttemptSubmit,
    QuizAttemptResponse,
    QuizAttemptResult,
    QuizStats,
    DifficultyLevel,
    AIModel
)
from app.utils.auth import get_current_active_user
from app.utils.serializers import quiz_to_dict, quiz_to_list_dict, quiz_attempt_to_dict

router = APIRouter()


@router.post("/create-direct", response_model=QuizResponse)
async def create_quiz_direct(
    quiz_data: QuizDirectCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a quiz directly with questions and answers"""
    
    # Create quiz questions from the provided data
    quiz_questions = []
    correct_answers_data = []
    
    for question in quiz_data.questions:
        quiz_questions.append({
            "question": question.question,
            "options": question.options,
            "question_type": question.question_type,
            "explanation": question.explanation
        })
    
    # Process correct answers
    for answer in quiz_data.correct_answers:
        correct_answers_data.append(answer.correct_option)
    
    # Create new quiz
    new_quiz = Quiz(
        title=quiz_data.title,
        description=quiz_data.description,
        subject=quiz_data.subject,
        difficulty=quiz_data.difficulty.value,
        questions=quiz_questions,
        correct_answers=correct_answers_data,
        time_limit=quiz_data.time_limit,
        max_score=quiz_data.max_score,
        creator_id=current_user.id,
        is_public=quiz_data.is_public,
        ai_model_used="direct"
    )
    
    db.add(new_quiz)
    await db.commit()
    
    # Get creator username
    creator_username = current_user.username
    
    # Prepare response - convert UUIDs to strings
    quiz_dict = quiz_to_dict(new_quiz, creator_username)
    return QuizResponse.model_validate(quiz_dict)


@router.post("/generate", response_model=QuizResponse)
async def generate_quiz(
    quiz_data: QuizCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Generate a quiz from questionnaire (placeholder - will implement AI later)"""
    
    # Get questionnaire
    questionnaire_result = await db.execute(
        select(Questionnaire).where(Questionnaire.id == quiz_data.questionnaire_id)
    )
    questionnaire = questionnaire_result.scalar_one_or_none()
    
    if not questionnaire:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Questionnaire not found"
        )
    
    # Check access to questionnaire
    if not questionnaire.is_public and questionnaire.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to private questionnaire"
        )
    
    # For now, create a simple quiz from questionnaire questions
    # TODO: Implement AI generation
    quiz_questions = []
    correct_answers = []
    
    for i, q in enumerate(questionnaire.questions):
        question_text = q.get("question", "")
        # Create simple multiple choice question (placeholder)
        quiz_questions.append({
            "question": question_text,
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "question_type": "multiple_choice"
        })
        correct_answers.append({
            "question_index": i,
            "correct_option": 0,  # Placeholder - first option
            "explanation": "This is a placeholder explanation."
        })
    
    # Create quiz
    new_quiz = Quiz(
        questionnaire_id=questionnaire.id,
        creator_id=current_user.id,
        title=quiz_data.title or f"Quiz: {questionnaire.title}",
        description=f"Generated from questionnaire: {questionnaire.title}",
        subject=questionnaire.subject,
        questions=quiz_questions,
        correct_answers=correct_answers,
        time_limit=quiz_data.time_limit,
        difficulty=questionnaire.difficulty_level,
        max_score=quiz_data.max_score,
        is_public=quiz_data.is_public,
        ai_model_used=quiz_data.ai_model.value if quiz_data.ai_model else "template",
        generation_time=1  # Placeholder
    )
    
    db.add(new_quiz)
    await db.commit()
    await db.refresh(new_quiz)
    
    # Update questionnaire usage
    questionnaire.increment_usage()
    await db.commit()
    
    # Prepare response - convert UUIDs to strings
    quiz_dict = quiz_to_dict(new_quiz, current_user.username)
    return QuizResponse.model_validate(quiz_dict)


@router.get("/", response_model=List[QuizListResponse])
async def get_quizzes(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    subject: Optional[str] = Query(None),
    difficulty: Optional[DifficultyLevel] = Query(None),
    search: Optional[str] = Query(None),
    current_user: Optional[User] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of quizzes"""
    
    query = select(Quiz, User.username).outerjoin(User, Quiz.creator_id == User.id)
    
    conditions = []
    
    # Show public quizzes and user's own quizzes
    if current_user:
        conditions.append(
            or_(Quiz.is_public == True, Quiz.creator_id == current_user.id)
        )
    else:
        conditions.append(Quiz.is_public == True)
    
    if subject:
        conditions.append(Quiz.subject.ilike(f"%{subject}%"))
    
    if difficulty:
        conditions.append(Quiz.difficulty == difficulty.value)
    
    if search:
        search_condition = or_(
            Quiz.title.ilike(f"%{search}%"),
            Quiz.description.ilike(f"%{search}%")
        )
        conditions.append(search_condition)
    
    if conditions:
        query = query.where(and_(*conditions))
    
    query = query.order_by(Quiz.created_at.desc()).offset(skip).limit(limit)
    
    result = await db.execute(query)
    quizzes_with_creators = result.all()
    
    # Prepare response - convert UUIDs to strings
    response_list = []
    for quiz, creator_username in quizzes_with_creators:
        quiz_dict = quiz_to_list_dict(quiz, creator_username)
        response_list.append(QuizListResponse.model_validate(quiz_dict))
    
    return response_list


@router.post("/{quiz_id}/start", response_model=QuizAttemptResponse)
async def start_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Start a quiz attempt"""
    
    quiz_result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = quiz_result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    if not quiz.is_public and quiz.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to private quiz"
        )
    
    new_attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz.id,
        max_score=quiz.max_score
    )
    
    db.add(new_attempt)
    await db.commit()
    
    # Use the original object without refresh - all required fields should be available
    # The UUIDs and timestamps are generated by the database, but we can work with what we have
    attempt_dict = quiz_attempt_to_dict(new_attempt, quiz.title, quiz.subject)
    return QuizAttemptResponse.model_validate(attempt_dict)


@router.get("/{quiz_id}", response_model=QuizResponse)
async def get_quiz(
    quiz_id: str,
    current_user: Optional[User] = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Get quiz by ID"""
    
    quiz_result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = quiz_result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Check access permissions
    if not quiz.is_public and (not current_user or quiz.creator_id != current_user.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to private quiz"
        )
    
    # Get creator username
    creator_result = await db.execute(select(User.username).where(User.id == quiz.creator_id))
    creator_username = creator_result.scalar_one_or_none() or "Unknown"
    
    # Prepare response - convert UUIDs to strings
    quiz_dict = quiz_to_dict(quiz, creator_username)
    return QuizResponse.model_validate(quiz_dict)


@router.delete("/{quiz_id}")
async def delete_quiz(
    quiz_id: str,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a quiz"""
    
    # Get quiz
    quiz_result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = quiz_result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Check if user owns the quiz or is admin
    if quiz.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this quiz"
        )
    
    # Delete associated quiz attempts first
    await db.execute(delete(QuizAttempt).where(QuizAttempt.quiz_id == quiz_id))
    
    # Delete the quiz
    await db.delete(quiz)
    await db.commit()
    
    return {"message": "Quiz deleted successfully"}


@router.post("/{quiz_id}/submit")
async def submit_quiz(
    quiz_id: str,
    submission_data: dict,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit quiz answers and complete the attempt"""
    
    # Get the quiz
    quiz_result = await db.execute(select(Quiz).where(Quiz.id == quiz_id))
    quiz = quiz_result.scalar_one_or_none()
    
    if not quiz:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Quiz not found"
        )
    
    # Get the most recent active attempt for this user and quiz
    attempt_result = await db.execute(
        select(QuizAttempt).where(
            QuizAttempt.user_id == current_user.id,
            QuizAttempt.quiz_id == quiz.id,
            QuizAttempt.is_completed == False
        ).order_by(QuizAttempt.created_at.desc())
    )
    attempt = attempt_result.first()
    if attempt:
        attempt = attempt[0]  # Extract the QuizAttempt object from the Row
    
    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active quiz attempt found"
        )
    
    # Extract submission data
    answers = submission_data.get("answers", [])
    time_taken = submission_data.get("time_taken", 0)
    
    # Calculate score
    correct_count = 0
    total_questions = len(quiz.questions)
    
    # Compare user answers with stored correct answers
    for i, user_answer in enumerate(answers):
        if i < len(quiz.correct_answers) and i < total_questions:
            # Get the correct answer for this question
            correct_answer = quiz.correct_answers[i]
            
            # Handle both simple integer answers and complex answer objects
            if isinstance(correct_answer, dict):
                # If correct_answer is a dict with question_index and correct_option
                correct_option = correct_answer.get("correct_option")
            else:
                # If correct_answer is just an integer (0-indexed option)
                correct_option = correct_answer
            
            # Compare user's answer with correct option
            if user_answer == correct_option:
                correct_count += 1
    
    score = int((correct_count / total_questions) * quiz.max_score) if total_questions > 0 else 0
    percentage = (correct_count / total_questions) * 100 if total_questions > 0 else 0
    accuracy = percentage
    
    # Update the attempt
    attempt.answers = answers  # Store user's answers
    attempt.score = score
    attempt.percentage = int(round(percentage))  # Convert to integer for database
    attempt.time_taken = time_taken
    attempt.is_completed = True
    attempt.completed_at = func.now()
    attempt.correct_answers = correct_count
    attempt.incorrect_answers = total_questions - correct_count
    attempt.skipped_answers = 0  # Assuming no skipped answers for now
    attempt.accuracy = int(round(accuracy))  # Convert to integer for database
    attempt.speed = int(total_questions / (time_taken / 60)) if time_taken > 0 else 0  # Convert to integer
    
    # Update user statistics
    current_user.add_score(score)
    current_user.increment_quizzes_taken()
    
    # Update quiz statistics
    quiz.times_taken += 1
    
    # Recalculate quiz average score
    quiz_attempts_result = await db.execute(
        select(func.avg(QuizAttempt.percentage)).where(
            QuizAttempt.quiz_id == quiz.id,
            QuizAttempt.is_completed == True
        )
    )
    quiz_avg_percentage = quiz_attempts_result.scalar() or 0.0
    quiz.average_score = float(quiz_avg_percentage)
    
    # Recalculate quiz average time
    quiz_time_result = await db.execute(
        select(func.avg(QuizAttempt.time_taken)).where(
            QuizAttempt.quiz_id == quiz.id,
            QuizAttempt.is_completed == True
        )
    )
    quiz_avg_time = quiz_time_result.scalar() or 0.0
    quiz.average_time = float(quiz_avg_time)
    
    await db.commit()
    await db.refresh(attempt)
    await db.refresh(current_user)
    
    # Prepare response
    attempt_dict = quiz_attempt_to_dict(attempt, quiz.title, quiz.subject)
    return QuizAttemptResponse.model_validate(attempt_dict)