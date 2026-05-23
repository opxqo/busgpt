from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from jose import jwt, JWTError

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.utils.rate_limit import check_auth_rate_limit, record_auth_failure, record_auth_success
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login-oauth2")

# OAuth2 login helper (standard form data) for Swagger documentation support
from fastapi.security import OAuth2PasswordRequestForm

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    result = await db.execute(select(User).filter(User.id == int(user_id)))
    user = result.scalars().first()
    if user is None:
        raise credentials_exception
    return user


async def get_current_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, request: Request, db: AsyncSession = Depends(get_db)):
    rate_limit_key = check_auth_rate_limit(request, user_in.phone)
    # Check if user already exists
    result = await db.execute(select(User).filter(User.phone == user_in.phone))
    existing_user = result.scalars().first()
    if existing_user:
        record_auth_failure(rate_limit_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone number already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        phone=user_in.phone,
        nickname=user_in.nickname,
        avatar=user_in.avatar,
        role="admin" if user_in.phone in settings.admin_phone_set else "user",
        password_hash=hashed_password
    )
    db.add(db_user)
    await db.flush()  # Populates db_user.id
    await db.commit()
    await db.refresh(db_user)
    record_auth_success(rate_limit_key)
    
    return db_user

# Custom login schema to support JSON input in front-end
from pydantic import BaseModel

class LoginRequest(BaseModel):
    phone: str
    password: str

@router.post("/login", response_model=Token)
async def login_json(login_in: LoginRequest, request: Request, db: AsyncSession = Depends(get_db)):
    rate_limit_key = check_auth_rate_limit(request, login_in.phone)
    result = await db.execute(select(User).filter(User.phone == login_in.phone))
    user = result.scalars().first()
    if not user or not verify_password(login_in.password, user.password_hash):
        record_auth_failure(rate_limit_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect phone or password"
        )
    
    access_token = create_access_token(subject=user.id)
    record_auth_success(rate_limit_key)
    return {"access_token": access_token, "token_type": "bearer"}

# Supporting OAuth2 standard login form (for Swagger `/docs`)
@router.post("/login-oauth2", response_model=Token)
async def login_oauth2(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    rate_limit_key = check_auth_rate_limit(request, form_data.username)
    # OAuth2 form_data.username will contain the phone number
    result = await db.execute(select(User).filter(User.phone == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.password_hash):
        record_auth_failure(rate_limit_key)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect phone or password"
        )
    
    access_token = create_access_token(subject=user.id)
    record_auth_success(rate_limit_key)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user
