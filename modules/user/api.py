from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.core.security import create_access_token
from app.modules.user import schemas, service
from datetime import timedelta

router = APIRouter()

@router.post(
    "/users",
    response_model=schemas.UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="새로운 사용자 등록"
)
async def register_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    if await service.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    new_user = await service.create_user(db, user_in)
    return new_user

@router.post(
    "/token",
    response_model=schemas.Token,
    summary="로그인 및 Access Token 발급"
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    user = await service.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"username": user.username, "user_id":user.id},
        expires_delta = access_token_expires
    )
    
    return schemas.Token(access_token=access_token, token_type="bearer")