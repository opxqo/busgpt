from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    phone: str = Field(..., pattern=r"^1[3-9]\d{9}$", description="Mobile phone number")
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
    phone: str
    nickname: str
    avatar: str
    role: str = "user"
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None
