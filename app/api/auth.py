from datetime import datetime, timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.postgres import get_db
from app.core.config import settings
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user,
)

# These will be implemented with the complete models
# from app.models.users import User
# from app.schemas.auth import UserCreate, UserResponse, Token

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(
    # user_in: UserCreate,
    db: Session = Depends(get_db)
) -> Any:
    """
    Register a new user.
    
    Note: This is a stub that will be fully implemented once schemas are created.
    """
    # Check if username or email already exists
    # existing_user = db.query(User).filter(
    #     (User.username == user_in.username) | (User.email == user_in.email)
    # ).first()
    # if existing_user:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Username or email already registered"
    #     )
    
    # Create new user
    # hashed_password = get_password_hash(user_in.password)
    # user = User(
    #     username=user_in.username,
    #     email=user_in.email,
    #     hashed_password=hashed_password,
    #     grade_level=user_in.grade_level
    # )
    # db.add(user)
    # db.commit()
    # db.refresh(user)
    
    # Return the created user (without password)
    # return UserResponse.model_validate(user)
    
    # Placeholder return
    return {"message": "User registration endpoint (to be implemented)"}


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Any:
    """
    Get access token for user authentication.
    
    Note: This is a stub that will be fully implemented once models are created.
    """
    # Authenticate user
    # user = db.query(User).filter(User.username == form_data.username).first()
    # if not user or not verify_password(form_data.password, user.hashed_password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect username or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )

    # Update last login
    # user.last_login = datetime.utcnow()
    # db.commit()
    
    # Create access token
    # access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # access_token = create_access_token(
    #     subject=user.id, expires_delta=access_token_expires
    # )
    
    # Return the token
    # return Token(
    #     access_token=access_token,
    #     token_type="bearer",
    #     user_id=user.id
    # )
    
    # Placeholder return
    return {
        "access_token": "dummy_token",
        "token_type": "bearer",
        "user_id": 1
    }


@router.get("/user")
async def get_user_info(
    current_user: Any = Depends(get_current_user)
) -> Any:
    """
    Get information about the current user.
    
    Note: This is a stub that will be fully implemented once models are created.
    """
    # Return user info
    # return UserResponse.model_validate(current_user)
    
    # Placeholder return
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "grade_level": 8
    }