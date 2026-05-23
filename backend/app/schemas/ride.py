from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from decimal import Decimal
from app.schemas.user import UserResponse
from app.schemas.product import ProductResponse

class RideBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    product: str = Field(..., description="Product type (chatgpt-plus, chatgpt-team, chatgpt-pro)")
    total_seats: int = Field(..., gt=1, le=20)
    price_per_month: Decimal = Field(..., gt=0)
    duration: int = Field(..., gt=0, le=24, description="Duration in months")
    warranty_days: Optional[int] = Field(None, gt=0, le=730, description="Guaranteed service days")
    description: Optional[str] = ""
    contact_info: str = Field(..., min_length=1, description="Owner contact info (WeChat, phone, etc.)")
    contact_website: Optional[str] = Field("", max_length=255, description="Owner personal website")
    contact_price: Decimal = Field(..., ge=0, description="Price to view contact info in CNY")

class RideCreate(RideBase):
    pass

class RideUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=2, max_length=100)
    product: Optional[str] = Field(None, description="Product type (chatgpt-plus, chatgpt-team, chatgpt-pro)")
    total_seats: Optional[int] = Field(None, gt=1, le=20)
    price_per_month: Optional[Decimal] = Field(None, gt=0)
    duration: Optional[int] = Field(None, gt=0, le=24)
    warranty_days: Optional[int] = Field(None, gt=0, le=730)
    description: Optional[str] = None
    contact_info: Optional[str] = None
    contact_website: Optional[str] = Field(None, max_length=255)
    contact_price: Optional[Decimal] = Field(None, ge=0)
    status: Optional[str] = Field(None, description="open, closed, expired")

class RideResponse(BaseModel):
    id: int
    title: str
    product: str
    owner_id: int
    total_seats: int
    price_per_month: Decimal
    duration: int
    warranty_days: int
    description: str
    contact_price: Decimal
    status: str
    created_at: datetime
    expires_at: datetime
    purchase_count: int = 0
    remaining_seats: int = 0
    owner: UserResponse
    product_details: Optional[ProductResponse] = None

    class Config:
        from_attributes = True

class RideDetailResponse(RideResponse):
    contact_info: Optional[str] = None  # Only populated for owner or paid users
    contact_website: Optional[str] = None  # Only populated for owner or paid users
    is_purchased: bool = False  # Whether current user has purchased

    class Config:
        from_attributes = True
