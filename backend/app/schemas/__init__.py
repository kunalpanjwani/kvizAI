# Pydantic schemas package

from .auth import (
    UserCreate,
    UserLogin,
    UserResponse,
    Token,
    TokenData,
    RefreshToken,
    PasswordChange,
    PasswordReset,
    PasswordResetConfirm
)

from .user import (
    UserProfile,
    UserProfileUpdate,
    UserStats,
    UserPublicProfile
)

from .questionnaire import (
    QuestionnaireCreate,
    QuestionnaireUpdate,
    QuestionnaireResponse,
    QuestionnaireListResponse,
    QuestionnaireStats,
    QuestionnaireQuestion,
    DifficultyLevel
)

from .quiz import (
    QuizCreate,
    QuizDirectCreate,
    QuizResponse,
    QuizListResponse,
    QuizAttemptCreate,
    QuizAttemptSubmit,
    QuizAttemptResponse,
    QuizAttemptResult,
    QuizStats,
    QuizQuestion,
    QuizAnswer,
    AIModel
)

__all__ = [
    "UserCreate",
    "UserLogin", 
    "UserResponse",
    "Token",
    "TokenData",
    "RefreshToken",
    "PasswordChange",
    "PasswordReset",
    "PasswordResetConfirm",
    "UserProfile",
    "UserProfileUpdate",
    "UserStats",
    "UserPublicProfile",
    "QuestionnaireCreate",
    "QuestionnaireUpdate",
    "QuestionnaireResponse",
    "QuestionnaireListResponse",
    "QuestionnaireStats",
    "QuestionnaireQuestion",
    "DifficultyLevel",
    "QuizCreate",
    "QuizDirectCreate",
    "QuizResponse",
    "QuizListResponse",
    "QuizAttemptCreate",
    "QuizAttemptSubmit",
    "QuizAttemptResponse",
    "QuizAttemptResult",
    "QuizStats",
    "QuizQuestion",
    "QuizAnswer",
    "AIModel"
]