from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.order import Order
from app.models.ride import Ride
from app.models.user import User
from app.routers.auth import get_current_admin_user
from app.schemas.admin import (
    AdminOrderListResponse,
    AdminOrderListItem,
    AdminOverviewResponse,
    AdminRideListResponse,
    AdminRideListItem,
    AdminRideStatusUpdate,
    AdminUserDetailResponse,
    AdminUserListResponse,
    AdminUserListItem,
    AdminUserStatusUpdate,
)

router = APIRouter(prefix="/admin", tags=["admin"])

PAID_STATUS = "paid"


@router.get("/overview", response_model=AdminOverviewResponse)
async def get_overview(
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin_user),
):
    total_users = (await db.execute(select(func.count(User.id)))).scalar() or 0
    total_rides = (await db.execute(select(func.count(Ride.id)))).scalar() or 0
    total_orders = (await db.execute(select(func.count(Order.id)))).scalar() or 0
    total_revenue_result = await db.execute(
        select(func.coalesce(func.sum(Order.amount), 0)).filter(Order.status == PAID_STATUS)
    )
    total_revenue = total_revenue_result.scalar() or 0
    active_rides = (
        await db.execute(select(func.count(Ride.id)).filter(Ride.status == "open"))
    ).scalar() or 0
    today_new_users = (
        await db.execute(
            select(func.count(User.id)).filter(func.date(User.created_at) == date.today())
        )
    ).scalar() or 0

    return AdminOverviewResponse(
        total_users=total_users,
        total_rides=total_rides,
        total_orders=total_orders,
        total_revenue=total_revenue,
        active_rides=active_rides,
        today_new_users=today_new_users,
    )


@router.get("/users", response_model=AdminUserListResponse)
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    role: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin_user),
):
    # Subquery for ride counts per user
    ride_count_sq = (
        select(Ride.owner_id, func.count(Ride.id).label("cnt"))
        .group_by(Ride.owner_id)
        .subquery()
    )
    # Subquery for order counts per user
    order_count_sq = (
        select(Order.user_id, func.count(Order.id).label("cnt"))
        .group_by(Order.user_id)
        .subquery()
    )

    query = (
        select(
            User,
            func.coalesce(ride_count_sq.c.cnt, 0).label("ride_count"),
            func.coalesce(order_count_sq.c.cnt, 0).label("order_count"),
        )
        .outerjoin(ride_count_sq, ride_count_sq.c.owner_id == User.id)
        .outerjoin(order_count_sq, order_count_sq.c.user_id == User.id)
    )

    filters = []
    if search:
        pattern = f"%{search}%"
        filters.append(User.email.contains(search) | User.nickname.contains(search))
    if role:
        filters.append(User.role == role)

    if filters:
        query = query.where(and_(*filters))

    # Get total count
    count_query = select(func.count(User.id))
    if filters:
        count_query = count_query.where(and_(*filters))
    total = (await db.execute(count_query)).scalar() or 0

    # Get paginated results
    query = query.order_by(User.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)

    items = []
    for row in result.all():
        user = row[0]
        items.append(
            AdminUserListItem(
                id=user.id,
                email=user.email or "",
                phone=user.phone,
                nickname=user.nickname,
                avatar=user.avatar,
                role=user.role,
                is_active=user.is_active,
                created_at=user.created_at,
                ride_count=int(row[1]),
                order_count=int(row[2]),
            )
        )

    return AdminUserListResponse(items=items, total=total)


@router.get("/users/{user_id}", response_model=AdminUserDetailResponse)
async def get_user_detail(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin_user),
):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")

    ride_count = (
        await db.execute(
            select(func.count(Ride.id)).filter(Ride.owner_id == user_id)
        )
    ).scalar() or 0
    order_count = (
        await db.execute(
            select(func.count(Order.id)).filter(Order.user_id == user_id)
        )
    ).scalar() or 0

    return AdminUserDetailResponse(
        id=user.id,
        email=user.email or "",
        phone=user.phone,
        nickname=user.nickname,
        avatar=user.avatar,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        ride_count=ride_count,
        order_count=order_count,
    )


@router.put("/users/{user_id}/status", response_model=AdminUserDetailResponse)
async def update_user_status(
    user_id: int,
    body: AdminUserStatusUpdate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user),
):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.role == "admin" and user.id != admin.id:
        raise HTTPException(status_code=403, detail="不能修改其他管理员的状态")

    user.is_active = body.is_active
    await db.flush()
    await db.refresh(user)

    ride_count = (
        await db.execute(
            select(func.count(Ride.id)).filter(Ride.owner_id == user_id)
        )
    ).scalar() or 0
    order_count = (
        await db.execute(
            select(func.count(Order.id)).filter(Order.user_id == user_id)
        )
    ).scalar() or 0

    return AdminUserDetailResponse(
        id=user.id,
        email=user.email or "",
        phone=user.phone,
        nickname=user.nickname,
        avatar=user.avatar,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        ride_count=ride_count,
        order_count=order_count,
    )


@router.get("/rides", response_model=AdminRideListResponse)
async def list_rides(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    product: Optional[str] = None,
    status_filter: Optional[str] = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin_user),
):
    # Subquery for purchase counts per ride
    purchase_count_sq = (
        select(Order.ride_id, func.count(Order.id).label("cnt"))
        .filter(Order.status == PAID_STATUS)
        .group_by(Order.ride_id)
        .subquery()
    )

    query = (
        select(
            Ride,
            User.nickname.label("owner_nickname"),
            func.coalesce(purchase_count_sq.c.cnt, 0).label("purchase_count"),
        )
        .outerjoin(User, User.id == Ride.owner_id)
        .outerjoin(purchase_count_sq, purchase_count_sq.c.ride_id == Ride.id)
    )

    filters = []
    if search:
        filters.append(Ride.title.contains(search))
    if product:
        filters.append(Ride.product == product)
    if status_filter:
        filters.append(Ride.status == status_filter)

    if filters:
        query = query.where(and_(*filters))

    # Get total count
    count_query = select(func.count(Ride.id))
    if filters:
        count_query = count_query.where(and_(*filters))
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Ride.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)

    items = []
    for row in result.all():
        ride = row[0]
        purchase_count = int(row[2])
        onboard_seats = min(max(ride.recruit_seats or max((ride.total_seats or 1) - 1, 1), 1), ride.total_seats or 1)
        items.append(
            AdminRideListItem(
                id=ride.id,
                title=ride.title,
                product=ride.product,
                status=ride.status,
                total_seats=ride.total_seats,
                recruit_seats=onboard_seats,
                price_per_month=ride.price_per_month,
                duration=ride.duration,
                purchase_count=purchase_count,
                remaining_seats=max((ride.total_seats or 0) - onboard_seats, 0),
                owner_id=ride.owner_id,
                owner_nickname=row[1],
                created_at=ride.created_at,
            )
        )

    return AdminRideListResponse(items=items, total=total)


@router.put("/rides/{ride_id}/status")
async def update_ride_status(
    ride_id: int,
    body: AdminRideStatusUpdate,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin_user),
):
    if body.status not in ("open", "closed"):
        raise HTTPException(status_code=400, detail="状态值无效，仅支持 open 或 closed")

    result = await db.execute(select(Ride).filter(Ride.id == ride_id))
    ride = result.scalars().first()
    if not ride:
        raise HTTPException(status_code=404, detail="车位不存在")

    ride.status = body.status
    await db.flush()

    return {"id": ride.id, "status": ride.status}


@router.delete("/rides/{ride_id}")
async def delete_ride(
    ride_id: int,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin_user),
):
    result = await db.execute(select(Ride).filter(Ride.id == ride_id))
    ride = result.scalars().first()
    if not ride:
        raise HTTPException(status_code=404, detail="车位不存在")

    paid_order_count = (
        await db.execute(
            select(func.count(Order.id)).filter(
                and_(Order.ride_id == ride_id, Order.status == PAID_STATUS)
            )
        )
    ).scalar() or 0
    if paid_order_count > 0:
        raise HTTPException(status_code=400, detail="该车位存在联系方式解锁记录，无法删除")

    await db.delete(ride)
    await db.flush()

    return {"detail": "车位已删除"}


@router.get("/orders", response_model=AdminOrderListResponse)
async def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    status_filter: Optional[str] = Query(None, alias="status"),
    search: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    _admin: User = Depends(get_current_admin_user),
):
    query = (
        select(
            Order,
            Ride.title.label("ride_title"),
            Ride.product.label("ride_product"),
            User.nickname.label("user_nickname"),
            User.email.label("user_email"),
            User.phone.label("user_phone"),
        )
        .outerjoin(Ride, Ride.id == Order.ride_id)
        .outerjoin(User, User.id == Order.user_id)
    )

    filters = []
    if status_filter:
        filters.append(Order.status == status_filter)
    if search:
        filters.append(Order.id == int(search) if search.isdigit() else Order.id == 0)

    if filters:
        query = query.where(and_(*filters))

    count_query = select(func.count(Order.id))
    if filters:
        count_query = count_query.where(and_(*filters))
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Order.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)

    items = []
    for row in result.all():
        order = row[0]
        items.append(
            AdminOrderListItem(
                id=order.id,
                user_id=order.user_id,
                ride_id=order.ride_id,
                amount=order.amount,
                status=order.status,
                paid_at=order.paid_at,
                created_at=order.created_at,
                ride_title=row[1] or "",
                ride_product=row[2] or "",
                user_nickname=row[3] or "",
                user_email=row[4] or "",
                user_phone=row[5] or "",
            )
        )

    return AdminOrderListResponse(items=items, total=total)
