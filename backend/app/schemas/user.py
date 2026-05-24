from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    nickname: str = Field(..., min_length=2, max_length=50)
    avatar: Optional[str] = ""


class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=30)


class UserUpdate(BaseModel):
    nickname: Optional[str] = Field(None, min_length=2, max_length=50)
    avatar: Optional[str] = ""


class PasswordChange(BaseModel):
    current_password: str = Field(..., min_length=6, max_length=30)
    new_password: str = Field(..., min_length=6, max_length=30)


class UserResponse(BaseModel):
    id: int
    email: Optional[str] = None
    phone: Optional[str] = None
    nickname: str
    avatar: str
    role: str = "user"
    is_active: bool = True
    email_verified: bool = False
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[str] = None


class ResendActivationRequest(BaseModel):
    email: EmailStr
