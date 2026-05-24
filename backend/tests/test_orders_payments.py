from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional

import pytest
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from starlette.requests import Request

from app.config import settings
from app.database import Base
from app.models.activation_token import ActivationToken
from app.models.order import Order
from app.models.product import Product
from app.models.ride import Ride
from app.models.user import User
from app.routers import analytics, auth, orders, rides
from app.routers import users
from app.schemas.order import OrderCreate
from app.schemas.user import PasswordChange
from app.utils.security import create_access_token, get_password_hash, verify_password
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
                    email="owner1@example.com",
                    nickname="owner",
                    role="user",
                    password_hash=get_password_hash("secret123"),
                    email_verified_at=datetime.utcnow(),
                ),
                User(
                    id=2,
                    email="buyer@example.com",
                    nickname="buyer",
                    role="user",
                    password_hash=get_password_hash("secret123"),
                    email_verified_at=datetime.utcnow(),
                ),
                User(
                    id=3,
                    email="other@example.com",
                    nickname="other",
                    role="user",
                    password_hash=get_password_hash("secret123"),
                    email_verified_at=datetime.utcnow(),
                ),
                Ride(
                    id=1,
                    title="Plus shared seat",
                    product="chatgpt-plus",
                    owner_id=1,
                    total_seats=2,
                    recruit_seats=1,
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
async def test_create_order_unlocks_contact_for_free(db_session):
    buyer = await _user(db_session, 2)

    order = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    await db_session.commit()

    assert order.status == "paid"
    assert order.payment_status == "paid"
    assert order.amount == Decimal("0")
    assert order.contact_unlocked_at is not None
    assert order.ride_contact_info == "wechat: hidden_contact"

    token = create_access_token(subject=buyer.id)
    ride_detail = await rides.get_ride(1, _request(token), db_session)
    assert ride_detail.contact_info == "wechat: hidden_contact"
    assert ride_detail.is_purchased is True


@pytest.mark.asyncio
async def test_mock_payment_unlocks_contact_and_is_idempotent(db_session):
    buyer = await _user(db_session, 2)
    paid = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    await db_session.commit()
    paid_again = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)

    assert paid.status == "paid"
    assert paid.payment_provider == "mock"
    assert paid.contact_unlocked_at is not None
    assert paid.ride_contact_info == "wechat: hidden_contact"
    assert paid_again.status == "paid"
    assert paid_again.ride_purchase_count == 1

    token = create_access_token(subject=buyer.id)
    ride_detail = await rides.get_ride(1, _request(token), db_session)
    assert ride_detail.contact_info == "wechat: hidden_contact"


@pytest.mark.asyncio
async def test_duplicate_order_returns_existing_paid_unlock(db_session):
    buyer = await _user(db_session, 2)

    first = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)
    second = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)

    assert first.id == second.id
    assert second.status == "paid"


@pytest.mark.asyncio
async def test_contact_unlock_does_not_fill_ride(db_session):
    owner = await _user(db_session, 1)
    with pytest.raises(HTTPException) as own_error:
        await orders.create_order(OrderCreate(ride_id=1), owner, db_session)
    assert own_error.value.status_code == 400

    buyer = await _user(db_session, 2)
    other = await _user(db_session, 3)
    first = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)

    ride = await db_session.get(Ride, 1)
    ride.status = "open"
    await db_session.commit()

    second = await orders.create_order(OrderCreate(ride_id=1), other, db_session)
    ride_detail = await rides.get_ride(1, _request(), db_session)

    assert first.status == "paid"
    assert second.status == "paid"
    assert ride.status == "open"
    assert ride_detail.purchase_count == 2
    assert ride_detail.recruit_seats == 1
    assert ride_detail.remaining_seats == 1


@pytest.mark.asyncio
async def test_login_rate_limit_returns_429(db_session):
    reset_auth_rate_limits()
    request = _request(host="10.0.0.1")
    payload = auth.LoginRequest(email="buyer@example.com", password="bad-password")

    for _ in range(5):
        with pytest.raises(HTTPException) as login_error:
            await auth.login_json(payload, request, db_session)
        assert login_error.value.status_code == 400

    with pytest.raises(HTTPException) as limited_error:
        await auth.login_json(payload, request, db_session)
    assert limited_error.value.status_code == 429


@pytest.mark.asyncio
async def test_email_registration_requires_activation_and_hashes_token(db_session, monkeypatch):
    reset_auth_rate_limits()
    sent = {}

    def fake_send_activation_email(email: str, token: str) -> None:
        sent["email"] = email
        sent["token"] = token

    monkeypatch.setattr(auth, "send_activation_email", fake_send_activation_email)
    request = _request(host="10.0.0.2")

    created = await auth.register(
        auth.UserCreate(
            email="new-user@example.com",
            nickname="new user",
            password="secret123",
        ),
        request,
        db_session,
    )

    assert created.email == "new-user@example.com"
    assert created.email_verified is False
    assert sent["email"] == "new-user@example.com"
    assert sent["token"]

    token_result = await db_session.execute(select(ActivationToken))
    activation = token_result.scalars().one()
    assert activation.token_hash == auth._activation_token_hash(sent["token"])
    assert activation.token_hash != sent["token"]

    login_payload = auth.LoginRequest(email="new-user@example.com", password="secret123")
    with pytest.raises(HTTPException) as inactive_error:
        await auth.login_json(login_payload, request, db_session)
    assert inactive_error.value.status_code == 403

    response = await auth.activate_account(sent["token"], redirect=False, db=db_session)
    assert response["detail"] == "邮箱已激活"

    login_response = await auth.login_json(login_payload, request, db_session)
    assert login_response["access_token"]


@pytest.mark.asyncio
async def test_user_can_change_password_with_current_password(db_session):
    buyer = await _user(db_session, 2)

    with pytest.raises(HTTPException) as password_error:
        await users.change_password(
            PasswordChange(current_password="wrong123", new_password="newsecret123"),
            buyer,
            db_session,
        )
    assert password_error.value.status_code == 400

    result = await users.change_password(
        PasswordChange(current_password="secret123", new_password="newsecret123"),
        buyer,
        db_session,
    )
    await db_session.refresh(buyer)

    assert result["message"] == "Password updated successfully"
    assert verify_password("newsecret123", buyer.password_hash)


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
    assert overview.total_revenue == Decimal("0.00")
    assert overview.active_rides == 1
    assert sales_trends[0].orders == 1
    assert sales_trends[0].revenue == Decimal("0.00")
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
    paid = await orders.create_order(OrderCreate(ride_id=1), buyer, db_session)

    sales = await orders.get_my_sales(owner, db_session)

    assert paid.contact_unlocked_at is not None
    assert sales["total_unlocks"] == 1
    assert sales["rides"][0]["unlock_count"] == 1
    assert sales["rides"][0]["recruit_seats"] == 1
    assert sales["rides"][0]["remaining_seats"] == 1
    assert sales["rides"][0]["latest_unlock_at"] is not None
