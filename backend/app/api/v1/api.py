"""
Main API router for v1 endpoints
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, questionnaires, quizzes, leaderboards, ai

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(questionnaires.router, prefix="/questionnaires", tags=["questionnaires"])
api_router.include_router(quizzes.router, prefix="/quizzes", tags=["quizzes"])
api_router.include_router(leaderboards.router, prefix="/leaderboards", tags=["leaderboards"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"]) 