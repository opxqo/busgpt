from fastapi import APIRouter, Depends, HTTPException, status, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import or_, and_, func
from datetime import datetime, timedelta
from typing import List, Optional

from app.database import get_db
from app.models.ride import Ride
from app.models.order import Order
from app.models.product import Product
from app.models.user import User
from app.schemas.ride import RideCreate, RideUpdate, RideResponse, RideDetailResponse
from app.schemas.product import ProductResponse, ProductUpdate
from app.routers.auth import get_current_user, get_current_admin_user, oauth2_scheme
from jose import jwt, JWTError
from app.config import settings

router = APIRouter(tags=["rides"])


def default_warranty_days(duration: int) -> int:
    return 365 if duration >= 12 else duration * 30


def get_recruit_seats(ride: Ride) -> int:
    return max(int(ride.recruit_seats or max((ride.total_seats or 1) - 1, 1)), 1)


def validate_seats(total_seats: int, recruit_seats: int, product: Product, purchase_count: int = 0) -> None:
    if total_seats > product.max_seats:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum seats allowed for {product.label} is {product.max_seats}"
        )
    if recruit_seats >= total_seats:
        raise HTTPException(status_code=400, detail="上车人数必须小于车位总人数，车主本人也占 1 位")
    if recruit_seats < purchase_count:
        raise HTTPException(status_code=400, detail="上车人数不能小于已拼车人数")


async def get_ride_purchase_count(db: AsyncSession, ride_id: int) -> int:
    result = await db.execute(
        select(func.count(Order.id)).filter(
            and_(Order.ride_id == ride_id, Order.status == "paid")
        )
    )
    return result.scalar() or 0


def build_ride_response(
    ride: Ride,
    purchase_count: int,
    contact_info: Optional[str] = None,
    contact_website: Optional[str] = None,
    is_purchased: bool = False,
) -> RideDetailResponse:
    recruit_seats = get_recruit_seats(ride)
    remaining_seats = max(recruit_seats - purchase_count, 0)
    warranty_days = ride.warranty_days or default_warranty_days(ride.duration)
    return RideDetailResponse(
        id=ride.id,
        title=ride.title,
        product=ride.product,
        owner_id=ride.owner_id,
        total_seats=ride.total_seats,
        recruit_seats=recruit_seats,
        price_per_month=ride.price_per_month,
        duration=ride.duration,
        warranty_days=warranty_days,
        description=ride.description or "",
        contact_price=ride.contact_price,
        status=ride.status,
        created_at=ride.created_at,
        expires_at=ride.expires_at,
        purchase_count=purchase_count,
        remaining_seats=remaining_seats,
        owner=ride.owner,
        product_details=ride.product_details,
        contact_info=contact_info,
        contact_website=contact_website,
        is_purchased=is_purchased,
    )

# Helper: optionally get current user (returns None if not authenticated)
async def get_optional_user(request: Request, db: AsyncSession = Depends(get_db)) -> Optional[User]:
    try:
        auth_header = request.headers.get("authorization", "")
        if not auth_header.startswith("Bearer "):
            return None
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = int(payload.get("sub", 0))
        if not user_id:
            return None
        result = await db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()
    except (JWTError, ValueError, Exception):
        return None

# 1. Product Listing Endpoint
@router.get("/products", response_model=List[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()


@router.get("/products/{product_type}", response_model=ProductResponse)
async def get_product(product_type: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).filter(Product.type == product_type))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/products/{product_type}", response_model=ProductResponse)
async def update_product(
    product_type: str,
    product_in: ProductUpdate,
    current_user: User = Depends(get_current_admin_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Product).filter(Product.type == product_type))
    product = result.scalars().first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.label = product_in.label
    product.official_price = product_in.official_price
    product.color = product_in.color
    product.max_seats = product_in.max_seats
    product.description = product_in.description

    db.add(product)
    await db.flush()
    await db.commit()
    await db.refresh(product)
    return product

# 2. Get My Owned Rides
@router.get("/my/rides/owned", response_model=List[RideDetailResponse])
async def get_my_owned_rides(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Ride)
        .filter(Ride.owner_id == current_user.id)
        .options(selectinload(Ride.owner), selectinload(Ride.product_details))
        .order_by(Ride.created_at.desc())
    )
    rides = result.scalars().all()
    responses = []
    for ride in rides:
        purchase_count = await get_ride_purchase_count(db, ride.id)
        responses.append(build_ride_response(ride, purchase_count, ride.contact_info, ride.contact_website, True))
    return responses

# 3. Ride List (Market) with filtering
@router.get("/rides", response_model=List[RideResponse])
async def get_rides(
    product: Optional[str] = None,
    status_filter: Optional[str] = None,
    query: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    stmt = select(Ride).options(
        selectinload(Ride.owner),
        selectinload(Ride.product_details),
    )
    
    filters = []
    if product:
        filters.append(Ride.product == product)
    if status_filter:
        filters.append(Ride.status == status_filter)
    else:
        # Default: show only open rides
        filters.append(Ride.status == "open")
        
    if query:
        filters.append(
            or_(
                Ride.title.ilike(f"%{query}%"),
                Ride.description.ilike(f"%{query}%")
            )
        )
        
    if filters:
        stmt = stmt.filter(and_(*filters))
        
    stmt = stmt.order_by(Ride.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(stmt)
    rides = result.scalars().all()
    responses = []
    for ride in rides:
        purchase_count = await get_ride_purchase_count(db, ride.id)
        responses.append(build_ride_response(ride, purchase_count))
    return responses

# 4. Create Ride
@router.post("/rides", response_model=RideDetailResponse)
async def create_ride(
    ride_in: RideCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    # Verify product exists
    prod_result = await db.execute(select(Product).filter(Product.type == ride_in.product))
    product = prod_result.scalars().first()
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product type")
        
    recruit_seats = ride_in.recruit_seats or max(ride_in.total_seats - 1, 1)
    validate_seats(ride_in.total_seats, recruit_seats, product)
        
    # Calculate expiry date
    warranty_days = ride_in.warranty_days or default_warranty_days(ride_in.duration)
    expires_at = datetime.utcnow() + timedelta(days=warranty_days)
    
    db_ride = Ride(
        title=ride_in.title,
        product=ride_in.product,
        owner_id=current_user.id,
        total_seats=ride_in.total_seats,
        recruit_seats=recruit_seats,
        price_per_month=ride_in.price_per_month,
        duration=ride_in.duration,
        warranty_days=warranty_days,
        description=ride_in.description,
        contact_info=ride_in.contact_info,
        contact_website=ride_in.contact_website or "",
        contact_price=ride_in.contact_price,
        status="open",
        expires_at=expires_at
    )
    
    db.add(db_ride)
    await db.flush()
    await db.commit()
    
    # Reload with relationships
    result = await db.execute(
        select(Ride)
        .filter(Ride.id == db_ride.id)
        .options(
            selectinload(Ride.owner),
            selectinload(Ride.product_details),
        )
    )
    ride = result.scalars().first()
    
    return build_ride_response(ride, 0, ride.contact_info, ride.contact_website, True)

# 5. Get Ride Details (conditionally returns contact_info)
@router.get("/rides/{ride_id}", response_model=RideDetailResponse)
async def get_ride(
    ride_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Ride)
        .filter(Ride.id == ride_id)
        .options(
            selectinload(Ride.owner),
            selectinload(Ride.product_details),
        )
    )
    ride = result.scalars().first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
    
    # Get optional current user
    current_user = await get_optional_user(request, db)
    
    # Check if user is owner or has purchased
    is_owner = current_user and current_user.id == ride.owner_id
    is_purchased = False
    
    if current_user and not is_owner:
        order_result = await db.execute(
            select(Order).filter(
                and_(Order.user_id == current_user.id, Order.ride_id == ride_id, Order.status == "paid")
            )
        )
        is_purchased = order_result.scalars().first() is not None
    
    purchase_count = await get_ride_purchase_count(db, ride_id)
    return build_ride_response(
        ride,
        purchase_count,
        ride.contact_info if (is_owner or is_purchased) else None,
        ride.contact_website if (is_owner or is_purchased) else None,
        bool(is_purchased or is_owner),
    )

# 6. Update Ride Details
@router.put("/rides/{ride_id}", response_model=RideDetailResponse)
async def update_ride(
    ride_id: int,
    ride_in: RideUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Ride)
        .filter(Ride.id == ride_id)
        .options(
            selectinload(Ride.owner),
            selectinload(Ride.product_details),
        )
    )
    ride = result.scalars().first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
        
    if ride.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not own this ride")

    purchase_count = await get_ride_purchase_count(db, ride_id)
    product_type = ride_in.product if ride_in.product is not None else ride.product
    product_result = await db.execute(select(Product).filter(Product.type == product_type))
    product = product_result.scalars().first()
    if not product:
        raise HTTPException(status_code=400, detail="Invalid product type")

    total_seats = ride_in.total_seats if ride_in.total_seats is not None else ride.total_seats
    recruit_seats = ride_in.recruit_seats if ride_in.recruit_seats is not None else get_recruit_seats(ride)
    validate_seats(total_seats, recruit_seats, product, purchase_count)

    if ride_in.title is not None:
        ride.title = ride_in.title
    if ride_in.product is not None:
        ride.product = ride_in.product
    if ride_in.total_seats is not None:
        ride.total_seats = ride_in.total_seats
    if ride_in.recruit_seats is not None:
        ride.recruit_seats = ride_in.recruit_seats
    if ride_in.price_per_month is not None:
        ride.price_per_month = ride_in.price_per_month
    if ride_in.duration is not None:
        ride.duration = ride_in.duration
        if ride_in.warranty_days is None:
            ride.warranty_days = default_warranty_days(ride_in.duration)
            ride.expires_at = datetime.utcnow() + timedelta(days=ride.warranty_days)
    if ride_in.warranty_days is not None:
        ride.warranty_days = ride_in.warranty_days
        ride.expires_at = datetime.utcnow() + timedelta(days=ride_in.warranty_days)
    if ride_in.description is not None:
        ride.description = ride_in.description
    if ride_in.contact_info is not None:
        ride.contact_info = ride_in.contact_info
    if ride_in.contact_website is not None:
        ride.contact_website = ride_in.contact_website
    if ride_in.contact_price is not None:
        ride.contact_price = ride_in.contact_price
    if ride_in.status is not None:
        if ride_in.status not in ["open", "closed", "expired"]:
            raise HTTPException(status_code=400, detail="Invalid status value")
        ride.status = ride_in.status
        
    db.add(ride)
    await db.flush()
    await db.commit()

    result = await db.execute(
        select(Ride)
        .filter(Ride.id == ride_id)
        .options(
            selectinload(Ride.owner),
            selectinload(Ride.product_details),
        )
    )
    ride = result.scalars().first()
    return build_ride_response(ride, purchase_count, ride.contact_info, ride.contact_website, True)

# 7. Delete Ride
@router.delete("/rides/{ride_id}")
async def delete_ride(
    ride_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Ride).filter(Ride.id == ride_id))
    ride = result.scalars().first()
    if not ride:
        raise HTTPException(status_code=404, detail="Ride not found")
        
    if ride.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not own this ride")

    purchase_count = await get_ride_purchase_count(db, ride_id)
    if purchase_count > 0:
        raise HTTPException(status_code=400, detail="Ride has paid passengers and cannot be deleted. Close it instead.")

    await db.delete(ride)
    await db.commit()
    return {"message": "Ride successfully deleted"}
