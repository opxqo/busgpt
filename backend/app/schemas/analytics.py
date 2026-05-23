from datetime import date
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class SalesOverviewResponse(BaseModel):
    total_revenue: Decimal
    paid_orders: int
    active_rides: int
    new_rides: int
    average_order_amount: Decimal


class SalesTrendPoint(BaseModel):
    date: date
    orders: int
    revenue: Decimal
    average_order_amount: Decimal


class PriceTrendPoint(BaseModel):
    date: date
    product: str
    ride_count: int
    average_price_per_month: Decimal
    average_contact_price: Decimal
    minimum_price_per_month: Decimal
    maximum_price_per_month: Decimal


class ProductRankingItem(BaseModel):
    product: str
    product_label: str
    orders: int
    revenue: Decimal
    average_order_amount: Decimal


class RideRankingItem(BaseModel):
    ride_id: int
    ride_title: str
    product: str
    orders: int
    revenue: Decimal
    total_seats: int
    remaining_seats: int
    status: str
    owner_id: int
    owner_nickname: Optional[str] = None
