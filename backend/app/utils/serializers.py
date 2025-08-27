"""
Serialization utilities for converting models to response formats
"""

from app.models.user import User
from app.models.questionnaire import Questionnaire
from app.models.quiz import Quiz
from app.models.quiz_attempt import QuizAttempt


def user_to_dict(user: User) -> dict:
    """Convert User model to dictionary with string UUID"""
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "profile_picture": user.profile_picture,
        "bio": user.bio,
        "total_score": user.total_score,
        "quizzes_taken": user.quizzes_taken,
        "quizzes_created": user.quizzes_created,
        "is_active": user.is_active,
        "is_verified": user.is_verified,
        "created_at": user.created_at,
        "last_login": user.last_login
    }


def user_to_public_dict(user: User) -> dict:
    """Convert User model to public profile dictionary with string UUID"""
    return {
        "id": str(user.id),
        "username": user.username,
        "profile_picture": user.profile_picture,
        "bio": user.bio,
        "total_score": user.total_score,
        "quizzes_taken": user.quizzes_taken,
        "quizzes_created": user.quizzes_created,
        "created_at": user.created_at
    }


def questionnaire_to_dict(questionnaire: Questionnaire, creator_username: str = None) -> dict:
    """Convert Questionnaire model to dictionary with string UUIDs"""
    return {
        "id": str(questionnaire.id),
        "creator_id": str(questionnaire.creator_id),
        "title": questionnaire.title,
        "description": questionnaire.description,
        "subject": questionnaire.subject,
        "difficulty_level": questionnaire.difficulty_level,
        "questions": questionnaire.questions,
        "version": questionnaire.version,
        "is_public": questionnaire.is_public,
        "is_template": questionnaire.is_template,
        "times_used": questionnaire.times_used,
        "average_score": questionnaire.average_score,
        "question_count": len(questionnaire.questions) if questionnaire.questions else 0,
        "created_at": questionnaire.created_at,
        "updated_at": questionnaire.updated_at,
        "creator_username": creator_username
    }


def questionnaire_to_list_dict(questionnaire: Questionnaire, creator_username: str = None) -> dict:
    """Convert Questionnaire model to list response dictionary with string UUIDs"""
    return {
        "id": str(questionnaire.id),
        "title": questionnaire.title,
        "description": questionnaire.description,
        "subject": questionnaire.subject,
        "difficulty_level": questionnaire.difficulty_level,
        "question_count": len(questionnaire.questions) if questionnaire.questions else 0,
        "times_used": questionnaire.times_used,
        "average_score": questionnaire.average_score,
        "is_public": questionnaire.is_public,
        "is_template": questionnaire.is_template,
        "created_at": questionnaire.created_at,
        "creator_username": creator_username
    }


def quiz_to_dict(quiz: Quiz, creator_username: str = None) -> dict:
    """Convert Quiz model to dictionary with string UUIDs"""
    return {
        "id": str(quiz.id),
        "questionnaire_id": str(quiz.questionnaire_id) if quiz.questionnaire_id else None,
        "creator_id": str(quiz.creator_id) if quiz.creator_id else None,
        "title": quiz.title,
        "description": quiz.description,
        "subject": quiz.subject,
        "questions": quiz.questions,
        "correct_answers": quiz.correct_answers,
        "time_limit": quiz.time_limit,
        "difficulty": quiz.difficulty,
        "max_score": quiz.max_score,
        "is_global": quiz.is_global,
        "is_public": quiz.is_public,
        "is_template": quiz.is_template,
        "ai_model_used": quiz.ai_model_used,
        "generation_time": quiz.generation_time,
        "times_taken": quiz.times_taken,
        "average_score": quiz.average_score,
        "average_time": quiz.average_time,
        "expires_at": quiz.expires_at,
        "created_at": quiz.created_at,
        "updated_at": quiz.updated_at,
        "question_count": len(quiz.questions) if quiz.questions else 0,
        "creator_username": creator_username
    }


def quiz_to_list_dict(quiz: Quiz, creator_username: str = None) -> dict:
    """Convert Quiz model to list response dictionary with string UUIDs"""
    return {
        "id": str(quiz.id),
        "title": quiz.title,
        "description": quiz.description,
        "subject": quiz.subject,
        "difficulty": quiz.difficulty,
        "question_count": len(quiz.questions) if quiz.questions else 0,
        "max_score": quiz.max_score,
        "time_limit": quiz.time_limit,
        "times_taken": quiz.times_taken,
        "average_score": quiz.average_score,
        "is_public": quiz.is_public,
        "ai_model_used": quiz.ai_model_used,
        "created_at": quiz.created_at,
        "creator_username": creator_username
    }


def quiz_attempt_to_dict(attempt: QuizAttempt, quiz_title: str = None, quiz_subject: str = None) -> dict:
    """Convert QuizAttempt model to dictionary with string UUIDs"""
    from datetime import datetime, timezone
    
    # Handle server-default timestamps that might not be available on new objects
    now = datetime.now(timezone.utc)
    
    return {
        "id": str(attempt.id),
        "user_id": str(attempt.user_id),
        "quiz_id": str(attempt.quiz_id),
        "score": attempt.score,
        "max_score": attempt.max_score,
        "percentage": attempt.percentage,
        "time_taken": attempt.time_taken,
        "started_at": attempt.started_at if attempt.started_at else now,
        "completed_at": attempt.completed_at,
        "is_completed": attempt.is_completed,
        "is_timed_out": attempt.is_timed_out,
        "correct_answers": attempt.correct_answers,
        "incorrect_answers": attempt.incorrect_answers,
        "skipped_answers": attempt.skipped_answers,
        "accuracy": attempt.accuracy,
        "speed": attempt.speed,
        "created_at": attempt.created_at if attempt.created_at else now,
        "quiz_title": quiz_title,
        "quiz_subject": quiz_subject
    }