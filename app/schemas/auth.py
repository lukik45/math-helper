from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, validator


class UserBase(BaseModel):
    """Base user schema with shared attributes"""
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    grade_level: Optional[int] = Field(None, ge=1, le=12)


class UserCreate(UserBase):
    """Schema for user creation with password"""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for user updates"""
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    grade_level: Optional[int] = Field(None, ge=1, le=12)
    is_active: Optional[bool] = None
    password: Optional[str] = Field(None, min_length=8)


class UserResponse(UserBase):
    """Schema for user response data"""
    id: int
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token"""
    access_token: str
    token_type: str
    user_id: int


class TokenPayload(BaseModel):
    """Schema for token payload"""
    sub: Optional[int] = None
    exp: Optional[datetime] = None