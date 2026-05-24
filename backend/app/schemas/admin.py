from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class AdminOverviewResponse(BaseModel):
    total_users: int
    total_rides: int
    total_orders: int
    total_revenue: Decimal
    active_rides: int
    today_new_users: int


class AdminUserListItem(BaseModel):
    id: int
    email: str
    phone: Optional[str] = None
    nickname: str
    avatar: str
    role: str
    is_active: bool
    created_at: datetime
    ride_count: int
    order_count: int


class AdminUserListResponse(BaseModel):
    items: list[AdminUserListItem]
    total: int


class AdminUserDetailResponse(BaseModel):
    id: int
    email: str
    phone: Optional[str] = None
    nickname: str
    avatar: str
    role: str
    is_active: bool
    created_at: datetime
    ride_count: int
    order_count: int


class AdminUserStatusUpdate(BaseModel):
    is_active: bool


class AdminRideListItem(BaseModel):
    id: int
    title: str
    product: str
    status: str
    total_seats: int
    recruit_seats: int
    price_per_month: Decimal
    duration: int
    purchase_count: int
    remaining_seats: int
    owner_id: int
    owner_nickname: Optional[str] = None
    created_at: datetime


class AdminRideListResponse(BaseModel):
    items: list[AdminRideListItem]
    total: int


class AdminRideStatusUpdate(BaseModel):
    status: str


class AdminOrderListItem(BaseModel):
    id: int
    user_id: int
    ride_id: int
    amount: Decimal
    status: str
    paid_at: Optional[datetime] = None
    created_at: datetime
    ride_title: str
    ride_product: str
    user_nickname: str
    user_email: str
    user_phone: Optional[str] = None


class AdminOrderListResponse(BaseModel):
    items: list[AdminOrderListItem]
    total: int
