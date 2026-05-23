from datetime import datetime, timedelta
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.order import Order
from app.models.product import Product
from app.models.ride import Ride
from app.models.user import User
from app.schemas.analytics import (
    PriceTrendPoint,
    ProductRankingItem,
    RideRankingItem,
    SalesOverviewResponse,
    SalesTrendPoint,
)

router = APIRouter(prefix="/analytics", tags=["analytics"])

PAID_STATUS = "paid"


def _start_time(days: int) -> datetime:
    return datetime.utcnow() - timedelta(days=days)


def _decimal(value) -> Decimal:
    if value is None:
        return Decimal("0")
    return Decimal(str(value))


@router.get("/sales/overview", response_model=SalesOverviewResponse)
async def get_sales_overview(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    start = _start_time(days)

    paid_orders_result = await db.execute(
        select(
            func.count(Order.id),
            func.coalesce(func.sum(Order.amount), 0),
            func.coalesce(func.avg(Order.amount), 0),
        ).filter(and_(Order.status == PAID_STATUS, Order.paid_at >= start))
    )
    paid_orders, total_revenue, average_order_amount = paid_orders_result.one()

    active_rides_result = await db.execute(
        select(func.count(Ride.id)).filter(Ride.status == "open")
    )
    new_rides_result = await db.execute(
        select(func.count(Ride.id)).filter(Ride.created_at >= start)
    )

    return SalesOverviewResponse(
        total_revenue=_decimal(total_revenue),
        paid_orders=paid_orders or 0,
        active_rides=active_rides_result.scalar() or 0,
        new_rides=new_rides_result.scalar() or 0,
        average_order_amount=_decimal(average_order_amount),
    )


@router.get("/sales/trends", response_model=List[SalesTrendPoint])
async def get_sales_trends(
    days: int = Query(30, ge=1, le=365),
    db: AsyncSession = Depends(get_db),
):
    start = _start_time(days)
    result = await db.execute(
        select(
            func.date(Order.paid_at).label("day"),
            func.count(Order.id),
            func.coalesce(func.sum(Order.amount), 0),
            func.coalesce(func.avg(Order.amount), 0),
        )
        .filter(and_(Order.status == PAID_STATUS, Order.paid_at >= start))
        .group_by(func.date(Order.paid_at))
        .order_by(func.date(Order.paid_at))
    )

    return [
        SalesTrendPoint(
            date=row[0],
            orders=row[1] or 0,
            revenue=_decimal(row[2]),
            average_order_amount=_decimal(row[3]),
        )
        for row in result.all()
    ]


@router.get("/prices/trends", response_model=List[PriceTrendPoint])
async def get_price_trends(
    days: int = Query(90, ge=1, le=365),
    product: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    start = _start_time(days)
    filters = [Ride.created_at >= start]
    if product:
        filters.append(Ride.product == product)

    result = await db.execute(
        select(
            func.date(Ride.created_at).label("day"),
            Ride.product,
            func.count(Ride.id),
            func.coalesce(func.avg(Ride.price_per_month), 0),
            func.coalesce(func.avg(Ride.contact_price), 0),
            func.coalesce(func.min(Ride.price_per_month), 0),
            func.coalesce(func.max(Ride.price_per_month), 0),
        )
        .filter(and_(*filters))
        .group_by(func.date(Ride.created_at), Ride.product)
        .order_by(func.date(Ride.created_at), Ride.product)
    )

    return [
        PriceTrendPoint(
            date=row[0],
            product=row[1],
            ride_count=row[2] or 0,
            average_price_per_month=_decimal(row[3]),
            average_contact_price=_decimal(row[4]),
            minimum_price_per_month=_decimal(row[5]),
            maximum_price_per_month=_decimal(row[6]),
        )
        for row in result.all()
    ]


@router.get("/rankings/products", response_model=List[ProductRankingItem])
async def get_product_rankings(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    start = _start_time(days)
    result = await db.execute(
        select(
            Ride.product,
            Product.label,
            func.count(Order.id).label("orders"),
            func.coalesce(func.sum(Order.amount), 0).label("revenue"),
            func.coalesce(func.avg(Order.amount), 0).label("average_order_amount"),
        )
        .join(Ride, Ride.id == Order.ride_id)
        .join(Product, Product.type == Ride.product)
        .filter(and_(Order.status == PAID_STATUS, Order.paid_at >= start))
        .group_by(Ride.product, Product.label)
        .order_by(func.count(Order.id).desc(), func.coalesce(func.sum(Order.amount), 0).desc())
        .limit(limit)
    )

    return [
        ProductRankingItem(
            product=row[0],
            product_label=row[1],
            orders=row[2] or 0,
            revenue=_decimal(row[3]),
            average_order_amount=_decimal(row[4]),
        )
        for row in result.all()
    ]


@router.get("/rankings/rides", response_model=List[RideRankingItem])
async def get_ride_rankings(
    days: int = Query(30, ge=1, le=365),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    start = _start_time(days)
    result = await db.execute(
        select(
            Ride.id,
            Ride.title,
            Ride.product,
            Ride.total_seats,
            Ride.status,
            Ride.owner_id,
            User.nickname,
            func.count(Order.id).label("orders"),
            func.coalesce(func.sum(Order.amount), 0).label("revenue"),
        )
        .join(Order, Order.ride_id == Ride.id)
        .join(User, User.id == Ride.owner_id)
        .filter(and_(Order.status == PAID_STATUS, Order.paid_at >= start))
        .group_by(
            Ride.id,
            Ride.title,
            Ride.product,
            Ride.total_seats,
            Ride.status,
            Ride.owner_id,
            User.nickname,
        )
        .order_by(func.count(Order.id).desc(), func.coalesce(func.sum(Order.amount), 0).desc())
        .limit(limit)
    )

    items = []
    for row in result.all():
        orders = row[7] or 0
        items.append(
            RideRankingItem(
                ride_id=row[0],
                ride_title=row[1],
                product=row[2],
                total_seats=row[3],
                status=row[4],
                owner_id=row[5],
                owner_nickname=row[6],
                orders=orders,
                revenue=_decimal(row[8]),
                remaining_seats=max((row[3] or 0) - orders, 0),
            )
        )
    return items
