from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.requests import Request

from app.config import settings
from app.database import Base
from app.models.order import Order
from app.models.product import Product
from app.models.ride import Ride
from app.models.user import User
from app.routers import analytics, auth, orders, rides
from app.schemas.order import OrderCreate
from app.utils.security import create_access_token, get_password_hash
from app.utils.rate_limit import reset_auth_rate_limits


@pytest.fixture
async def db_session():
    settings.ENVIRONMENT = "test"
    settings.SECRET_KEY = "test-secret-key-with-more-than-32-characters"
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    Session = async_sessionmaker(engine, expire_on_commit=False)
    async with Session() as session:
        session.add_all(
            [
                Product(
                    type="chatgpt-plus",
                    label="Plus",
                    official_price=Decimal("20.00"),
                    color="#10b981",
                    max_seats=2,
                    description="Plus",
                ),
                User(
                    id=1,
                    phone="13800000001",
                    nickname="owner",
                    role="user",
                    password_hash=get_password_hash("secret123"),
                ),
                User(
                    id=2,
                    phone="13800000002",
                    nickname="buyer",
                    role="user",
                    password_hash=get_password_hash("secret123"),
                ),
                User(
                    id=3,
                    phone="13800000003",
                    nickname="other",
                    role="user",
                    password_hash=get_password_hash("secret123"),
                ),
                Ride(
                    id=1,
                    title="Plus shared seat",
                    product="chatgpt-plus",
                    owner_id=1,
                    total_seats=2,
                    price_per_month=Decimal("10.00"),
                    duration=1,
                    description="public",
                    contact_info="wechat: hidden_contact",
                    contact_price=Decimal("5.00"),
                    status="open",
                    expires_at=datetime.utcnow() + timedelta(days=30),
                ),
            ]
        )
        await session.commit()
        yield session

    await engine.dispose()


def _request(token: Optional[str] = None, host: str = "127.0.0.1") -> Request:
    headers = []
    if token:
        headers.append((b"authorization", f"Bearer {token}".encode()))
    return Request({"type": "http", "method": "GET", "path": "/", "headers": headers, "client": (host, 12345)})


async def _user(db_session, user_id: int) -> User:
    return await db_session.get(User, user_id)


@pytest.mark.asyncio
async def test_create_order_is_pending_and_does_not_unlock_contact(db_session):
    buyer = await _user(db_session, 2)

    order = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    await db_session.commit()

    assert order.status == "pending"
    assert order.payment_status == "pending"
    assert order.ride_contact_info == ""

    token = create_access_token(subject=buyer.id)
    ride_detail = await rides.get_ride(1, _request(token), db_session)
    assert ride_detail.contact_info is None
    assert ride_detail.is_purchased is False


@pytest.mark.asyncio
async def test_mock_payment_unlocks_contact_and_is_idempotent(db_session):
    buyer = await _user(db_session, 2)
    pending = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    await db_session.commit()

    paid = await orders.pay_order_mock(pending.id, buyer, db_session)
    await db_session.commit()
    paid_again = await orders.pay_order_mock(pending.id, buyer, db_session)

    assert paid.status == "paid"
    assert paid.payment_provider == "mock"
    assert paid.payment_no
    assert paid.contact_unlocked_at is not None
    assert paid.ride_contact_info == "wechat: hidden_contact"
    assert paid_again.status == "paid"
    assert paid_again.ride_purchase_count == 1

    token = create_access_token(subject=buyer.id)
    ride_detail = await rides.get_ride(1, _request(token), db_session)
    assert ride_detail.contact_info == "wechat: hidden_contact"


@pytest.mark.asyncio
async def test_duplicate_order_returns_existing_pending_order(db_session):
    buyer = await _user(db_session, 2)

    first = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    second = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)

    assert first.id == second.id
    assert second.status == "pending"


@pytest.mark.asyncio
async def test_owner_cannot_buy_and_full_ride_cannot_be_paid(db_session):
    owner = await _user(db_session, 1)
    with pytest.raises(HTTPException) as own_error:
        await orders.create_order(OrderCreate(ride_id=1), owner, db_session)
    assert own_error.value.status_code == 400

    buyer = await _user(db_session, 2)
    other = await _user(db_session, 3)
    first = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    second = await orders.create_order(OrderCreate(ride_id=1), other, db_session)
    await orders.pay_order_mock(first.id, buyer, db_session)

    ride = await db_session.get(Ride, 1)
    ride.total_seats = 1
    ride.status = "open"
    await db_session.commit()

    with pytest.raises(HTTPException) as full_error:
        await orders.pay_order_mock(second.id, other, db_session)
    assert full_error.value.status_code == 400


@pytest.mark.asyncio
async def test_login_rate_limit_returns_429(db_session):
    reset_auth_rate_limits()
    request = _request(host="10.0.0.1")
    payload = auth.LoginRequest(phone="13800000002", password="bad-password")

    for _ in range(5):
        with pytest.raises(HTTPException) as login_error:
            await auth.login_json(payload, request, db_session)
        assert login_error.value.status_code == 400

    with pytest.raises(HTTPException) as limited_error:
        await auth.login_json(payload, request, db_session)
    assert limited_error.value.status_code == 429


def test_default_secret_is_rejected_outside_test():
    original_env = settings.ENVIRONMENT
    original_secret = settings.SECRET_KEY
    try:
        settings.ENVIRONMENT = "production"
        settings.SECRET_KEY = "supersecretkeyforbusgptsessiontokens12345!@#%"
        with pytest.raises(RuntimeError):
            settings.validate_security_settings()
    finally:
        settings.ENVIRONMENT = original_env
        settings.SECRET_KEY = original_secret


@pytest.mark.asyncio
async def test_analytics_sales_and_rankings(db_session):
    buyer = await _user(db_session, 2)
    pending = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    await orders.pay_order_mock(pending.id, buyer, db_session)

    order = await db_session.get(Order, pending.id)
    order.paid_at = datetime.utcnow() - timedelta(days=1)
    order.contact_unlocked_at = order.paid_at
    await db_session.commit()

    overview = await analytics.get_sales_overview(30, db_session)
    sales_trends = await analytics.get_sales_trends(30, db_session)
    price_trends = await analytics.get_price_trends(90, None, db_session)
    product_rankings = await analytics.get_product_rankings(30, 10, db_session)
    ride_rankings = await analytics.get_ride_rankings(30, 10, db_session)

    assert overview.paid_orders == 1
    assert overview.total_revenue == Decimal("5.00")
    assert overview.active_rides == 1
    assert sales_trends[0].orders == 1
    assert sales_trends[0].revenue == Decimal("5.00")
    assert price_trends[0].product == "chatgpt-plus"
    assert price_trends[0].average_price_per_month == Decimal("10.00")
    assert product_rankings[0].product == "chatgpt-plus"
    assert product_rankings[0].orders == 1
    assert ride_rankings[0].ride_id == 1
    assert ride_rankings[0].orders == 1


@pytest.mark.asyncio
async def test_owner_sales_records_unlock_counts(db_session):
    buyer = await _user(db_session, 2)
    owner = await _user(db_session, 1)
    pending = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    paid = await orders.pay_order_mock(pending.id, buyer, db_session)

    sales = await orders.get_my_sales(owner, db_session)

    assert paid.contact_unlocked_at is not None
    assert sales["total_unlocks"] == 1
    assert sales["rides"][0]["unlock_count"] == 1
    assert sales["rides"][0]["latest_unlock_at"] is not None
