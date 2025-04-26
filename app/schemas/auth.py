from typing import Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    user_id: int


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserBase(BaseModel):
    username: str
    email: EmailStr
    grade_level: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True