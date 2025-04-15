from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str
    grade_level: Optional[int] = None


class UserLogin(BaseModel):
    username: str
    password: str


class UserProfile(UserBase):
    id: int
    grade_level: Optional[int] = None
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int


class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None