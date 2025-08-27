"""
Questionnaire schemas for request/response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    """Difficulty levels for questionnaires"""
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class QuestionnaireQuestion(BaseModel):
    """Schema for individual questionnaire question"""
    question: str = Field(..., description="The question text")
    context: Optional[str] = Field(None, description="Additional context or background information")
    keywords: Optional[List[str]] = Field(None, description="Keywords related to this question")
    expected_answer_type: Optional[str] = Field(None, description="Expected type of answer (e.g., 'multiple_choice', 'short_answer')")


class QuestionnaireCreate(BaseModel):
    """Schema for creating a new questionnaire"""
    title: str = Field(..., min_length=1, max_length=200, description="Questionnaire title")
    description: Optional[str] = Field(None, description="Questionnaire description")
    subject: str = Field(..., min_length=1, max_length=100, description="Subject category")
    difficulty_level: DifficultyLevel = Field(DifficultyLevel.MEDIUM, description="Difficulty level")
    questions: List[QuestionnaireQuestion] = Field(..., min_items=1, description="List of questions")
    is_public: bool = Field(False, description="Whether questionnaire is publicly accessible")


class QuestionnaireUpdate(BaseModel):
    """Schema for updating a questionnaire"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="Questionnaire title")
    description: Optional[str] = Field(None, description="Questionnaire description")
    subject: Optional[str] = Field(None, min_length=1, max_length=100, description="Subject category")
    difficulty_level: Optional[DifficultyLevel] = Field(None, description="Difficulty level")
    questions: Optional[List[QuestionnaireQuestion]] = Field(None, min_items=1, description="List of questions")
    is_public: Optional[bool] = Field(None, description="Whether questionnaire is publicly accessible")


class QuestionnaireResponse(BaseModel):
    """Schema for questionnaire response"""
    id: str
    creator_id: str
    title: str
    description: Optional[str] = None
    subject: str
    difficulty_level: str
    questions: List[Dict[str, Any]]  # JSON questions
    version: int = 1
    is_public: bool = False
    is_template: bool = False
    times_used: int = 0
    average_score: int = 0
    question_count: int = 0
    created_at: datetime
    updated_at: datetime
    
    # Creator information
    creator_username: Optional[str] = None
    
    class Config:
        from_attributes = True


class QuestionnaireListResponse(BaseModel):
    """Schema for questionnaire list item"""
    id: str
    title: str
    description: Optional[str] = None
    subject: str
    difficulty_level: str
    question_count: int = 0
    times_used: int = 0
    average_score: int = 0
    is_public: bool = False
    is_template: bool = False
    created_at: datetime
    creator_username: Optional[str] = None
    
    class Config:
        from_attributes = True


class QuestionnaireStats(BaseModel):
    """Schema for questionnaire statistics"""
    total_questionnaires: int
    public_questionnaires: int
    template_questionnaires: int
    user_questionnaires: int
    most_popular_subjects: List[Dict[str, Any]]
    difficulty_distribution: Dict[str, int]