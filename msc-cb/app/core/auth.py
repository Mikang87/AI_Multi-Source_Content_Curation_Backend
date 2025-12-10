from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import decode_access_token
from app.modules.user.service import get_user_by_username
from app.modules.user.models import UserConfig

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> UserConfig:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
    payload = decode_access_token(token)
    username: str = payload.get("username")
    
    if username is None:
        raise credentials_exception
    
    user = await get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_user_id(user: UserConfig = Depends(get_current_user)) -> int:
    
    return user.id