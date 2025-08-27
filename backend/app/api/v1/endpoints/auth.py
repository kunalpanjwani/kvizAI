"""
Authentication endpoints
"""

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.utils.auth import (
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_active_user,
    create_user_token_response
)

router = APIRouter()


@router.post("/register", response_model=Token)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """Register a new user"""
    
    # Check if username already exists
    existing_user = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    if existing_user.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    existing_email = await db.execute(
        select(User).where(User.email == user_data.email)
    )
    if existing_email.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(new_user.id), "username": new_user.username}
    )
    
    return create_user_token_response(new_user, access_token)


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """Login user with username/email and password"""
    
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login time
    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return create_user_token_response(user, access_token)


@router.post("/login-json", response_model=Token)
async def login_json(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    """Login user with JSON payload (alternative to form data)"""
    
    user = await authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password"
        )
    
    # Update last login time
    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    
    # Create access token
    access_token = create_access_token(
        data={"sub": str(user.id), "username": user.username}
    )
    
    return create_user_token_response(user, access_token)


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_active_user)):
    """Get current user information"""
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
    return UserResponse.model_validate(user_dict)


@router.post("/refresh")
async def refresh_token():
    """Refresh access token"""
    # For now, we'll use stateless JWT tokens
    # In production, consider implementing refresh tokens with database storage
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh token not implemented - use login to get new token"
    )


@router.post("/logout")
async def logout():
    """Logout user"""
    # With stateless JWT tokens, logout is handled client-side
    # In production, consider implementing token blacklisting
    return {"message": "Logout successful - remove token from client storage"}