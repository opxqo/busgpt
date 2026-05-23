from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from decimal import Decimal
from app.schemas.user import UserResponse

class OrderCreate(BaseModel):
    ride_id: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    ride_id: int
    amount: Decimal
    status: str
    payment_provider: str = "mock"
    payment_no: Optional[str] = None
    payment_status: str = "pending"
    paid_at: Optional[datetime] = None
    expired_at: Optional[datetime] = None
    idempotency_key: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderDetailResponse(OrderResponse):
    """Order with related ride info for 'my purchases' page"""
    ride_title: str = ""
    ride_product: str = ""
    ride_price_per_month: Decimal = 0
    ride_duration: int = 0
    ride_total_seats: int = 0
    ride_purchase_count: int = 0
    ride_remaining_seats: int = 0
    ride_status: str = ""
    ride_contact_info: str = ""
    ride_owner: Optional[UserResponse] = None

    class Config:
        from_attributes = True
