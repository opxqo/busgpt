from datetime import datetime, timedelta
from uuid import uuid4
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, func

from app.config import settings
from app.database import get_db
from app.models.order import Order
from app.models.ride import Ride
from app.models.user import User
from app.schemas.order import OrderCreate, OrderDetailResponse
from app.routers.auth import get_current_user
from app.services.payments import get_payment_provider

router = APIRouter(tags=["orders"])

ORDER_STATUS_PENDING = "pending"
ORDER_STATUS_PAID = "paid"
ORDER_STATUS_CANCELLED = "cancelled"
ORDER_STATUS_EXPIRED = "expired"
ORDER_STATUS_REFUNDED = "refunded"
TERMINAL_REUSABLE_STATUSES = {ORDER_STATUS_EXPIRED, ORDER_STATUS_CANCELLED}


def get_recruit_seats(ride: Ride) -> int:
    return max(int(ride.recruit_seats or max((ride.total_seats or 1) - 1, 1)), 1)


async def get_ride_purchase_count(db: AsyncSession, ride_id: int) -> int:
    result = await db.execute(
        select(func.count(Order.id)).filter(
            and_(Order.ride_id == ride_id, Order.status == ORDER_STATUS_PAID)
        )
    )
    return result.scalar() or 0


def _order_expired(order: Order) -> bool:
    return (
        order.status == ORDER_STATUS_PENDING
        and order.expired_at is not None
        and order.expired_at <= datetime.utcnow()
    )


def _mark_order_expired(order: Order) -> None:
    order.status = ORDER_STATUS_EXPIRED
    order.payment_status = ORDER_STATUS_EXPIRED
    order.updated_at = datetime.utcnow()


async def _expire_if_needed(db: AsyncSession, order: Order) -> bool:
    if not _order_expired(order):
        return False
    _mark_order_expired(order)
    db.add(order)
    await db.flush()
    return True


def build_order_detail(order: Order, ride: Optional[Ride]) -> OrderDetailResponse:
    purchase_count = 0
    remaining_seats = 0
    show_contact = order.status == ORDER_STATUS_PAID
    if ride:
        purchase_count = getattr(ride, "_purchase_count", 0)
        remaining_seats = max(get_recruit_seats(ride) - purchase_count, 0)

    return OrderDetailResponse(
        id=order.id,
        user_id=order.user_id,
        ride_id=order.ride_id,
        amount=order.amount,
        status=order.status,
        payment_provider=order.payment_provider,
        payment_no=order.payment_no,
        payment_status=order.payment_status,
        paid_at=order.paid_at,
        contact_unlocked_at=order.contact_unlocked_at,
        expired_at=order.expired_at,
        idempotency_key=order.idempotency_key,
        created_at=order.created_at,
        updated_at=order.__dict__.get("updated_at"),
        ride_title=ride.title if ride else "已删除",
        ride_product=ride.product if ride else "",
        ride_price_per_month=ride.price_per_month if ride else 0,
        ride_duration=ride.duration if ride else 0,
        ride_total_seats=ride.total_seats if ride else 0,
        ride_recruit_seats=get_recruit_seats(ride) if ride else 0,
        ride_purchase_count=purchase_count,
        ride_remaining_seats=remaining_seats,
        ride_status=ride.status if ride else "deleted",
        ride_contact_info=ride.contact_info if (ride and show_contact) else "",
        ride_contact_website=ride.contact_website if (ride and show_contact) else "",
        ride_owner=ride.owner if ride else None,
    )


async def _load_ride(db: AsyncSession, ride_id: int) -> Optional[Ride]:
    result = await db.execute(
        select(Ride)
        .filter(Ride.id == ride_id)
        .options(selectinload(Ride.owner))
    )
    return result.scalars().first()


async def _load_order_for_user(db: AsyncSession, order_id: int, user_id: int) -> Order:
    result = await db.execute(
        select(Order)
        .filter(and_(Order.id == order_id, Order.user_id == user_id))
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    await _expire_if_needed(db, order)
    return order


async def _order_response(db: AsyncSession, order: Order) -> OrderDetailResponse:
    ride = await _load_ride(db, order.ride_id)
    if ride:
        ride._purchase_count = await get_ride_purchase_count(db, ride.id)
    return build_order_detail(order, ride)


@router.post("/orders", response_model=OrderDetailResponse)
async def create_order(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    ride = await _load_ride(db, order_in.ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="车位不存在")

    if ride.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="您不能购买自己发布的车位联系方式")

    purchase_count = await get_ride_purchase_count(db, ride.id)
    existing_result = await db.execute(
        select(Order).filter(
            and_(Order.user_id == current_user.id, Order.ride_id == order_in.ride_id)
        )
    )
    existing = existing_result.scalars().first()
    if existing:
        await _expire_if_needed(db, existing)
        if existing.status == ORDER_STATUS_PAID:
            ride._purchase_count = purchase_count
            return build_order_detail(existing, ride)
        if existing.status == ORDER_STATUS_PENDING:
            ride._purchase_count = purchase_count
            return build_order_detail(existing, ride)
        if existing.status not in TERMINAL_REUSABLE_STATUSES:
            raise HTTPException(status_code=400, detail="该订单当前状态不可重新支付")

    if ride.status != "open":
        raise HTTPException(status_code=400, detail="该车位已关闭或过期")

    if purchase_count >= get_recruit_seats(ride):
        ride.status = "closed"
        db.add(ride)
        await db.flush()
        raise HTTPException(status_code=400, detail="该车位人数已满")

    if existing:
        existing.amount = 0
        existing.status = ORDER_STATUS_PAID
        existing.payment_status = ORDER_STATUS_PAID
        existing.payment_provider = settings.PAYMENT_PROVIDER
        existing.payment_no = None
        existing.paid_at = datetime.utcnow()
        existing.contact_unlocked_at = existing.paid_at
        existing.expired_at = None
        existing.idempotency_key = uuid4().hex
        existing.updated_at = datetime.utcnow()
        db.add(existing)
        if purchase_count + 1 >= get_recruit_seats(ride):
            ride.status = "closed"
            db.add(ride)
        await db.flush()
        ride._purchase_count = purchase_count + 1
        return build_order_detail(existing, ride)

    order = Order(
        user_id=current_user.id,
        ride_id=ride.id,
        amount=0,
        status=ORDER_STATUS_PAID,
        payment_provider=settings.PAYMENT_PROVIDER,
        payment_status=ORDER_STATUS_PAID,
        paid_at=datetime.utcnow(),
        contact_unlocked_at=datetime.utcnow(),
        idempotency_key=uuid4().hex,
    )
    db.add(order)
    if purchase_count + 1 >= get_recruit_seats(ride):
        ride.status = "closed"
        db.add(ride)
    await db.flush()
    ride._purchase_count = purchase_count + 1
    return build_order_detail(order, ride)


@router.post("/orders/{order_id}/pay/mock", response_model=OrderDetailResponse)
async def pay_order_mock(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    order = await _load_order_for_user(db, order_id, current_user.id)
    ride = await _load_ride(db, order.ride_id)
    if not ride:
        raise HTTPException(status_code=404, detail="车位不存在")

    if order.status == ORDER_STATUS_PAID:
        return await _order_response(db, order)

    if order.status != ORDER_STATUS_PENDING:
        raise HTTPException(status_code=400, detail="订单当前状态不可支付")

    if ride.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="您不能购买自己发布的车位联系方式")

    if ride.status != "open":
        raise HTTPException(status_code=400, detail="该车位已关闭或过期")

    purchase_count = await get_ride_purchase_count(db, ride.id)
    if purchase_count >= get_recruit_seats(ride):
        ride.status = "closed"
        db.add(ride)
        await db.flush()
        raise HTTPException(status_code=400, detail="该车位人数已满")

    provider = get_payment_provider("mock")
    try:
        payment = await provider.confirm_payment(order.id, order.amount)
    except Exception:
        raise HTTPException(status_code=400, detail="模拟支付失败，请稍后再试")

    order.status = ORDER_STATUS_PAID
    order.payment_status = payment.status
    order.payment_provider = payment.provider
    order.payment_no = payment.payment_no
    order.paid_at = payment.paid_at
    order.contact_unlocked_at = payment.paid_at or datetime.utcnow()
    order.updated_at = datetime.utcnow()
    db.add(order)

    if purchase_count + 1 >= get_recruit_seats(ride):
        ride.status = "closed"
        db.add(ride)

    await db.flush()
    return await _order_response(db, order)


@router.get("/orders/mine", response_model=List[OrderDetailResponse])
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()

    responses = []
    for order in orders:
        await _expire_if_needed(db, order)
        responses.append(await _order_response(db, order))

    return responses


@router.get("/orders/check/{ride_id}")
async def check_purchase(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Order).filter(
            and_(
                Order.user_id == current_user.id,
                Order.ride_id == ride_id,
                Order.status == ORDER_STATUS_PAID,
            )
        )
    )
    order = result.scalars().first()
    return {"purchased": order is not None}


@router.get("/orders/{order_id}", response_model=OrderDetailResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    order = await _load_order_for_user(db, order_id, current_user.id)
    return await _order_response(db, order)


@router.get("/my/rides/sales")
async def get_my_sales(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    rides_result = await db.execute(
        select(Ride).filter(Ride.owner_id == current_user.id)
    )
    my_rides = rides_result.scalars().all()

    if not my_rides:
        return {"total_revenue": 0, "total_orders": 0, "total_unlocks": 0, "rides": []}

    ride_ids = [r.id for r in my_rides]
    orders_result = await db.execute(
        select(Order)
        .filter(and_(Order.ride_id.in_(ride_ids), Order.status == ORDER_STATUS_PAID))
        .order_by(Order.created_at.desc())
    )
    orders = orders_result.scalars().all()

    total_revenue = sum(float(o.amount) for o in orders)

    ride_stats = []
    for ride in my_rides:
        ride_orders = [o for o in orders if o.ride_id == ride.id]
        ride_stats.append({
            "ride_id": ride.id,
            "ride_title": ride.title,
            "order_count": len(ride_orders),
            "unlock_count": len(ride_orders),
            "revenue": sum(float(o.amount) for o in ride_orders),
            "total_seats": ride.total_seats,
            "recruit_seats": get_recruit_seats(ride),
            "remaining_seats": max(get_recruit_seats(ride) - len(ride_orders), 0),
            "status": ride.status,
            "latest_unlock_at": max((o.contact_unlocked_at or o.paid_at or o.created_at for o in ride_orders), default=None),
        })

    return {
        "total_revenue": total_revenue,
        "total_orders": len(orders),
        "total_unlocks": len(orders),
        "rides": ride_stats,
    }
