from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.security import get_password_hash, verify_password
from app.modules.user.models import UserConfig
from app.modules.user.schemas import UserCreate
from typing import Optional

async def get_user_by_username(db: AsyncSession, username: str):
    stmt = select(UserConfig).where(UserConfig.username==username)
    result = await db.execute(stmt)
    return result.scalar()

async def create_user(db: AsyncSession, user_data: UserCreate) -> UserConfig:
    hashed_password = get_password_hash(user_data.password)
    
    new_user = UserConfig(
        username=user_data.username,
        password=hashed_password
    )
    
    db.add(new_user)
    await db.flush()
    await db.commit()
    return new_user

async def authenticate_user(db:AsyncSession, username: str, password: str) -> Optional[UserConfig]:
    user = await get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user