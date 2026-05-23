from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.user import User
from app.schemas.user import PasswordChange, UserUpdate, UserResponse
from app.routers.auth import get_current_user
from app.utils.security import get_password_hash, verify_password

router = APIRouter(prefix="/users", tags=["users"])

@router.put("/me", response_model=UserResponse)
async def update_profile(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if user_in.nickname is not None:
        current_user.nickname = user_in.nickname
    if user_in.avatar is not None:
        current_user.avatar = user_in.avatar
        
    db.add(current_user)
    await db.flush()
    await db.commit()
    await db.refresh(current_user)
    return current_user

@router.put("/me/password")
async def change_password(
    password_in: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if not verify_password(password_in.current_password, current_user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="当前密码不正确")
    if password_in.current_password == password_in.new_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="新密码不能与当前密码相同")

    current_user.password_hash = get_password_hash(password_in.new_password)
    db.add(current_user)
    await db.flush()
    await db.commit()
    return {"message": "Password updated successfully"}

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_public(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
