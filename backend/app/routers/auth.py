import secrets
from hashlib import sha256
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError

from app.database import get_db
from app.models.activation_token import ActivationToken
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    Token,
    ResendActivationRequest,
)
from app.utils.security import (
    verify_password,
    get_password_hash,
    create_access_token,
)
from app.utils.rate_limit import (
    check_auth_rate_limit,
    record_auth_failure,
    record_auth_success,
)
from app.utils.email import send_activation_email
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login-oauth2"
)

ACTIVATION_TOKEN_EXPIRE_HOURS = 24


def _activation_token_hash(token: str) -> str:
    return sha256(token.encode("utf-8")).hexdigest()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    result = await db.execute(select(User).filter(User.id == int(user_id)))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )
    if user.email_verified_at is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请先激活邮箱后再登录",
        )
    return user


async def get_current_admin_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required",
        )
    return current_user


async def _generate_activation_token(
    db: AsyncSession, user_id: int
) -> str:
    """Generate a new activation token, removing any previous ones for this user."""
    # Delete old tokens for this user
    old_tokens = await db.execute(
        select(ActivationToken).filter(ActivationToken.user_id == user_id)
    )
    for old in old_tokens.scalars().all():
        await db.delete(old)

    token = secrets.token_urlsafe(48)[:64]
    activation = ActivationToken(
        user_id=user_id,
        token_hash=_activation_token_hash(token),
        expires_at=datetime.utcnow()
        + timedelta(hours=ACTIVATION_TOKEN_EXPIRE_HOURS),
    )
    db.add(activation)
    return token


@router.post("/register", response_model=UserResponse)
async def register(
    user_in: UserCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    rate_limit_key = check_auth_rate_limit(request, user_in.email)

    # Check if email already exists
    result = await db.execute(
        select(User).filter(User.email == user_in.email.lower())
    )
    existing_user = result.scalars().first()
    if existing_user:
        record_auth_failure(rate_limit_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册",
        )

    # Create new user (unverified)
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email.lower(),
        nickname=user_in.nickname,
        avatar=user_in.avatar,
        role=(
            "admin"
            if user_in.email.lower() in settings.admin_email_set
            else "user"
        ),
        password_hash=hashed_password,
        email_verified_at=None,
    )
    db.add(db_user)
    await db.flush()  # Populates db_user.id

    # Generate activation token and send email
    token = await _generate_activation_token(db, db_user.id)
    await db.commit()
    await db.refresh(db_user)

    send_activation_email(db_user.email, token)
    record_auth_success(rate_limit_key)

    return db_user


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/login", response_model=Token)
async def login_json(
    login_in: LoginRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    rate_limit_key = check_auth_rate_limit(request, login_in.email)
    result = await db.execute(
        select(User).filter(User.email == login_in.email.lower())
    )
    user = result.scalars().first()
    if not user or not verify_password(login_in.password, user.password_hash):
        record_auth_failure(rate_limit_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱或密码不正确",
        )

    if user.email_verified_at is None:
        record_auth_failure(rate_limit_key)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请先激活邮箱。如未收到激活邮件，请点击重新发送。",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账号已被禁用",
        )

    access_token = create_access_token(subject=user.id)
    record_auth_success(rate_limit_key)
    return {"access_token": access_token, "token_type": "bearer"}


from fastapi.security import OAuth2PasswordRequestForm


@router.post("/login-oauth2", response_model=Token)
async def login_oauth2(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    rate_limit_key = check_auth_rate_limit(request, form_data.username)
    result = await db.execute(
        select(User).filter(User.email == form_data.username.lower())
    )
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        record_auth_failure(rate_limit_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱或密码不正确",
        )

    if user.email_verified_at is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="请先激活邮箱",
        )

    access_token = create_access_token(subject=user.id)
    record_auth_success(rate_limit_key)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/activate")
async def activate_account(
    token: str = Query(...),
    redirect: bool = Query(False),
    db: AsyncSession = Depends(get_db),
):
    def activation_response(status_value: str, reason: str = ""):
        if redirect:
            url = f"{settings.FRONTEND_URL}/activate?status={status_value}"
            if reason:
                url = f"{url}&reason={reason}"
            return RedirectResponse(url=url)
        if status_value == "success":
            return {"detail": "邮箱已激活"}
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "invalid_token": "激活链接无效，请检查是否完整复制了链接。",
                "expired": "激活链接已过期，请重新发送激活邮件。",
                "user_not_found": "对应的用户不存在，请重新注册。",
            }.get(reason, "激活失败，请重新发送激活邮件。"),
        )

    result = await db.execute(
        select(ActivationToken).filter(
            ActivationToken.token_hash == _activation_token_hash(token)
        )
    )
    activation = result.scalars().first()

    if not activation:
        return activation_response("error", "invalid_token")

    if activation.expires_at < datetime.utcnow():
        await db.delete(activation)
        await db.commit()
        return activation_response("error", "expired")

    # Activate the user
    user_result = await db.execute(
        select(User).filter(User.id == activation.user_id)
    )
    user = user_result.scalars().first()
    if not user:
        return activation_response("error", "user_not_found")

    user.email_verified_at = datetime.utcnow()
    await db.delete(activation)
    await db.commit()

    return activation_response("success")


@router.post("/resend-activation")
async def resend_activation(
    body: ResendActivationRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    rate_limit_key = check_auth_rate_limit(request, body.email)

    result = await db.execute(
        select(User).filter(User.email == body.email.lower())
    )
    user = result.scalars().first()

    # Always return success to prevent email enumeration
    if not user or user.email_verified_at is not None:
        record_auth_success(rate_limit_key)
        return {"detail": "如果该邮箱已注册且未激活，激活邮件已重新发送。"}

    token = await _generate_activation_token(db, user.id)
    await db.commit()

    send_activation_email(user.email, token)
    record_auth_success(rate_limit_key)

    return {"detail": "激活邮件已重新发送，请查收。"}


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
