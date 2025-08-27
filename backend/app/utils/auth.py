"""
Authentication utilities for JWT tokens and password hashing
"""

from datetime import datetime, timedelta, timezone
from typing import Optional, Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.schemas.auth import TokenData


# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData:
    """Verify and decode JWT token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        username: str = payload.get("username")
        
        if user_id is None:
            raise credentials_exception
            
        token_data = TokenData(user_id=user_id, username=username)
        return token_data
    except JWTError:
        raise credentials_exception


async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Get user by username"""
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Get user by email"""
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    """Get user by ID"""
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def authenticate_user(db: AsyncSession, username: str, password: str) -> Union[User, bool]:
    """Authenticate user with username/email and password"""
    # Try to find user by username first
    user = await get_user_by_username(db, username)
    
    # If not found by username, try email
    if not user:
        if "@" in username:  # Looks like an email
            user = await get_user_by_email(db, username)
    
    if not user:
        return False
    
    if not verify_password(password, user.password_hash):
        return False
    
    return user


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token)
    user = await get_user_by_id(db, token_data.user_id)
    
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Get current active user (must be active)"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def create_user_token_response(user: User, access_token: str) -> dict:
    """Create standardized token response"""
    from app.schemas.auth import UserResponse, Token
    
    # Convert UUID to string for response
    user_dict = {
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
    
    user_response = UserResponse.model_validate(user_dict)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,  # Convert to seconds
        user=user_response
    ).model_dump()