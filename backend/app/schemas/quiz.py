"""
Quiz schemas for request/response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    """Difficulty levels for quizzes"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class AIModel(str, Enum):
    """Available AI models for quiz generation"""
    LLAMA2 = "llama2"
    GEMINI = "gemini"
    TEMPLATE = "template"


class QuizQuestion(BaseModel):
    """Schema for quiz question"""
    question: str = Field(..., description="The question text")
    options: List[str] = Field(..., min_items=2, description="Answer options")
    question_type: str = Field("multiple_choice", description="Type of question")
    explanation: Optional[str] = Field(None, description="Explanation of the correct answer")


class QuizAnswer(BaseModel):
    """Schema for quiz answer (for internal use)"""
    question_index: int = Field(..., description="Index of the question")
    correct_option: int = Field(..., description="Index of the correct option")
    explanation: Optional[str] = Field(None, description="Explanation of the correct answer")


class QuizCreate(BaseModel):
    """Schema for creating a quiz from questionnaire"""
    questionnaire_id: str = Field(..., description="ID of the questionnaire to generate quiz from")
    title: Optional[str] = Field(None, description="Custom title for the quiz")
    time_limit: Optional[int] = Field(None, ge=1, le=180, description="Time limit in minutes")
    max_score: int = Field(100, ge=1, le=1000, description="Maximum score for the quiz")
    is_public: bool = Field(True, description="Whether quiz is publicly accessible")
    ai_model: Optional[AIModel] = Field(AIModel.LLAMA2, description="AI model to use for generation")


class QuizDirectCreate(BaseModel):
    """Schema for creating a quiz directly (without questionnaire)"""
    title: str = Field(..., min_length=1, max_length=200, description="Quiz title")
    description: Optional[str] = Field(None, description="Quiz description")
    subject: str = Field(..., min_length=1, max_length=100, description="Subject category")
    difficulty: DifficultyLevel = Field(DifficultyLevel.MEDIUM, description="Difficulty level")
    questions: List[QuizQuestion] = Field(..., min_items=1, description="List of questions")
    correct_answers: List[QuizAnswer] = Field(..., min_items=1, description="List of correct answers")
    time_limit: Optional[int] = Field(None, ge=1, le=180, description="Time limit in minutes")
    max_score: int = Field(100, ge=1, le=1000, description="Maximum score for the quiz")
    is_public: bool = Field(True, description="Whether quiz is publicly accessible")


class QuizResponse(BaseModel):
    """Schema for quiz response"""
    id: str
    questionnaire_id: Optional[str] = None
    creator_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    subject: str
    questions: List[Dict[str, Any]]  # Quiz questions with options
    correct_answers: List[Union[int, Dict[str, Any]]] = []  # Correct answers for scoring
    time_limit: Optional[int] = None
    difficulty: str
    max_score: int = 100
    is_global: bool = False
    is_public: bool = True
    is_template: bool = False
    ai_model_used: Optional[str] = None
    generation_time: Optional[int] = None
    times_taken: int = 0
    average_score: float = 0.0
    average_time: float = 0.0
    expires_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    # Additional computed fields
    question_count: int = 0
    creator_username: Optional[str] = None
    
    class Config:
        from_attributes = True


class QuizListResponse(BaseModel):
    """Schema for quiz list item"""
    id: str
    title: str
    description: Optional[str] = None
    subject: str
    difficulty: str
    question_count: int = 0
    max_score: int = 100
    time_limit: Optional[int] = None
    times_taken: int = 0
    average_score: float = 0.0
    is_public: bool = True
    ai_model_used: Optional[str] = None
    created_at: datetime
    creator_username: Optional[str] = None
    
    class Config:
        from_attributes = True


class QuizAttemptCreate(BaseModel):
    """Schema for starting a quiz attempt"""
    quiz_id: str = Field(..., description="ID of the quiz to attempt")


class QuizAttemptAnswer(BaseModel):
    """Schema for submitting quiz answers"""
    question_index: int = Field(..., ge=0, description="Index of the question")
    selected_option: int = Field(..., ge=0, description="Index of the selected option")


class QuizAttemptSubmit(BaseModel):
    """Schema for submitting quiz attempt"""
    attempt_id: str = Field(..., description="ID of the quiz attempt")
    answers: List[QuizAttemptAnswer] = Field(..., description="List of answers")
    time_taken: Optional[int] = Field(None, description="Time taken in seconds")


class QuizAttemptResponse(BaseModel):
    """Schema for quiz attempt response"""
    id: str
    user_id: str
    quiz_id: str
    score: int = 0
    max_score: int
    percentage: int = 0
    time_taken: int = 0
    started_at: datetime
    completed_at: Optional[datetime] = None
    is_completed: bool = False
    is_timed_out: bool = False
    correct_answers: int = 0
    incorrect_answers: int = 0
    skipped_answers: int = 0
    accuracy: int = 0
    speed: int = 0
    created_at: datetime
    
    # Quiz information
    quiz_title: Optional[str] = None
    quiz_subject: Optional[str] = None
    
    class Config:
        from_attributes = True


class QuizAttemptResult(BaseModel):
    """Schema for detailed quiz attempt results"""
    attempt: QuizAttemptResponse
    quiz: QuizResponse
    detailed_results: List[Dict[str, Any]]  # Question-by-question results
    user_rank: Optional[int] = None
    total_attempts: int = 0


class QuizStats(BaseModel):
    """Schema for quiz statistics"""
    total_quizzes: int
    public_quizzes: int
    ai_generated_quizzes: int
    template_quizzes: int
    total_attempts: int
    average_completion_rate: float
    most_popular_subjects: List[Dict[str, Any]]
    difficulty_distribution: Dict[str, int]
    ai_model_usage: Dict[str, int]