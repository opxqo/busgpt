from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, func
from typing import List, Optional

from app.database import get_db
from app.models.order import Order
from app.models.ride import Ride
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderDetailResponse
from app.routers.auth import get_current_user

router = APIRouter(tags=["orders"])


async def get_ride_purchase_count(db: AsyncSession, ride_id: int) -> int:
    result = await db.execute(
        select(func.count(Order.id)).filter(
            and_(Order.ride_id == ride_id, Order.status == "paid")
        )
    )
    return result.scalar() or 0


def build_order_detail(order: Order, ride: Optional[Ride]) -> OrderDetailResponse:
    purchase_count = 0
    remaining_seats = 0
    if ride:
        purchase_count = getattr(ride, "_purchase_count", 0)
        remaining_seats = max((ride.total_seats or 0) - purchase_count, 0)

    return OrderDetailResponse(
        id=order.id,
        user_id=order.user_id,
        ride_id=order.ride_id,
        amount=order.amount,
        status=order.status,
        created_at=order.created_at,
        ride_title=ride.title if ride else "已删除",
        ride_product=ride.product if ride else "",
        ride_price_per_month=ride.price_per_month if ride else 0,
        ride_duration=ride.duration if ride else 0,
        ride_total_seats=ride.total_seats if ride else 0,
        ride_purchase_count=purchase_count,
        ride_remaining_seats=remaining_seats,
        ride_status=ride.status if ride else "deleted",
        ride_contact_info=ride.contact_info if ride else "",
        ride_owner=ride.owner if ride else None
    )

# 1. Purchase contact info for a ride
@router.post("/orders", response_model=OrderDetailResponse)
async def purchase_contact(
    order_in: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Check ride exists
    ride_result = await db.execute(
        select(Ride)
        .filter(Ride.id == order_in.ride_id)
        .options(selectinload(Ride.owner))
    )
    ride = ride_result.scalars().first()
    if not ride:
        raise HTTPException(status_code=404, detail="车位不存在")
    
    # Cannot purchase own ride
    if ride.owner_id == current_user.id:
        raise HTTPException(status_code=400, detail="您不能购买自己发布的车位联系方式")
    
    # Check if ride is open
    if ride.status != "open":
        raise HTTPException(status_code=400, detail="该车位已关闭或过期")

    purchase_count = await get_ride_purchase_count(db, ride.id)
    if purchase_count >= ride.total_seats:
        ride.status = "closed"
        db.add(ride)
        await db.flush()
        raise HTTPException(status_code=400, detail="该车位人数已满")
    
    # Check if already purchased
    existing = await db.execute(
        select(Order).filter(
            and_(Order.user_id == current_user.id, Order.ride_id == order_in.ride_id)
        )
    )
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="您已经购买过该车位的联系方式")
    
    # Create order
    order = Order(
        user_id=current_user.id,
        ride_id=ride.id,
        amount=ride.contact_price,
        status="paid"
    )
    db.add(order)
    await db.flush()
    if purchase_count + 1 >= ride.total_seats:
        ride.status = "closed"
        db.add(ride)
    await db.commit()
    await db.refresh(order)

    ride._purchase_count = await get_ride_purchase_count(db, ride.id)
    return build_order_detail(order, ride)

# 2. Get my purchase history
@router.get("/orders/mine", response_model=List[OrderDetailResponse])
async def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Order)
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc())
    )
    orders = result.scalars().all()
    
    # Build detail responses
    responses = []
    for order in orders:
        ride_result = await db.execute(
            select(Ride)
            .filter(Ride.id == order.ride_id)
            .options(selectinload(Ride.owner))
        )
        ride = ride_result.scalars().first()
        if ride:
            ride._purchase_count = await get_ride_purchase_count(db, ride.id)
        responses.append(build_order_detail(order, ride))
    
    return responses

# 3. Check if I've purchased a specific ride
@router.get("/orders/check/{ride_id}")
async def check_purchase(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Order).filter(
            and_(Order.user_id == current_user.id, Order.ride_id == ride_id, Order.status == "paid")
        )
    )
    order = result.scalars().first()
    return {"purchased": order is not None}

# 4. Get sales records for my rides (as owner)
@router.get("/my/rides/sales")
async def get_my_sales(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Get all ride IDs owned by current user
    rides_result = await db.execute(
        select(Ride).filter(Ride.owner_id == current_user.id)
    )
    my_rides = rides_result.scalars().all()
    
    if not my_rides:
        return {"total_revenue": 0, "total_orders": 0, "rides": []}
    
    ride_ids = [r.id for r in my_rides]
    
    # Get all orders for these rides
    orders_result = await db.execute(
        select(Order)
        .filter(and_(Order.ride_id.in_(ride_ids), Order.status == "paid"))
        .order_by(Order.created_at.desc())
    )
    orders = orders_result.scalars().all()
    
    total_revenue = sum(float(o.amount) for o in orders)
    
    # Group by ride
    ride_stats = []
    for ride in my_rides:
        ride_orders = [o for o in orders if o.ride_id == ride.id]
        ride_stats.append({
            "ride_id": ride.id,
            "ride_title": ride.title,
            "order_count": len(ride_orders),
            "revenue": sum(float(o.amount) for o in ride_orders),
            "total_seats": ride.total_seats,
            "remaining_seats": max((ride.total_seats or 0) - len(ride_orders), 0),
            "status": ride.status,
        })
    
    return {
        "total_revenue": total_revenue,
        "total_orders": len(orders),
        "rides": ride_stats
    }
